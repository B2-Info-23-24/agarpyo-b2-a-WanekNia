import random
import pygame
import sys
import math

class Game:
    def __init__(self, nbrFood=5, nbrPiege=2, control_mode="Clavier"):
        self.control_mode = control_mode
        # Init
        pygame.init()
        self.debug_font = pygame.font.Font(None, 24)  # Police

        # GameSize
        self.width, self.height = 1280, 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Agario-like")

        # Create Pawn
        self.player = Player(self.width // 2, self.height // 2 , self.control_mode)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        # SpriteGroup Entity (food)
        self.entities = pygame.sprite.Group()

        # SpriteGroup Piege
        self.pieges = pygame.sprite.Group()

        # Add Food
        for _ in range(nbrFood):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            entity = Entity(x, y)
            self.entities.add(entity)

        # Add piege
        for _ in range(nbrPiege):
            x = random.randint(70, 1200)
            y = random.randint(50, 700)
            piege = Piege(x, y)
            self.pieges.add(piege)

    def run(self):
        clock = pygame.time.Clock()
        game_over = False
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Update sprite
            self.all_sprites.update()
            self.entities.update()

            # Colision Pawn<->Entity
            for entity in self.entities:
                if pygame.sprite.collide_circle(self.player, entity):
                    self.player.mange(entity)
                    entity.reposition()

            # Colision Pawn<->Piege
            for piege in self.pieges:
                if pygame.sprite.collide_circle(self.player, piege) and piege.radius < self.player.radius:
                    # End Game
                    self.show_end_screen()
                    pygame.quit()
                    sys.exit()

            self.screen.fill((128, 128, 128))

            # Show sprite
            self.all_sprites.draw(self.screen)
            self.entities.draw(self.screen)  # Ajouté pour dessiner les entités sur l'écran
            self.pieges.draw(self.screen)

            # Debug
            self.draw_debug_info()

            # Refresh
            pygame.display.flip()

            # Frequency
            clock.tick(60)


    def draw_debug_info(self):
        debug_color = (0, 0, 0) 
        if self.control_mode == "Souris":
            control_text = "Mouse"
        elif self.control_mode == "Clavier":
            control_text = "Z Q S D"
        debug_text = f"Score: {self.player.score}"
        debug_text = f"Player Position: {self.player.rect.center} | Control: {control_text}"
        debug_surf = self.debug_font.render(debug_text, True, debug_color)
        self.screen.blit(debug_surf, (10, 10))

    def show_end_screen(self):
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        self.screen.fill(BLACK)
        end_text = self.debug_font.render("Fin de la partie ! Appuyez sur Entrée pour revenir au menu.", True, WHITE)
        text_rect = end_text.get_rect(center=(self.width / 2, self.height / 2))
        self.screen.blit(end_text, text_rect)
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False




import pygame
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, control_mode="Souris"):
        super().__init__()
        self.radius = 40
        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        self.color = (0, 0, 255)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 1
        self.score = 0
        self.control_mode = control_mode

    def update(self):
        if self.control_mode == "Souris":
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx = mouse_x - self.rect.centerx
            dy = mouse_y - self.rect.centery
            distance = math.sqrt(dx**2 + dy**2)  # distance truc j'ai pa compris

            threshold = 10 # marge d'erreur

            if distance > threshold:
                angle = math.atan2(dy, dx)
                self.rect.x += self.speed * math.cos(angle)
                self.rect.y += self.speed * math.sin(angle)
        elif self.control_mode == "Clavier":
            keys = pygame.key.get_pressed()
            dx = dy = 0
            if keys[pygame.K_z]:
                dy -= self.speed
            if keys[pygame.K_s]:
                dy += self.speed
            if keys[pygame.K_q]:
                dx -= self.speed
            if keys[pygame.K_d]:
                dx += self.speed
            self.rect.x += dx
            self.rect.y += dy

        # TP
        if self.rect.top <= 0:
            self.rect.bottom = 719
        elif self.rect.bottom >= 720:
            self.rect.top = 1
        elif self.rect.right >= 1280:
            self.rect.left = 1
        elif self.rect.left <= 0:
            self.rect.right = 1280

    
    def mange(self, entity):
        self.radius += 2  # Augmenter le rayon
        self.speed += 0.2  # Augmenter la vitesse 
        self.score += 1
        
        #update le sprite
        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=self.rect.center)

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, radius=10, color=(0, 255, 0)):
        super().__init__()
        self.radius = radius
        self.color = color
        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(x, y))
    
    def reposition(self):
        # x, Y rng
        new_x = random.randint(0, 1280)
        new_y = random.randint(0, 720)
        self.rect.center = (new_x, new_y)

class Piege(pygame.sprite.Sprite):
    def __init__(self, x, y, color=(255, 0, 0)):
        super().__init__()
        self.radius = random.randint(20, 70) 
        self.color = color
        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(x, y))


if __name__ == "__main__":
    game = Game()
    game.run()
