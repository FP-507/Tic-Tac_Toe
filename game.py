import pygame
import sys

# Inicializar pygame
pygame.init()

# Constantes
ANCHO, ALTO = 600, 600
LINEA_ANCHO = 15
TABLERO_ANCHO = 15
TAMANO_CELDA = ANCHO // 3
RADIO_CIRCULO = 60
ANCHO_CRUZ = 25
ESPACIO_CRUZ = 55

# Colores
COLOR_FONDO = (28, 170, 156)
COLOR_LINEA = (23, 145, 135)
COLOR_CIRCULO = (239, 231, 200)
COLOR_CRUZ = (66, 66, 66)

# Configuración de la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Tic Tac Toe')
pantalla.fill(COLOR_FONDO)

# Tablero
tablero = [[None for _ in range(3)] for _ in range(3)]

# Dibujar líneas del tablero
def dibujar_lineas():
    # Líneas horizontales
    pygame.draw.line(pantalla, COLOR_LINEA, (0, TAMANO_CELDA), (ANCHO, TAMANO_CELDA), LINEA_ANCHO)
    pygame.draw.line(pantalla, COLOR_LINEA, (0, 2 * TAMANO_CELDA), (ANCHO, 2 * TAMANO_CELDA), LINEA_ANCHO)
    # Líneas verticales
    pygame.draw.line(pantalla, COLOR_LINEA, (TAMANO_CELDA, 0), (TAMANO_CELDA, ALTO), LINEA_ANCHO)
    pygame.draw.line(pantalla, COLOR_LINEA, (2 * TAMANO_CELDA, 0), (2 * TAMANO_CELDA, ALTO), LINEA_ANCHO)

# Dibujar figuras
def dibujar_figuras():
    for fila in range(3):
        for col in range(3):
            if tablero[fila][col] == 'O':
                pygame.draw.circle(pantalla, COLOR_CIRCULO, 
                                  (int(col * TAMANO_CELDA + TAMANO_CELDA // 2), 
                                   int(fila * TAMANO_CELDA + TAMANO_CELDA // 2)), 
                                  RADIO_CIRCULO, 15)
            elif tablero[fila][col] == 'X':
                # Dibujar X (dos líneas cruzadas)
                pygame.draw.line(pantalla, COLOR_CRUZ, 
                                (col * TAMANO_CELDA + ESPACIO_CRUZ, fila * TAMANO_CELDA + TAMANO_CELDA - ESPACIO_CRUZ),
                                (col * TAMANO_CELDA + TAMANO_CELDA - ESPACIO_CRUZ, fila * TAMANO_CELDA + ESPACIO_CRUZ), 
                                ANCHO_CRUZ)
                pygame.draw.line(pantalla, COLOR_CRUZ, 
                                (col * TAMANO_CELDA + ESPACIO_CRUZ, fila * TAMANO_CELDA + ESPACIO_CRUZ),
                                (col * TAMANO_CELDA + TAMANO_CELDA - ESPACIO_CRUZ, fila * TAMANO_CELDA + TAMANO_CELDA - ESPACIO_CRUZ), 
                                ANCHO_CRUZ)

# Marcar casilla
def marcar_casilla(fila, col, jugador):
    tablero[fila][col] = jugador

# Verificar casilla disponible
def casilla_disponible(fila, col):
    return tablero[fila][col] is None

# Verificar si el tablero está lleno
def tablero_lleno():
    for fila in range(3):
        for col in range(3):
            if tablero[fila][col] is None:
                return False
    return True

# Verificar ganador
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

# Mostrar mensaje de fin de juego
def mostrar_mensaje(mensaje):
    pygame.time.delay(500)
    pantalla.fill(COLOR_FONDO)
    fuente = pygame.font.SysFont('courier', 40)
    texto = fuente.render(mensaje, True, COLOR_CRUZ)
    pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - texto.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(3000)

# Reiniciar juego
def reiniciar():
    pantalla.fill(COLOR_FONDO)
    dibujar_lineas()
    for fila in range(3):
        for col in range(3):
            tablero[fila][col] = None

# Función principal
def main():
    dibujar_lineas()
    jugador = 'X'
    juego_activo = True
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.MOUSEBUTTONDOWN and juego_activo:
                mouseX = evento.pos[0] // TAMANO_CELDA
                mouseY = evento.pos[1] // TAMANO_CELDA
                
                if casilla_disponible(mouseY, mouseX):
                    marcar_casilla(mouseY, mouseX, jugador)
                    
                    if verificar_ganador(jugador):
                        juego_activo = False
                        dibujar_figuras()
                        mostrar_mensaje(f'¡Jugador {jugador} gana!')
                    elif tablero_lleno():
                        juego_activo = False
                        dibujar_figuras()
                        mostrar_mensaje('¡Empate!')
                    else:
                        jugador = 'O' if jugador == 'X' else 'X'
                    
                    dibujar_figuras()
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    reiniciar()
                    juego_activo = True
                    jugador = 'X'
        
        pygame.display.update()

if __name__ == "__main__":
    main()