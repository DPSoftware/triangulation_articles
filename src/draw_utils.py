import cairo
from io import BytesIO


def render_svg(v, f, canvas_size=300):
    svg_io = BytesIO()

    cairo.ImageSurface()
    with cairo.SVGSurface(svg_io, canvas_size, canvas_size) as surface:
        context = cairo.Context(surface)
        context.set_source_rgba(0, 0, 0, 1)
        context.set_line_width(1)
        context.set_line_cap(cairo.LINE_CAP_ROUND)
        context.set_line_join(cairo.LINE_JOIN_ROUND)
        context.set_source_rgb(1, 0, 0)

        for id0, id1, id2 in f:
            p0 = v[id0]
            p1 = v[id1]
            p2 = v[id2]

            context.move_to(p0[0], p0[1])
            context.line_to(p1[0], p1[1])
            context.line_to(p2[0], p2[1])
            context.close_path()
            context.stroke()

    return svg_io.getvalue()
