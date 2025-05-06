import pygame
import sys
import numpy as np
import time

# Inicializar pygame
pygame.init()

# Constantes para la configuración del juego
ANCHO, ALTO = 600, 600  # Dimensiones de la ventana del juego
LINEA_ANCHO = 15  # Grosor de las líneas del tablero
TABLERO_ANCHO = 15  # Grosor de las líneas del tablero
TAMANO_CELDA = ANCHO // 3  # Tamaño de cada celda del tablero
RADIO_CIRCULO = 60  # Radio del círculo que representa la IA
ANCHO_CRUZ = 25  # Grosor de la cruz que representa al jugador
ESPACIO_CRUZ = 55  # Espaciado interno de la cruz

# Colores utilizados en el juego
COLOR_FONDO = (28, 170, 156)  # Color de fondo
COLOR_LINEA = (23, 145, 135)  # Color de las líneas del tablero
COLOR_CIRCULO = (239, 231, 200)  # Color del círculo (IA)
COLOR_CRUZ = (66, 66, 66)  # Color de la cruz (Jugador)
COLOR_TEXTO = (239, 231, 200)  # Color del texto de los mensajes

# Configuración de la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))  # Crear la ventana del juego
pygame.display.set_caption('Tic Tac Toe - 1 Jugador vs IA')  # Título de la ventana
pantalla.fill(COLOR_FONDO)  # Rellenar el fondo con el color definido

# Tablero de juego representado como una matriz 3x3
tablero = np.zeros((3, 3))  # Inicialmente todas las casillas están vacías (0)

# Dibujar las líneas del tablero
def dibujar_lineas():
    # Líneas horizontales
    pygame.draw.line(pantalla, COLOR_LINEA, (0, TAMANO_CELDA), (ANCHO, TAMANO_CELDA), LINEA_ANCHO)
    pygame.draw.line(pantalla, COLOR_LINEA, (0, 2 * TAMANO_CELDA), (ANCHO, 2 * TAMANO_CELDA), LINEA_ANCHO)
    # Líneas verticales
    pygame.draw.line(pantalla, COLOR_LINEA, (TAMANO_CELDA, 0), (TAMANO_CELDA, ALTO), LINEA_ANCHO)
    pygame.draw.line(pantalla, COLOR_LINEA, (2 * TAMANO_CELDA, 0), (2 * TAMANO_CELDA, ALTO), LINEA_ANCHO)

