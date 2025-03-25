import pygame
import random
import sys
import math
import os

# Inicialización de Pygame
pygame.init()
pygame.mixer.init()

# Configuraciones de pantalla
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Galaxian Defender")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

# Fuentes
pygame.font.init()
fuente_titulo = pygame.font.Font(None, 74)
fuente_menu = pygame.font.Font(None, 36)

class Jugador(pygame.sprite.Sprite):
    def __init__(self, imagen_nave):
        super().__init__()
        # Manejar imagen con ruta completa
        self.image = pygame.image.load(imagen_nave)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO - 10
        self.velocidad_x = 0
        self.vidas = 3
        self.puntuacion = 0
        self.nivel_actual = 1

    def update(self):
        self.rect.x += self.velocidad_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO

    def disparar(self):
        bala = Bala(self.rect.centerx, self.rect.top)
        return bala

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, imagen_enemigo, tipo_movimiento):
        super().__init__()
        # Manejar imagen con ruta completa
        self.image = pygame.image.load(imagen_enemigo)
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.velocidad_y = random.randrange(1, 5)
        self.tipo_movimiento = tipo_movimiento
        self.contador_movimiento = 0

    def update(self):
        # Diferentes tipos de movimiento de enemigos
        if self.tipo_movimiento == 'zigzag':
            self.rect.y += self.velocidad_y
            self.rect.x += math.sin(self.contador_movimiento * 0.1) * 2
            self.contador_movimiento += 1
        elif self.tipo_movimiento == 'diagonal':
            self.rect.y += self.velocidad_y
            self.rect.x += self.velocidad_y / 2
        else:
            self.rect.y += self.velocidad_y

        if self.rect.top > ALTO:
            self.rect.x = random.randrange(ANCHO - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.velocidad_y = random.randrange(1, 5)

class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 15))
        self.image.fill(BLANCO)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.velocidad_y = -10

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.bottom < 0:
            self.kill()

def dibujar_texto(superficie, texto, tamaño, x, y, color):
    fuente = pygame.font.Font(None, tamaño)
    texto_superficie = fuente.render(texto, True, color)
    texto_rect = texto_superficie.get_rect()
    texto_rect.midtop = (x, y)
    superficie.blit(texto_superficie, texto_rect)

