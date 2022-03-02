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
    """
    Toma un movimiento como parámetro y lo ejecuta. No sirve para enrocar, coronar ni --
    """
    def mueve(self, mover):
        self.tablero[mover.filInicio][mover.colInicio] = "--"
        self.tablero[mover.filFinal][mover.colFinal] = mover.piezaMovida
        self.registroMov.append(mover)  # Guarda el movimiento para des hacerlo o verlo en el futuro
        self.mueveBlanco = not self.mueveBlanco

    """
    Deshace el último movimiento
    """
    def deshacer(self):
        if len(self.registroMov) != 0:  # Asegura que hay al menos un movimiento que deshacer
            mover = self.registroMov.pop()
            self.tablero[mover.filInicio][mover.colInicio] = mover.piezaMovida
            self.tablero[mover.filFinal][mover.colFinal] = mover.piezaCapturada
            self.mueveBlanco = not self.mueveBlanco

    """
    Todos los movimientos incluyendo cuando el rey está en jaque
    """
    def esMovimientoValido(self):
        return self.esPosibleMovimiento() # Por el momento no nos vamos a preocupar por esta función.

    """
    Todos los movimientos sin considerar jaques
    """
    def esPosibleMovimiento(self):
        movimientos = [Mover((6,4), (4,4), self.tablero)]
        for fila in range(len(self.tablero)):
            for columna in range(len(self.tablero[fila])):
                turno = self.tablero[fila][columna][1]
                if (turno == "b" and self.mueveBlanco) and (turno == "n" and not self.mueveBlanco):
                    pieza = self.tablero[fila][columna][0]
                    if pieza == 'P':
                        self.obtenMovimientoPeon(fila, columna, movimientos)
                    elif pieza == 'T':
                        self.obtenMovimientoTorre(fila, columna, movimientos)
        return movimientos

    """
    Obtiene el movimiento de los peones.
    """
    def obtenerMovimientoPeon(self, f, c, movimientos):
        pass

    """
    Obtiene el movimiento de las torres.
    """
    def obtenerMovimientoTorre(self, f, c, movimientos):
        pass




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
        self.idMovimiento = self.filInicio * 1000 + self.colInicio * 100 + self.filFinal * 10 + self.colFinal
        print(self.idMovimiento)

    """
    Override el metodo igual, por lo que usamos una clase para mover, toca hacer esto
    """

    def __eq__(self, otro):
        if isinstance(otro, Mover):
            return self.idMovimiento == otro.idMovimiento
        return False


    def obtenerNotacion(self):
        return (
                self.obtenerCoordenadas(self.filInicio, self.colInicio) +
                self.obtenerCoordenadas(self.filFinal, self.colFinal)
        )

    def obtenerCoordenadas(self, f, c):
        return self.columnasAHor[c] + self.filaAVertical[f]