# Dibujar las figuras (cruces y círculos) en el tablero
def dibujar_figuras():
    for fila in range(3):
        for col in range(3):
            if tablero[fila][col] == 1:  # Jugador (X)
                # Dibujar la cruz
                pygame.draw.line(pantalla, COLOR_CRUZ, 
                                (col * TAMANO_CELDA + ESPACIO_CRUZ, fila * TAMANO_CELDA + TAMANO_CELDA - ESPACIO_CRUZ),
                                (col * TAMANO_CELDA + TAMANO_CELDA - ESPACIO_CRUZ, fila * TAMANO_CELDA + ESPACIO_CRUZ), 
                                ANCHO_CRUZ)
                pygame.draw.line(pantalla, COLOR_CRUZ, 
                                (col * TAMANO_CELDA + ESPACIO_CRUZ, fila * TAMANO_CELDA + ESPACIO_CRUZ),
                                (col * TAMANO_CELDA + TAMANO_CELDA - ESPACIO_CRUZ, fila * TAMANO_CELDA + TAMANO_CELDA - ESPACIO_CRUZ), 
                                ANCHO_CRUZ)
            elif tablero[fila][col] == 2:  # IA (O)
                # Dibujar el círculo
                pygame.draw.circle(pantalla, COLOR_CIRCULO, 
                                  (int(col * TAMANO_CELDA + TAMANO_CELDA // 2), 
                                   int(fila * TAMANO_CELDA + TAMANO_CELDA // 2)), 
                                  RADIO_CIRCULO, 15)

# Marcar una casilla con el jugador correspondiente
def marcar_casilla(fila, col, jugador):
    tablero[fila][col] = jugador

# Verificar si una casilla está disponible
def casilla_disponible(fila, col):
    return tablero[fila][col] == 0

# Verificar si el tablero está lleno
def tablero_lleno():
    for fila in range(3):
        for col in range(3):
            if tablero[fila][col] == 0:  # Si hay una casilla vacía, el tablero no está lleno
                return False
    return True

# Verificar si un jugador ha ganado
def verificar_ganador(jugador):
    # Verificar filas
    for fila in range(3):
        if tablero[fila][0] == jugador and tablero[fila][1] == jugador and tablero[fila][2] == jugador:
            return True
    
    # Verificar columnas
    for col in range(3):
        if tablero[0][col] == jugador and tablero[1][col] == jugador and tablero[2][col] == jugador:
            return True
    
    # Verificar diagonales
    if tablero[0][0] == jugador and tablero[1][1] == jugador and tablero[2][2] == jugador:
        return True
    if tablero[0][2] == jugador and tablero[1][1] == jugador and tablero[2][0] == jugador:
        return True
    
    return False

# Algoritmo minimax para determinar el mejor movimiento de la IA
def minimax(tablero, profundidad, es_maximizando):
    # Condiciones base: verificar si hay un ganador o si el tablero está lleno
    if verificar_ganador(2):  # IA gana
        return 1
    elif verificar_ganador(1):  # Jugador gana
        return -1
    elif tablero_lleno():  # Empate
        return 0
    
    # Maximizar el puntaje para la IA
    if es_maximizando:
        mejor_puntaje = -np.inf
        for fila in range(3):
            for col in range(3):
                if tablero[fila][col] == 0:
                    tablero[fila][col] = 2
                    puntaje = minimax(tablero, profundidad + 1, False)
                    tablero[fila][col] = 0
                    mejor_puntaje = max(puntaje, mejor_puntaje)
        return mejor_puntaje
    # Minimizar el puntaje para el jugador
    else:
        mejor_puntaje = np.inf
        for fila in range(3):
            for col in range(3):
                if tablero[fila][col] == 0:
                    tablero[fila][col] = 1
                    puntaje = minimax(tablero, profundidad + 1, True)
                    tablero[fila][col] = 0
                    mejor_puntaje = min(puntaje, mejor_puntaje)
        return mejor_puntaje

# Determinar el mejor movimiento para la IA
def mejor_movimiento():
    mejor_puntaje = -np.inf
    movimiento = None
    
    for fila in range(3):
        for col in range(3):
            if tablero[fila][col] == 0:
                tablero[fila][col] = 2
                puntaje = minimax(tablero, 0, False)
                tablero[fila][col] = 0
                if puntaje > mejor_puntaje:
                    mejor_puntaje = puntaje
                    movimiento = (fila, col)
    
    if movimiento:
        return movimiento
    return None

# Mostrar un mensaje en la pantalla
def mostrar_mensaje(mensaje):
    pygame.time.delay(500)  # Pausa breve antes de mostrar el mensaje
    pantalla.fill(COLOR_FONDO)  # Limpiar la pantalla
    fuente = pygame.font.SysFont('courier', 40)  # Fuente del texto
    texto = fuente.render(mensaje, True, COLOR_TEXTO)  # Renderizar el mensaje
    pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - texto.get_height() // 2))  # Centrar el texto
    pygame.display.update()
    pygame.time.delay(3000)  # Mostrar el mensaje durante 3 segundos

# Reiniciar el juego
def reiniciar():
    pantalla.fill(COLOR_FONDO)  # Limpiar la pantalla
    dibujar_lineas()  # Redibujar las líneas del tablero
    for fila in range(3):
        for col in range(3):
            tablero[fila][col] = 0  # Vaciar el tablero

# Función principal del juego
def main():
    dibujar_lineas()  # Dibujar el tablero inicial
    jugador = 1  # 1 para humano (X), 2 para IA (O)
    juego_activo = True  # Estado del juego
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:  # Salir del juego
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.MOUSEBUTTONDOWN and juego_activo and jugador == 1:
                # Obtener la posición del clic del jugador
                mouseX = evento.pos[0] // TAMANO_CELDA
                mouseY = evento.pos[1] // TAMANO_CELDA
                
                if casilla_disponible(mouseY, mouseX):  # Verificar si la casilla está disponible
                    marcar_casilla(mouseY, mouseX, 1)  # Marcar la casilla para el jugador
                    
                    if verificar_ganador(1):  # Verificar si el jugador ganó
                        juego_activo = False
                        dibujar_figuras()
                        mostrar_mensaje('¡Ganaste!')
                    elif tablero_lleno():  # Verificar si hay empate
                        juego_activo = False
                        dibujar_figuras()
                        mostrar_mensaje('¡Empate!')
                    else:
                        jugador = 2  # Cambiar el turno a la IA
                        dibujar_figuras()
                        
                        # Turno de la IA
                        if juego_activo:
                            time.sleep(0.5)  # Pausa para simular "pensamiento"
                            movimiento = mejor_movimiento()
                            if movimiento:
                                fila, col = movimiento
                                marcar_casilla(fila, col, 2)
                                
                                if verificar_ganador(2):  # Verificar si la IA ganó
                                    juego_activo = False
                                    dibujar_figuras()
                                    mostrar_mensaje('¡La IA gana!')
                                elif tablero_lleno():  # Verificar si hay empate
                                    juego_activo = False
                                    dibujar_figuras()
                                    mostrar_mensaje('¡Empate!')
                                else:
                                    jugador = 1  # Cambiar el turno al jugador
                            
                            dibujar_figuras()
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:  # Reiniciar el juego al presionar "R"
                    reiniciar()
                    juego_activo = True
                    jugador = 1
        
        pygame.display.update()  # Actualizar la pantalla

# Ejecutar el juego si el archivo se ejecuta directamente
if __name__ == "__main__":
    main()