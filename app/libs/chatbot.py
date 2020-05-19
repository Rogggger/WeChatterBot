from app.chatterbot import ChatBot
from app.chatterbot import response_selection
from app.chatterbot import comparisons
from app.chatterbot.trainers import ChatterBotCorpusTrainer
from app.chatterbot import languages

chatbot = ChatBot(
    "My ChatterBot",
    logic_adapters=[
        "chatterbot.logic.BestMatch",
        "chatterbot.logic.RulesResponseAdapter",
        "chatterbot.logic.ConstAdapter"
    ],
    tagger_language=languages.CHI,
    statement_comparison_function=comparisons.JaccardSimilarity,
    response_selection_method=response_selection.get_random_response,
    const_response='没看懂唉',
    const_confidence=0.1,
    read_only=True
)


def train_chatbot():
    # only need to run once
    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train("chatterbot.corpus.chinese")
