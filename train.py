import argparse
import sys
import os
import re
from random import choice
from collections import defaultdict
import pickle


def gen_lines_from_files(list_of_corpuses):
    for corpus in list_of_corpuses:
        with open(corpus, 'r', encoding='utf-8') as file:
            for line in file:
                yield line.lower()


def gen_tokens(lines):
    alphabet = re.compile(u'[а-яА-Я0-9]+')
    for line in lines:
        for token in alphabet.findall(line):
            yield token


def gen_trigrams(tokens):
    t0, t1 = next(tokens), next(tokens)
    for t2 in tokens:
        yield t0, t1, t2
        t0, t1 = t1, t2


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


parser = argparse.ArgumentParser(description='Обучение триграмной модели')
parser.add_argument('--model', type=str, help='путь к файлу, в который сохраняется модель')
parser.add_argument('--inputdir', type=str, default='stdin',
                    help='путь к директории, в которой лежит коллекция документов. '
                         'Если данный аргумент не задан, считать, что тексты вводятся из stdin.')
my_namespace = parser.parse_args()
directory = my_namespace.inputdir

# Потоковый ввод
if directory == 'stdin':
    with open('text_stdin.txt', 'w', encoding='utf-8') as file:
        for line in sys.stdin:
            file.write(line)
    list_of_filenames = ['text_stdin.txt']
else:
    # список файлов в директории для обучения
    list_of_filenames = [directory + '\\' + s for s in os.listdir(directory)]

# Обучение модели
my_model = MyTrigramModel.fit(list_of_filenames)

# Сохранение модели
filename = my_namespace.model
with open(filename, 'wb') as file:
    pickle.dump(my_model, file)
