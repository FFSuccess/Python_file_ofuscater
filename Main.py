import random
import base64
from cryptography.fernet import Fernet

file_to_obfuscate = input("Give file path: ")
passes = int(input("How many times do you want your file to be encrypted? "))


letters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E',
           'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
    'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e',
           'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


def encrypt_caesar(key, message):
    return_message = ""
    for char in message:
        ascii_val = ord(char)
        shifted = (ascii_val + key) % 256
        return_message += chr(shifted)
    return return_message

def encrypt_2(message):
    key = Fernet.generate_key()
    f = Fernet(key)
    encrypted = f.encrypt(message.encode('utf-8'))
    return f"\"{key.decode('utf-8')}\"", encrypted.decode('utf-8')


for i in range(1, passes+1):
    temp = 'Q'
    for x in range(0, 20):
        temp += letters[random.randint(0, 61)]
    temp_2 = 'Q'
    for x in range(0, 20):
        temp_2 += letters[random.randint(0, 61)]
    temp_3 = 'Q'
    for x in range(0, 20):
        temp_3 += letters[random.randint(0, 61)]
    temp_4 = 'Q'
    for x in range(0, 20):
        temp_4 += letters[random.randint(0, 61)]
    def generate_decrypt_2():
        return f'''def {temp}({temp_2}, {temp_3}):
        {temp_4} = Fernet({temp_2}.encode('utf-8'))
        return {temp_4}.decrypt({temp_3}.encode('utf-8')).decode('utf-8')'''


    def generate_caesar_function():
        return f'''def {temp}({temp_2}, {temp_3}):
        {temp_4} = ""
        for char in {temp_3}:
            ascii_val = ord(char)
            shifted = (ascii_val - {temp_2}) % 256
            {temp_4} += chr(shifted)
        return {temp_4}'''

    try:
        with open(file_to_obfuscate, "r", encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print("File not found!")
        exit()
    if len(content) >= 8869782:
        print("File too big, terminating!")
        exit()
    if random.randint(1,2) == 2:
        method = "ceaser"
        rand_key = random.randint(1, 255)
        encrypted_content = encrypt_caesar(rand_key, content)
        base64_content = base64.b64encode(encrypted_content.encode('latin-1')).decode('ascii')
        func_to_use = generate_caesar_function()
    else:
        method = "encryption"
        rand_key, encrypted_content = encrypt_2(content)
        base64_content = base64.b64encode(encrypted_content.encode('latin-1')).decode('ascii')
        func_to_use = generate_decrypt_2()
    obfuscated_code = f'''import base64
from cryptography.fernet import Fernet
encrypted_data = "{base64_content}"
key = {rand_key}

{func_to_use}

decoded = base64.b64decode(encrypted_data).decode('latin-1')
original_code = {temp}(key, decoded)
exec(original_code)'''
    with open(file_to_obfuscate, "w", encoding='utf-8') as new_file:
        new_file.write(obfuscated_code)
    print(f"File obfuscated to: {file_to_obfuscate} on pass {i} using {method}.")
