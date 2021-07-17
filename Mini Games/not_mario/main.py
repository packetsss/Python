from utils import *

class Mario:
    def __init__(self, win, pos, character):
        self.win = win
        self.pos = pos
        self.character = character

        self.left_bound = -22
        self.right_bound = 18
        self.up_bound = -33
        self.down_bound = 31
    
    def update(self, pos, draw=True, flipped=False):
        self.pos = pos
        if draw:
            self.draw(flipped)
            
    def jumping(self, press_time, acceleration_time=JUMP_SPEED_MULTIPLIER):
        jump_start = time.time()
        acceleration = press_time * 130

        start_velocity = acceleration_time * acceleration
        if start_velocity < 35:
            start_velocity = 35
        elif start_velocity > 90:
            start_velocity = 90

        return jump_start, start_velocity

    def falling(self):
        x, y = np.int_(self.pos)

        # self.win.set_at((x, y + self.down_bound), GREEN)
        if self.hitbox((x, y + 1), "down", default_color=SCREEN_BACKGROUND_COLOR, all_pixel=True):
            return True
        return False

    def hitbox(self, pos, direction, default_color=BLACK, all_pixel=False, draw_hitbox=True):
        all_pixel_list = []
        x, y = np.int_(pos)
        direction_dict = {
            "left": self.left_bound,
            "right": self.right_bound,
            "up": self.up_bound,
            "down": self.down_bound,
        }
        
        if direction == "up" or direction == "down":
            for i in range(self.left_bound + 1, self.right_bound - 1):
                if all_pixel:
                    all_pixel_list.append(
                        self.win.get_at((x + i, y + direction_dict[direction]))[:3] == default_color)

                elif self.win.get_at((x + i, y + direction_dict[direction]))[:3] == default_color:
                    return True
                
                if draw_hitbox:
                    self.win.set_at((x + i, y + direction_dict[direction]), RED)

            if all_pixel:
                return np.count_nonzero(all_pixel_list) == len(range(self.left_bound + 1, self.right_bound - 1))

        else:
            for i in range(self.up_bound + 1, self.down_bound - 1):
                if all_pixel:
                    all_pixel_list.append(
                        self.win.get_at((x + direction_dict[direction], y + i))[:3] == default_color)
                

                elif self.win.get_at((x + direction_dict[direction], y + i))[:3] == default_color:
                    return True
                
                if draw_hitbox:
                    self.win.set_at((x + direction_dict[direction], y + i), RED)

            if all_pixel:
                return np.count_nonzero(all_pixel_list) == len(range(self.up_bound + 1, self.down_bound - 1))
    
        return False

    def draw(self, flipped):
        def relocation(pos):
            if not flipped:
                return pos[0] - CHARACTER_WIDTH / 3 - 5, pos[1] - CHARACTER_HEIGHT / 2
            else:
                return pos[0] - CHARACTER_WIDTH / 3 * 2 + 1, pos[1] - CHARACTER_HEIGHT / 2

        self.win.blit(self.character, relocation(self.pos))
        self.win.set_at(np.int_(self.pos), RED)

    def draw_old(self):
        x_range = [*range(-3, 3), *range(-4, 6), *range(-4, 4), 
        *range(-5, 6), *range(-5, 7), *range(-5, 6), *range(-3, 5), 
        *range(-4, 3), *range(-5, 5), *([*range(-6, 6)] * 4), 
        -4, -3, -2, 1, 2, 3, -5, -4, -3, 2, 3, 4, -6, -5, -4, -3, 2, 3, 4, 5]

        idx = [6, 10, 8, 11, 12, 11, 8, 7, 10, 12, 12, 12, 12, 6, 6, 8]
        y_range = [x for x in range(-7, 9) for _ in idx]
        
        pixel_list = []
        for x, y in zip(x_range, y_range):
            pixel_list.append([int(self.pos[0]) + x, int(self.pos[1]) + y])

        ct = 0
        for i, x in enumerate(idx):
            for j in range(x):
                x, y = pixel_list[ct]
                pixel_list[ct] = [x + j, y + i]
                ct += 1
    
        enlarge_type = [[0, 0], [0, 1], [1, 0], [1, 1]]
        for x in pixel_list:
            for t in enlarge_type:
                pixel = [x[0] + t[0], x[1] + t[1]]
                self.win.set_at(pixel, MAGENTA)


class Map:
    def __init__(self, win):
        self.win = win
    
    def base_line(self):
        pg.draw.line(self.win, GRAY, (0, GROUND_HEIGHT), (WIDTH, GROUND_HEIGHT), 3)
    
    def pipe(self, pos, width, height):
        pg.draw.rect(self.win, BLACK, pg.Rect(pos[0], GROUND_HEIGHT - height, width, height), width=2)
        pg.draw.rect(self.win, BLACK, pg.Rect(pos[0] - width / 3, GROUND_HEIGHT - height - height * 0.3 + 1, width * (5 / 3), height * 0.3), width=2)


