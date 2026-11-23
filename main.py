"""Interfaz Flet basada en eventos."""
from functools import partial

import flet as ft

from juego import Juego
from modelos import Opcion, Resultado


class InterfazJuego:
    def __init__(self, pagina: ft.Page, juego: Juego):
        self.pagina = pagina
        self.juego = juego
        self.resultado = ft.Text(size=27, weight=ft.FontWeight.BOLD)
        self.elecciones = ft.Text(color="#475569")
        self.contadores = [ft.Text(size=23, weight=ft.FontWeight.BOLD) for _ in range(4)]
        self.historial = ft.Column(spacing=10)
        self.reinicio = ft.OutlinedButton(content="Reiniciar partida", on_click=self.reiniciar)

    @staticmethod
    def tarjeta(*controles):
        return ft.Container(
            content=ft.Column(controls=list(controles), spacing=12),
            padding=20, border_radius=18, bgcolor="#FFFFFF",
            border=ft.Border.all(1, "#DEE6EF"),
        )

    def montar(self):
        pagina = self.pagina
        pagina.title = "Piedra, Papel o Tijera"
        pagina.theme_mode = ft.ThemeMode.LIGHT
        pagina.theme = ft.Theme(color_scheme_seed="#087F72")
        pagina.bgcolor = "#EDF5F4"
        pagina.padding = 20
        pagina.scroll = ft.ScrollMode.AUTO
        pagina.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        botones = ft.Row(wrap=True, spacing=10, run_spacing=10, controls=[
            ft.FilledButton(content=opcion.value, on_click=partial(self.jugar, opcion))
            for opcion in Opcion
        ])
        marcador = ft.Row(wrap=True, spacing=24, run_spacing=12, controls=[
            ft.Column(controls=[valor, ft.Text(etiqueta, color="#475569")], spacing=2)
            for valor, etiqueta in zip(
                self.contadores, ("Victorias", "Derrotas", "Empates", "Rondas")
            )
        ])
        self.refrescar()
        pagina.add(ft.Container(width=690, content=ft.Column(spacing=16, controls=[
            ft.Text("Piedra, Papel o Tijera", size=35, weight=ft.FontWeight.BOLD,
                    color="#102D31"),
            ft.Text("Elige una opción para jugar una ronda contra la computadora.",
                    color="#475569", size=16),
            self.tarjeta(botones, self.resultado, self.elecciones),
            self.tarjeta(marcador, self.reinicio),
            self.tarjeta(ft.Text("Últimas cinco rondas", size=19, weight=ft.FontWeight.BOLD),
                         self.historial),
        ])))

    def jugar(self, opcion, evento):
        self.juego.jugar(opcion)
        self.refrescar()
        self.pagina.update()

    def reiniciar(self, evento):
        self.juego.reiniciar()
        self.refrescar()
        self.pagina.update()

    def refrescar(self):
        juego = self.juego
        historial = juego.historial
        estadisticas = juego.estadisticas
        valores = [estadisticas[resultado] for resultado in Resultado]
        for control, valor in zip(self.contadores, [*valores, juego.rondas_jugadas]):
            control.value = str(valor)
        self.reinicio.disabled = not historial
        if historial:
            ronda = historial[0]
            self.resultado.value = ronda.resultado.value
            self.elecciones.value = (
                f"{juego.humano.nombre}: {ronda.humano} · "
                f"{juego.computadora.nombre}: {ronda.computadora}"
            )
        else:
            self.resultado.value = "Todo listo para jugar"
            self.elecciones.value = "Aquí verás las elecciones de cada ronda."
        self.historial.controls = [
            ft.Text(f"Ronda {ronda.numero} · {ronda.humano} vs. {ronda.computadora}"
                    f" · {ronda.resultado}")
            for ronda in historial
        ] or [ft.Text("Todavía no hay rondas.", color="#475569")]


def main(pagina: ft.Page):
    InterfazJuego(pagina, Juego()).montar()


if __name__ == "__main__":
    ft.run(main)
