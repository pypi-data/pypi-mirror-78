# Copyright (c) 2020, Manfred Moitzi
# License: MIT License

import pytest
import ezdxf
from ezdxf.addons.drawing.properties import RenderContext, compile_line_pattern
from ezdxf.entities import Layer
from ezdxf.lldxf import const


@pytest.fixture(scope='module')
def doc():
    d = ezdxf.new(setup=True)
    d.layers.new('Test', dxfattribs={
        'color': 5,  # blue: 0000ff
        'linetype': 'DOT',
        'lineweight': 70,  # 0.70
    })
    msp = d.modelspace()
    msp.add_line((0, 0), (1, 0), dxfattribs={
        'color': 256,  # by layer
        'linetype': 'BYLAYER',
        'lineweight': -1,  # by layer
        'layer': 'Test',
    })
    msp.add_line((0, 0), (1, 0), dxfattribs={
        'color': 1,  # red: ff0000
        'linetype': 'DASHED',
        'lineweight': 50,  # 0.50
        'layer': 'Test',
    })
    blk = d.blocks.new('MyBlock')
    blk.add_line((0, 0), (1, 0), dxfattribs={
        'color': 0,  # by block
        'linetype': 'BYBLOCK',
        'lineweight': -2,  # by block
        'layer': 'Test',
    })
    blk.add_line((0, 0), (1, 0), dxfattribs={
        'color': 1,  # red: ff0000
        'linetype': 'DASHED',
        'lineweight': 50,  # 0.50
        'layer': 'Test',
    })
    blk.add_line((0, 0), (1, 0), dxfattribs={
        'color': 256,  # by layer
        'linetype': 'BYLAYER',
        'lineweight': -1,  # by layer
        'layer': 'Test',
    })
    msp.add_blockref('MyBlock', insert=(0, 0), dxfattribs={
        'color': 3,  # green: 00ff00
        'linetype': 'CENTER',
        'lineweight': 13,  # 0.13
    })
    return d


def test_load_default_ctb(doc):
    ctx = RenderContext(doc, ctb='color.ctb')
    assert bool(ctx.plot_styles) is True
    assert ctx.plot_styles[1].color == (255, 0, 0)


def test_new_ctb(doc):
    ctx = RenderContext(doc)
    assert bool(ctx.plot_styles) is True
    assert ctx.plot_styles[1].color == (255, 0, 0)


def test_resolve_entity_visibility():
    doc = ezdxf.new()
    layout = doc.modelspace()
    doc.layers.new(name='visible', dxfattribs={'color': 0})
    doc.layers.new(name='invisible', dxfattribs={'color': -1})  # color < 0 => invisible
    doc.layers.new(name='frozen', dxfattribs={'flags': Layer.FROZEN})  # also invisible
    doc.layers.new(name='noplot', dxfattribs={'plot': 0})  # visible in the CAD application but not when exported

    for export_mode in (False, True):
        ctx = RenderContext(layout.doc, export_mode=export_mode)

        text = layout.add_text('a', {'invisible': 0, 'layer': 'non_existent'})
        assert ctx.resolve_visible(text) is True

        text = layout.add_text('a', {'invisible': 0, 'layer': 'visible'})
        assert ctx.resolve_visible(text) is True

        for layer in ['invisible', 'frozen']:
            text = layout.add_text('a', {'invisible': 0, 'layer': layer})
            assert ctx.resolve_visible(text) is False

        for layer in ['non_existent', 'visible', 'invisible', 'frozen', 'noplot']:
            text = layout.add_text('a', {'invisible': 1, 'layer': layer})
            assert ctx.resolve_visible(text) is False

    ctx = RenderContext(layout.doc, export_mode=False)
    text = layout.add_text('a', {'invisible': 0, 'layer': 'noplot'})
    assert ctx.resolve_visible(text) is True

    ctx = RenderContext(layout.doc, export_mode=True)
    text = layout.add_text('a', {'invisible': 0, 'layer': 'noplot'})
    assert ctx.resolve_visible(text) is False


