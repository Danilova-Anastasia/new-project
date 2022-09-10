import argparse
import pickle
from train import MyTrigramModel


def generate_text():
    parser = argparse.ArgumentParser(description='генерация текстов')
    parser.add_argument('--model', type=str, help='путь к файлу, из которого загружается модель')
    parser.add_argument('--length', type=int, help='длина генерируемой последовательности')
    parser.add_argument('--prefix', type=str, default='-1',
                        help='необязательный аргумент. Начало предложения одно или два cлова. '
                             'Если не указано, начальное слово будет выбрано случайно из всех слов.')

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


if __name__ == '__main__':
    generate_text()
