# =========================================================
# PROFESSIONAL POSE DINO
# =========================================================
#
# FEATURES
#
# ✅ GIỮ NGUYÊN PHYSICS GAME GỐC
# ✅ VỖ TAY = SPACE
# ✅ VAI CAO = JUMP
# ✅ VAI THẤP = DUCK
# ✅ WEBCAM OVERLAY
# ✅ MEDIAPIPE POSE
# ✅ HỆ TRỤC TỌA ĐỘ
# ✅ BIRD + CACTUS
# ✅ GAME OVER
# ✅ SCORE
#
# =========================================================

import pygame
import sys
import os
import random
import cv2
import mediapipe as mp
import math
from collections import deque



def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

pygame.init()

# =========================================================
# SCREEN
# =========================================================

SCREEN_HEIGHT = 700
SCREEN_WIDTH = 1400

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Professional Pose Dino")

# =========================================================
# ASSETS
# =========================================================

RUNNING = [
    pygame.image.load(resource_path("Assets/Dino/DinoRun1.png")),
    pygame.image.load(resource_path("Assets/Dino/DinoRun2.png"))
]

JUMPING = pygame.image.load(
    resource_path("Assets/Dino/DinoJump.png")
)

DUCKING = [
    pygame.image.load(resource_path("Assets/Dino/DinoDuck1.png")),
    pygame.image.load(resource_path("Assets/Dino/DinoDuck2.png"))
]

SMALL_CACTUS = [
    pygame.image.load(resource_path("Assets/Cactus/SmallCactus1.png")),
    pygame.image.load(resource_path("Assets/Cactus/SmallCactus2.png")),
    pygame.image.load(resource_path("Assets/Cactus/SmallCactus3.png"))
]

LARGE_CACTUS = [
    pygame.image.load(resource_path("Assets/Cactus/LargeCactus1.png")),
    pygame.image.load(resource_path("Assets/Cactus/LargeCactus2.png")),
    pygame.image.load(resource_path("Assets/Cactus/LargeCactus3.png"))
]

BIRD = [
    pygame.image.load(resource_path("Assets/Bird/Bird1.png")),
    pygame.image.load(resource_path("Assets/Bird/Bird2.png"))
]

CLOUD = pygame.image.load(
    resource_path("Assets/Other/Cloud.png")
)

BG = pygame.image.load(
    resource_path("Assets/Other/Track.png")
)

# =========================================================
# MEDIAPIPE
# =========================================================

