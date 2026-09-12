import requests

from config import Config


class AIServiceError(Exception):
    pass


class AIService:

    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.model = "openai/gpt-oss-20b"
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"

    def _get_business_context(self):
        return Config.BUSINESS_CONTEXT

    def yanit_uret(self, mesaj, gecmis=None):

        if not self.api_key:
            return (
                "Demo mode is active. "
                "A Groq API key could not be found, "
                "so a real AI response cannot be generated right now."
            )

        if gecmis is None:
            gecmis = []

        messages = [
            {
                "role": "system",
                "content": self._get_business_context()
            }
        ]

        messages.extend(gecmis)

        messages.append(
            {
                "role": "user",
                "content": mesaj
            }
        )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 500
        }

        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=30
            )

            if not response.ok:
                raise AIServiceError(
                    f"Groq API error. "
                    f"Status: {response.status_code} "
                    f"Details: {response.text}"
                )

            result = response.json()

            return result["choices"][0]["message"]["content"]

        except requests.RequestException as error:
            raise AIServiceError(
                f"An error occurred while connecting to the AI service: {error}"
            ) from error

        except (KeyError, IndexError, TypeError) as error:
            raise AIServiceError(
                f"The AI response was not in the expected format: {error}"
            ) from error


ai_service = AIService()