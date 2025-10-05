from pydantic import BaseModel


class ErrorMessage(BaseModel):
    """Represents an error message."""

    message: str
