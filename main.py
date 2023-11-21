import pygame
import sys

# Inicializar Pygame
pygame.init()

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Configuración de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Beat Jumper")

# Definir clase para el personaje
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.y_speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.rect.y -= self.y_speed

# Crear sprite del jugador
player = Player()

# Crear grupo de sprites y agregar el jugador
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Bucle principal
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Actualizar
    all_sprites.update()

    # Dibujar
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Refrescar la pantalla
    pygame.display.flip()

    # Establecer el límite de cuadros por segundo
    clock.tick(60)

# Salir del juego
pygame.quit()
sys.exit()

