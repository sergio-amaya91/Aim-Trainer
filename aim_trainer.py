import pygame
import random
import math
import time
pygame.init()

#window size
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")

#speed at which targets appear
TARGET_INCREMENT = 1000
TARGET_EVENT = pygame.USEREVENT

TARGET_PADDING = 30

#speed at which friendlies appear
FRIEND_INCREMENT = 800
FRIEND_EVENT = pygame.USEREVENT

FRIEND_PADDING = 30

# UI Design
BG_COLOR = (0, 25, 40)
TOP_BAR_HEIGHT = 50
LABEL_FONT = pygame.font.SysFont("timesnewroman", 24)


LIVES =10

#target class
class Target:
    MAX_SIZE = 30
    COLOR = "red"
    SECOND_COLOR = "white"

    def __init__(self, x,y, rand_rate):
        self.x =x
        self.y = y
        self.size = 0
        self.GROWTH_RATE = rand_rate
        self.grow = True

    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False
        
        if self.grow:
         self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

#target design
    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x,self.y), self.size)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x,self.y), self.size * 0.8)
        pygame.draw.circle(win, self.COLOR, (self.x,self.y), self.size * 0.6)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x,self.y), self.size * 0.4)

    def collide(self, x, y):
        dis= math.sqrt((self.x - x)**2 + (self.y -y)**2)
        return dis <= self.size

#friendly targets class
class Friend:
    MAX_SIZE = 30
    COLOR = "green"
    SECOND_COLOR = "white"

    def __init__(self, x, y, rand_rate):
        self.x =x
        self.y = y
        self.size = 0
        self.GROWTH_RATE = rand_rate
        self.grow = True

    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False
        
        if self.grow:
         self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

#friend design
    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x,self.y), self.size)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x,self.y), self.size * 0.8)
        pygame.draw.circle(win, self.COLOR, (self.x,self.y), self.size * 0.6)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x,self.y), self.size * 0.4)

    def collide(self, x, y):
        dis= math.sqrt((self.x - x)**2 + (self.y -y)**2)
        return dis <= self.size


#Draw Friendly and targets to window
def draw(win, friends, targets):
    win.fill(BG_COLOR)

    for target in targets:
        target.draw(win)
    
    for friend in friends:
        friend.draw(win)            
 
def format_time(secs):
    milli = math.floor(int(secs *1000 %1000)/100)
    seconds = int(round(secs %60, 1))
    minutes = int(secs //60)

    return f"{minutes:02d}:{seconds:02d}.{milli}"

#Top Bar analytics
def draw_top_bar(win, elapsed_time, targets_pressed, misses, friends_hit):
    pygame.draw.rect(win, "grey", (0,0, WIDTH, TOP_BAR_HEIGHT))
    
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "black")
    
    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed : {speed} t/s", 1, "black")
    hits_label = LABEL_FONT.render(f"Hits : {targets_pressed}", 1, "black")

    lives_label = LABEL_FONT.render(f"Lives : {LIVES - misses - friends_hit}", 1, "black")

    win.blit(time_label, (5,5))
    win.blit(speed_label, (200,5))
    win.blit(hits_label, (400,5))
    win.blit(lives_label, (600,5))


#end screen analytics   
def end_screen(win, elapsed_time, targets_pressed, clicks, friends_hit):
    win.fill(BG_COLOR)
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "white")
    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed : {speed} t/s", 1, "white")
    hits_label = LABEL_FONT.render(f"Hits : {targets_pressed}", 1, "white")
    friends_hit_label = LABEL_FONT.render(f"Friends Hit : {friends_hit}", 1, "white")
    restart_label = LABEL_FONT.render("Press any key to restart or close window to quit", 1, "yellow")
    
#determine accuracy
    if  clicks == 0:
        accuracy = 0
    else:     
        accuracy = round(targets_pressed/clicks *100, 1)
    
    accuracy_label = LABEL_FONT.render(f"Accuracy : {accuracy}%", 1, "white")
    
    win.blit(time_label, (get_middle(time_label),150))
    win.blit(speed_label, (get_middle(speed_label),200))
    win.blit(hits_label, (get_middle(hits_label),250))
    win.blit(accuracy_label, (get_middle(accuracy_label),300))
    win.blit(friends_hit_label, (get_middle(friends_hit_label), 350))
    win.blit(restart_label, (get_middle(restart_label), 400))

    pygame.display.update()
#end or restart game
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
    
            elif event.type == pygame.KEYDOWN:
                main()
                    
   
#formula to draw to middle
def get_middle(surface):
    return WIDTH/2 - surface.get_width()/2

#main
def main():
    run = True
    targets = []
    friends = []
    clock = pygame.time.Clock()

    targets_pressed = 0
    clicks = 0
    misses = 0
    friends_hit = 0
    start_time = time.time()


    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

    while run:
        clock.tick(60)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                target = Target(x,y,random.random())
                targets.append(target)

            if event.type == FRIEND_EVENT:
                x = random.randint(FRIEND_PADDING, WIDTH - FRIEND_PADDING)
                y = random.randint(FRIEND_PADDING + TOP_BAR_HEIGHT, HEIGHT - FRIEND_PADDING)
                friend = Friend(x,y, random.random())
                friends.append(friend)    
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks +=1
        
        for target in targets:
            target.update()

            if target.size <= 0:
                targets.remove(target)
                misses += 1

            if click and target.collide(*mouse_pos):
                targets.remove(target)
                targets_pressed += 1

            
        
        for friend in friends:
            friend.update()

            if friend.size <= 0:
                friends.remove(friend)
                

            if click and friend.collide(*mouse_pos):
                friends.remove(friend)
                friends_hit += 1
                        

        if (misses + friends_hit) >= LIVES:
                end_screen(WIN, elapsed_time, targets_pressed, clicks, friends_hit)
                break        

        draw(WIN, friends, targets)
        draw_top_bar(WIN, elapsed_time, targets_pressed, misses, friends_hit)
        pygame.display.update()

            

    pygame.quit()

if __name__ =="__main__":
    main()