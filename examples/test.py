import sys
sys.path.append('../')
sys.path.append('../app/chatterbot_api')
from app.chatterbot_api import chatterbot
from app.chatterbot_api.chatterbot.trainers import ChatterBotCorpusTrainer

chatbot = chatterbot.ChatBot(
    "My ChatterBot",
    tagger_language=chatterbot.languages.CHI,
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": chatterbot.comparisons.JaccardSimilarity,
            "response_selection_method": chatterbot.response_selection.get_most_frequent_response
        }
    ]
)
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.chinese")
message = '苹果真好吃'
res = chatbot.get_response(message)
print(res)