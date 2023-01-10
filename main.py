import src.ear_clipping as ec
import numpy as np
import cairo


def main():
    number_of_edges = 12
    tau = 2 * np.pi
    # arranging angles from 0 till TAU excl
    angle_range = np.arange(0, tau, tau / number_of_edges).reshape(-1, 1)
    # making a collection of points which form a circle
    points = np.hstack((np.cos(angle_range), np.sin(angle_range)))
    # decreasing all odd elements to get a concave polygon
    points[::2] *= 0.8
    # making a closing path
    path = np.array([x for x in range(number_of_edges)])

    triangles = np.array(ec.ear_clipping(points, path))

    canvas_size = 700

    with cairo.SVGSurface("./polygon.svg", canvas_size, canvas_size) as surface:
        context = cairo.Context(surface)
        context.set_source_rgba(0, 0, 0, 1)
        context.set_line_width(2)
        context.set_line_cap(cairo.LINE_CAP_ROUND)
        context.set_line_join(cairo.LINE_JOIN_ROUND)

        scaled_points = ((points + 1) * (canvas_size - 40)) / 2 + 20

        context.set_source_rgb(1, 0, 0)

        for id0, id1, id2 in triangles:
            p0 = scaled_points[id0]
            p1 = scaled_points[id1]
            p2 = scaled_points[id2]

            context.move_to(p0[0], p0[1])
            context.line_to(p1[0], p1[1])
            context.line_to(p2[0], p2[1])
            context.close_path()
            context.stroke()


if __name__ == "__main__":
    main()
