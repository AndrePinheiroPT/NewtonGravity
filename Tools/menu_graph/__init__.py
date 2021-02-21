import pygame


class Checkbox:
    def __init__(self, position, text, activate, font_text):
        self.position = position
        self.text = font_text.render(text, False, (255, 255, 255))
        self.activate = activate
        self.out_of_checkboxes = 0
        self.color_box = [0, 255, 0] if self.activate else [255, 0, 0]

    def change_state(self):
        self.activate = 0 if self.activate else 1
        self.color_box = [0, 255, 0] if self.activate else [255, 0, 0]

    def show_checkbox(self, screen_param):
        pygame.draw.rect(screen_param, self.color_box, [self.position[0], self.position[1], 10, 10])
        screen_param.blit(self.text, (self.position[0] + 15, self.position[1] - 4))

    def check_checkbox(self, mouse_state):
        self.out_of_checkboxes = 1
        if 10 <= mouse_state[0] <= 20 and self.position[1] <= mouse_state[1] <= self.position[1] + 10:
            self.out_of_checkboxes = 0
