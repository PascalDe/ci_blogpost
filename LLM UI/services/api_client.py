import requests
from config import FASTAPI_BASE_URL, ASK_ENDPOINT, REQUEST_TIMEOUT

class ApiClient:

    def ask_error(self, error_message: str) -> str:
        url = f"{FASTAPI_BASE_URL}{ASK_ENDPOINT}"

        try:
            response = requests.post(url,json={"error_message": error_message},timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            data = response.json()
            return data.get("llm_answer", "Didn't receive an answer.")
        except Exception as e:
            print("Request Exception:", e)
            return f"An error occured while receiving an answer: {e}"