class Character:
    def __init__(self, character_folder_path, animation_speed=ANIMATION_SPEED):
        self.character_list, self.flipped_list = self._char_init(character_folder_path)
        self.rotate_index = 0
        self.animation_speed = animation_speed
    
    def _char_init(self, path):
        char_lst = []
        flipp_lst = []
        for subdir, dirs, files in os.walk(path):
            for file in files:
                char = pg.image.load(os.path.join(subdir, file))
                char_lst.append(pg.transform.scale(char, (CHARACTER_WIDTH, CHARACTER_HEIGHT)))
                flipp_lst.append(False)
        return char_lst, flipp_lst
    
    def get_character(self, flip_state):
        if self.rotate_index >= len(self.character_list) * self.animation_speed:
            self.rotate_index = 0

        if flip_state != self.flipped_list[self.rotate_index // self.animation_speed]:
            self.flipped_list[self.rotate_index // self.animation_speed] = flip_state
            self.character_list[self.rotate_index // self.animation_speed] = pg.transform.flip\
                (self.character_list[self.rotate_index // self.animation_speed], True, False)

        char = self.character_list[self.rotate_index // self.animation_speed]
        self.rotate_index += 1
        return char


def run(timer=False):
    character_idle_list = Character(f"{pathlib.Path(__file__).parent.absolute()}/assets/Idle")
    character_walk_list = Character(f"{pathlib.Path(__file__).parent.absolute()}/assets/Walk")
    character_sprint_list = Character(f"{pathlib.Path(__file__).parent.absolute()}/assets/Run")
    character_jump_list = Character(f"{pathlib.Path(__file__).parent.absolute()}/assets/Jump")
    

    win = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Not Mario")
    clock = pg.time.Clock()
    exit = False
    flipped = False
    jumping, falling, walking, sprinting = False, False, False, False

    mario_pos = [WIDTH / 2, GROUND_HEIGHT - 50]
    mario = Mario(win, mario_pos, character_idle_list.get_character(flipped))
    map = Map(win)

    while not exit:
        start_time = time.time()

        # Draw background
        win.fill(SCREEN_BACKGROUND_COLOR)

        map.base_line()
        map.pipe((200, 0), 30, 70)
        map.pipe((400, 0), 80, 30)

        map.pipe((700, 0), 50, 100)
        map.pipe((1000, 0), 20, 60)

        # Animations
        if jumping or falling:
            mario.character = character_jump_list.get_character(flipped)
        elif sprinting and walking:
            mario.character = character_sprint_list.get_character(flipped)
        elif walking:
            mario.character = character_walk_list.get_character(flipped)
        else:
            mario.character = character_idle_list.get_character(flipped)

        x, y = mario_pos

        # Jumping & falling physics
        if jumping:
            time_passed = (time.time() - jump_start) * TIME_MULTIPLIER
            change_y = start_velocity * time_passed - 0.5 * GRAVITY * pow(time_passed, 2)

            if change_y > prev_change_y:
                y = start_jumping_pos[1] - change_y
                prev_change_y = change_y
            else:
                jumping = False

        if falling:
            time_passed = (time.time() - fall_start) * TIME_MULTIPLIER
            if mario.hitbox((x, y), "down", default_color=SCREEN_BACKGROUND_COLOR, all_pixel=True):
                change_y = -0.5 * GRAVITY * pow(time_passed, 2)
                y = start_falling_pos[1] - change_y
            else:
                falling = False
                y -= 1

        # Key strike control
        walking = False
        keys = pg.key.get_pressed()
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            if not mario.hitbox((x, y), "left"):
                x -= MOVING_SPEED_MULTIPLIER if not sprinting else SPRINT_MULTIPLIER
                flipped = True
                walking = True

        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            if not mario.hitbox((x, y), "right"):
                x += MOVING_SPEED_MULTIPLIER if not sprinting else SPRINT_MULTIPLIER
                flipped = False
                walking = True

        if mario.hitbox((x, y), "up"):
            jumping = False
            y += 1

        elif mario.hitbox((x, y), "down"):
            jumping = False
            y -= 1

        # update character
        mario_pos = [x, y]
        mario.update(mario_pos, draw=True, flipped=flipped)

        # falling control
        if not jumping and not falling and mario.falling():
            fall_start = time.time()
            start_falling_pos = mario_pos
            falling = True

        # Other key strikes
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    count_jump_start = time.time()
                if event.key == pg.K_LSHIFT:
                    sprinting = True
            elif event.type == pg.KEYUP:
                if event.key == pg.K_SPACE and (not jumping and not falling):
                    jump_start, start_velocity = mario.jumping(time.time() - count_jump_start)
                    start_jumping_pos = mario_pos
                    prev_change_y, jumping = 0, True

                    # Dynamic animation speed using jump speed
                    t = start_velocity / GRAVITY * 70
                    character_jump_list.animation_speed = round(t)
                    character_jump_list.rotate_index = 0
                if event.key == pg.K_LSHIFT:
                    sprinting = False

        clock.tick(FPS)
        pg.display.update()

        if timer:
            print(time.time() - start_time)

    pg.display.quit()
    pg.quit()
    sys.exit()

if __name__ == '__main__':
    run()