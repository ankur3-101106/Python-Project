import pygame
import time
import random
import math
import json
from typing import List, Dict, Tuple

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 160

# Colors (Monkeytype-inspired theme)
COLORS = {
    'bg': (21, 21, 21),
    'text_default': (100, 100, 100),
    'text_correct': (255, 255, 255),
    'text_incorrect': (255, 100, 100),
    'text_current': (255, 200, 50),
    'cursor': (255, 200, 50),
    'stats': (150, 150, 150),
    'accent': (255, 200, 50)
}

# Sample texts for typing test
SAMPLE_TEXTS = [
    "The quick brown fox jumps over the lazy dog and runs through the forest with great speed and agility.",
    "Programming is not about what you know it is about what you can figure out when you need to solve problems.",
    "In the world of technology innovation happens at lightning speed and adaptation is the key to survival.",
    "The art of writing code is like composing music where every line has rhythm and every function has purpose.",
    "Success in life comes from persistence dedication and the willingness to learn from your mistakes every day.",
    "The beauty of nature lies in its complexity from the smallest atom to the largest galaxy in space.",
    "Communication is the bridge between confusion and clarity helping people understand each other better.",
    "Time is the most valuable resource we have and how we use it determines the quality of our lives.",
]

class TypingTest:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Monkeytype Clone - Typing Speed Test")
        self.clock = pygame.time.Clock()
        
        # Fonts - Try to load Meslo Nerd Font, fallback to monospace
        try:
            self.font_large = pygame.font.Font("MesloLGS NF Regular.ttf", 32)
            self.font_medium = pygame.font.Font("MesloLGS NF Regular.ttf", 24)
            self.font_small = pygame.font.Font("MesloLGS NF Regular.ttf", 20)
        except:
            # Fallback to system monospace font
            try:
                self.font_large = pygame.font.SysFont("meslo", 32)
                self.font_medium = pygame.font.SysFont("meslo", 24)
                self.font_small = pygame.font.SysFont("meslo", 20)
            except:
                # Final fallback to monospace
                self.font_large = pygame.font.SysFont("monospace", 32)
                self.font_medium = pygame.font.SysFont("monospace", 24)
                self.font_small = pygame.font.SysFont("monospace", 20)
        
        # Generate typing sounds
        self.generate_sounds()
        
        # Test state
        self.reset_test()
        
    def generate_sounds(self):
        """Generate simple beep sounds for keypress feedback"""
        try:
            # Create simple sine wave sounds
            sample_rate = 22050
            duration = 0.1
            
            # Correct keypress sound (higher pitch)
            correct_freq = 800
            correct_samples = int(sample_rate * duration)
            correct_wave = []
            for i in range(correct_samples):
                wave_value = int(4096 * math.sin(2 * math.pi * correct_freq * i / sample_rate))
                correct_wave.append([wave_value, wave_value])
            
            self.sound_correct = pygame.sndarray.make_sound(pygame.array.array('h', correct_wave)) # type: ignore
            self.sound_correct.set_volume(0.3)
            
            # Incorrect keypress sound (lower pitch)
            incorrect_freq = 300
            incorrect_samples = int(sample_rate * duration)
            incorrect_wave = []
            for i in range(incorrect_samples):
                wave_value = int(4096 * math.sin(2 * math.pi * incorrect_freq * i / sample_rate))
                incorrect_wave.append([wave_value, wave_value])
            
            self.sound_incorrect = pygame.sndarray.make_sound(pygame.array.array('h', incorrect_wave)) # type: ignore
            self.sound_incorrect.set_volume(0.3)
            
        except Exception as e:
            print(f"Could not generate sounds: {e}")
            self.sound_correct = None
            self.sound_incorrect = None
    
    def reset_test(self):
        """Reset the typing test to initial state"""
        self.text = random.choice(SAMPLE_TEXTS)
        self.typed_text = ""
        self.current_index = 0
        self.start_time = None
        self.end_time = None
        self.errors = 0
        self.test_completed = False
        self.wpm = 0
        self.accuracy = 100
        
    def calculate_stats(self):
        """Calculate WPM and accuracy in real-time"""
        if self.start_time is None:
            return
            
        elapsed_time = time.time() - self.start_time
        if elapsed_time > 0:
            # Calculate WPM (assuming average word length of 5 characters)
            characters_typed = len(self.typed_text)
            words_typed = characters_typed / 5
            self.wpm = int((words_typed / elapsed_time) * 60)
            
            # Calculate accuracy
            if characters_typed > 0:
                correct_chars = characters_typed - self.errors
                self.accuracy = int((correct_chars / characters_typed) * 100)
    
    def handle_keypress(self, key_char: str):
        """Handle character input and check correctness"""
        if self.test_completed:
            return
            
        # Start timer on first keypress
        if self.start_time is None:
            self.start_time = time.time()
        
        # Check if character is correct
        if self.current_index < len(self.text):
            expected_char = self.text[self.current_index]
            
            if key_char == expected_char:
                # Correct character
                self.typed_text += key_char
                self.current_index += 1
                if self.sound_correct:
                    self.sound_correct.play()
            else:
                # Incorrect character
                self.typed_text += key_char
                self.current_index += 1
                self.errors += 1
                if self.sound_incorrect:
                    self.sound_incorrect.play()
            
            # Check if test is completed
            if self.current_index >= len(self.text):
                self.end_time = time.time()
                self.test_completed = True
        
        self.calculate_stats()
    
    def handle_backspace(self):
        """Handle backspace key"""
        if self.current_index > 0 and not self.test_completed:
            self.current_index -= 1
            self.typed_text = self.typed_text[:-1]
            self.calculate_stats()
    
    def draw_text_with_highlighting(self):
        """Draw the text with character-by-character highlighting"""
        y_offset = WINDOW_HEIGHT // 2 - 100
        x_start = 50
        line_height = 40
        max_width = WINDOW_WIDTH - 100
        
        current_x = x_start
        current_y = y_offset
        
        for i, char in enumerate(self.text):
            # Determine color based on typing progress
            if i < self.current_index:
                # Already typed
                if i < len(self.typed_text):
                    if self.typed_text[i] == char:
                        color = COLORS['text_correct']
                    else:
                        color = COLORS['text_incorrect']
                else:
                    color = COLORS['text_default']
            elif i == self.current_index:
                # Current character
                color = COLORS['text_current']
                # Draw cursor background
                cursor_rect = pygame.Rect(current_x - 2, current_y, 2, 30)
                pygame.draw.rect(self.screen, COLORS['cursor'], cursor_rect)
            else:
                # Not yet typed
                color = COLORS['text_default']
            
            # Render character
            char_surface = self.font_large.render(char, True, color)
            char_width = char_surface.get_width()
            
            # Handle line wrapping
            if current_x + char_width > max_width:
                current_x = x_start
                current_y += line_height
            
            self.screen.blit(char_surface, (current_x, current_y))
            current_x += char_width
    
    def draw_stats(self):
        """Draw real-time statistics"""
        stats_y = 100
        
        # WPM
        wpm_text = f"WPM: {self.wpm}"
        wpm_surface = self.font_medium.render(wpm_text, True, COLORS['accent'])
        self.screen.blit(wpm_surface, (50, stats_y))
        
        # Accuracy
        accuracy_text = f"Accuracy: {self.accuracy}%"
        accuracy_surface = self.font_medium.render(accuracy_text, True, COLORS['stats'])
        self.screen.blit(accuracy_surface, (200, stats_y))
        
        # Progress
        progress = (self.current_index / len(self.text)) * 100 if len(self.text) > 0 else 0
        progress_text = f"Progress: {progress:.1f}%"
        progress_surface = self.font_medium.render(progress_text, True, COLORS['stats'])
        self.screen.blit(progress_surface, (400, stats_y))
        
        # Timer
        if self.start_time:
            if self.test_completed and self.end_time:
                elapsed = self.end_time - self.start_time
            else:
                elapsed = time.time() - self.start_time
            timer_text = f"Time: {elapsed:.1f}s"
            timer_surface = self.font_medium.render(timer_text, True, COLORS['stats'])
            self.screen.blit(timer_surface, (600, stats_y))
    
    def draw_results(self):
        """Draw final results when test is completed"""
        if not self.test_completed:
            return
        
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Results box
        box_width = 500
        box_height = 350
        box_x = (WINDOW_WIDTH - box_width) // 2
        box_y = (WINDOW_HEIGHT - box_height) // 2
        
        # Draw box background and border
        pygame.draw.rect(self.screen, COLORS['bg'], (box_x, box_y, box_width, box_height))
        pygame.draw.rect(self.screen, COLORS['accent'], (box_x, box_y, box_width, box_height), 3)
        
        # Results text
        results_y = box_y + 40
        
        # Title
        title_surface = self.font_large.render("Test Complete!", True, COLORS['accent'])
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, results_y))
        self.screen.blit(title_surface, title_rect)
        
        # Final stats with better spacing
        final_wpm = self.font_medium.render(f"Final WPM: {self.wpm}", True, COLORS['text_correct'])
        final_wpm_rect = final_wpm.get_rect(center=(WINDOW_WIDTH // 2, results_y + 70))
        self.screen.blit(final_wpm, final_wpm_rect)
        
        final_accuracy = self.font_medium.render(f"Accuracy: {self.accuracy}%", True, COLORS['text_correct'])
        final_accuracy_rect = final_accuracy.get_rect(center=(WINDOW_WIDTH // 2, results_y + 110))
        self.screen.blit(final_accuracy, final_accuracy_rect)
        
        # Calculate and display total time
        total_time = self.end_time - self.start_time if self.end_time and self.start_time else 0
        time_text = self.font_medium.render(f"Total Time: {total_time:.1f}s", True, COLORS['text_correct'])
        time_rect = time_text.get_rect(center=(WINDOW_WIDTH // 2, results_y + 150))
        self.screen.blit(time_text, time_rect)
        
        # Character stats
        total_chars = len(self.typed_text)
        correct_chars = total_chars - self.errors
        chars_text = self.font_small.render(f"Characters: {correct_chars}/{total_chars} correct", True, COLORS['stats'])
        chars_rect = chars_text.get_rect(center=(WINDOW_WIDTH // 2, results_y + 190))
        self.screen.blit(chars_text, chars_rect)
        
        # Instructions
        restart_text = self.font_small.render("Press SPACE to restart or ESC to quit", True, COLORS['accent'])
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, results_y + 240))
        self.screen.blit(restart_text, restart_rect)
    
    def draw_instructions(self):
        """Draw initial instructions"""
        if self.start_time is None:
            instruction_text = "Start typing to begin the test..."
            instruction_surface = self.font_medium.render(instruction_text, True, COLORS['stats'])
            instruction_rect = instruction_surface.get_rect(center=(WINDOW_WIDTH // 2, 50))
            self.screen.blit(instruction_surface, instruction_rect)
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    
                    elif event.key == pygame.K_SPACE and self.test_completed:
                        self.reset_test()
                    
                    elif event.key == pygame.K_BACKSPACE:
                        self.handle_backspace()
                    
                    elif event.unicode and event.unicode.isprintable() and not self.test_completed:
                        self.handle_keypress(event.unicode)
            
            # Clear screen
            self.screen.fill(COLORS['bg'])
            
            # Draw UI elements
            self.draw_instructions()
            self.draw_stats()
            self.draw_text_with_highlighting()
            self.draw_results()
            
            # Update display
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    try:
        game = TypingTest()
        game.run()
    except Exception as e:
        print(f"Error running typing test: {e}")
        pygame.quit()
