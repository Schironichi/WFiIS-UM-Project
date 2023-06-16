import pygame.time

from utils.imports import *


class FallingBird(gym.Env):
    def __init__(self, randomPositions=True, FPS=500):
        pygame.init()
        self.all_sprites = self.info = self.player = self.render_mode = self.game_over = self.prev_dist = None
        self.action = self.dist = self.done = self.observation = self.obstacle_rects = self.score_text = None
        self.FONT = pygame.font.Font(None, 36)
        self.screen = pygame.display.set_mode((Window.WIDTH, Window.HEIGHT))
        self.iterations=self.reward = self.score = self.prev_score = 0
        self.action_space = gym.spaces.Discrete(3)
        self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(6,), dtype=np.float32)
        self.positions = Positions.RANDOM if randomPositions else Positions.STATIC
        self.FPS = FPS
        self.clock = pygame.time.Clock()

    def step(self, action):
        obstacle_left = self.positions[self.score]
        obstacle_right = obstacle_left + Obstacle.WIDTH
        self.prev_dist = abs(self.player.rect.x - obstacle_left) + abs(
            self.player.rect.x + self.player.width - obstacle_right)
        self.make_action(action)

        # Najważniejszy part, tutaj liczymy wszystko w sumie
        self.game_over, self.score, self.obstacle_rects = self.update_game_state(self.obstacle_rects)
        self.observation = self.get_positions(self.obstacle_rects)
        self.observation.append(action)
        self.observation = np.array(self.observation).astype(np.float32)
        self.info = {}
        if self.game_over:
            self.done = True
        self.reward = self.calculate_reward(action)
        if self.render_mode == 'human':
            self.render()

        return self.observation, self.reward, self.done, self.info

    def calculate_reward(self, action):
        if self.done:
            reward_a = -1000
        else:
            reward_a = 0
        # B: passing obstacle
        if self.prev_score < self.score:
            reward_b = 1000
            self.prev_score = self.score
        else:
            reward_b = 0
        # C: being in good spot
        obstacle_left = self.positions[self.score]
        obstacle_right = obstacle_left + Obstacle.WIDTH
        self.dist = abs(self.player.rect.x - obstacle_left) + abs(
            self.player.rect.x + self.player.width - obstacle_right)
        if self.dist > 51:
            reward_c = -5
        else:
            reward_c = 10
        # D: distance punishment
        if self.prev_dist > self.dist:
            reward_d = 1
        else:
            reward_d = -20
        # E: moving when player is between obstacles
        if self.dist < 51 and self.action != Actions.NO_ACTION:
            reward_e = -10
        else:
            reward_e = 0
        return reward_a + reward_b + reward_c + reward_d + reward_e

    def make_action(self, action):
        if action == Actions.LEFT_ACTION:
            if self.player.rect.left > 7:
                self.player.rect.move_ip(-8, 0)

        elif action == Actions.RIGHT_ACTION:
            if self.player.rect.right < Window.WIDTH - 7:
                self.player.rect.move_ip(8, 0)

        elif action == Actions.NO_ACTION:
            pass

    def reset(self):
        self.done = self.game_over = False
        print(f"Score: {self.score}")
        self.iterations += 1
        if self.iterations % 2000 == 0:
            self.positions = [random.randint(0, 700) for _ in range(102)]
        self.score = 0
        self.obstacle_rects = []
        self.player = Player(Window.WIDTH // 2, 0)
        # first obstacle
        self.obstacle_rects.append([
            # left part
            pygame.Rect(0, Window.HEIGHT // 2, self.positions[0], Obstacle.HEIGHT),
            # right part
            pygame.Rect(self.positions[0] + Obstacle.WIDTH, Window.HEIGHT // 2, Window.WIDTH - Obstacle.WIDTH,
                        Obstacle.HEIGHT)
        ])

        # second obstacle
        self.obstacle_rects.append([
            pygame.Rect(0, Window.HEIGHT, self.positions[1], Obstacle.HEIGHT),
            pygame.Rect(self.positions[1] + Obstacle.WIDTH, Window.HEIGHT, Window.WIDTH - Obstacle.WIDTH,
                        Obstacle.HEIGHT)
        ])

        # observation
        self.action = 0
        self.observation = self.get_positions(self.obstacle_rects)
        self.observation.append(self.action)
        self.observation = np.array(self.observation).astype(np.float32)

        # reward
        self.reward = 0
        self.score = 0
        self.prev_score = 0

        obstacle_left = self.positions[self.score]
        obstacle_right = obstacle_left + Obstacle.WIDTH
        self.dist = abs(self.player.rect.x - obstacle_left) + abs(
            self.player.rect.x + self.player.width - obstacle_right)

        if self.render_mode == 'human':
            pygame.init()
            pygame.display.set_caption("Falling Bird - DR PR KK")
            self.FONT = pygame.font.Font(None, 36)
            self.clock = pygame.time.Clock()
            self.screen = pygame.display.set_mode((Window.WIDTH, Window.HEIGHT))
            self.player = Player(Window.WIDTH // 2, 0)
            self.render()

        return self.observation

    def render(self, render_mode='human'):
        # Clear the screen
        self.screen.fill(Colors.BLACK)

        # Draw the player
        #self.all_sprites.draw(self.screen)
        pygame.draw.rect(self.screen, Colors.BLUE, self.player.rect)

        # Draw the obstacles
        for obstacle_rect in self.obstacle_rects:
            pygame.draw.rect(self.screen, Colors.GRAY, obstacle_rect[0])
            pygame.draw.rect(self.screen, Colors.GRAY, obstacle_rect[1])

        # Draw the score
        self.score_text = self.FONT.render(f"Score: {self.score}", True, Colors.WHITE)
        self.screen.blit(self.score_text, (10, Window.HEIGHT - 30))

        # Update the screen
        pygame.display.update()
        self.clock.tick(self.FPS)

    def player_input_handler(self, keys):
        # Handle input
        if keys[pygame.K_a]:
            if self.player.rect.left > 7:
                self.player.rect.move_ip(-8, 0)
        if keys[pygame.K_d]:
            if self.player.rect.right < Window.WIDTH - 7:
                self.player.rect.move_ip(8, 0)

    def get_positions(self, obstacle_rects):
        obstacle_left = self.positions[self.score]
        obstacle_right = obstacle_left + Obstacle.WIDTH
        obstacle_height = obstacle_rects[0][0].y if obstacle_rects[0][0].y >= 0 else 0
        return [self.player.rect.x, self.player.rect.x + self.player.width, obstacle_height, obstacle_left,
                obstacle_right]

    def update_game_state(self, obstacles):
        # Move the obstacles down
        game_over = False
        for obstacle_rect in obstacles:
            obstacle_rect[0].move_ip(0, -Obstacle.SPEED)
            obstacle_rect[1].move_ip(0, -Obstacle.SPEED)

            # Check for collisions
            if self.player.rect.colliderect(obstacle_rect[0]) or self.player.rect.colliderect(
                    obstacle_rect[1]) or self.score == 100:
                '''obstacle_left = positions[score] obstacle_right = obstacle_left + Obstacle.WIDTH Obstacle. = 
                obstacle_rect[0].y if obstacle_rect[0].y >= 0 else 0 print(f"Player.left: {player.rect.x} Player.right: {
                player.rect.x + PLAYER_WIDTH} Obst wysokosc: {Obstacle.}  Obst left: {obstacle_left}  Obst right: {
                obstacle_right} Score: {score}")'''
                game_over = True

            # If the obstacle goes off the screen, move it back to the bottom delete obst and create a new one at the bottom
            if obstacle_rect[0].bottom <= 0 and not game_over:
                self.score += 1
                obstacles.pop(0)
                obstacles.append([
                    # left part
                    pygame.Rect(0, Window.HEIGHT, self.positions[self.score + 1], Obstacle.HEIGHT),
                    # right part
                    pygame.Rect(self.positions[self.score + 1] + Obstacle.WIDTH, Window.HEIGHT,
                                Window.WIDTH - Obstacle.WIDTH, Obstacle.HEIGHT)
                ])

        return game_over, self.score, obstacles

    def close(self):
        pygame.quit()
