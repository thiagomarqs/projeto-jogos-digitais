import pygame


class Button():
    def __init__(self, text, x, y, width, height, inactive_color, active_color, text_color, font_size, font=None):
        self.start_pos = pygame.Rect(x, y, height, width)
        self.text = text
        self.text_color = text_color
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.font = font
        self.font_size = font_size

    def draw(self, mouse, window):
        if self.start_pos.left < mouse[0] < self.start_pos.right and self.start_pos.top < mouse[1] < self.start_pos.bottom:
            pygame.draw.rect(
                window, self.active_color, self.start_pos)
        else:
            pygame.draw.rect(
                window, self.inactive_color, self.start_pos)

        small_font = pygame.font.SysFont(self.font, self.font_size)
        small_text = small_font.render(self.text, True, self.text_color)
        text_rect = small_text.get_rect()
        text_rect.center = (self.start_pos.center)
        window.blit(small_text, text_rect)

    def is_clicked(self, mouse, clicks):
        if self.start_pos.left < mouse[0] < self.start_pos.right and self.start_pos.top < mouse[1] < self.start_pos.bottom and clicks[0] == 1:
            return True
        return False
