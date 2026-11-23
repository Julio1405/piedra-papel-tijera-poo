import pytest

from juego import Juego
from modelos import Computadora, Opcion, Resultado


@pytest.mark.parametrize(
    "ganadora, perdedora",
    [(Opcion.PIEDRA, Opcion.TIJERA), (Opcion.TIJERA, Opcion.PAPEL),
     (Opcion.PAPEL, Opcion.PIEDRA)],
)
def test_reglas(ganadora, perdedora):
    assert Juego.determinar_resultado(ganadora, perdedora) is Resultado.VICTORIA
    assert Juego.determinar_resultado(perdedora, ganadora) is Resultado.DERROTA


@pytest.mark.parametrize("opcion", list(Opcion))
def test_empates(opcion):
    assert Juego.determinar_resultado(opcion, opcion) is Resultado.EMPATE


class ComputadoraConTijera(Computadora):
    def elegir(self, seleccion=None):
        return Opcion.TIJERA


@pytest.fixture
def juego():
    return Juego(computadora=ComputadoraConTijera("Computadora"))


def test_marcador_e_historial(juego):
    for opcion in ("Piedra", "Papel", "Tijera") * 2:
        juego.jugar(opcion)
    assert juego.estadisticas == dict.fromkeys(Resultado, 2)
    assert juego.rondas_jugadas == 6
    assert [ronda.numero for ronda in juego.historial] == [6, 5, 4, 3, 2]
    assert juego.historial[0].resultado is Resultado.EMPATE


def test_reinicio(juego):
    juego.jugar("Piedra")
    juego.reiniciar()
    assert juego.estadisticas == dict.fromkeys(Resultado, 0)
    assert juego.rondas_jugadas == 0
    assert juego.historial == ()
    assert juego.jugar("Piedra").numero == 1


def test_eleccion_invalida(juego):
    with pytest.raises(ValueError, match="Elige Piedra, Papel o Tijera"):
        juego.jugar("Lagarto")
    assert juego.rondas_jugadas == 0
    assert juego.historial == ()


def test_encapsulamiento(juego):
    juego.estadisticas[Resultado.VICTORIA] = 900
    assert juego.estadisticas[Resultado.VICTORIA] == 0
