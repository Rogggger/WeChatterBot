import sys
sys.path.append('../')
sys.path.append('../app/chatterbot_api')
from app.chatterbot_api.chatterbot import *
from app.chatterbot_api.chatterbot import response_selection
from app.chatterbot_api import chatterbot
from app.chatterbot_api.chatterbot.trainers import ChatterBotCorpusTrainer

chatbot = chatterbot.ChatBot(
    "My ChatterBot",
    tagger_language=chatterbot.languages.CHI,
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": comparisons.JaccardSimilarity,
            "response_selection_method": response_selection.get_most_frequent_response
        }
    ]
)
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.chinese")
message = '你喝酒么'
res = chatbot.get_response(message)
print(res)