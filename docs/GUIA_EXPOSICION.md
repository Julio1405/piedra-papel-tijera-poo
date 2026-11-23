# Guía de exposición

## Qué hace el programa

El jugador elige Piedra, Papel o Tijera y la computadora elige al azar. La pantalla muestra las dos elecciones y el resultado, acumula el marcador y guarda las cinco rondas más recientes durante la partida.

## Demostración

1. Pulsa **Piedra** y señala las dos elecciones y el resultado. Si ambos eligieron Piedra, usa el empate para explicar la regla de igualdad.
2. Juega cinco rondas más. El marcador cuenta seis y el historial muestra de la ronda 6 a la 2. Suma victorias, derrotas y empates para comprobar el total.
3. Pulsa **Reiniciar partida**. Comprueba que los cuatro indicadores quedan en cero y el historial se vacía. Juega otra ronda y muestra que vuelve a ser la ronda 1.

## Clases y conceptos

- **Participante** guarda el nombre y exige que sus subclases implementen `elegir()`. Es una abstracción del comportamiento que ambos jugadores tienen en común.
- **JugadorHumano** y **Computadora** heredan de `Participante`. La primera clase valida la opción recibida y la segunda usa `random.choice()`.
- **Polimorfismo.** El juego llama a `elegir()` en ambos objetos. El método que se ejecuta depende de la clase concreta del participante.
- **Juego** contiene la regla y el estado. Lee las elecciones, genera una `Ronda` y actualiza sus colecciones internas. Las propiedades entregan un diccionario nuevo y una tupla de rondas inmutables, lo que protege los datos al consultarlos.
- **InterfazJuego** construye los controles Flet. Pulsar un botón activa un callback que llama a `Juego` y después refresca la pantalla.
- **Opcion**, **Resultado** y **Ronda** representan el vocabulario y los datos de cada jugada.

Si preguntan por la arquitectura, explica que `modelos.py` define los participantes y los datos, `juego.py` aplica las reglas y `main.py` conecta Flet a la partida. Por eso pytest puede comprobar las reglas sin abrir una ventana. En la versión estática, Pyodide ejecuta Python dentro del navegador.

## Guion de cuatro minutos

| Tiempo | Qué decir y mostrar |
|---|---|
| 0:00–0:35 | «Este juego permite jugar contra la computadora y ver cómo evoluciona el marcador». Abre la pantalla inicial y señala los tres botones. |
| 0:35–1:20 | Juega una ronda. Lee las dos elecciones y explica que piedra gana a tijera, tijera a papel y papel a piedra. Si las opciones son iguales, hay empate. |
| 1:20–2:00 | Completa seis rondas, comprueba el límite del historial y muestra el reinicio. |
| 2:00–3:15 | Abre el diagrama del informe. Explica `Participante`, sus dos subclases, las dos llamadas a `elegir()` y las propiedades de `Juego`. |
| 3:15–4:00 | Señala el callback y explica cómo se actualiza la interfaz. Comenta que las pruebas simulan una computadora con elección fija y que una entrada inválida deja las estadísticas intactas. |
