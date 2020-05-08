from app.chatterbot import ChatBot
from app.chatterbot import response_selection
from app.chatterbot import comparisons
from app.chatterbot.trainers import ChatterBotCorpusTrainer
from app.chatterbot import languages

chatbot = ChatBot(
    "My ChatterBot",
    logic_adapters=[
        "chatterbot.logic.BestMatch",
        "chatterbot.logic.RulesResponseAdapter"
    ],
    tagger_language=languages.CHI,
    statement_comparison_function=comparisons.JaccardSimilarity,
    response_selection_method=response_selection.get_most_frequent_response
)
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.chinese")


