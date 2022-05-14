"""Название: helper.py

Автор: hwpy
Дата: 2022 Март
Описание: Пакет функций для работы с файлами
"""

import os
import patoolib
import collections
import numpy as np
from typing import List

# кортеж расширений архивов для обработки
TUPLE_OF_ARCHIVES = ('.rar', '.zip', '.7z')


def recursive_unpack(path: str, drop_archive: bool = False) -> None:
    """Обход каталогов и разархивирование самого архива
           и его вложенных архивов типа rar / zip / 7z

    Аргументы:
        - path (str) путь к архиву
        - drop_archive (bool) удалить исходный архив (по умолчанию {False})

    Возвращает:
        None
    """

    for root, _, files in os.walk(path):
        print(f"Файл будет сохранен в каталог: {root}!")
        for file in files:
            if file.endswith(TUPLE_OF_ARCHIVES):
                try:
                    patoolib.extract_archive(
                        os.path.join(root, file),
                        outdir=root
                    )
                    if drop_archive:
                        os.remove(os.path.join(root, file))
                except patoolib.util.PatoolError:
                    # Файл уже разархивирован
                    continue
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(TUPLE_OF_ARCHIVES):
                recursive_unpack(root)
                break


def single_unpack(path: str, drop_archive: bool = False) -> None:
    """Разархивирование файла типа rar / zip / 7z
           без вложенности

    Аргументы:
        - path (str) путь к архиву
        - drop_archive (bool) удалить исходный архив (по умолчанию {False})

    Возвращает:
        None
    """
    for root, dirs, files in os.walk(path):
        print(f"Файл будет сохранен в каталог: {root}!")
        for file in files:
            if file.endswith(TUPLE_OF_ARCHIVES):
                print(file, root, dirs)
                try:
                    patoolib.extract_archive(
                        os.path.join(root, file),
                        outdir=root
                    )
                    if drop_archive:
                        os.remove(os.path.join(root, file))
                except patoolib.util.PatoolError:
                    continue


def build_vocabulary(
    tokenized_texts: List[List],
    max_size: int = 40000,
    max_doc_freq: float = 0.8,
    min_count: int = 5,
    pad_word: bool = None
):
    """Построить словарь из токенизированных текстов

    Аргументы:
        - tokenized_texts () - Токинезированные тексты

        - max_size (int) - Количество слов, которые будут в словаре - самые частотные (по умолчанию: {40000})
        - max_doc_freq (float) - Верхняя граница частотности (по умолчанию: {0.8})
        - min_count (int) - Нижняя граница кол-во употреблений (по умолчанию: {5})
        - pad_word (_type_) - Добавить слово с индексом 0 (по умолчанию: {None})

    Возвращает:
        _type_ - Словарь, частотность
    """

    word_counts = collections.defaultdict(int)
    doc_n = 0

    # посчитать количество документов, в которых употребляется каждое слово
    # а также общее количество документов
    for txt in tokenized_texts:
        doc_n += 1
        unique_text_tokens = set(txt)
        for token in unique_text_tokens:
            word_counts[token] += 1

    # убрать слишком редкие и слишком частые слова
    word_counts = {word: cnt for word, cnt in word_counts.items()
                   if cnt >= min_count and cnt / doc_n <= max_doc_freq}

    # отсортировать слова по убыванию частоты
    sorted_word_counts = sorted(word_counts.items(),
                                reverse=True,
                                key=lambda pair: pair[1])

    # добавим несуществующее слово с индексом 0 для удобства пакетной обработки
    if pad_word is not None:
        sorted_word_counts = [(pad_word, 0)] + sorted_word_counts

    # если у нас по прежнему слишком много слов, оставить только max_size самых частотных
    if len(word_counts) > max_size:
        sorted_word_counts = sorted_word_counts[:max_size]

    # нумеруем слова
    word2id = {word: i for i, (word, _) in enumerate(sorted_word_counts)}

    # нормируем частоты слов
    word2freq = np.array([cnt / doc_n for _, cnt in sorted_word_counts], dtype='float32')

    return word2id, word2freq