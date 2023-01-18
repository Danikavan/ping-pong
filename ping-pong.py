from pygame import *
from random import randint

#шрифты и надписи
font.init()
font1 = font.SysFont(Arial, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.SysFont(Arial, 36)
rel = font2.render('Wait, reload...', True, (150, 0, 0))
 
#нам нужны такие картинки:
img_back = "galaxy.jpg" # фон игры
img_racket = "racket.jpg" # ракетка
img_ball = "ball.png" # мяч
 
#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
#конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)
 
        #каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
        #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
#метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
#класс главного игрока
class Player(GameSprite):
    #метод для управления спрайтом стрелками клавиатуры
    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
           self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_width - 5:
           self.rect.y += self.speed
    def update_r(self):
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_width - 5:
            self.rect.y += self.speed
 
#Создаём окошко
win_width = 700
win_height = 500
display.set_caption("Ping Pong")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
 
#создаём спрайты
racket1 = Player(img_racket, 5, 100, 5, 100, 10)
racket2 = Player(img_racket, 5, 600, 5, 100, 10)

bullets = sprite.Group()

#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
#Основной цикл игры:
run = True #флаг сбрасывается кнопкой закрытия окна
num_fire = 0
rel_time = False
timec = 0
while run:
    #событие нажатия на кнопку “Закрыть”
    for e in event.get():
        if e.type == QUIT:
            run = False
        #событие нажатия на пробел - спрайт стреляет
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    fire_sound.play()
                    ship.fire()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:
                    rel_time = True

    if rel_time == True:
        timec += 1
        window.blit(rel, (200, 250))
        if timec == 60:
            rel_time = False
            num_fire = 0
            timec = 0

    if not finish:
       #обновляем фон
        window.blit(background,(0,0))

        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        sprites_list2 = sprite.spritecollide(ship, monsters, False)

        for i in sprites_list:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        for i in sprites_list2:
            window.blit(lose, (200, 200))
            finish = True

        if lost >= 3:
            window.blit(lose, (200, 200))
            finish = True

        if score >= 10:
            window.blit(win, (200, 200))
            finish = True

        #пишем текст на экране
        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
 
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
 
        #производим движения спрайтов
        ship.update()
        monsters.update()
        bullets.update()
 
        #обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
    
    display.update()
   #цикл срабатывает каждую 0.05 секунд
    time.delay(50)