import traceback
import sys

class CustomException(Exception):
    def __init__(self, message, error_detail: sys):
        super().__init__(message)
        self.message = self.get_detailed_error_message(message, error_detail)

    @staticmethod
    def get_detailed_error_message(message, error_detail: sys):
        _, _, exc_tb = error_detail.exc_info()
        filename = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
        return f"Error occurred in {filename}, line number: {line_number}. Message: {message}"
    
    def __str__(self):
        return self.message