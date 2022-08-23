from math import gcd
from random import randint


def coprime_check(a, b):
    """
    Checks for coprimity
    Returns True/False
    """
    return gcd(a, b) == 1


def xgcd(p, q):
    """
    Performs the extended Euclidean algorithm
    Returns the gcd, coefficient of a and coefficient of b
    """
    a, old_a = 0, 1
    b, old_b = 1, 0

    while q != 0:
        quotient = p // q
        p, q = q, p - quotient * q
        old_a, a = a, old_a - quotient * a
        old_b, b = b, old_b - quotient * b

    return old_a, old_b


def choose_open_exponent(totient):
    """
    Choosing random open exponent that coprime with totient
    Returns open exponent
    """
    while True:
        e = randint(2, totient)
        if coprime_check(e, totient):
            return e


def choose_keys(not_default_e=False):
    """
    Chooses two primes from list of 50mil primes, chooses E and D exponent
    (Default chooses e = 65537), writes public and private keys in files.
    """
    try:
        # Creating list of 50mil primes
        f = open('primes.txt', 'r')
    except FileNotFoundError:
        print('File primes.txt is not found')
        return
    else:
        primes = f.read().split(',')
        f.close()

        # Choosing two random big primes
        prime1 = int(primes[randint(40000000, 49999720)])
        prime2 = int(primes[randint(40000000, 49999720)])
        while prime1 == prime2:
            prime1 = int(primes[randint(40000000, 49999720)])
            prime2 = int(primes[randint(40000000, 49999720)])

        totient = (prime1 - 1) * (prime2 - 1)
        # n is secondary key
        n = prime1 * prime2

        # Choosing e
        if not not_default_e:
            e = 65537
        else:
            # You can just use 65537 as e, no difference, as it public
            # It does not give feedback on security
            e = choose_open_exponent(totient)

        # Choosing d exponent
        x, y = xgcd(e, totient)
        if x > 0:
            d = x
        else:
            d = x + totient

        # Writing keys in two separate files
        f_public = open('public_keys.txt', 'w')
        f_public.write(str(n) + '\n')
        f_public.write(str(e) + '\n')
        f_public.close()

        f_private = open('private_keys.txt', 'w')
        f_private.write(str(n) + '\n')
        f_private.write(str(d) + '\n')
        f_private.close()
        print('Keys have been written in public_keys.txt and private_keys.txt')
        return


def encrypt(message, public_key_file='public_keys.txt', to_save_in_file=False):
    """
    Turns string into cipher by ASCII code
    Returns cipher in int
    """
    try:
        # Opening keys
        f = open(public_key_file, 'r')
    except FileNotFoundError:
        print('File is not found')
    else:
        n = int(f.readline())
        e = int(f.readline())
        f.close()

        # Turn message in cipher - ASCII code in base, e exponent mod n
        # cipher = [pow(ord(char), e, n) for char in message]
        cipher_str = ', '.join(map(str, [pow(ord(char), e, n) for char in message]))

        if to_save_in_file:
            f = open('cipher.txt', 'w')
            f.write(cipher_str)
            f.close()

        return cipher_str


def decrypt(cipher, private_key_file='private_keys.txt', to_save_in_file=False):
    """
    Turns cipher into ASCII code (symbols)
    Returns string
    """
    try:
        # Turning string into list with int elements
        # list_cipher = list(cipher.split(", "))
        list_cipher = [int(el) for el in list(cipher.split(", "))]
    except ValueError:
        print("This is not a cipher")
        return

    try:
        # Opening keys
        f = open(private_key_file, 'r')
    except FileNotFoundError:
        print('File is not found')
        return
    n = int(f.readline())
    d = int(f.readline())
    f.close()

    # Decrypting cipher
    # ascii_list = [pow(unicode, d, n) for unicode in list_cipher]
    message = [chr(char) for char in [pow(unicode, d, n) for unicode in list_cipher]]

    if to_save_in_file:
        f = open('plaintext.txt', 'w')
        f.write(''.join(message))
        f.close()

    return ''.join(message)


def main():
    answer = input("""
Options: 
1. Generate new keys
2. Encrypt
3. Decrypt
(Type 1/2/3)
""")

    if answer == "1":
        answer = input('Default public exponent is 65537. If you do not want to change it - press enter\n')
        print('Generating new keys...')
        choose_keys() if answer == '' else choose_keys(True)
        main()

    elif answer == "2":
        print('If the keys file have original name - press enter')
        public_key_file = input('Type the name of the key file: ')

        answer_input = ''
        message = ''
        while answer_input != "type" and answer_input != "file":
            answer_input = input("Do you want type your message or input file? (type/file)\n")
            if answer_input == "type":
                message = input('Input your message to be encrypted: ')
            elif answer_input == "file":
                address = input('Input address of the file: ')
                f = open(address, 'r')
                message = f.read()
                f.close()

        answer_output = ''
        while answer_output != "y" and answer_output != "n":
            answer_output = input("Save in file? (y/n)\n")
            if public_key_file == '' and answer_output == 'y':
                print(encrypt(message, to_save_in_file=True))
            elif public_key_file != '' and answer_output == 'y':
                print(encrypt(message, public_key_file, True))
            elif public_key_file == '' and answer_output == 'n':
                print(encrypt(message))
            elif public_key_file != '' and answer_output == 'n':
                print(encrypt(message, public_key_file))
        main()

    elif answer == "3":
        print('If the keys file have original name - press enter')
        private_key_file = input('Type the name of the key file: ')

        message = ''
        answer_input = ''
        while answer_input != "type" and answer_input != "file":
            answer_input = input("Do you want type your message or input file? (type/file)\n")
            if answer_input == "type":
                message = input('Input your message to be decrypted: ')
            elif answer_input == "file":
                address = input('Input address of the file: ')
                f = open(address, 'r')
                message = f.read()
                f.close()

        answer_output = ''
        while answer_output != "y" and answer_output != "n":
            answer_output = input("Save in file? (y/n)\n")
            if private_key_file == '' and answer_output == 'y':
                print(decrypt(message, to_save_in_file=True))
            elif private_key_file != '' and answer_output == 'y':
                print(decrypt(message, private_key_file, True))
            elif private_key_file == '' and answer_output == 'n':
                print(decrypt(message))
            elif private_key_file != '' and answer_output == 'n':
                print(decrypt(message, private_key_file))
        main()

    else:
        return


print('''
============================================================================================================
=================================== RSA Encryptor / Decrypter ==============================================
''')
main()
