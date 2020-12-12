import requests
from bs4 import BeautifulSoup

AVAILABLE_LANGUAGES = {
    '0': 'all',
    '1': 'Arabic',
    '2': 'German',
    '3': 'English',
    '4': 'Spanish',
    '5': 'French',
    '6': 'Hebrew',
    '7': 'Japanese',
    '8': 'Dutch',
    '9': 'Polish',
    '10': 'Portuguese',
    '11': 'Romanian',
    '12': 'Russian',
    '13': 'Turkish',
}

def show_available_languages():
    """Function for showing all available languages."""
    print("Hello, you're welcome to the translator. Translator supports: ")
    for idx, element in AVAILABLE_LANGUAGES.items():
        if idx != '0':
            print(f"{idx}. {element}")

def make_url(language_from: str, language_to: str, word: str) -> list:
    """Function for making url. Always returns list with all made links (if one language was chose, list of len 1)."""
    # return list with one url if just one language
    if language_to != '0':
        return [f"https://context.reverso.net/translation/{AVAILABLE_LANGUAGES[language_from].lower()}-"
                f"{AVAILABLE_LANGUAGES[language_to].lower()}"
                f"/{word}"]

    # return list of url's if more that one language
    urls = []
    for current_language in list(AVAILABLE_LANGUAGES.values())[1:]:
        urls.append(f"https://context.reverso.net/translation/{AVAILABLE_LANGUAGES[language_from].lower()}-"
                    f"{current_language.lower()}/{word}")
    return urls

def results_print_and_write(singles: list, sentences: list, language: str, user_word: str, num_of_translations: int):
    """Function for writing results to file."""
    with open(f'{user_word}.txt', 'a+', encoding="UTF-8") as f:
        f.write(f'{language} Translations:\n')

        # single words
        singles = singles[:num_of_translations]
        for word in singles:
            f.write(word + '\n')
        f.write(f'\n{language} Examples:\n')

        # sentences
        for i in range(len(singles)):
            f.write(sentences[i * 2] + "\n")
            f.write(sentences[i * 2 + 1] + '\n\n')
        f.write('\n')
    read_file(f"{user_word}.txt")

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
    """Funcion for taking user input."""
    print('Type the number of your language: ')
    user_language_from = input()
    print("Type the number of a language you want to translate to or '0' to translate to all languages:")
    user_language_to = input()
    print('Type the word you want to translate:')
    user_word = input()
    return user_language_from, user_language_to, user_word

def make_translations(url: list, user_language_num: str, user_word: str):
    """Function for webscraping data from reverso.net"""
    global session
    num_of_translations = 1 if user_language_num == '0' else 5
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/80.0.3987.132 Safari/537.36"}
    for idx, link in enumerate(url, 1):
        request = session.get(link, headers=headers)
        soup = BeautifulSoup(request.content, 'lxml')
        # check_response(request)

        single_results = [x.get_text(strip=True) for x in soup.select("#translations-content > .translation")]
        # strip(), not get_text(strip=True) because it is a sentence, and it would delete some whitespaces in it
        quote_results = [x.text.strip() for x in soup.select("#examples-content > .example >  .ltr")]
        if user_language_num == '0':
            results_print_and_write(single_results, quote_results, AVAILABLE_LANGUAGES[str(idx)], user_word,
                                    num_of_translations)
        else:
            results_print_and_write(single_results, quote_results, AVAILABLE_LANGUAGES[user_language_num], user_word,
                                    num_of_translations)

def main():
    global session  # session for faster loading
    session = requests.Session()
    show_available_languages()
    user_language_from_num, user_language_to_num, user_word = take_input()
    url = make_url(language_from=user_language_from_num,
                   language_to=user_language_to_num,
                   word=user_word)
    make_translations(url, user_language_to_num, user_word)

if __name__ == '__main__':  # run as script
    main()