class PoseController:

    def __init__(self):

        self.mp_pose = mp.solutions.pose

        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        self.draw = mp.solutions.drawing_utils

        self.origin_x = 0
        self.origin_y = 0

        self.jump_line = 0
        self.duck_line = 0

        self.history = deque(maxlen=5)

        self.clap_counter = 0

        self.jump_triggered = False

    # =====================================================

    def process(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = self.pose.process(rgb)

        return result

    # =====================================================

    def get_point(self, result, landmark, w, h):

        lm = result.pose_landmarks.landmark[landmark]

        return int(lm.x * w), int(lm.y * h)

    # =====================================================

    def draw_landmarks(self, frame, result):

        if result.pose_landmarks:

            self.draw.draw_landmarks(
                frame,
                result.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS
            )

    # =====================================================

    def detect_clap(self, frame, result):

        if not result.pose_landmarks:
            return False

        h, w, _ = frame.shape

        left = self.get_point(
            result,
            self.mp_pose.PoseLandmark.LEFT_WRIST,
            w,
            h
        )

        right = self.get_point(
            result,
            self.mp_pose.PoseLandmark.RIGHT_WRIST,
            w,
            h
        )

        distance = int(math.hypot(
            left[0] - right[0],
            left[1] - right[1]
        ))

        cv2.line(frame, left, right, (255, 255, 0), 3)

        cv2.putText(
            frame,
            f"CLAP DIST: {distance}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 0),
            2
        )

        if distance < 70:

            self.clap_counter += 1

            if self.clap_counter > 8:

                self.origin_x = (left[0] + right[0]) // 2
                self.origin_y = (left[1] + right[1]) // 2

                self.jump_line = self.origin_y - 80
                self.duck_line = self.origin_y + 80

                self.clap_counter = 0

                return True

        else:
            self.clap_counter = 0

        return False

    # =====================================================

    def detect_action(self, frame, result):

        if not result.pose_landmarks:
            return "NORMAL"

        h, w, _ = frame.shape

        ls_x, ls_y = self.get_point(
            result,
            self.mp_pose.PoseLandmark.LEFT_SHOULDER,
            w,
            h
        )

        rs_x, rs_y = self.get_point(
            result,
            self.mp_pose.PoseLandmark.RIGHT_SHOULDER,
            w,
            h
        )

        center_x = (ls_x + rs_x) // 2
        center_y = (ls_y + rs_y) // 2

        self.history.append(center_y)

        smooth_y = int(sum(self.history) / len(self.history))

        # =================================================
        # DRAW
        # =================================================

        cv2.circle(frame, (ls_x, ls_y), 10, (255, 0, 0), -1)
        cv2.circle(frame, (rs_x, rs_y), 10, (255, 0, 0), -1)

        cv2.circle(frame, (center_x, smooth_y), 12, (255, 0, 255), -1)

        cv2.circle(
            frame,
            (self.origin_x, self.origin_y),
            10,
            (0, 255, 255),
            -1
        )

        # AXIS
        cv2.line(
            frame,
            (0, self.origin_y),
            (w, self.origin_y),
            (255, 255, 0),
            2
        )

        cv2.line(
            frame,
            (self.origin_x, 0),
            (self.origin_x, h),
            (255, 255, 0),
            2
        )

        # JUMP LINE
        cv2.line(
            frame,
            (0, self.jump_line),
            (w, self.jump_line),
            (0, 255, 0),
            2
        )

        # DUCK LINE
        cv2.line(
            frame,
            (0, self.duck_line),
            (w, self.duck_line),
            (0, 0, 255),
            2
        )

        action = "NORMAL"

        # =================================================
        # JUMP
        # =================================================

        if smooth_y < self.jump_line:

            if not self.jump_triggered:

                action = "JUMP"

                self.jump_triggered = True

        else:

            self.jump_triggered = False

        # =================================================
        # DUCK
        # =================================================

        if smooth_y > self.duck_line:

            action = "DUCK"

        cv2.putText(
            frame,
            f"ACTION: {action}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 0, 0),
            3
        )

        return action

# =========================================================
# DINO
# =========================================================

class Dinosaur:

    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):

        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL

        self.image = self.run_img[0]

        self.dino_rect = self.image.get_rect()

        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):

        if self.dino_duck:
            self.duck()

        if self.dino_run:
            self.run()

        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump:

            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True

        elif userInput[pygame.K_DOWN] and not self.dino_jump:

            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False

        elif not (self.dino_jump or userInput[pygame.K_DOWN]):

            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):

        self.image = self.duck_img[self.step_index // 5]

        self.dino_rect = self.image.get_rect()

        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK

        self.step_index += 1

    def run(self):

        self.image = self.run_img[self.step_index // 5]

        self.dino_rect = self.image.get_rect()

        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

        self.step_index += 1

    def jump(self):

        self.image = self.jump_img

        if self.dino_jump:

            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8

        if self.jump_vel < - self.JUMP_VEL:

            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):

        SCREEN.blit(
            self.image,
            (self.dino_rect.x, self.dino_rect.y)
        )

# =========================================================
# CLOUD
# =========================================================

class Cloud:

    def __init__(self):

        self.x = SCREEN_WIDTH + random.randint(800, 1000)

        self.y = random.randint(50, 100)

        self.image = CLOUD

        self.width = self.image.get_width()

    def update(self):

        self.x -= game_speed

        if self.x < -self.width:

            self.x = SCREEN_WIDTH + random.randint(2500, 3000)

            self.y = random.randint(50, 100)

    def draw(self, SCREEN):

        SCREEN.blit(self.image, (self.x, self.y))

# =========================================================
# OBSTACLES
# =========================================================

class Obstacle:

    def __init__(self, image, type):

        self.image = image
        self.type = type

        self.rect = self.image[self.type].get_rect()

        self.rect.x = SCREEN_WIDTH

    def update(self):

        self.rect.x -= game_speed

        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):

        SCREEN.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):

    def __init__(self, image):

        self.type = random.randint(0, 2)

        super().__init__(image, self.type)

        self.rect.y = 325

class LargeCactus(Obstacle):

    def __init__(self, image):

        self.type = random.randint(0, 2)

        super().__init__(image, self.type)

        self.rect.y = 300

