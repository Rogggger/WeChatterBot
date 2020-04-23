from flask import Blueprint
from app.chatterbot_api import chatterbot
from app.chatterbot_api.chatterbot import languages
from app.chatterbot_api.chatterbot.trainers import ChatterBotCorpusTrainer

from app.chatterbot_api.chatterbot import *
from app.chatterbot_api.chatterbot import response_selection
from app.chatterbot_api.chatterbot.trainers import ChatterBotCorpusTrainer
bp_response = Blueprint('/chatterbot', __name__)

chatbot = chatterbot.ChatBot(
    "chatbot",
    tagger_language=chatterbot.languages.CHI,
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": comparisons.JaccardSimilarity,
            "response_selection_method": response_selection.get_most_frequent_response
        }
    ]
)
#chatbot = chatterbot.ChatBot('chatbot',tagger_language=languages.CHI)
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.chinese")

@bp_response.route('/<message>')
def response(message):
    res = chatbot.get_response(message)
    return res.text