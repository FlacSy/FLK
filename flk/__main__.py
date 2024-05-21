from flk.parser import Parser
import argparse


def parse_args():
    """
    Разбирает аргументы командной строки.

    Возвращает объект с аргументами, где 'filename' - имя файла, который нужно спарсить.
    """
    parser = argparse.ArgumentParser(description="Парсер файлов")
    parser.add_argument('filename', type=str, help='Имя файла для парсинга')
    return parser.parse_args()

def main():
    """
    Основная функция для запуска парсера из командной строки.

    Использует аргументы командной строки для определения файла для парсинга и выводит результаты.
    Обрабатывает исключения, возникающие в процессе парсинга.
    """
    args = parse_args()
    parser = Parser()
    try:
        data = parser.parse_file(args.filename)
        print(data)
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()