class Bird(Obstacle):

    def __init__(self, image):

        self.type = 0

        super().__init__(image, self.type)

        self.rect.y = 250

        self.index = 0

    def draw(self, SCREEN):

        if self.index >= 9:
            self.index = 0

        SCREEN.blit(self.image[self.index // 5], self.rect)

        self.index += 1

# =========================================================
# MAIN
# =========================================================

cap = cv2.VideoCapture(0)
if not cap.isOpened():

    print("ERROR: Cannot open webcam")

    input("Press Enter to exit...")

    exit()
controller = PoseController()

pose_action = "NORMAL"

def main():

    global game_speed
    global x_pos_bg
    global y_pos_bg
    global points
    global obstacles
    global pose_action

    run = True

    clock = pygame.time.Clock()

    player = Dinosaur()

    cloud = Cloud()

    game_speed = 20

    x_pos_bg = 0
    y_pos_bg = 380

    points = 0

    font = pygame.font.Font('freesansbold.ttf', 20)

    obstacles = []

    death_count = 0

    # =====================================================
    # SCORE
    # =====================================================

    def score():

        global points
        global game_speed

        points += 1

        if points % 100 == 0:
            game_speed += 1

        text = font.render(
            "Points: " + str(points),
            True,
            (0, 0, 0)
        )

        SCREEN.blit(text, (40, 40))

    # =====================================================
    # BACKGROUND
    # =====================================================

    def background():

        global x_pos_bg
        global y_pos_bg

        image_width = BG.get_width()

        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))

        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))

        if x_pos_bg <= -image_width:

            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))

            x_pos_bg = 0

        x_pos_bg -= game_speed

    # =====================================================
    # LOOP
    # =====================================================

    while run:

        ret, frame = cap.read()

        if ret:

            frame = cv2.flip(frame, 1)

            result = controller.process(frame)

            controller.draw_landmarks(frame, result)

            pose_action = controller.detect_action(frame, result)

            webcam = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            webcam = cv2.resize(webcam, (420, 260))

            webcam_surface = pygame.surfarray.make_surface(
                webcam.swapaxes(0, 1)
            )

        # =================================================
        # USER INPUT TỪ POSE
        # =================================================

        userInput = {
            pygame.K_UP: False,
            pygame.K_DOWN: False
        }

        if pose_action == "JUMP":
            userInput[pygame.K_UP] = True

        elif pose_action == "DUCK":
            userInput[pygame.K_DOWN] = True

        # =================================================
        # EVENTS
        # =================================================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                cap.release()

                pygame.quit()

                os._exit(0)

        SCREEN.fill((255, 255, 255))

        # =================================================
        # GAME
        # =================================================

        player.draw(SCREEN)

        player.update(userInput)

        if len(obstacles) == 0:

            rand = random.randint(0, 2)

            if rand == 0:

                obstacles.append(
                    SmallCactus(SMALL_CACTUS)
                )

            elif rand == 1:

                obstacles.append(
                    LargeCactus(LARGE_CACTUS)
                )

            else:

                obstacles.append(
                    Bird(BIRD)
                )

        for obstacle in obstacles:

            obstacle.draw(SCREEN)

            obstacle.update()

            if player.dino_rect.colliderect(obstacle.rect):

                pygame.time.delay(1000)

                death_count += 1

                menu(death_count)

        background()

        cloud.draw(SCREEN)

        cloud.update()

        score()

        # =================================================
        # WEBCAM UI
        # =================================================

        pygame.draw.rect(
            SCREEN,
            (0, 0, 0),
            (950, 20, 430, 270),
            3
        )

        SCREEN.blit(webcam_surface, (955, 25))

        pygame.display.update()

        clock.tick(60)

# =========================================================
# MENU
# =========================================================

def menu(death_count):

    global points

    run = True

    while run:

        SCREEN.fill((255, 255, 255))

        font = pygame.font.Font('freesansbold.ttf', 30)

        # =============================================
        # CAMERA
        # =============================================

        ret, frame = cap.read()

        if ret:

            frame = cv2.flip(frame, 1)

            result = controller.process(frame)

            # LANDMARKS
            controller.draw_landmarks(frame, result)

            # ACTION DEBUG
            controller.detect_action(frame, result)

            # CLAP
            clap = controller.detect_clap(frame, result)

            # =========================================
            # WEBCAM OVERLAY
            # =========================================

            webcam = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            webcam = cv2.resize(webcam, (420, 260))

            webcam_surface = pygame.surfarray.make_surface(
                webcam.swapaxes(0, 1)
            )

            pygame.draw.rect(
                SCREEN,
                (0, 0, 0),
                (950, 20, 430, 270),
                3
            )

            SCREEN.blit(webcam_surface, (955, 25))

            # =========================================
            # START / RESTART
            # =========================================

            if clap:
                main()

        # =============================================
        # TEXT
        # =============================================

        if death_count == 0:

            text = font.render(
                "CLAP TO START",
                True,
                (0, 0, 0)
            )

        else:

            text = font.render(
                "CLAP TO RESTART",
                True,
                (0, 0, 0)
            )

            score = font.render(
                "Your Score: " + str(points),
                True,
                (0, 0, 0)
            )

            SCREEN.blit(score, (520, 420))

        SCREEN.blit(
            text,
            (500, 350)
        )

        SCREEN.blit(
            RUNNING[0],
            (650, 250)
        )

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                cap.release()

                pygame.quit()

                os._exit(0)

# =========================================================
# START PROGRAM
# =========================================================

if __name__ == "__main__":

    try:

        menu(death_count=0)

    except Exception as e:

        print("CRASH:", e)

        input("Press Enter to exit...")