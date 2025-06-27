import random
import sys

import pygame

# Initialisation de Pygame
pygame.init()

# Constantes
LARGEUR = 450  # Format 9:16
HAUTEUR = 800
FPS = 60

# Couleurs
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
BLEU = (100, 150, 255)

# Paramètres des raquettes
RAQUETTE_LARGEUR = 15
RAQUETTE_HAUTEUR = 140
VITESSE_RAQUETTE = 10

# Paramètres de la balle
BALLE_TAILLE = 15
VITESSE_BALLE_X = 5
VITESSE_BALLE_Y = 3


class Raquette:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, RAQUETTE_LARGEUR, RAQUETTE_HAUTEUR)
        self.vitesse = VITESSE_RAQUETTE
        self.direction = 1  # 1 pour bas, -1 pour haut

    def deplacer(self, balle):
        # Déterminer si la balle est du côté de la raquette
        raquette_cote_gauche = self.rect.left < LARGEUR // 2
        balle_cote_gauche = balle.rect.centerx < LARGEUR // 2

        if raquette_cote_gauche == balle_cote_gauche:
            # Suivre la balle normalement
            if balle.rect.centery < self.rect.centery:
                self.rect.y -= self.vitesse
            elif balle.rect.centery > self.rect.centery:
                self.rect.y += self.vitesse
        else:
            # Recentrer la raquette verticalement
            centre_ecran = HAUTEUR // 2
            if self.rect.centery < centre_ecran:
                self.rect.y += self.vitesse
            elif self.rect.centery > centre_ecran:
                self.rect.y -= self.vitesse

        # Empêcher la raquette de sortir de l'écran
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HAUTEUR:
            self.rect.bottom = HAUTEUR

    def dessiner(self, ecran):
        # Charger l'image une seule fois et la redimensionner à la taille de la raquette
        if not hasattr(self, "image"):
            image = pygame.image.load("img/raquette.png").convert_alpha()
            self.image = pygame.transform.smoothscale(
                image, (RAQUETTE_LARGEUR, RAQUETTE_HAUTEUR)
            )
        ecran.blit(self.image, self.rect)


