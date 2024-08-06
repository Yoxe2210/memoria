import pygame
import sys
import math
import time
import random

pygame.init()
pygame.font.init()
pygame.mixer.init()

altura_boton = 30
medida_cuadro = 130
nombre_imagen_oculta = "imagenes/oculta.png"
imagen_oculta = pygame.image.load(nombre_imagen_oculta)
segundos_mostrar_pieza = 2

class Cuadro:
    def __init__(self, fuente_imagen):
        self.mostrar = True
        self.descubierto = False
        self.fuente_imagen = fuente_imagen
        self.imagen_real = pygame.image.load(fuente_imagen)
        

cuadros = [
    [Cuadro("img/circulo.jpg"), Cuadro("img/circulo.jpg"),
     Cuadro("img/cuadrado.jpg"), Cuadro("img/cuadrado.jpg")],
    [Cuadro("img/diamante.jpg"), Cuadro("img/diamante.jpg"),
     Cuadro("img/ovalo.jpg"), Cuadro("img/ovalo.jpg")],
    [Cuadro("img/triangulo.jpg"), Cuadro("img/triangulo.jpg"),
     Cuadro("img/otro.jpg"), Cuadro("img/otro.jpg")],
    [Cuadro("img/hexagono.jpg"), Cuadro("img/hexagono.jpg"),
     Cuadro("img/rectangulo.jpg"), Cuadro("img/rectangulo.jpg")],
]

color_blanco = (255, 255, 255)
color_negro = (0, 0, 0)
color_gris = (206, 206, 206)
color_azul = (30, 136, 229)
color_verde = (0, 255, 0)
color_rojo = (255, 0, 0)

sonido_fondo = pygame.mixer.Sound("imagenes/fondo.wav")
sonido_clic = pygame.mixer.Sound("imagenes/clic.wav")
sonido_exito = pygame.mixer.Sound("imagenes/ganador.wav")
sonido_fracaso = pygame.mixer.Sound("imagenes/equivocado.wav")
sonido_voltear = pygame.mixer.Sound("imagenes/voltear.wav")

anchura_pantalla = len(cuadros[0]) * medida_cuadro
altura_pantalla = (len(cuadros) * medida_cuadro) + altura_boton
anchura_boton = anchura_pantalla

tamanio_fuente = 20
fuente = pygame.font.SysFont("Arial", tamanio_fuente)
xFuente = int((anchura_boton / 2) - (tamanio_fuente / 2))
yFuente = int(altura_pantalla - altura_boton)

boton = pygame.Rect(0, altura_pantalla - altura_boton, anchura_boton, altura_boton)

ultimos_segundos = None
puede_jugar = True
juego_iniciado = False
x1 = None
y1 = None
x2 = None
y2 = None

def ocultar_todos_los_cuadros():
    for fila in cuadros:
        for cuadro in fila:
            cuadro.mostrar = False
            cuadro.descubierto = False

def aleatorizar_cuadros():
    cantidad_filas = len(cuadros)
    cantidad_columnas = len(cuadros[0])
    for y in range(cantidad_filas):
        for x in range(cantidad_columnas):
            x_aleatorio = random.randint(0, cantidad_columnas - 1)
            y_aleatorio = random.randint(0, cantidad_filas - 1)
            cuadro_temporal = cuadros[y][x]
            cuadros[y][x] = cuadros[y_aleatorio][x_aleatorio]
            cuadros[y_aleatorio][x_aleatorio] = cuadro_temporal

def comprobar_si_gana():
    if gana():
        pygame.mixer.Sound.play(sonido_exito)
        mostrar_mensaje_reinicio()

def gana():
    for fila in cuadros:
        for cuadro in fila:
            if not cuadro.descubierto:
                return False
    return True

