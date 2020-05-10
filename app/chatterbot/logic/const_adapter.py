from app.chatterbot.logic import LogicAdapter


class ConstAdapter(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        from app.chatterbot.conversation import Statement

        self.text = kwargs.get('const_response', '看不懂唉')
        self.confidence = kwargs.get('const_confidence', 0.0)

        self.response_statement = Statement(text=self.text)

    def process(self, statement, additional_response_selection_parameters=None):
        self.response_statement.confidence = self.confidence
        return self.response_statement
