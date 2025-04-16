#! /bin/python3
 
import string
 
alphabet = list(string.ascii_lowercase)
alphabet_es = alphabet[:]
alphabet_es.insert(alphabet.index('n')+1, 'ñ')
 
#dicc_es = [x.upper() for x in ['hola', 'todos', 'la', 'lo', 'si', 'de', 'no', 'mi', 'las', 'los', 'como', 'que']]
#dicc_en = [x.upper() for x in ['hello', 'a', 'an', 'the', 'i', 'then' 'that', 'problem']]
dicc_es = []
dicc_en = []

with open('./diccES.txt', 'r', encoding="utf-8") as f:
    for line in f:
        dicc_es.append(line[:-1].upper())

with open('./diccEN.txt', 'r') as f:
    for line in f:
        dicc_es.append(line[:-1].upper())

main_dicc = {
    'ES': {
        'alphabet': alphabet_es,
        'dicc': dicc_es
        },
    'EN': {
        'alphabet': alphabet,
        'dicc': dicc_en
        },
}
 
def options() -> None:

    '''
    Args:
        None

    Return:
        None
    '''

    option = input(">> Escoge una opción Crifrar(C)/Descifrar(D): ")

    if option.lower() not in ['c', 'd']:
        print('>> [!] Opción escogida incorrecta')
        options()

    return option.lower()
 
def cipher() -> None:

    '''
    Args:
        None

    Return:
        None
    '''

    language = input('\n>> Escoge un alfabeto Español(ES)/English(EN): ')

    if language.lower() in ['en','es']:
        if language.lower() == 'es':
            text = cipherText(alphabet_es)
        else:
            text = cipherText(alphabet)

        print(f'>> El texto cifrado es: {text}')

    else:
        print('>> [!] Opción escogida incorrecta')
        cipher()

    return None

def cipherText(list_alphabet: list) -> str:

    '''
    Args:
        list_alphabet: list - Alphabet list

    Return:
        cipher_text: Str - Text encripted
    '''

    text = input('>> Introduce el texto a cifrar: ')
    try:
        salt = int(input('>> Introduce el salto: '))
    except:
        print('>> [!] El salto debe ser un número')
        cipherText(list_alphabet)

    cipher_text = ''

    for index in range(len(text)):
        letter = text[index].lower()
        new_letter = letter
        if letter in list_alphabet:
            new_letter = list_alphabet[(list_alphabet.index(letter) + salt ) % len(list_alphabet)]

        cipher_text += new_letter.upper()

    return cipher_text
 
def decipher() -> None:

    '''
    Args:
        None

    Return:
        None
    '''

    saltAnswer = input('\n>> ¿Conoces el salto?(S/N): ').lower()
    salt = None

    if saltAnswer not in ['s', 'n']:
        print('>> [!] Opción escogida incorrecta')
        decipher()
    elif saltAnswer == 's':
        try:
            salt = int(input('>> Introduce el salto: '))
        except:
            print('>> [!] El salto debe ser un número')
            decipher()

    alphabetAnswer = input('>> ¿Conoces el alfabeto?(S/N): ').lower()
    list_alphabet = None
    language_code = None

    if alphabetAnswer not in ['s', 'n']:
        print('>> [!] Opción escogida incorrecta')
        decipher()
    elif alphabetAnswer == 's':
        language = input('>> Escoge un alfabeto Español(ES)/English(EN): ').lower()

        if language in ['en','es']:
            if language == 'es':
                list_alphabet = alphabet_es
            else:
                list_alphabet = alphabet
            language_code = language.upper()
        else:
            print('>> [!] Opción escogida incorrecta')
            decipher()

    decipherText(salt,list_alphabet,language_code)

    return None        
 