def mostrar_mensaje_reinicio():
    global puede_jugar
    puede_jugar = False
    pantalla_juego.fill(color_blanco)
    mensaje = "Felicidades Completaste el Juego! ¿Quieres volver a jugar?"
    texto = fuente.render(mensaje, True, color_negro)
    rect_texto = texto.get_rect(center=(anchura_pantalla / 2, altura_pantalla / 2 - 30))
    pantalla_juego.blit(texto, rect_texto)

    boton_si = pygame.Rect(anchura_pantalla / 2 - 75, altura_pantalla / 2, 60, 30)
    boton_no = pygame.Rect(anchura_pantalla / 2 + 15, altura_pantalla / 2, 60, 30)

    pygame.draw.rect(pantalla_juego, color_verde, boton_si)
    pygame.draw.rect(pantalla_juego, color_rojo, boton_no)

    texto_si = fuente.render("Sí", True, color_blanco)
    texto_no = fuente.render("No", True, color_blanco)

    pantalla_juego.blit(texto_si, (anchura_pantalla / 2 - 55, altura_pantalla / 2 + 5))
    pantalla_juego.blit(texto_no, (anchura_pantalla / 2 + 35, altura_pantalla / 2 + 5))

    pygame.display.update()

    esperando_respuesta = True
    while esperando_respuesta:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton_si.collidepoint(event.pos):
                    reiniciar_juego()
                    esperando_respuesta = False
                elif boton_no.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

def reiniciar_juego():
    global juego_iniciado, x1, y1, x2, y2, ultimos_segundos, puede_jugar
    juego_iniciado = False
    x1 = None
    y1 = None
    x2 = None
    y2 = None
    ultimos_segundos = None
    puede_jugar = True
    iniciar_juego()

def iniciar_juego():
    pygame.mixer.Sound.play(sonido_clic)
    global juego_iniciado
    for i in range(3):
        aleatorizar_cuadros()
    ocultar_todos_los_cuadros()
    juego_iniciado = True

pantalla_juego = pygame.display.set_mode((anchura_pantalla, altura_pantalla))
pygame.display.set_caption('Memoria del inicio del sistema')
pygame.mixer.Sound.play(sonido_fondo, -1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and puede_jugar:
            xAbsoluto, yAbsoluto = event.pos
            if boton.collidepoint(event.pos):
                if not juego_iniciado:
                    iniciar_juego()
                else:
                    reiniciar_juego()
            else:
                if not juego_iniciado:
                    continue
                x = math.floor(xAbsoluto / medida_cuadro)
                y = math.floor(yAbsoluto / medida_cuadro)
                cuadro = cuadros[y][x]
                if cuadro.mostrar or cuadro.descubierto:
                    continue
                if x1 is None and y1 is None:
                    x1 = x
                    y1 = y
                    cuadros[y1][x1].mostrar = True
                    pygame.mixer.Sound.play(sonido_voltear)
                else:
                    x2 = x
                    y2 = y
                    cuadros[y2][x2].mostrar = True
                    cuadro1 = cuadros[y1][x1]
                    cuadro2 = cuadros[y2][x2]
                    if cuadro1.fuente_imagen == cuadro2.fuente_imagen:
                        cuadros[y1][x1].descubierto = True
                        cuadros[y2][x2].descubierto = True
                        x1 = None
                        x2 = None
                        y1 = None
                        y2 = None
                        pygame.mixer.Sound.play(sonido_clic)
                    else:
                        pygame.mixer.Sound.play(sonido_fracaso)
                        ultimos_segundos = int(time.time())
                        puede_jugar = False
                comprobar_si_gana()

    ahora = int(time.time())
    if ultimos_segundos is not None and ahora - ultimos_segundos >= segundos_mostrar_pieza:
        cuadros[y1][x1].mostrar = False
        cuadros[y2][x2].mostrar = False
        x1 = None
        x2 = None
        y1 = None
        y2 = None
        ultimos_segundos = None
        puede_jugar = True

    pantalla_juego.fill(color_gris)

    for y in range(len(cuadros)):
        for x in range(len(cuadros[y])):
            cuadro = cuadros[y][x]
            if cuadro.mostrar or cuadro.descubierto:
                pantalla_juego.blit(cuadro.imagen_real, (x * medida_cuadro, y * medida_cuadro))
            else:
                pantalla_juego.blit(imagen_oculta, (x * medida_cuadro, y * medida_cuadro))

    if not juego_iniciado:
        pygame.draw.rect(pantalla_juego, color_azul, boton)
        texto_boton = fuente.render("Iniciar juego", True, color_blanco)
        pantalla_juego.blit(texto_boton, (xFuente, yFuente))
    else:
        pygame.draw.rect(pantalla_juego, color_azul, boton)
        texto_boton = fuente.render("Reiniciar juego", True, color_blanco)
        pantalla_juego.blit(texto_boton, (xFuente, yFuente))

    pygame.display.update()
