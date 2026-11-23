"""Participantes y valores que se intercambian durante una ronda."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import StrEnum
import random


class Opcion(StrEnum):
    PIEDRA = "Piedra"
    PAPEL = "Papel"
    TIJERA = "Tijera"


class Resultado(StrEnum):
    VICTORIA = "Victoria"
    DERROTA = "Derrota"
    EMPATE = "Empate"


@dataclass(frozen=True)
class Ronda:
    numero: int
    humano: Opcion
    computadora: Opcion
    resultado: Resultado


class Participante(ABC):
    def __init__(self, nombre: str):
        self.nombre = nombre

    @abstractmethod
    def elegir(self, seleccion: str | None = None) -> Opcion:
        """Devuelve la opción del participante."""


class JugadorHumano(Participante):
    def elegir(self, seleccion: str | None = None) -> Opcion:
        try:
            return Opcion(seleccion)
        except ValueError:
            raise ValueError("Elige Piedra, Papel o Tijera.") from None


class Computadora(Participante):
    def elegir(self, seleccion: str | None = None) -> Opcion:
        return random.choice(tuple(Opcion))
