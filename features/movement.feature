Feature: Movimiento de células del mismo equipo

  Escenario: Mover célula de nivel 1 a una celda adyacente vacía
    Dado que tengo una célula de nivel 1 en la posición (3, 3)
    Y la celda adyacente en la posición (4, 3) está vacía
    Cuando intento mover la célula a la posición (4, 3)
    Entonces la célula se mueve exitosamente a la posición (4, 3)

  Escenario: Intentar mover célula de nivel 1 a una celda ocupada por otra célula de nivel 1
    Dado que tengo una célula de nivel 1 en la posición (3, 3)
    Y otra célula de nivel 1 en la posición (4, 3)
    Cuando intento mover la célula a la posición (4, 3)
    Entonces las células se fusionan generando una nueva célula nivel 2 en la posición (4, 3)

  Escenario: Intentar mover célula de nivel 1 a una celda adyacente ocupada por célula de nivel 3
    Dado que tengo una célula de nivel 1 en la posición (3, 3)
    Y una célula de nivel 3 en la posición (4, 3)
    Cuando intento mover la célula nivel 1 a la posición (4, 3)
    Entonces ambas células coexisten en la celda (4, 3)

  Escenario: Intentar mover célula de nivel 2 a una celda adyacente ocupada por célula de nivel 1
    Dado que tengo una célula de nivel 2 en la posición (3, 3)
    Y una célula de nivel 1 en la posición (4, 3)
    Cuando intento mover la célula nivel 2 a la posición (4, 3)
    Entonces las células no pueden fusionarse y ambas coexisten en la posición (4, 3)

  Escenario: Mover célula a celda ocupada por 2 células de diferente nivel (coexistiendo)
    Dado que tengo una célula de nivel 1 en la posición (2, 2)
    Y una célula de nivel 2 en la posición (2, 2)
    Y tengo otra célula de nivel 1 en la posición (3, 2)
    Cuando intento mover la célula nivel 1 a la posición (2, 2)
    Entonces mueren las células de nivel 1 y sobrevive la célula de nivel 2 en la posicion (2,2)
