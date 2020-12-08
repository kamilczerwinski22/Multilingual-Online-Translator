import requests
from bs4 import BeautifulSoup

def show_message():
    print('Type "en" if you want to translate from French into English, or "fr" if you want to translate from English into French:')



def main():
    show_message()
    user_input_language = input()
    print("Type the word you want to translate:")
    user_input_text = input()
    print(f'You chose "{user_input_language}" as the language to translate "{user_input_text}" to.')

    request = requests.get(make_url(user_input_language, user_input_text), headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(request.content, 'lxml')

    if request.ok:
        print('200 OK')
    else:
        print('Something went wrong')
        exit()

    single_results = [element.get_text(strip=True) for element in soup.select('.translation')]

    quote_results = []
    for div in soup.find_all("div", {'class': "example"}):
        span_tag = [a.get_text() for a in div.find_all("span", {'class': "text"})]
        for element in span_tag:
            quote_results.append(element.strip())

    print('Translations')
    print(single_results)
    print(quote_results)


def make_url(language_to: str, text: str) -> str:
    full_url = 'https://context.reverso.net/translation/'
    if language_to == 'fr':
        full_url += 'english-french/'
    else:
        full_url += 'french-english/'

    return full_url + text


if __name__ == '__main__':  # run as script
    main()
