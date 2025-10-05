class NotFoundError(Exception):
    """Raised when an entity is not found."""

    def __init__(self) -> None:
        """Initializes the exception."""
        self.message = 'Not Found'
        super().__init__(self.message)
