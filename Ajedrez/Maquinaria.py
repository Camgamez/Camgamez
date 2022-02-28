"""
Esta clase es responsable de guardar toda la información sobre el estado actual del juego. También es responsable
de determinar si el movimiento es válido y va a mantener un registro de los movimientos.
"""

class EstadoJuego():
    def __init__(self):
        # El tablero es in arreglo bi-dimensional 8x8. Cada elemento de la lista tiene dos caracteres.
        # El primer caracter representa el tipo de ficha "T", "C", "A", "D", "T"
        # El segundo caracter representa el color "b" o "n"

        self.tablero = [
            ["Tn", "Cn", "An", "Dn", "Rn", "An", "Cn", "Tn"],
            ["Pn", "Pn", "Pn", "Pn", "Pn", "Pn", "Pn", "Pn"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["Pb", "Pb", "Pb", "Pb", "Pb", "Pb", "Pb", "Pb"],
            ["Tb", "Cb", "Ab", "Db", "Rb", "Ab", "Cb", "Tb"]
        ]
        self.mueveBlanco = True
        self.registroMov = []

    def mueve(self, mover):
        self.tablero[mover.filInicio][mover.colInicio] = "--"
        self.tablero[mover.filFinal][mover.colFinal] = mover.piezaMovida
        self.registroMov.append(mover) #Guarda el movimiento para des hacerlo o verlo en el futuro
        self.mueveBlanco = not self.mueveBlanco


class Mover():
    # mapea llaves a sus valores
    # llave: valor
    verticalAfilas = {"1": 7, "2": 6, "3": 5, "4": 4,
                      "5": 3, "6": 2, "7": 1, "8": 0
                      }
    filaAVertical = {v: k for k, v in verticalAfilas.items()}

    horizontalACol = {"a": 0, "b": 1, "c": 2, "d": 3,
                      "e": 4, "f": 5, "g": 6, "h": 7
                      }
    columnasAHor = {v: k for k, v in horizontalACol.items()}

    def __init__(self, posInicio, posFin, tablero):
        self.filInicio = posInicio[0]
        self.colInicio = posInicio[1]

        self.filFinal = posFin[0]
        self.colFinal = posFin[1]

        self.piezaMovida = tablero[self.filInicio][self.colInicio]
        self.piezaCapturada = tablero[self.filFinal][self.colFinal]

    def obtenerNotacion(self):
        return (
                self.obtenerCoordenadas(self.filInicio, self.colInicio) +
                self.obtenerCoordenadas(self.filFinal, self.colFinal)
        )

    def obtenerCoordenadas(self, f, c):
        return self.columnasAHor[c] + self.filaAVertical[f]
