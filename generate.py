import argparse
import pickle
from random import choice
from collections import defaultdict
import train

class MyTrigramModel:
    @staticmethod
    def fit(list_of_corpuses):
        lines = gen_lines_from_files(list_of_corpuses)
        tokens = gen_tokens(lines)
        trigrams = gen_trigrams(tokens)

        bi, tri = defaultdict(int), defaultdict(int)

        for t0, t1, t2 in trigrams:
            bi[t0, t1] += 1
            tri[t0, t1, t2] += 1

        model = {}
        for (t0, t1, t2), freq in tri.items():
            if (t0, t1) in model:
                model[t0, t1].append((t2, freq / bi[t0, t1]))
            else:
                model[t0, t1] = [(t2, freq / bi[t0, t1])]
        return model

    @staticmethod
    def generate(model, length, prefix='-1'):
        phrase = ''
        bigrams = tuple(filter(lambda key: key[0] == prefix, model))
        # Если ввели 2 слова
        if tuple(prefix.split()) in model:
            t0, t1 = prefix.split()

        # Если ввели одно слово и оно есть в биграммах
        elif prefix != '-1' and len(bigrams) != 0:
            t0, t1 = choice(tuple(filter(lambda key: key[0] == prefix, model)))

        # Введеного слова нет в биграммах или ничего не ввели
        else:
            t0, t1 = choice(tuple(model))
        phrase += t0
        for i in range(length - len(prefix.split())):
            phrase += ' ' + t1
            t0, t1 = t1, choice(model[t0, t1])[0]
        return phrase.capitalize() + '.'


parser = argparse.ArgumentParser(description='генерация текстов')
parser.add_argument('--model', type=str, help='путь к файлу, из которого загружается модель')
parser.add_argument('--length', type=int, help='длина генерируемой последовательности')
parser.add_argument('--prefix', type=str, default='-1',
                    help='необязательный аргумент. Начало предложения одно или два cлова. '
                         'Если не указано, выбираем начальное слово случайно из всех слов.')

my_namespace = parser.parse_args()

# Загружаем модель
filename = my_namespace.model
with open(filename, 'rb') as file:
    model_from_pickle = pickle.load(file)

# Генерируем текст
prefix = my_namespace.prefix.lower()
length = my_namespace.length

gen_text = MyTrigramModel.generate(model=model_from_pickle, length=length, prefix=prefix)
print(gen_text)
