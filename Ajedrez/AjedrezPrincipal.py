"""
Este archivo corre el operador principal del juego.
Es responsable de manejar la interacción del usuario y mostrar el objeto EstadoJuego
"""
import pygame as p
from Ajedrez import Maquinaria

p.init()
ANCHO = ALTO = 512  # Esto es resolución
DIMENSION = 8  # Las dimensiones de un tablero de ajedres son 8x8
TAMANO_CUAD = ALTO // DIMENSION
MAX_FPS = 15  # Para animaciones
IMAGENES = {}

"""
Cargar imágenes es una operacion costosa, por eso solo se hará una vez.
Inicializar un diccionario global de imagenes. Esto se hará exactamente una vez.
"""


def cargarImagenes():
    # Aquí estoy cargando las imágenes en el juego
    piezas = ["Ab", "An", "Cb", "Cn", "Db", "Dn", "Pb", "Pn", "Rb", "Rn", "Tb", "Tn"]
    for pieza in piezas:
        IMAGENES[pieza] = p.transform.scale(
            p.image.load("imagenes/" + pieza + ".png"),
            (TAMANO_CUAD, TAMANO_CUAD)
        )


"""
Este es el operador principal del código.
Va a manejar la interacción con usuario y actualizar las gráficas.
"""

def main():
    screen = p.display.set_mode((ANCHO, ALTO))
    reloj = p.time.Clock()
    screen.fill(p.Color("white"))
    ej = Maquinaria.EstadoJuego()
    movimientosValidos = ej.esMovimientoValido()
    movimientoHecho = False # variable Flag para verificar si el movimiento es valido
    cargarImagenes() # Solo se hace una vez

    corriendo = True
    cuadSelec = () # Ningun cuadrado seleccionado, mantiene el registro de el ultimo click del usuario, tupla (fil, col)
    clickJugador = [] # Mantiene el registro de los clicks de usuario [(fil1, col1),(fil2, col2)]}
    while corriendo:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # Eventos de mouse
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # coordenadas (x, y)
                col = location[0] // TAMANO_CUAD
                fil = location[1] // TAMANO_CUAD
                if cuadSelec == (fil, col): #Si el usuario clickea dos veces la misma pieza, la des selecciona
                    cuadSelec = ()
                    clickJugador = []
                else:
                    cuadSelec = (fil, col)
                    clickJugador.append(cuadSelec) #agrega el valor, tanto para el primer como el segundo click
                # ¿Acaba de hacer uno o dos clicks?
                if len(clickJugador) == 2: #despues del segundo click.
                    movimiento = Maquinaria.Mover(clickJugador[0], clickJugador[1], ej.tablero)
                    print(movimiento.obtenerNotacion())
                    if movimiento in movimientosValidos:
                        ej.mueve(movimiento)
                        movimientoHecho = True
                    cuadSelec = () # Reinicia la jugada
                    clickJugador = []

            # Controlador teclado
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # deshacer cuando presiona "z"
                    ej.deshacer()
                    movimientoHecho = True

        if movimientoHecho:
            movimientosValidos = ej.esMovimientoValido()
            movimientoHecho = False

        dibujarEstadoJuego(screen, ej)
        reloj.tick(MAX_FPS)
        p.display.flip()

"""
Responsable de todas las gráficas del estado de juego actual.
"""
def dibujarEstadoJuego(screen, ej):
    dibujarTablero(screen)
    dibujarPiezas(screen, ej.tablero)

"""
Dibuja los cuadrados del tablero, la esquina esquierda SIEMPRE es blanca.
"""


def dibujarTablero(pantalla):
    colores = [p.Color("white"), p.Color("light blue")]
    for f in range(DIMENSION):
        for c in range(DIMENSION):
            color = colores[((f+c)%2)]
            p.draw.rect(pantalla, color, p.Rect(f*TAMANO_CUAD, c*TAMANO_CUAD, TAMANO_CUAD, TAMANO_CUAD))


"""
Dibuja las piezas en el tablero usando el EstadoJuego.tablero actual
"""


def dibujarPiezas(pantalla, tablero):
    for f in range(DIMENSION):
        for c in range(DIMENSION):
            pieza = tablero[c][f]
            if pieza != "--": # NO es espacio en blanco
                pantalla.blit(IMAGENES[pieza], p.Rect(f*TAMANO_CUAD, c*TAMANO_CUAD, TAMANO_CUAD, TAMANO_CUAD))


if __name__ == "__main__":
    main()

