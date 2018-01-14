''' Handles all stair logic in our game '''
#pylint: disable-msg=C0103, W0603
import random
import settings
import sounds
import images
import person as Person

width = 150
height = 20

stair_list = []
border = 31

def reset_stair():
    ''' Clear stair list '''
    global stair_list
    stair_list = []

def regen_stair():
    ''' Check if stairs are out of bounds and regenerate new stairs '''
    if stair_list[0].y < 35:
        stair_list.pop(0)
        generate_stair(8)

def generate_stair(count):
    ''' Generate random stair type '''
    type_number = random.randint(1, 24)
    if 1 <= type_number <= 10:
        stair_list.append(Stair(count))
    elif 11 <= type_number <= 14:
        stair_list.append(StingStair(count))
    elif 15 <= type_number <= 17:
        stair_list.append(CloudStair(count))
    elif 18 <= type_number <= 20:
        stair_list.append(MovingStair(count))
    else:
        stair_list.append(BlackholeStair(count))

class Stair:
    ''' Base and also normal stair entity '''
    def __init__(self, count):
        self.pass_through = False
        self.x = random.uniform(border, settings.game_width - border - width)
        self.y = 640 - 75 * (8 - count)
        self.photo = images.normal

    def update(self):
        ''' Executes stair logic for every loop '''
        self.y -= 2

    def collision_check(self, person):
        ''' Checks if stair has collided '''
        if self.pass_through:
            return False

        return self.y + height > (person.y + Person.height - 1) > self.y and \
           self.x + 15 <= (person.x + Person.width) <= (self.x + width + Person.width - 15)

    def collide(self, person):
        ''' Collision logic of stair and person'''
        person.y = self.y - Person.height
        if self != person.last_stair:
            person.blackhole_size = 0
            if person.life_count < 12:                        # 若沒滿血就加一
                person.life_count += 1                       # 若梯子是-10往上，要抵銷自然落下就要-20
            person.last_stair = self


class StingStair(Stair):
    ''' Sting stair entity '''
    def __init__(self, count):
        Stair.__init__(self, count)
        self.photo = images.sting

    def update(self):
        Stair.update(self)

    def collision_check(self, person):
        return Stair.collision_check(self, person)

    def collide(self, person):
        if self != person.last_stair:
            sounds.sounds["Hurt"].play()
            person.life_count += -5
            person.last_stair = self
            if person.life_count <= 0:
                person.death()
        Stair.collide(self, person)

class CloudStair(Stair):
    ''' Cloud stair entity '''
    def __init__(self, count):
        Stair.__init__(self, count)
        self.photo = images.cloud

    def update(self):
        Stair.update(self)

    def collision_check(self, person):
        ''' Checks if stair has collided '''
        if self.pass_through:
            return False

        return self.y + height + 20 > (person.y + Person.height - 1) > self.y - 40 and \
           self.x + 15 <= (person.x + Person.width) <= (self.x + width + Person.width - 15)

    def collide(self, person):
        person.y -= 4

class MovingStair(Stair):
    ''' Moving stair entity '''
    def __init__(self, count):
        Stair.__init__(self, count)
        self.original_x = random.randint(border, settings.game_width - border - width - 90)

        self.stair_speed = random.randint(10, 20) / 10
        self.x = random.randint(self.original_x, self.original_x + 90)

        self.direction = random.randint(0, 1)
        if self.direction == 0:
            self.direction = -1

    def update(self):
        Stair.update(self)
        self.x += self.stair_speed * self.direction
        if self.x < self.original_x or self.x > self.original_x + 90:
            self.direction *= -1

    def collision_check(self, person):
        return Stair.collision_check(self, person)

    def collide(self, person):
        person.y = self.y - height
        person.x += self.stair_speed * self.direction
        Stair.collide(self, person)

class BlackholeStair(Stair):
    ''' Blackhole stair entity '''
    def __init__(self, count):
        Stair.__init__(self, count)
        self.photo = images.blackhole

    def update(self):
        Stair.update(self)

    def collision_check(self, person):
        return Stair.collision_check(self, person)

    def collide(self, person):
        person.x -= person.direction[-1]
        person.blackhole_size += 1
        target_x = self.x + width // 2 - Person.width // 2
        person.x += (target_x - person.x) / abs(target_x - person.x) * 2

        if person.blackhole_size == Person.height / 2:
            person.blackhole_size = 0
            person.y = random.randint(80, settings.game_height * 0.4)
            person.x = random.randint(60, settings.game_width - 60)

        Stair.collide(self, person)
