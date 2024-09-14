from pydantic import BaseModel

class ErrorSchema(BaseModel):
    """
    Schema representing an error message.

    Attributes:
        message (str): The error message.
    """
    message: str