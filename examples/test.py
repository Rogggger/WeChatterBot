from app.chatterbot import *
from app.chatterbot import response_selection
from app import chatterbot
from app.chatterbot.trainers import ChatterBotCorpusTrainer
from app.chatterbot.trainers import TsvTrainer
import os


if __name__ == '__main__':
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
    chatbot.storage.create_rule(text='今天天气真好',in_response_to='是啊')
    #trainer = ChatterBotCorpusTrainer(chatbot)
    #trainer.train("chatterbot.corpus.chinese")
    trainer = TsvTrainer(chatbot)
    files = os.listdir('../../clean_chat_corpus')
    for file in files:
        print('training with:' + file)
        trainer.train('../../clean_chat_corpus/'+file)
        break
    message = '今天天气真好'
    res = chatbot.get_response(message)
    print(res)