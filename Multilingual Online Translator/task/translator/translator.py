import requests
from bs4 import BeautifulSoup


available_languages = {
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

def show_message():
    print("Hello, you're welcome to the translator. Translator supports: ")
    for idx, element in available_languages.items():
        print(f"{idx}. {element}")

def make_url(language_from: str, language_to: str, word: str) -> str:


    return f"https://context.reverso.net/translation/{available_languages[language_from].lower()}-" \
           f"{available_languages[language_to].lower()}" \
           f"/{word}"

def results_print(singles: list, sentences: list, language: str):
    print('\nContext examples:\n')
    print(f'{language} Translations::')

    # single words
    singles = singles[:5]  # only 5 words
    for word in singles:
        print(word)

    print(f'\n{language} Examples:')

    # sentences
    for i in range(len(singles)):
        print(sentences[i * 2])
        print(sentences[i * 2 + 1] + '\n')

def check_response(response):
    if response.ok:
        print('200 OK')
    else:
        print('Something went wrong')
        exit()

def take_input() -> tuple:
    print('Type the number of your language: ')
    user_language_from = input()
    print('Type the number of language you want to translate to: ')
    user_language_to = input()
    print('Type the word you want to translate:')
    user_word = input()
    return user_language_from, user_language_to, user_word


def main():
    show_message()
    user_language_from_num, user_language_to_num, user_word = take_input()

    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/80.0.3987.132 Safari/537.36"}
    url = make_url(language_from=user_language_from_num,
                   language_to=user_language_to_num,
                   word=user_word)

    request = requests.get(url, headers=headers)
    soup = BeautifulSoup(request.content, 'lxml')

    check_response(request)

    single_results = [x.get_text(strip=True) for x in soup.select("#translations-content > .translation")]

    # strip(), not get_text(strip=True) because it is a sentence, and it would delete some whitespaces in it
    quote_results = [x.text.strip() for x in soup.select("#examples-content > .example >  .ltr")]

    results_print(single_results, quote_results, available_languages[user_language_to_num])



if __name__ == '__main__':  # run as script
    main()
