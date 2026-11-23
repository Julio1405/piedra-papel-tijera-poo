"""Reglas y estado de una partida."""
from collections import Counter, deque

from modelos import Computadora, JugadorHumano, Opcion, Participante, Resultado, Ronda


class Juego:
    _GANA_A = {
        Opcion.PIEDRA: Opcion.TIJERA,
        Opcion.TIJERA: Opcion.PAPEL,
        Opcion.PAPEL: Opcion.PIEDRA,
    }

    def __init__(self, humano: Participante | None = None,
                 computadora: Participante | None = None):
        self.humano = humano if humano is not None else JugadorHumano("Tú")
        self.computadora = computadora if computadora is not None else Computadora("Computadora")
        self._marcador: Counter[Resultado] = Counter()
        self._historial: deque[Ronda] = deque(maxlen=5)

    @property
    def estadisticas(self) -> dict[Resultado, int]:
        return {resultado: self._marcador[resultado] for resultado in Resultado}

    @property
    def rondas_jugadas(self) -> int:
        return self._marcador.total()

    @property
    def historial(self) -> tuple[Ronda, ...]:
        return tuple(self._historial)

    @classmethod
    def determinar_resultado(cls, humano: Opcion, computadora: Opcion) -> Resultado:
        if humano == computadora:
            return Resultado.EMPATE
        if cls._GANA_A[humano] == computadora:
            return Resultado.VICTORIA
        return Resultado.DERROTA

    def jugar(self, seleccion: str) -> Ronda:
        humano = self.humano.elegir(seleccion)
        computadora = self.computadora.elegir()
        resultado = self.determinar_resultado(humano, computadora)
        ronda = Ronda(self.rondas_jugadas + 1, humano, computadora, resultado)
        self._marcador[resultado] += 1
        self._historial.appendleft(ronda)
        return ronda

    def reiniciar(self) -> None:
        self._marcador.clear()
        self._historial.clear()
