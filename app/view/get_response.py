from flask import Blueprint
from app import chatterbot
from app.chatterbot import languages
from app.chatterbot.trainers import ChatterBotCorpusTrainer
from app.chatterbot import *
from app.chatterbot import response_selection
from app.chatterbot.trainers import ChatterBotCorpusTrainer
bp_response = Blueprint('chatterbot', __name__,url_prefix='/chatterbot')

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
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.chinese")
@bp_response.route('/<message>')
def response(message):
    res = chatbot.get_response(message)
    return res.text