def test_resolve_attrib_visibility():
    doc = ezdxf.new()
    layout = doc.modelspace()
    block = doc.blocks.new(name='block')
    doc.layers.new(name='invisible', dxfattribs={'color': -1})  # color < 0 => invisible

    block.add_attdef('att1', (0, 0), '', {})
    block.add_attdef('att2', (0, 0), '', {'flags': const.ATTRIB_INVISIBLE})
    block.add_attdef('att3', (0, 0), '', {'layer': 'invisible'})

    i = layout.add_blockref('block', (0, 0))
    i.add_auto_attribs({'att1': 'abc', 'att2': 'def', 'att3': 'hij'})

    assert not i.attribs[0].is_invisible
    assert i.attribs[1].is_invisible
    assert not i.attribs[2].is_invisible

    ctx = RenderContext(layout.doc)
    assert ctx.resolve_visible(i.attribs[0]) is True
    assert ctx.resolve_visible(i.attribs[1]) is False
    assert ctx.resolve_visible(i.attribs[2]) is False


def test_resolve_entity_color(doc):
    ctx = RenderContext(doc)
    msp = doc.modelspace()
    lines = msp.query('LINE')
    line1 = ctx.resolve_all(lines[0])
    assert line1.color == '#0000ff'  # by layer

    line2 = ctx.resolve_all(lines[1])
    assert line2.color == '#ff0000'


def test_resolve_entity_linetype(doc):
    ctx = RenderContext(doc)
    msp = doc.modelspace()
    lines = msp.query('LINE')

    line1 = ctx.resolve_all(lines[0])
    assert line1.linetype_name == 'DOT'  # by layer

    line2 = ctx.resolve_all(lines[1])
    assert line2.linetype_name == 'DASHED'


def test_resolve_entity_lineweight(doc):
    ctx = RenderContext(doc)
    msp = doc.modelspace()
    lines = msp.query('LINE')

    line1 = ctx.resolve_all(lines[0])
    assert line1.lineweight == 0.70  # by layer

    line2 = ctx.resolve_all(lines[1])
    assert line2.lineweight == 0.50


def test_resolve_block_entities(doc):
    ctx = RenderContext(doc)
    msp = doc.modelspace()
    blockref = msp.query('INSERT').first
    ctx.push_state(ctx.resolve_all(blockref))
    assert ctx.inside_block_reference is True
    lines = list(blockref.virtual_entities())

    # properties by block
    line1 = ctx.resolve_all(lines[0])
    assert lines[0].dxf.linetype == 'BYBLOCK'
    assert line1.color == '#00ff00'
    assert line1.linetype_name == 'CENTER'
    assert line1.lineweight == 0.13

    # explicit properties
    line2 = ctx.resolve_all(lines[1])
    assert lines[1].dxf.linetype == 'DASHED'
    assert line2.color == '#ff0000'
    assert line2.linetype_name == 'DASHED'
    assert line2.lineweight == 0.50

    # properties by layer 'Test'
    line3 = ctx.resolve_all(lines[2])
    assert lines[2].dxf.linetype == 'BYLAYER'
    assert line3.color == '#0000ff'
    assert line3.linetype_name == 'DOT'
    assert line3.lineweight == 0.70
    
    ctx.pop_state()
    assert ctx.inside_block_reference is False


def test_compile_pattern():
    assert compile_line_pattern(0, [0.0]) == tuple()
    assert compile_line_pattern(2.0, [1.25, -0.25, 0.25, -0.25]) == (1.25, 0.25, 0.25, 0.25)
    assert compile_line_pattern(3.5, [2.5, -0.25, 0.5, -0.25]) == (2.5, 0.25, 0.5, 0.25)
    assert compile_line_pattern(1.4, [1.0, -0.2, 0.0, -0.2]) == (1.0, 0.2, 0.0, 0.2)
    assert compile_line_pattern(0.2, [0.0, -0.2]) == (0.0, 0.2)
    assert compile_line_pattern(2.6, [2.0, -0.2, 0.0, -0.2, 0.0, -0.2]) == (2.0, 0.2, 0.0, 0.2, 0.0, 0.2)


if __name__ == '__main__':
    pytest.main([__file__])
