class DatabaseConnectionError(Exception):
    """Raised when the database connection fails."""
    pass

class DuplicateFeedbackError(Exception):
    """Raised when a student tries to submit feedback twice for the same course."""
    pass

class AuthenticationError(Exception):
    """Raised when login fails due to invalid credentials."""
    pass

class FileHandlingError(Exception):
    """Raised when reading/writing the log file fails."""
    pass
