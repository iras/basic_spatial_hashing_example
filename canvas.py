import OpenGL.GLUT as glut
import OpenGL.GL as gl
import sys, math


class Canvas:

    def __init__(self, window_size, external_funct, data):
        assert window_size > 0
        self.external_funct = external_funct
        self.window_size = window_size
        self.half_window_size = self.window_size * 0.5
        self.pixel_size = 6.0  # canvas pixel size expressed in screen pixels.
        self.half_pixel_size = self.pixel_size * 0.5
        self.pixel_mult = self.pixel_size / self.window_size
        self.data = data
        self.mouse_pos = (self.half_window_size, self.half_window_size)
        self.max = 25.0  # square box's side.

        self._glut_init()

    def _glut_init(self):
        glut.glutInit(sys.argv)
        glut.glutInitDisplayMode(glut.GLUT_RGB | glut.GLUT_SINGLE)
        glut.glutInitWindowSize(self.window_size, self.window_size)
        glut.glutInitWindowPosition(0, 0)
        glut.glutCreateWindow(sys.argv[0])
        glut.glutDisplayFunc(self._display)
        glut.glutSpecialFunc(self._on_key_press)
        glut.glutMouseFunc(self._on_mouse_click)
        glut.glutMotionFunc(self._on_mouse_move)
        glut.glutReshapeFunc(self._on_window_resize);
        glut.glutIdleFunc(self._on_idle)
        glut.glutMainLoop()

    def _on_key_press(self, key, x, y):
        if key == 27:  # escape
            sys.exit()

    def _on_mouse_click(self, button, state, x, y):
        if state == glut.GLUT_DOWN:
            self.mouse_pos = (x, y)

    def _on_mouse_move(self, x, y):
        self.mouse_pos = (x, y)

    def _on_window_resize(self, x, y):
        # NB: resize back to the original size as the
        #     mapping below is only for fixed-size windows.
        glut.glutReshapeWindow(self.window_size, self.window_size);

    def _get_cartesian_pos_from_screenspace_pos(self, x, y):
        # NB: fixed-size window's mapping.
        return (
            math.floor((x - self.half_window_size) / self.half_pixel_size),
            math.floor((self.half_window_size - y) / self.half_pixel_size),
        )

    def _get_screenspace_pos_from_cartesian_pos(self, x, y, z):
        return x * self.pixel_mult, y * self.pixel_mult, z * self.pixel_mult

    def _add_pixel(self, x, y, z):
        # NB: a canvas's "pixel" is made up of two triangles (1 quad polygon).
        quad_vertices = [
            (x, self.pixel_mult + y, 0),
            (x, y, 0),
            (self.pixel_mult + x, y, 0),
            (self.pixel_mult + x, self.pixel_mult + y, 0),
        ]
        for quad_vertex in quad_vertices:
            gl.glVertex3f(*quad_vertex)

    def _plot_big_pixels(self, points):
        gl.glBegin(gl.GL_QUADS)
        for point in points:
            self._add_pixel(*point)
        gl.glEnd()

    def _remap(self, points):
        return [
            self._get_screenspace_pos_from_cartesian_pos(*tuple_x_y_z)
            for tuple_x_y_z in points
        ]

    def _display(self):
        gl.glClearColor(0, 0, 0, 0)  # black background.
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        gl.glColor3f(0, 1, 0)
        self._add_mouse_centered_square()

        gl.glColor3f(1, 1, 1)
        self._plot_big_pixels(self._remap(self.data.points))

        gl.glColor3f(1, 0, 0)
        self._plot_big_pixels(self._remap(self.data.neighbouring_points))

        gl.glFlush()

    def _add_mouse_centered_square(self):
        # NB: this is only a reference square anchored the mouse pos.
        x1, y1 = self._get_cartesian_pos_from_screenspace_pos(*self.mouse_pos)
        x, y, z = self._get_screenspace_pos_from_cartesian_pos(x1, y1, 0)
        side = self.max * self.pixel_mult / 2.0
        v0 = (x - side, side + y, 0)
        v1 = (x - side, y - side, 0)
        v2 = (side + x, y - side, 0)
        v3 = (side + x, side + y, 0)

        gl.glBegin(gl.GL_LINES)
        for line_vertex in [v0, v1, v1, v2, v2, v3, v3, v0]:
            gl.glVertex3f(*line_vertex)
        gl.glEnd()

    def _on_idle(self):
        x, y = self._get_cartesian_pos_from_screenspace_pos(*self.mouse_pos)
        self.external_funct((x, y, 0))
        glut.glutPostRedisplay()
