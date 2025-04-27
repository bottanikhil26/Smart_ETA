import sys
class SmartetaException(Exception):
    """Base class for all exceptions raised by Smarteta."""
    def __init__(self,error_message,error_detail:sys):
        """
        Args:
            error_message (str): The error message to be displayed.
            error_detail (sys): The error detail object.
        """
        self.error_message = error_message
        _,_,exc_tb = error_detail.exc_info()

        self.line_number = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        """
        Returns the string representation of the exception.
        """
        return  f"Error occurred in python script name [{self.file_name}] at line number [{self.line_number}] error message [{self.error_message}]"
    
