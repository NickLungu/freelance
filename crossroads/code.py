import pygame
import random
import datetime

# Инициализация Pygame
pygame.init()

# Определение размеров окна
WIDTH = 800
HEIGHT = 600

# Определение цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# Создание окна
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Моделирование движения на перекрестке дорог")

# Load the background image
background_img = pygame.image.load("bg.jpg")  # Replace "background.jpg" with your image file

# Scale the image to fit the window size
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

clock = pygame.time.Clock()


# Класс для представления автомобиля
class Car:
    def __init__(self, x, y, speed, direction, direction_in_line):
        self.x = x
        self.y = y
        self.speed = speed
        # коэффициент скорость для торможения
        self.coeff = 1
        # x - слева направо, y - сверху вниз
        self.direction = direction
        # по какой полосе едет
        self.direction_in_line = direction_in_line

    def move(self, stop_flag=False):
        if self.direction == 'x':
            if self.direction_in_line == 'r':
                self.x -= self.speed * self.coeff
            else:
                self.x += self.speed * self.coeff
        elif self.direction == 'y':
            if self.direction_in_line == 'r':
                self.y += self.speed * self.coeff
            else:
                self.y -= self.speed * self.coeff

    def draw(self):
        if self.direction == 'x':
            pygame.draw.rect(window, ORANGE, (self.x, self.y, 20, 10))
        else:
            pygame.draw.rect(window, ORANGE, (self.x, self.y, 10, 20))

# Класс для представления дороги
class Road:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        pygame.draw.rect(window, BLACK, (self.x, self.y, self.width, self.height))


# Класс для представления светофора
class TrafficLight:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.color = RED

    def change_color(self):
        if self.color == RED:
            self.color = GREEN
        else:
            self.color = RED

    def draw(self):
        if self.direction == 'y':
            pygame.draw.rect(window, self.color, (self.x, self.y, 20, 40))
        if self.direction == 'x':
            pygame.draw.rect(window, self.color, (self.x, self.y, 40, 20))


# Класс для представления пешеходного перехода
class PedestrianCrossing:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.counter_for_passing_pedestrians = 0
        self.pedestrians = []

    def marker_for_pedestrians(self):
        # подсчитываем количество ожидающих перехода
        self.counter_for_passing_pedestrians = 0
        for p in self.pedestrians:
            if p.state == 1 or p.state == 2:
                self.counter_for_passing_pedestrians += 1
                continue
            if abs(self.x - p.x + 20) < 20:
                p.state = 1
                self.counter_for_passing_pedestrians += 1

    def update_crosing(self):
        for p in self.pedestrians:
            if p.state == 2:
                if p.x > WIDTH // 2 + 40:
                    p.state = 0

    def is_crossing_any(self):
        for p in self.pedestrians:
            if p.state == 2:
                return True
        return False

    def add_pedestrian(self):
        pedestrian = Pedestrian(0, self.y + 10)
        self.pedestrians.append(pedestrian)

    def remove_pedestrian(self, pedestrian):
        if pedestrian in self.pedestrians:
            self.pedestrians.remove(pedestrian)

    def draw(self):
        pygame.draw.rect(window, WHITE, (self.x, self.y, 80, 20))
        for pedestrian in self.pedestrians:
            pedestrian.draw()

    def update(self, traffic_light):
        if len(self.pedestrians) < 5:
            if random.randint(0, 100) < 2:  # Вероятность появления пешехода
                self.add_pedestrian()


# Класс для представления пешехода
class Pedestrian:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # 0 - идет
        # 1 - ждет
        # 2 - пересекает
        self.state = 0
        self.speed = random.randint(1, 3)

    def move(self):
        self.x += self.speed

    def draw(self):
        pygame.draw.circle(window, BLUE, (self.x, self.y), 5)

# Создание списка автомобилей
cars = []

