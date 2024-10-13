import pygame
import random
from algorithms import bubble_sort, selection_sort, insertion_sort, merge_sort, quick_sort, heap_sort

pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sorting Algorithm Visualizer")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (200, 200, 200)
BUTTON_COLOR = (100, 100, 200)
BUTTON_HOVER_COLOR = (150, 150, 255)
RESET_BUTTON_COLOR = (200, 100, 100)  # Different color for reset button
INPUT_COLOR_INACTIVE = (150, 150, 150)
INPUT_COLOR_ACTIVE = (200, 200, 255)

# Frame rate
FPS = 60

# Space reserved for the buttons (top 100 pixels)
BUTTON_AREA_HEIGHT = 100

# Button Class
class Button:
    def __init__(self, x, y, width, height, text, action=None, color=BUTTON_COLOR):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.font = pygame.font.SysFont('Arial', 18)
        self.color = color
        self.hover_color = BUTTON_HOVER_COLOR

    def draw(self, screen, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        text_surface = self.font.render(self.text, True, BLACK)
        screen.blit(text_surface, (self.rect.x + (self.rect.width // 2 - text_surface.get_width() // 2),
                                   self.rect.y + (self.rect.height // 2 - text_surface.get_height() // 2)))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class InputBox:
    def __init__(self, x, y, width, height, default_text="50", label="Array Size:"):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = INPUT_COLOR_INACTIVE
        self.text = default_text
        self.font = pygame.font.SysFont('Arial', 18)
        self.text_surface = self.font.render(self.text, True, BLACK)
        self.label = label
        self.label_surface = self.font.render(self.label, True, BLACK)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active state based on the mouse click
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = INPUT_COLOR_ACTIVE if self.active else INPUT_COLOR_INACTIVE

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text  # Return the text as the new number of elements
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.unicode.isdigit():
                    self.text += event.unicode

        self.text_surface = self.font.render(self.text, True, BLACK)
        return None

    def draw(self, screen):
        # Change the cursor to an I-beam when hovering over the input box
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)  # I-beam cursor
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  # Default arrow cursor

        # Draw the label
        screen.blit(self.label_surface, (self.rect.x - self.label_surface.get_width() - 10, self.rect.y + 5))

        # Draw the input box
        pygame.draw.rect(screen, self.color, self.rect, 2)
        # Draw the text
        screen.blit(self.text_surface, (self.rect.x + 5, self.rect.y + 5))
        # Reset width of the box if the text is too long
        self.rect.w = max(100, self.text_surface.get_width() + 10)

# Sorting Visualizer
class Visualizer:
    def __init__(self, array_len=50):
        self.width = WIDTH
        self.height = HEIGHT - BUTTON_AREA_HEIGHT  # Data visualization height minus button area
        self.array_len = array_len
        self.array = []
        self.generate_new_array()

    def generate_new_array(self):
        self.array = [random.randint(10, self.height - 10) for _ in range(self.array_len)]  # Limit height to available space

    def draw_data(self, array, color_array):
        screen.fill(WHITE, (0, BUTTON_AREA_HEIGHT, WIDTH, HEIGHT - BUTTON_AREA_HEIGHT))  # Clear only the data visualization area
        element_width = self.width // len(array)
        for i, height in enumerate(array):
            color = RED if color_array[i] == 'red' else GREEN if color_array[i] == 'green' else BLUE
            # Draw filled rectangles (bars)
            pygame.draw.rect(screen, color, (i * element_width, HEIGHT - height, element_width, height))
            # Draw borders (slightly smaller rectangle)
            pygame.draw.rect(screen, BLACK, (i * element_width, HEIGHT - height, element_width, height), 2)
        pygame.display.update((0, BUTTON_AREA_HEIGHT, WIDTH, HEIGHT - BUTTON_AREA_HEIGHT))  # Only update the data area

    def run_sorting_visualizer(self, sorting_algorithm):
        sorting_algorithm(self.array, self.draw_data, 0.001)

    def set_array_len(self, new_len):
        self.array_len = new_len
        self.generate_new_array()

def main():
    running = True
    clock = pygame.time.Clock()
    visualizer = Visualizer()

    # Create buttons for each sorting algorithm
    buttons = [
        Button(10, 10, 130, 40, "Bubble Sort", lambda: visualizer.run_sorting_visualizer(bubble_sort)),
        Button(150, 10, 130, 40, "Selection Sort", lambda: visualizer.run_sorting_visualizer(selection_sort)),
        Button(290, 10, 130, 40, "Insertion Sort", lambda: visualizer.run_sorting_visualizer(insertion_sort)),
        Button(430, 10, 130, 40, "Merge Sort", lambda: visualizer.run_sorting_visualizer(merge_sort)),
        Button(570, 10, 130, 40, "Quick Sort", lambda: visualizer.run_sorting_visualizer(quick_sort)),
        Button(710, 10, 80, 40, "Heap Sort", lambda: visualizer.run_sorting_visualizer(heap_sort)),  # Adjusted width of Heap Sort button
        Button(10, 60, 130, 40, "Reset Array", visualizer.generate_new_array, color=RESET_BUTTON_COLOR)  # Different color for Reset button
    ]

    # Create an input box for defining the number of data elements (default is 50)
    input_box = InputBox(600, 60, 100, 40)

    while running:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle input box events
            new_text = input_box.handle_event(event)
            if new_text is not None:
                if new_text.isdigit():  # Ensure it's a number
                    visualizer.set_array_len(int(new_text))

            # Detect button click
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.is_clicked(pos):
                        button.action()

        # Clear the button area only once
        screen.fill(WHITE, (0, 0, WIDTH, BUTTON_AREA_HEIGHT))

        # Draw buttons
        for button in buttons:
            button.draw(screen, mouse_pos)

        # Draw input box
        input_box.draw(screen)

        # Draw the array visualization
        visualizer.draw_data(visualizer.array, ['blue' for _ in range(len(visualizer.array))])

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