class Balle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BALLE_TAILLE, BALLE_TAILLE)
        self.vitesse_x = VITESSE_BALLE_X
        self.vitesse_y = VITESSE_BALLE_Y

    def deplacer(self):
        self.rect.x += self.vitesse_x
        self.rect.y += self.vitesse_y

        # Rebond sur les bords haut et bas
        if self.rect.top <= 0 or self.rect.bottom >= HAUTEUR:
            self.vitesse_y = -self.vitesse_y

    def rebondir_raquette(self, raquette):
        self.vitesse_x = -self.vitesse_x * 1.05
        # Calculer l'écart entre le centre de la balle et le centre de la raquette
        ecart = (
            (self.rect.centery - raquette.rect.centery) / (RAQUETTE_HAUTEUR / 2) * 10
        )
        # Limiter l'écart entre -10 et 10
        ecart = max(-10, min(10, ecart))
        # Définir la vitesse Y en fonction de l'écart (plus éloigné du centre = plus rapide)
        self.vitesse_y = ecart * 6
        # Ajouter une petite variation aléatoire
        self.vitesse_y += random.uniform(-1, 1)
        # Limiter la vitesse verticale
        self.vitesse_y = max(-6, min(6, self.vitesse_y))

    def reinitialiser(self):
        self.rect.center = (LARGEUR // 2, HAUTEUR // 2)
        self.vitesse_x = VITESSE_BALLE_X * random.choice([-1, 1])
        self.vitesse_y = 0

    def dessiner(self, ecran):
        # Charger l'image une seule fois et la redimensionner à la taille de la balle
        if not hasattr(self, "image"):
            image = pygame.image.load("img/balle.png").convert_alpha()
            self.image = pygame.transform.smoothscale(
                image, (BALLE_TAILLE, BALLE_TAILLE)
            )
        ecran.blit(self.image, self.rect)


# --- Ajout de la trace de la balle ---
class TraceBalle:
    def __init__(self):
        self.positions = []

    def ajouter(self, position):
        self.positions.append(position)
        # Limiter la longueur de la trace si besoin (optionnel)
        if len(self.positions) > 60:
            self.positions.pop(0)

    def effacer(self):
        self.positions.clear()

    def dessiner(self, ecran):
        for i, pos in enumerate(self.positions):
            # Alpha dégressif pour effet de disparition
            alpha = max(30, 180 - (len(self.positions) - 1 - i) * 3)
            surf = pygame.Surface((BALLE_TAILLE, BALLE_TAILLE), pygame.SRCALPHA)
            pygame.draw.ellipse(
                surf, (*BLEU, alpha), (0, 0, BALLE_TAILLE, BALLE_TAILLE)
            )
            ecran.blit(surf, (pos[0], pos[1]))


def main():
    # Création de l'écran
    ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Pong Vertical - Simulation")
    horloge = pygame.time.Clock()

    # Création des objets
    raquette_gauche_y = random.randint(0, HAUTEUR - RAQUETTE_HAUTEUR)
    raquette_droite_y = random.randint(0, HAUTEUR - RAQUETTE_HAUTEUR)
    raquette_gauche = Raquette(20, raquette_gauche_y)
    raquette_droite = Raquette(LARGEUR - 35, raquette_droite_y)
    balle = Balle(LARGEUR // 2, HAUTEUR // 2)
    trace_balle = TraceBalle()

    # Variables de score
    score_gauche = 0
    score_droite = 0
    font = pygame.font.Font(None, 36)

    running = True
    while running:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    # Réinitialiser la balle
                    balle.reinitialiser()

        # Déplacement des objets
        raquette_gauche.deplacer(balle)
        raquette_droite.deplacer(balle)
        balle.deplacer()
        trace_balle.ajouter([balle.rect.x, balle.rect.y])

        # Collision avec les raquettes
        # Jouer un son à chaque rebond
        if not hasattr(main, "rebond_son"):
            main.rebond_son = pygame.mixer.Sound("sound/rebond.mp3")
        if balle.rect.colliderect(raquette_gauche.rect) and balle.vitesse_x < 0:
            balle.rebondir_raquette(raquette_gauche)
            main.rebond_son.play()
        elif balle.rect.colliderect(raquette_droite.rect) and balle.vitesse_x > 0:
            balle.rebondir_raquette(raquette_droite)
            main.rebond_son.play()

        # Vérifier si la balle sort de l'écran
        if not hasattr(main, "victoire_son"):
            main.victoire_son = pygame.mixer.Sound("sound/victoire.mp3")
        if balle.rect.right < 0:
            score_droite += 1
            balle.reinitialiser()
            trace_balle.effacer()
            main.victoire_son.play()
        elif balle.rect.left > LARGEUR:
            score_gauche += 1
            balle.reinitialiser()
            trace_balle.effacer()
            main.victoire_son.play()

        # Dessin
        ecran.fill(NOIR)

        # Ligne centrale en pointillés
        for i in range(0, HAUTEUR, 20):
            if i % 40 == 0:
                pygame.draw.rect(ecran, BLANC, (LARGEUR // 2 - 2, i, 4, 15))

        # Dessiner les objets
        raquette_gauche.dessiner(ecran)
        raquette_droite.dessiner(ecran)
        balle.dessiner(ecran)
        trace_balle.dessiner(ecran)

        question_text = font.render(
            "Does she love you ?",
            True,
            BLANC,
        )
        question_rect = question_text.get_rect(center=(LARGEUR // 2, 20))
        ecran.blit(question_text, question_rect)

        answer_text = font.render("YES      NO", True, BLANC)
        answer_rect = answer_text.get_rect(center=(LARGEUR // 2, 60))
        ecran.blit(answer_text, answer_rect)

        score_text = font.render(f"{score_gauche}    {score_droite}", True, BLANC)
        score_rect = score_text.get_rect(center=(LARGEUR // 2, 80))
        ecran.blit(score_text, score_rect)

        # Dessiner un rectangle blanc pour le fond de la vitesse
        vitesse_val = abs(balle.vitesse_x) + abs(balle.vitesse_y)
        vitesse_text = font.render(
            f"Vitesse: {vitesse_val * 3.2:.1f} km/h",
            True,
            NOIR,
        )
        vitesse_rect = vitesse_text.get_rect(center=(LARGEUR // 2, HAUTEUR - 50))
        pygame.draw.rect(ecran, BLANC, vitesse_rect.inflate(20, 20), border_radius=8)
        ecran.blit(vitesse_text, vitesse_rect)

        pygame.display.flip()
        horloge.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
