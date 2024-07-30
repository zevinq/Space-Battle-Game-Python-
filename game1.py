import pygame
import time 
import random
pygame.font.init()

# Initialize the mixer module with pre_init to reduce latency
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

#define the size of the screen
WIDTH, HEIGHT = 1000, 800
#set up the window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Battle")

#import background from directory
#scale the image
BG = pygame.transform.scale(pygame.image.load("bg.jpg"), (WIDTH, HEIGHT)) 

#Set player's attribute
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60

#Set velocity at five 
PLAYER_VEL = 5
LASER_VEL = 7

#Set Star attribute
STAR_WIDTH = 20
STAR_HEIGHT = 40
STAR_VEL = 3

#Set up font for text
FONT = pygame.font.SysFont("comicsans", 40)
BUTTON_FONT = pygame.font.SysFont("comicsans", 24)  # Smaller font for the button

# Load laser image
LASER_IMAGE = pygame.image.load("laser.png")
LASER_IMAGE = pygame.transform.scale(LASER_IMAGE, (10, 40))

# Load explosion image
EXPLOSION_IMAGE = pygame.image.load("explosion.png")
EXPLOSION_IMAGE = pygame.transform.scale(EXPLOSION_IMAGE, (STAR_WIDTH, STAR_HEIGHT))

# Initialize the mixer module with pre_init to reduce latency
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# Load laser sound
LASER_SOUND = pygame.mixer.Sound("laser_sound.mp3")
LASER_SOUND.set_volume(0.3)  # set volume to 50%

# Load background music
pygame.mixer.music.load("bgm.mp3")  # load the music
pygame.mixer.music.set_volume(0.5)  # set bgm volome to 50%
pygame.mixer.music.play(-1)  # play bgm infintely


def draw_start_menu():
    WIN.blit(BG, (0, 0))
    title_text = FONT.render("Space Battle", 1, "white")
    WIN.blit(title_text, (WIDTH / 2 - title_text.get_width() / 2, HEIGHT / 2 - title_text.get_height() / 2 - 50))

    # Button
    button_color = (255, 255, 255)
    button_rect = pygame.Rect(WIDTH / 2 - 75, HEIGHT / 2 + 40, 150, 50)
    pygame.draw.rect(WIN, button_color, button_rect, 2)  # 2 is the border width

    button_text = BUTTON_FONT.render("Start Game", 1, "white")
    WIN.blit(button_text, (button_rect.x + (button_rect.width - button_text.get_width()) // 2, 
                           button_rect.y + (button_rect.height - button_text.get_height()) // 2))
    # Author text
    author_text = BUTTON_FONT.render("Author: Zevin Wang", 1, "green")
    WIN.blit(author_text, (WIDTH / 2 - author_text.get_width() / 2, button_rect.y + button_rect.height + 20))

    pygame.display.update()

    return button_rect

def draw(player_image, player_rect, elapsed_time, stars, star_image, lasers, explosions):
    WIN.blit(BG, (0, 0))
    
    #display current time on the game
    #font with white color
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))
    
    # Draw the player image
    WIN.blit(player_image, player_rect)

    # Draw lasers
    for laser in lasers:
        WIN.blit(LASER_IMAGE, (laser.x, laser.y))
     
    for star in stars:
        WIN.blit(star_image, (star.x, star.y))

    # Draw explosions
    for explosion in explosions:
        WIN.blit(EXPLOSION_IMAGE, explosion)

    pygame.display.update()

# if the player loses the game
#  a "You lost" message will be displayed
# and the player can press the 'quit' button to exit 
def draw_game_over():
    WIN.blit(BG, (0, 0))
    lost_text = FONT.render("You Lost!", 1, "white")
    WIN.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 2 - lost_text.get_height() / 2))

    # Button
    button_color = (255, 0, 0)
    button_rect = pygame.Rect(WIDTH / 2 - 50, HEIGHT / 2 + 40, 100, 50)
    pygame.draw.rect(WIN, button_color, button_rect)

    button_text = FONT.render("Quit", 1, "white")
    WIN.blit(button_text, (button_rect.x + (button_rect.width - button_text.get_width()) // 2, 
                           button_rect.y + (button_rect.height - button_text.get_height()) // 2))

    pygame.display.update()
    return button_rect

def main():
    #keep the window running
    run = True
    
    #import player image
    player_image = pygame.image.load("plane.png")
    player_image = pygame.transform.scale(player_image, (50, 50))
    player_rect = player_image.get_rect()
    player_rect.topleft = (200, HEIGHT - 50)
    
    # create a mask for player
    player_mask = pygame.mask.from_surface(player_image)

    #import star image
    star_image = pygame.image.load("star.png")
    star_image = pygame.transform.scale(star_image, (STAR_WIDTH, STAR_HEIGHT))
    
    # create a mask for star
    star_mask = pygame.mask.from_surface(star_image)

    #set a clock to make sure all computers run at the exact same speed 
    clock = pygame.time.Clock()
    
    #set start time
    #grab current time when the game started
    start_time = time.time()
    
    #calculate elapsed time since we start the game
    elapsed_time = 0
    
    star_add_increment = 2000
    # count when should we add the star on the screen
    star_count = 0
    
    stars = []
    lasers = []
    explosions = []
    explosion_timer = {}
    hit = False
    game_over = False

    # Display start menu
    start_button_rect = draw_start_menu()
    in_start_menu = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
                break
            if in_start_menu and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if start_button_rect.collidepoint(mouse_pos):
                    in_start_menu = False

        if in_start_menu:
            continue

        # count how many milliseconds have occurred since 
        # the last clock tick 
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time 
        
        if not game_over and star_count > star_add_increment:
            for _ in range(3):
                #x position of the star
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)
            
            # generate another star
            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
                break
            if game_over and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button_rect.collidepoint(mouse_pos):
                    run = False

        if game_over:
            continue
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.x - PLAYER_VEL >= 0:
            player_rect.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player_rect.x + PLAYER_VEL + player_rect.width <= WIDTH:
            player_rect.x += PLAYER_VEL
        if keys[pygame.K_SPACE]:
            laser = pygame.Rect(player_rect.x + player_rect.width // 2 - 5, player_rect.y - 40, 10, 40)
            lasers.append(laser)
            LASER_SOUND.play()  # Play laser sound

        # Update laser positions
        for laser in lasers[:]:
            laser.y -= LASER_VEL
            if laser.y < 0:
                lasers.remove(laser)

        # Check for laser collisions with stars
        for laser in lasers[:]:
            for star in stars[:]:
                if star.colliderect(laser):
                    explosions.append(star.topleft)
                    explosion_timer[star.topleft] = time.time()
                    lasers.remove(laser)
                    stars.remove(star)
                    break

        # Update explosion display
        for explosion in explosions[:]:
            if time.time() - explosion_timer[explosion] > 0.5:  # Explosion lasts for 0.5 seconds
                explosions.remove(explosion)
                del explosion_timer[explosion]

        # remove stars that hit the player or hit the bottom of the screen 
        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            else:
                # precise collision detection using masks
                offset = (star.x - player_rect.x, star.y - player_rect.y)
                if player_mask.overlap(star_mask, offset):
                    stars.remove(star)
                    hit = True
                    break

        if hit:
            game_over = True
            button_rect = draw_game_over()
        else:
            draw(player_image, player_rect, elapsed_time, stars, star_image, lasers, explosions)
    
    pygame.quit() 
    
if __name__ == "__main__":
    main()
    
