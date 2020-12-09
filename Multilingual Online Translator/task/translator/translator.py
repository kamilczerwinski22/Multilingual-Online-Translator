import requests
from bs4 import BeautifulSoup



def show_message():
    print('Type "en" if you want to translate from French into English, or "fr" if you want to translate from English into French:')

def make_url(language_to: str, word: str) -> str:
    language_dic = {'fr': 'english-french', 'en': 'french-english'}
    return f"https://context.reverso.net/translation/{language_dic[language_to]}/{word}"

def main():
    show_message()
    user_input_language = input()
    print("Type the word you want to translate:")
    user_input_text = input()
    print(f'You chose "{user_input_language}" as the language to translate "{user_input_text}" to.')

    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/80.0.3987.132 Safari/537.36"}
    url = make_url(user_input_language, user_input_text)
    request = requests.get(url, headers=headers)
    soup = BeautifulSoup(request.content, 'lxml')

    if request.ok:
        print('200 OK')
    else:
        print('Something went wrong')
        exit()



    single_results = [x.get_text(strip=True) for x in soup.select("#translations-content > .translation")]

    # strip(), not get_text(strip=True) because it is a sentence, and it would delete some whitespaces in it
    quote_results = [x.text.strip() for x in soup.select("#examples-content > .example >  .ltr")]

    print('Translations')
    print(single_results)
    print(quote_results)


if __name__ == '__main__':  # run as script
    main()
