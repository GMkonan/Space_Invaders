import pygame
import random
import math
from pygame import mixer

pygame.init()

#Cria a tela com o valor especificado
screen = pygame.display.set_mode((800, 600))

#background
background = pygame.image.load("background.png")

#background som
mixer.music.load('background.wav')
mixer.music.play(-1) #-1 para tornar a musica inifita(loop)


#Titulo e Icone(trabalhe com icones 32x32)
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#player(trabalhe com imagens 64x64)
PlayerImg = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 480
playerX_change = 0

#enemy(trabalhe com imagens 64x64)
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range (num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

#bullet(trabalhe com imagens 32x32)
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

#game over text
over_font = pygame.font.Font('freesansbold.ttf',64)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def win():
    win_text = over_font.render("Você Ganhou", True, (255, 255, 255))
    screen.blit(win_text, (200, 250))
    mixer.music.stop()
    win_music = mixer.Sound('win.wav')
    win_music.play()

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    mixer.music.stop()

def player(x, y):
    screen.blit(PlayerImg, (x, y)) #blit seria como desenhar a imagem dentro da tela do jogo

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False       

#loop que define a janela aberta e que deixa o jogador fechar a janela
running = True
while running:

    #muda a cor da tela em RGB(claramente)
    screen.fill((0, 0, 0))
    #background in loop
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
           
        
        #if keystroke is press check wheather its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 4.5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(playerX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT: #if statement pra ver se a tecla parou de ser pressionada
                playerX_change = 0

    #bloco de codigo para verificar o espaco da tela para a nave n sair dela
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    #movimento do inimigo  
    for i in range (num_of_enemies):
        
        #game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        #win
        if score_value == 2000:
            enemyY[i] = -2000
            win()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]
        if enemyY[i] >= 300:
            enemyX[i] += enemyX_change[i]

    #Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision: #um if sem a condicao no caso da a logica de fazer algo caso a colisao tenha acontecido
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 20
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    #movimento da bala
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change




    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()