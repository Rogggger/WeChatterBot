from app.chatterbot_api.chatterbot.logic import LogicAdapter
from app.chatterbot_api.chatterbot.conversation import Statement

class RulesAdapter(LogicAdapter):
    """
    Return a specific response to a specific input.

    :kwargs:
        * *input_text* (``str``) --
          The input text that triggers this logic adapter.
        * *output_text* (``str``) --
          The output text returned by this logic adapter.
    """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.chatbot = chatbot


    def can_process(self, statement):
        return True

    def process(self, statement, additional_response_selection_parameters=None):

        rules_list = self.chatbot.storage.filter() # 提取所有规则对话
        response = Statement(text='',confidence=0)
        for rule in rules_list:
            if statement.text == rule.text:
                response = rule
                rule.confidence=1
                break
        return response
