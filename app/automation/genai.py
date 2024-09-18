import json
import logging
from typing import Any

import google.generativeai as genai
from google.generativeai.types import HarmBlockThreshold, HarmCategory
from typing_extensions import TypedDict

from app.utilities.config import settings
from app.utilities.static_values import PROMPT_TEXT


class NewsSchema(TypedDict):
    title: str
    description: str
    source: str
    hashtags: list[str]


class AIResponseGenerator:
    def __init__(self) -> None:
        self.api_key = settings.genai_api_key
        self.model_name = settings.genai_model
        self.generation_config = genai.GenerationConfig(
            response_mime_type="application/json", response_schema=NewsSchema
        )
        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,  # noqa:E501
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,  # noqa:E501
        }
        self._configure_genai()

    def _configure_genai(self) -> None:
        """Configure the GenAI API client."""
        genai.configure(api_key=self.api_key)

    def get_ai_response(self, title: str, description: str) -> Any | None:
        """Generate AI response based on title and description."""
        model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=self.generation_config,
            safety_settings=self.safety_settings,
        )
        try:
            response = model.generate_content(
                contents=PROMPT_TEXT.format(title=title, description=description)
            )
            if response.text:
                return json.loads(response.text)
        except Exception as e:
            logging.error(f"Failed to generate AI response: {e}")
        return None
