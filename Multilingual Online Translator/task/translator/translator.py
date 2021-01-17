import requests
from bs4 import BeautifulSoup
import argparse

AVAILABLE_LANGUAGES = ('all',
                       'arabic',
                       'german',
                       'english',
                       'spanish',
                       'french',
                       'hebrew',
                       'japanese',
                       'dutch',
                       'polish',
                       'portuguese',
                       'romanian',
                       'russian',
                       'turkish')

session = None


def show_available_languages():
    """Function for showing all available languages."""
    print("Hello, you're welcome to the translator. Translator supports: ")
    for idx, element in enumerate(AVAILABLE_LANGUAGES[1:], 1):
        if idx != '0':
            print(f"{idx}. {element}")


def make_url(language_from: str, language_to: str, word: str) -> list:
    """Function for making url. Always returns list with all made links (if one language was chose, list of len 1)."""
    # return list with one url if just one language
    if language_to != 'all':
        return [f"https://context.reverso.net/translation/{language_from}-"
                f"{language_to}"
                f"/{word}"]

    # return list of url's if more that one language
    urls = []
    for current_language in AVAILABLE_LANGUAGES[1:]:
        if current_language != language_from:
            urls.append(f"https://context.reverso.net/translation/{language_from}-"
                        f"{current_language}/{word}")
    return urls


def results_write_to_file(singles: list, sentences: list, language: str, user_word: str, num_of_translations: int):
    """Function for writing results to file."""
    with open(f'{user_word}.txt', 'a+', encoding="UTF-8") as f:
        f.write(f'{language.capitalize()} Translations:\n')

        # single words
        singles = singles[:num_of_translations]
        for word in singles:
            f.write(word + '\n')
        f.write(f'\n{language.capitalize()} examples:\n')

        # sentences
        for i in range(len(singles)):
            f.write(sentences[i * 2] + "\n")
            f.write(sentences[i * 2 + 1] + '\n\n')
        f.write('\n')


def read_file(file: str):
    """Function for reading file."""
    with open(file, 'r+', encoding="UTF-8") as f:
        for line in f.readlines():
            print(line.strip())


def check_response(response):
    """Function for checking, if response webstrap is OK."""
    if response.ok:
        print('200 OK')
    else:
        print('Something went wrong')
        exit()


def take_input() -> tuple:
    """Function for taking user input."""
    print('Type the number of your language: ')
    user_language_from = input()
    print("Type the number of a language you want to translate to or '0' to translate to all languages:")
    user_language_to = input()
    print('Type the word you want to translate:')
    user_word = input()
    return user_language_from, user_language_to, user_word


def make_translations(url: list, check_if_all: str):
    """Function for webscraping data from reverso.net"""
    # global session, user_word
    num_of_translations = 1 if check_if_all == 'all' else 5
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/80.0.3987.132 Safari/537.36"}
    for idx, link in enumerate(url, 1):
        request = session.get(link, headers=headers)
        soup = BeautifulSoup(request.content, 'html.parser')
        # check_response(request)

        single_results = [x.get_text(strip=True) for x in soup.select("#translations-content > .translation")]
        quote_results = [item.text.strip() for item in soup.find_all('div', {'class': ['src', 'trg']})]
        quote_results = [x for x in quote_results if len(x) != 0]

        *_, language, user_word = link.split('/')
        language_from, language_to = language.split('-')
        results_write_to_file(single_results, quote_results, language_to, user_word,
                              num_of_translations)
    read_file(user_word + '.txt')


def main():
    global session  # session for faster loading
    session = requests.Session()
    # show_available_languages()
    # user_language_from_num, user_language_to_num, user_word = take_input()

    parser = argparse.ArgumentParser(
        description=''' Welcome to Multilingual Online Translator.
                        As arguments, first type your language, then language you want translate to,
                        and as a third argument your word.'''
    )
    parser.add_argument('user_language_from', action="store")
    parser.add_argument('user_language_to', action="store")
    parser.add_argument('user_word', action="store")
    args = parser.parse_args()

    url = make_url(language_from=args.user_language_from,
                   language_to=args.user_language_to,
                   word=args.user_word)
    make_translations(url, args.user_language_to)


if __name__ == '__main__':  # run as script
    main()
