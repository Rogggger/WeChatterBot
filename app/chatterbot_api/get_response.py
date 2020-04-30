from flask import Blueprint
from app.chatterbot_api.chatterbot import languages
from app.chatterbot_api.chatterbot import *
from app.chatterbot_api.chatterbot import response_selection
from app.chatterbot_api import chatterbot
from app.chatterbot_api.chatterbot.trainers import ChatterBotCorpusTrainer
from app.chatterbot_api.chatterbot.trainers import TsvTrainer
bp_response = Blueprint('/chatterbot', __name__)

chatbot = chatterbot.ChatBot(
    "My ChatterBot",
    logic_adapters=[
        "chatterbot.logic.BestMatch",
        "chatterbot.logic.RulesResponseAdapter"
    ],
    tagger_language=chatterbot.languages.CHI,
    statement_comparison_function=comparisons.JaccardSimilarity,
    response_selection_method=response_selection.get_most_frequent_response
)
trainer = TsvTrainer(chatbot)
files = os.listdir('../../clean_chat_corpus')
@bp_response.route('/<message>')
def response(message):
    res = chatbot.get_response(message)
    return res.text
