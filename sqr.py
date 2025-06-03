# -*- coding: utf-8 -*-
import pygame
import sys
import math
import random

pygame.init()
fenster = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Farben
rot = (255, 0, 0)
gelb = (255, 255, 0)
blau = (0, 0, 255)
schwarz = (0, 0, 0)
weiß = (255, 255, 255)

# Spieler
x, y = 100, 100
spieler_größe = 50
geschwindigkeit = 5

# Spielobjekte
gelbe_quadrate = []
blaue_punkte = []
max_objekte = 5
gruenes_dreieck = None  # kein Dreieck zu Beginn


font = pygame.font.SysFont(None, 30)
punkte = 0

def entfernung(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

while True:
    for ereignis in pygame.event.get():
        if ereignis.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif ereignis.type == pygame.MOUSEBUTTONDOWN:
            if ereignis.button == 1 and len(gelbe_quadrate) < max_objekte:
                mx, my = ereignis.pos
                gelbe_quadrate.append(pygame.Rect(mx, my, 30, 30))
                blaue_punkte.append([mx, my])

    # Tasteneingaben
    tasten = pygame.key.get_pressed()
    if tasten[pygame.K_LEFT]:  x -= geschwindigkeit
    if tasten[pygame.K_RIGHT]: x += geschwindigkeit
    if tasten[pygame.K_UP]:    y -= geschwindigkeit
    if tasten[pygame.K_DOWN]:  y += geschwindigkeit

    # Spieler-Rechteck
    spieler_rect = pygame.Rect(x, y, spieler_größe, spieler_größe)

    # Bewegung blauer Punkte & Kollision
    neue_gelb = []
    neue_blau = []
    for i in range(len(gelbe_quadrate)):
        ziel = gelbe_quadrate[i]
        verfolger = blaue_punkte[i]
        dx = x - verfolger[0]
        dy = y - verfolger[1]
        dist = math.hypot(dx, dy)
        if dist != 0:
            verfolger[0] += 2 * dx / dist
            verfolger[1] += 2 * dy / dist
            # Wenn Spieler getroffen, grünes Dreieck spawnen
        if spieler_rect.collidepoint(verfolger):
            gruenes_dreieck = pygame.Rect(random.randint(50, 750), random.randint(50, 550), 30, 30)
            continue  # dieser blaue Punkt wird gelöscht


        # Kollision Spieler – gelbes Quadrat
        if not spieler_rect.colliderect(ziel):
            neue_gelb.append(ziel)
            neue_blau.append(verfolger)
        else:
            punkte += 1  # Punktestand erhöhen

    gelbe_quadrate = neue_gelb
    blaue_punkte = neue_blau

    # Zeichnen
    fenster.fill(schwarz)
    pygame.draw.rect(fenster, rot, spieler_rect)
    for ziel in gelbe_quadrate:
        pygame.draw.rect(fenster, gelb, ziel)
    for punkt in blaue_punkte:
        pygame.draw.circle(fenster, blau, (int(punkt[0]), int(punkt[1])), 10)

    # Punktestand
    punkte_anzeige = font.render(f"Punkte: {punkte}", True, weiß)
    fenster.blit(punkte_anzeige, (10, 10))

    if gruenes_dreieck:
        pygame.draw.polygon(fenster, (0, 255, 0), [
            (gruenes_dreieck.centerx, gruenes_dreieck.top),
            (gruenes_dreieck.left, gruenes_dreieck.bottom),
            (gruenes_dreieck.right, gruenes_dreieck.bottom)
        ])

    pygame.display.flip()
    clock.tick(60)
