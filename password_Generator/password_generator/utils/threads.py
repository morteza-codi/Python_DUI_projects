"""
Thread utilities for the Password Generator application.

Contains worker threads for background processing.
"""

from time import sleep
from PyQt6.QtCore import QThread, pyqtSignal
from password_generator.core.generator import CustomCharSetPasswordGenerator
from password_generator.utils.config import Config


class PasswordWorkerThread(QThread):
    """Worker thread for animated password generation."""
    
    # Define a signal to communicate with the main thread
    result_ready = pyqtSignal(str)
    # Signal for progress updates
    progress_update = pyqtSignal(int)

    def __init__(self, char_set=None, length=16, iterations=7, delay=0.5):
        """Initialize the worker thread.
        
        Args:
            char_set (str): Character set for password generation
            length (int): Length of password to generate
            iterations (int): Number of passwords to generate
            delay (float): Delay between generations in seconds
        """
        super().__init__()
        self.char_set = char_set if char_set else Config.PREDEFINED_CHAR_SETS[Config.DEFAULT_CHAR_SET]
        self.length = length
        self.iterations = iterations
        self.delay = delay
        self.is_running = True
    
    def run(self):
        """Run the animated password generation."""
        try:
            # Validate input
            if not self.char_set:
                self.result_ready.emit("لطفا کاراکترهای مورد نظر را وارد کنید")
                return
                
            if self.length <= 0:
                self.result_ready.emit("طول رمز باید بزرگتر از صفر باشد")
                return
                
            # Create generator
            generator = CustomCharSetPasswordGenerator(self.char_set, self.length)
            
            # Generate passwords with a delay between each
            for i in range(self.iterations):
                if not self.is_running:
                    break
                    
                password = generator.generate()
                self.result_ready.emit(password)
                
                # Emit progress update (0-100%)
                progress = int((i + 1) / self.iterations * 100)
                self.progress_update.emit(progress)
                
                sleep(self.delay)
                
        except ValueError as e:
            self.result_ready.emit(str(e))
        except Exception as e:
            self.result_ready.emit(f"خطا: {str(e)}")
    
    def stop(self):
        """Stop the animation."""
        self.is_running = False