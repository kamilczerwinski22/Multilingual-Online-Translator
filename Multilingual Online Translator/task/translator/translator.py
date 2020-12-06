def show_message():
    print('Type "en" if you want to translate from French into English, or "fr" if you want to translate from English into French:')



def main():
    show_message()
    user_input_language = input()
    print("Type the word you want to translate:")
    user_input_text = input()
    print(f'You chose "{user_input_language}" as the language to translate "{user_input_text}" to.')

if __name__ == '__main__':  # run as script
    main()
