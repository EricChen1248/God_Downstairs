class Person:
    def __init__(self, width, x, y, photo, life_count, life_photo):
        self.width = width
        self.x = x
        self.y = y
        self.x_change = 0
        self.photo = photo        
        self.life_count = 12
        self.life_photo = life_photo
    def Update():
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.x_change += -5
                if event.key == pygame. K_RIGHT:
                    self.x_change += 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.x_change = 0
        self.x += self.x_change
        if self.x <= 0:
            self.x = 0
        if self.x + self.width >= display_width * 0.6:
            self.x + self.width = display_width * 0.6
        self.y += 10
        
    
    


