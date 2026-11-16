"""Base de Manim con la estética Scale (negro puro, línea gris, acento Foundry Tan) y formato vertical 1080×1920 / 30 fps.
Copiar este archivo a videos/<video>/manim/escena.py y heredar de `Reel`. Sin LaTeX instalado: usar Text/MarkupText (Geist Mono para números).
Con --transparent sale un .mov con fondo transparente para ponerlo sobre el 3D."""
from manim import *

config.pixel_width, config.pixel_height, config.frame_rate = 1080, 1920, 30
config.frame_height, config.frame_width = 16, 9
TAN, GRIS, GRIS_OSC, BLANCO = "#A8927C", "#929292", "#4D4D4D", "#FFFFFF"


class Reel(Scene):
    def construct_fondo(self): self.camera.background_color = BLACK


class Ejemplo(Reel):
    def construct(self):
        self.construct_fondo()
        ax = Axes(x_range=[-3, 3], y_range=[-1.5, 1.5], x_length=7, y_length=4, axis_config={"color": GRIS, "include_tip": False})
        g = ax.plot(lambda x: np.sin(x), color=TAN)
        self.play(Create(ax), run_time=1)
        self.play(Create(g), run_time=1.5)
        d = Dot(color=BLANCO).move_to(ax.i2gp(-3, g))
        self.play(MoveAlongPath(d, g), run_time=1.5, rate_func=linear)
