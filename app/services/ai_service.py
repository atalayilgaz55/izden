import requests

from config import Config


class AIServiceError(Exception):

    pass


class AIService:

    def __init__(self):
        self.api_key = Config.GROQ_API_KEY

        self.model = "llama-3.1-8b-instant"

        self.api_url = "https://api.groq.com/openai/v1/chat/completions"

    def _system_message(self):

        return Config.BUSINESS_CONTEXT

    def yanit_uret(self, mesaj, gecmis=None):

        if not self.api_key:
            return (
                "Şu anda demo modundayım. "
                "İZDEN; yarım bırakılmış yaratıcı çalışmaların "
                "başka insanlar tarafından devam ettirilebildiği "
                "katılımcı bir kültür ve sanat projesidir."
            )

        if gecmis is None:
            gecmis = []

        messages = [
            {
                "role": "system",
                "content": self._system_message()
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
            "temperature": 0.7
        }

        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=30
            )

            response.raise_for_status()

            result = response.json()

            return result["choices"][0]["message"]["content"]

        except requests.RequestException as error:
            raise AIServiceError(
                "Yapay zekâ servisine bağlanırken bir hata oluştu."
            ) from error

        except (KeyError, IndexError, TypeError):
            raise AIServiceError(
                "Yapay zekâ servisinden beklenmeyen bir cevap geldi."
            )



ai_service = AIService()