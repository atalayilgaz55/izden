from groq import Groq

from config import Config


class AIServiceError(Exception):
    pass


class AIService:

    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.model = "openai/gpt-oss-120b"

        if self.api_key:
            self.client = Groq(api_key=self.api_key)
        else:
            self.client = None

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

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3
            )

            return completion.choices[0].message.content

        except Exception as error:
            raise AIServiceError(
                "Yapay zekâ servisine bağlanırken bir hata oluştu."
            ) from error


ai_service = AIService()
