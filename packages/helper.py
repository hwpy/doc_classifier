"""Название: __init__.py

Автор: hwpy
Дата: 2022 Март
Описание: Пакет функций для работы с файлами
"""

import os
import patoolib

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
