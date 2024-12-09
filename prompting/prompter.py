from copy import deepcopy
from openai import OpenAI
from prompting.configuration import OpenAIConfiguration


class OpenAIPrompter:
    def __init__(self, config: OpenAIConfiguration):
        self.__client = OpenAI(api_key=config.api_key)
        self.__model = config.model

    def prompt(self, messages_template: list, template_mask: str, text: str) -> str:
        messages = deepcopy(messages_template)
        # Insert text into the message template.
        self.__prepare_messages(messages, template_mask, text)
        response = self.__client.chat.completions.create(
          model=self.__model,
          messages=messages
        )
        response = response.choices[0].message.content
        return response

    @staticmethod
    def __prepare_messages(messages: list, template_mask: str, text: str):
        # Insert text into the message template.
        for message in messages:
            if template_mask in message["content"]:
                message["content"] = message["content"].replace(template_mask, text)
