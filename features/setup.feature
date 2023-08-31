Feature: Setup

  Escenario: Elección de tamaño de grilla y nombre de usuario
    Dado que estoy en la página de inicio del juego
    Cuando elijo el tamaño de grilla "50x50"
    Y ingreso el nombre de usuario "jugador1"
    Y hago clic en el botón "Comenzar partida"
    Entonces debería ver la pantalla de inicio de la partida

  Escenario: Elección de equipo
    Dado que estoy en la pantalla de inicio de la partida
    Y ya he ingresado el nombre de usuario "jugador2"
    Cuando elijo el equipo "Equipo del Agua"
    Y hago clic en el botón "Comenzar partida"
    Entonces debería ver la pantalla de juego con el equipo "Equipo del Agua"

  Escenario: Inicio de partida con nombre de usuario vacío
    Dado que estoy en la página de inicio del juego
    Cuando dejo el campo de nombre de usuario vacío
    Y elijo el tamaño de grilla "75x75"
    Y hago clic en el botón "Comenzar partida"
    Entonces debería ver un mensaje de error indicando que el nombre de usuario es requerido
