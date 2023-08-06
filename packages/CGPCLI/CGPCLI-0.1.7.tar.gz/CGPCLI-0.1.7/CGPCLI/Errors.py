from sys import exc_info

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class ConnectionTimeOut(Error):
    """Exception raised when server closes connection due timeout"""

    def __init__(self, message='Server has closed the connection due time out'):
        self.expression = exc_info()[2]
        self.message = message  

class CommandFailedError(Error):
    """Exception raised when server occures an error"""

    def __init__(self, message):
        self.expression = exc_info()[2]
        self.message = message  
    
class NotValidCGPStringError(Error):
    """Exception raised when parser can't parse a string"""

    def __init__(self, message='Can not parse this string'):
        self.expression = exc_info()[2]
        self.message = message
    
class FailedLogin(Error):
    """Exception raised when username or password does not match"""

    def __init__(self, message):
        self.expression = exc_info()[2]
        self.message = message