# Создание объектов дорог и светофоров
road1 = Road(0, HEIGHT//2 - 20, WIDTH, 40)
road2 = Road(WIDTH//2 - 20, 0, 40, HEIGHT)

traffic_lights = [
    TrafficLight(WIDTH//2 - 10, HEIGHT//2 - 60, 'y'),
    TrafficLight(WIDTH//2 - 10, HEIGHT//2 + 20, 'y'),
]

pedestrian_crossing1 = PedestrianCrossing(WIDTH//2 - 40, HEIGHT//2 - 50)
pedestrian_crossing2 = PedestrianCrossing(WIDTH//2 - 40, HEIGHT//2 + 30)

# Основной цикл программы
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.blit(background_img, (0, 0))

    # Рисование дорог
    road1.draw()
    road2.draw()

    pygame.draw.line(window, WHITE, (0, HEIGHT // 2), (WIDTH, HEIGHT//2))
    pygame.draw.line(window, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    # Рисование светофоров
    for traffic_light in traffic_lights:
        traffic_light.draw()

    # Рисование пешеходных переходов
    pedestrian_crossing1.draw()
    pedestrian_crossing2.draw()

    # Создание новых автомобилей и распределение их по дорогам и полосам
    if random.randint(0, 100)*0.7 < 2:  # Вероятность появления автомобиля
        direction = 'x' if random.randint(1,2) == 1 else 'y'

        if direction == 'x':
            y = random.choice([HEIGHT // 2 - 15, HEIGHT // 2 + 7])
            if y == HEIGHT // 2 + 7:
                direction_in_line = 'l'
                x = 0
            else:
                direction_in_line = 'r'
                x = WIDTH
            min_speed = 10
            if len(cars)>0:
                min_speed = min([car.speed for car in cars])
            else:
                speed = min(min_speed,random.randint(1, 3))
            # speed = min(min_speed,)
            car = Car(x, y, speed, direction, direction_in_line)
            cars.append(car)
        else:
            x = random.choice([WIDTH // 2 - 15, WIDTH // 2 + 7])
            if x == WIDTH // 2 - 15:
                direction_in_line = 'r'
                y = 0
            else:
                direction_in_line = 'l'
                y = HEIGHT
            min_speed = 10
            if len(cars) > 0:
                min_speed = min([car.speed for car in cars])
            else:
                speed = min(min_speed, random.randint(1, 3))
            car = Car(x, y, speed, direction, direction_in_line)
            cars.append(car)

    # Движение автомобилей
    for car in cars:

        car.coeff = 1
        if traffic_lights[0].color == GREEN:
            # просчитываем коэффициент торможения
            if car.direction == 'y' and car.direction_in_line == 'r':
                distance = abs(car.y - traffic_lights[0].y)
                if distance < 100:
                    car.coeff = min(1, distance / 100)

            if car.direction == 'x':
                pass

        if traffic_lights[1].color == GREEN:
            # просчитываем коэффициент торможения
            if car.direction == 'y' and car.direction_in_line == 'l':
                distance = abs(car.y - traffic_lights[1].y)
                if distance < 50:
                    car.coeff = min(1, abs(car.y - traffic_lights[1].y - 30) / 10)
            if car.direction == 'x':
                pass

        # if car.direction == 'y':
        #     car.move()
        # if car.direction == 'x':
        #     car.move()
        car.move()
        car.draw()

    # проверяем очередь на светофоре
    pedestrian_crossing1.marker_for_pedestrians()
    pedestrian_crossing2.marker_for_pedestrians()

    # Смена цвета светофоров
    flag_wait = 0
    if (pedestrian_crossing1.is_crossing_any() or pedestrian_crossing2.is_crossing_any()):

        # желтый ставим если одна из машин в центре перекрестка, пока 5 человек уже накопилось и
        # ждут перехода
        for car in cars:
            if car.y > traffic_lights[0].y and car.y < traffic_lights[1].y and car.direction == 'y':
                traffic_lights[0].color = YELLOW
                traffic_lights[1].color = YELLOW
                flag_wait = 1
                break
        if flag_wait == 0:
            # иначе зеленый
            traffic_lights[0].color = GREEN
            traffic_lights[1].color = GREEN
    else:
        traffic_lights[0].color = RED
        traffic_lights[1].color = RED

    # Обновление пешеходных переходов
    pedestrian_crossing1.update(traffic_lights[0])
    pedestrian_crossing2.update(traffic_lights[1])

    # Движение пешеходов
    for pedestrian in pedestrian_crossing1.pedestrians:
        # считаем расстояние до светофора
        distance = abs(pedestrian.x - traffic_lights[0].x)
        # если число ожидающих больше четырех и текущий пешеход ждет на светофоре,
        # то ставим его в состояние перехода, так как в таком случае загорается зеленый
        if pedestrian_crossing1.counter_for_passing_pedestrians >= 5 and pedestrian.state == 1:
            pedestrian.state = 2
        # если хотя бы один в состоянии перехрда или дистанция больше 20 (не дошел до перехода),
        # и не горит желтый свет, то пешеход идет
        if (pedestrian_crossing1.is_crossing_any() or distance > 20) and flag_wait == 0:
            pedestrian.move()
        # удаляем пещехода из списка, если он вылез за экран
        if pedestrian.x > WIDTH or pedestrian.y > HEIGHT:
            pedestrian_crossing1.remove_pedestrian(pedestrian)
        # обновляем данные по состоянмию перехода
        pedestrian_crossing1.update_crosing()

    # аналогично для второго перехода
    for pedestrian in pedestrian_crossing2.pedestrians:
        distance = abs(pedestrian.x - traffic_lights[1].x)
        if pedestrian_crossing2.counter_for_passing_pedestrians >= 5 and pedestrian.state == 1:
            pedestrian.state = 2
        if (pedestrian_crossing2.is_crossing_any() or distance > 20) and flag_wait == 0:
            pedestrian.move()
        if pedestrian.x > WIDTH or pedestrian.y > HEIGHT:
            pedestrian_crossing2.remove_pedestrian(pedestrian)
        pedestrian_crossing2.update_crosing()



    pygame.display.flip()
    clock.tick(60)

pygame.quit()
