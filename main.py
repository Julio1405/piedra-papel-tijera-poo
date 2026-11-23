"""Interfaz Flet basada en eventos."""
import asyncio

import flet as ft

from juego import Juego
from modelos import Opcion, Resultado

FONDO = "#10101C"
PANEL = "#1B1B2C"
BORDE = "#34334C"
TEXTO = "#F9F7FF"
SUAVE = "#BDB9D2"
ACENTO = "#C7B1FF"

ICONOS = {
    Opcion.PIEDRA: ft.Icons.LANDSCAPE_ROUNDED,
    Opcion.PAPEL: ft.Icons.DESCRIPTION_ROUNDED,
    Opcion.TIJERA: ft.Icons.CONTENT_CUT_ROUNDED,
}
COLORES = {
    Opcion.PIEDRA: "#FFC084",
    Opcion.PAPEL: "#BDB6FF",
    Opcion.TIJERA: "#7CE6D3",
}
RESULTADOS = {
    Resultado.VICTORIA: ("¡Ganaste!", "#89EBB4"),
    Resultado.DERROTA: ("Ganó la computadora", "#FFABA9"),
    Resultado.EMPATE: ("¡Empate!", "#FFDB93"),
}


class InterfazJuego:
    def __init__(self, pagina: ft.Page, juego: Juego):
        self.pagina = pagina
        self.juego = juego
        self.animando = False
        self.resultado = ft.Text(size=24, weight=ft.FontWeight.BOLD,
                                 text_align=ft.TextAlign.CENTER)
        self.detalle = ft.Text(size=13, color=SUAVE, text_align=ft.TextAlign.CENTER)
        self.icono_humano = ft.Icon(ft.Icons.QUESTION_MARK_ROUNDED, size=40)
        self.icono_cpu = ft.Icon(ft.Icons.QUESTION_MARK_ROUNDED, size=40)
        self.eleccion_humana = ft.Text(weight=ft.FontWeight.BOLD, color=TEXTO)
        self.eleccion_cpu = ft.Text(weight=ft.FontWeight.BOLD, color=TEXTO)
        self.contadores = [ft.Text(size=25, weight=ft.FontWeight.BOLD)
                           for _ in range(4)]
        self.historial = ft.Column(spacing=8)
        self.reinicio = ft.TextButton(
            content="Reiniciar partida", icon=ft.Icons.RESTART_ALT_ROUNDED,
            on_click=self.reiniciar,
        )
        self.botones = [
            ft.FilledButton(
                content=ft.Column(
                    [ft.Icon(ICONOS[opcion], size=23), ft.Text(opcion.value)],
                    spacing=5, alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                expand=True, height=68, data=opcion,
                style=ft.ButtonStyle(
                    color=COLORES[opcion],
                    bgcolor={ft.ControlState.HOVERED: "#3C3456",
                             ft.ControlState.DEFAULT: "#2C2943"},
                    padding=6, shape=ft.RoundedRectangleBorder(radius=14),
                ),
                on_click=self.jugar,
            )
            for opcion in Opcion
        ]

    @staticmethod
    def tarjeta(*controles, col=12):
        return ft.Container(
            content=ft.Column(list(controles), spacing=14,
                              horizontal_alignment=ft.CrossAxisAlignment.STRETCH),
            col=col, padding=16, border_radius=20, bgcolor=PANEL,
            border=ft.Border.all(1, BORDE),
        )

    @staticmethod
    def participante(nombre, icono, eleccion):
        return ft.Container(
            expand=True, bgcolor="#26243A", border_radius=14, padding=10,
            content=ft.Column(
                [ft.Text(nombre, color=SUAVE, size=12), icono, eleccion],
                spacing=7, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    def montar(self):
        pagina = self.pagina
        pagina.title = "Piedra, Papel o Tijera"
        pagina.theme_mode = ft.ThemeMode.DARK
        pagina.theme = ft.Theme(color_scheme_seed="#A88AFD")
        pagina.bgcolor = FONDO
        pagina.padding = 14
        pagina.scroll = ft.ScrollMode.AUTO
        pagina.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        arena = ft.Row([
            self.participante("Tú", self.icono_humano, self.eleccion_humana),
            ft.Text("VS", size=13, weight=ft.FontWeight.BOLD, color=ACENTO),
            self.participante("Computadora", self.icono_cpu, self.eleccion_cpu),
        ], spacing=8)
        estado = ft.Semantics(
            live_region=True,
            content=ft.Column([self.resultado, self.detalle], spacing=4,
                              horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        )
        juego = self.tarjeta(
            ft.Text("Elige tu jugada", size=18, weight=ft.FontWeight.BOLD, color=TEXTO),
            ft.Row(self.botones, spacing=6), arena, estado,
            col={"xs": 12, "md": 7},
        )
        marcador = ft.ResponsiveRow([
            ft.Container(
                col=6, bgcolor="#26243A", border_radius=12, padding=10,
                content=ft.Column(
                    [valor, ft.Text(etiqueta, size=12, color=SUAVE)], spacing=2,
                ),
            )
            for valor, etiqueta in zip(
                self.contadores, ("Victorias", "Derrotas", "Empates", "Rondas")
            )
        ], spacing=8, run_spacing=8)
        estadisticas = self.tarjeta(
            ft.Text("Marcador", size=18, weight=ft.FontWeight.BOLD, color=TEXTO),
            marcador, self.reinicio, col={"xs": 12, "md": 5},
        )
        historial = self.tarjeta(
            ft.Row([ft.Icon(ft.Icons.HISTORY_ROUNDED, size=19, color=ACENTO),
                    ft.Text("Últimas cinco rondas", size=18,
                            weight=ft.FontWeight.BOLD, color=TEXTO)]),
            self.historial,
        )
        cabecera = ft.Container(
            padding=20, border_radius=20,
            gradient=ft.LinearGradient(
                begin=ft.Alignment.CENTER_LEFT, end=ft.Alignment.CENTER_RIGHT,
                colors=["#38265D", "#22243F"],
            ),
            content=ft.Column([
                ft.Text("Piedra, Papel o Tijera", size=34, color=TEXTO,
                        weight=ft.FontWeight.BOLD),
                ft.Text("Juega contra la computadora.", size=15, color=SUAVE),
            ], spacing=4),
        )
        self.refrescar()
        pagina.add(ft.Container(max_width=920, content=ft.Column([
            cabecera,
            ft.ResponsiveRow([juego, estadisticas, historial], spacing=14, run_spacing=14),
        ], spacing=14, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)))

    @staticmethod
    def mostrar_opcion(icono, etiqueta, opcion):
        icono.icon = ICONOS.get(opcion, ft.Icons.QUESTION_MARK_ROUNDED)
        icono.color = COLORES.get(opcion, SUAVE)
        etiqueta.value = opcion.value if opcion else "—"

    async def jugar(self, evento):
        if self.animando:
            return
        opcion = evento.control.data
        self.animando = True
        self.reinicio.disabled = True
        for boton in self.botones:
            boton.disabled = True
        self.mostrar_opcion(self.icono_humano, self.eleccion_humana, opcion)
        self.resultado.value = "La computadora está eligiendo…"
        self.resultado.color = ACENTO
        self.detalle.value = "Tu jugada ya está elegida."

        try:
            for giro in list(Opcion) * 2:
                self.mostrar_opcion(self.icono_cpu, self.eleccion_cpu, giro)
                self.pagina.update()
                await asyncio.sleep(0.18)
            self.juego.jugar(opcion)
        finally:
            self.animando = False
            for boton in self.botones:
                boton.disabled = False
            self.refrescar()
            self.pagina.update()

    def reiniciar(self, evento):
        if self.animando:
            return
        self.juego.reiniciar()
        self.refrescar()
        self.pagina.update()

    def refrescar(self):
        juego = self.juego
        historial = juego.historial
        valores = [juego.estadisticas[resultado] for resultado in Resultado]
        colores = [color for _, color in RESULTADOS.values()]
        for control, valor, color in zip(
            self.contadores, [*valores, juego.rondas_jugadas], [*colores, TEXTO]
        ):
            control.value = str(valor)
            control.color = color
        self.reinicio.disabled = not historial

        ronda = historial[0] if historial else None
        self.mostrar_opcion(self.icono_humano, self.eleccion_humana,
                            ronda.humano if ronda else None)
        self.mostrar_opcion(self.icono_cpu, self.eleccion_cpu,
                            ronda.computadora if ronda else None)
        if ronda:
            self.resultado.value, self.resultado.color = RESULTADOS[ronda.resultado]
            self.detalle.value = f"Ronda {ronda.numero} completada"
        else:
            self.resultado.value = "Todo listo para jugar"
            self.resultado.color = TEXTO
            self.detalle.value = "Pulsa Piedra, Papel o Tijera para empezar."

        self.historial.controls = [
            ft.Container(
                padding=10, bgcolor="#26243A", border_radius=10,
                content=ft.Row([
                    ft.Text(f"Ronda {ronda.numero} · {ronda.humano} vs. {ronda.computadora}",
                            color=TEXTO, expand=True),
                    ft.Text(ronda.resultado.value, color=RESULTADOS[ronda.resultado][1],
                            weight=ft.FontWeight.BOLD),
                ]),
            )
            for ronda in historial
        ] or [ft.Text("Todavía no hay rondas.", color=SUAVE)]


def main(pagina: ft.Page):
    InterfazJuego(pagina, Juego()).montar()


if __name__ == "__main__":
    ft.run(main)