def decipherText(salt: int=None, list_alphabet: list=None, language_code: str = None) -> None:

    '''
    Args:
        salt: Int - Text salt
        list_alphabet: list - Alphabet list
        language_code: Str - Language code
    Return:
        None
    '''

    textRes = [] # (text, language, salt)
    text = input('>> Introduce el texto a descifrar: ')

    # Salt: No y Alph: No
    if salt is None and list_alphabet is None:
        for language_code in main_dicc.keys():
            list_alphabet_def = main_dicc[language_code]['alphabet']
            for saltI in range(len(list_alphabet_def)):
                cipher_text = ''
                for index in range(len(text)):
                    letter = text[index].lower()
                    new_letter = letter
                    if letter in list_alphabet_def:
                        new_letter = list_alphabet_def[(list_alphabet_def.index(letter) - saltI ) % len(list_alphabet_def)]
                    cipher_text += new_letter.upper()
                textRes.append((cipher_text, language_code, saltI))

    # Salt: No y Alph: Si
    if salt is None and list_alphabet is not None:
        for saltI in range(len(list_alphabet)):
            cipher_text = ''
            for index in range(len(text)):
                letter = text[index].lower()
                new_letter = letter
                if letter in list_alphabet:
                    new_letter = list_alphabet[(list_alphabet.index(letter) - saltI ) % len(list_alphabet)]
                cipher_text += new_letter.upper()
            textRes.append((cipher_text, language_code, saltI))

    # Salt: Si y Alph: No
    if salt is not None and list_alphabet is None:
        for language_code in main_dicc.keys():
            list_alphabet_def = main_dicc[language_code]['alphabet']
            cipher_text = ''
            for index in range(len(text)):
                letter = text[index].lower()
                new_letter = letter
                if letter in list_alphabet_def:
                    new_letter = list_alphabet_def[(list_alphabet_def.index(letter) - salt ) % len(list_alphabet_def)]
                cipher_text += new_letter.upper()
            textRes.append((cipher_text, language_code, salt))

    # Salt: Si y Alph: Si
    if salt is not None and list_alphabet is not None:
        cipher_text = ''

        for index in range(len(text)):
            letter = text[index].lower()
            new_letter = letter
            if letter in list_alphabet:
                new_letter = list_alphabet[(list_alphabet.index(letter) - salt ) % len(list_alphabet)]
            cipher_text += new_letter.upper()
        textRes.append((cipher_text, language_code, salt))

    printResults(textRes, text)
 
def printResults(textRes: list, orignalText: str) -> None:

    '''
    Args:
        textRes: list of tuples (text, language_code, salt) - Posible decipher text
        saveResults: Str - Original text

    Return:
        None
    '''

    countSolutions = 0
    posibleTexts = []

    if len(textRes) == 0:
        print('>> [!] No se han encontrado posibles descifrados')
        return None
    for textDec,language_code,saltTuple in textRes:
        language_code_aux = searchDicctionary(textDec, language_code)
        if language_code_aux != 'NOT FOUND':
            countSolutions += 1
            posibleTexts.append((textDec,language_code,saltTuple))

    posibleTexts.sort(key= lambda x: textAccuracy(x), reverse=True)
    print('\n[*] Los resultados con más coincidencias son:\n')
    for textDec,language_code,saltTuple in posibleTexts[:5]:
        print(65*'-')
        print(f'\n>> Posible texto descifrado({language_code}) - Salt: {saltTuple} - Coincidencias: {textAccuracy((textDec,language_code,saltTuple))}: {textDec}\n')
    print(65*'-')

    saveResults(orignalText, textRes, posibleTexts, countSolutions)

def textAccuracy(entry: tuple):

    text,language_code,salt = entry
    counter = {code: 0 for code in main_dicc.keys()}
    for word in text.split(' '):
        for language_code in main_dicc.keys():
            if word in main_dicc[language_code]['dicc']:
                counter[language_code] += 1

    return max(counter.values())
 
def saveResults(text: str, textRes: list, posibleTexts: list, countSolutions: int):

    file = './CesarSolution.log'
    with open(file,'w', encoding="utf-8") as f:
        f.write("'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''")
        f.write(f'\nTexto introducido: {text}\n')
        f.write("'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''")

        f.write("\n'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''")
        f.write(f'\nResultados principales:\n')
        f.write("'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''")
        f.write('\n------------------------------------------------')
        for textDec,language_code,saltTuple in posibleTexts:
            f.write(f'\n>> Posible texto descifrado({language_code}) - Salt: {saltTuple} - Coincidencias: {textAccuracy((textDec,language_code,saltTuple))}: {textDec}\n')
            f.write('------------------------------------------------')

        f.write(f'\nSoluciones encontradas: {countSolutions}')
        f.write('\n------------------------------------------------')

        f.write("\n'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''")
        f.write(f'\nResultados completos:\n')
        f.write("'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''")
        f.write('\n------------------------------------------------')

        for textDec,language_code,saltTuple in textRes:
            f.write(f'\n>> Posible texto descifrado({language_code}) - Salt: {saltTuple}: {textDec}\n')
            f.write('------------------------------------------------')

    print(f'\n>> Solución y resultados guardados en archivo {file}')
 
def searchDicctionary(text: str, language_code: str=None) -> str:

    '''
    Args:
        text: str - Text string

    Return:
        Language code: str
    '''

    counter = {code: 0 for code in main_dicc.keys()}
    for word in text.split(' '):
        for language_code in main_dicc.keys():
            if word in main_dicc[language_code]['dicc']:
                counter[language_code] += 1

    if all(value == 0 for value in counter.values()):
        return "NOT FOUND"
    else:
        return max(counter, key=counter.get)
 
if __name__ == '__main__':
 
    print('##############################################')
    print('############## CIFRADO CESAR #################')
    print('##############################################')
    print("\n>> Bienvenido al cifrado Cesar automático")
    print(f'>> Diccionarios disponibles: {list(main_dicc.keys())}\n')

    option = options()
    if option == 'c':
        cipher()
    if option == 'd':
        decipher()
 