def seleccion_nave():
    pantalla.fill(NEGRO)
    dibujar_texto(pantalla, "SELECCIONA TU NAVE", 74, ANCHO//2, ALTO//4, BLANCO)
    
    # Cargar imágenes de naves
    naves = [
        os.path.join('imagenes', 'nave1.png'),
        os.path.join('imagenes', 'nave2.png'),
        os.path.join('imagenes', 'nave3.png')
    ]
    
    # Verificar que existan las imágenes
    for nave in naves:
        if not os.path.exists(nave):
            print(f"Falta la imagen: {nave}")
            sys.exit()
    
    # Cargar imágenes de naves
    imagenes_naves = [pygame.image.load(nave) for nave in naves]
    imagenes_naves = [pygame.transform.scale(img, (100, 100)) for img in imagenes_naves]
    
    # Posiciones de las naves
    posiciones = [
        (ANCHO//4, ALTO//2),
        (ANCHO//2, ALTO//2),
        (3*ANCHO//4, ALTO//2)
    ]
    
    # Dibujar naves
    for i, (img, pos) in enumerate(zip(imagenes_naves, posiciones)):
        rect = img.get_rect(center=pos)
        pantalla.blit(img, rect)
        # Número de selección
        dibujar_texto(pantalla, f"Nave {i+1} - Pulsa {i+1}", 36, pos[0], pos[1]+100, BLANCO)
    
    pygame.display.flip()
    
    # Esperar selección
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    return naves[0]
                if evento.key == pygame.K_2:
                    return naves[1]
                if evento.key == pygame.K_3:
                    return naves[2]

def pantalla_inicio():
    pantalla.fill(NEGRO)
    dibujar_texto(pantalla, "GALAXIAN DEFENDER", 74, ANCHO//2, ALTO//4, BLANCO)
    dibujar_texto(pantalla, "Presiona ESPACIO para comenzar", 36, ANCHO//2, ALTO//2, BLANCO)
    dibujar_texto(pantalla, "Presiona Q para salir", 36, ANCHO//2, ALTO*3//4, BLANCO)
    pygame.display.flip()
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return
                if evento.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def pantalla_game_over(puntuacion):
    pantalla.fill(NEGRO)
    dibujar_texto(pantalla, "GAME OVER", 74, ANCHO//2, ALTO//4, ROJO)
    dibujar_texto(pantalla, f"Puntuación: {puntuacion}", 36, ANCHO//2, ALTO//2, BLANCO)
    dibujar_texto(pantalla, "Presiona R para reiniciar", 36, ANCHO//2, ALTO*3//4, BLANCO)
    pygame.display.flip()
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    return
                if evento.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def crear_formacion_enemigos(nivel, imagen_enemigo):
    tipos_movimiento = ['normal', 'zigzag', 'diagonal']
    enemigos = pygame.sprite.Group()
    
    # Cantidad de enemigos aumenta con el nivel
    num_enemigos = 8 + (nivel * 2)
    for i in range(num_enemigos):
        # Distribución aleatoria de tipos de movimiento
        tipo_movimiento = random.choice(tipos_movimiento)
        enemigo = Enemigo(imagen_enemigo, tipo_movimiento)
        enemigos.add(enemigo)
    
    return enemigos

def juego_principal(imagen_nave, imagen_enemigo):
    # Configuración del reloj
    reloj = pygame.time.Clock()

    # Grupos de sprites
    todos_los_sprites = pygame.sprite.Group()
    enemigos = pygame.sprite.Group()
    balas = pygame.sprite.Group()

    # Crear jugador
    jugador = Jugador(imagen_nave)
    todos_los_sprites.add(jugador)

    # Crear enemigos iniciales
    enemigos = crear_formacion_enemigos(jugador.nivel_actual, imagen_enemigo)
    todos_los_sprites.add(enemigos)

    # Bucle principal del juego
    ejecutando = True
    while ejecutando:
        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    jugador.velocidad_x = -5
                if evento.key == pygame.K_RIGHT:
                    jugador.velocidad_x = 5
                if evento.key == pygame.K_SPACE:
                    bala = jugador.disparar()
                    todos_los_sprites.add(bala)
                    balas.add(bala)
            
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                    jugador.velocidad_x = 0

        # Actualizar
        todos_los_sprites.update()

        # Colisiones bala-enemigo
        colisiones = pygame.sprite.groupcollide(enemigos, balas, True, True)
        for colision in colisiones:
            jugador.puntuacion += 10
            
            # Verificar si se ha eliminado todos los enemigos
            if len(enemigos) == 0:
                jugador.nivel_actual += 1
                enemigos = crear_formacion_enemigos(jugador.nivel_actual, imagen_enemigo)
                todos_los_sprites.add(enemigos)

        # Colisiones enemigo-jugador
        colisiones_jugador = pygame.sprite.spritecollide(jugador, enemigos, True)
        for colision in colisiones_jugador:
            jugador.vidas -= 1
            
            if jugador.vidas <= 0:
                ejecutando = False

        # Dibujar
        pantalla.fill(NEGRO)
        todos_los_sprites.draw(pantalla)
        
        # Dibujar vidas, puntuación y nivel
        dibujar_texto(pantalla, f"Vidas: {jugador.vidas}", 24, 50, 10, BLANCO)
        dibujar_texto(pantalla, f"Puntuación: {jugador.puntuacion}", 24, ANCHO-200, 10, BLANCO)
        dibujar_texto(pantalla, f"Nivel: {jugador.nivel_actual}", 24, ANCHO//2, 10, BLANCO)

        # Actualizar pantalla
        pygame.display.flip()

        # Controlar la velocidad del juego
        reloj.tick(60)

    return jugador.puntuacion

def main():
    # Crear carpeta de imágenes si no existe
    if not os.path.exists('imagenes'):
        os.makedirs('imagenes')
        print("Crea una carpeta 'imagenes' y agrega 'nave1.png', 'nave2.png', 'nave3.png' y 'enemigo.png'")
        sys.exit()

    # Selección de nave del jugador
    imagen_nave = seleccion_nave()
    
    # Ruta de imagen de enemigo
    imagen_enemigo = os.path.join('imagenes', 'enemigo.png')

    # Bucle principal del programa
    while True:
        pantalla_inicio()
        puntuacion = juego_principal(imagen_nave, imagen_enemigo)
        pantalla_game_over(puntuacion)

if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()