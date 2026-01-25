# controller/error_controller.py

from services.api_client import ApiClient

class ErrorController:

    def __init__(self):
        self.api_client = ApiClient()

    def handle_error(self, error_message: str) -> str:
        if not error_message.strip():
            raise ValueError("Error message is empty")

        return self.api_client.ask_error(error_message)