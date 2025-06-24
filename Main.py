import random
import base64
from cryptography.fernet import Fernet
from copy import deepcopy

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
    temp_5 = 'Q'
    for x in range(0, 20):
        temp_5 += letters[random.randint(0, 61)]
    temp_6 = 'Q'
    for x in range(0, 20):
        temp_6 += letters[random.randint(0, 61)]
    temp_7 = 'Q'
    for x in range(0, 20):
        temp_7 += letters[random.randint(0, 61)]
    temp_8 = 'Q'
    for x in range(0, 20):
        temp_8 += letters[random.randint(0, 61)]
    temp_9 = 'Q'
    for x in range(0, 20):
        temp_9 += letters[random.randint(0, 61)]
    temp_list = []
    for x in range(0, 100):
        temp_10 = 'Q'
        for y in range(0, 20):
            temp_10 += letters[random.randint(0, 61)]
        temp_list.append(temp_10)
    list_of_vars = deepcopy(temp_list)
    temp_list.append(temp_9)
    random.shuffle(temp_list)
    temp_11 = ''


    def generate_decrypt_2():
        return f'''def {temp}({temp_2}, {temp_3}):
    try:
        {temp_4} = Fernet({temp_2}.encode('utf-8'))
        return {temp_4}.decrypt({temp_3}.encode('utf-8')).decode('utf-8')
    except:
        pass
'''


    def generate_caesar_function():
        return f'''def {temp}({temp_2}, {temp_3}):
    try:
        {temp_4} = ""
        for {temp_5} in {temp_3}:
            {temp_6} = ord({temp_5})
            {temp_4} += chr(({temp_6} - {temp_2}) % 256)
        return {temp_4}
    except:
        pass
'''

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
        base64_content = base64.b64encode(encrypted_content.encode("latin-1")).decode("ascii")
        func_to_use = generate_caesar_function()
    else:
        method = "encryption"
        rand_key, encrypted_content = encrypt_2(content)
        base64_content = base64.b64encode(encrypted_content.encode("latin-1")).decode("ascii")
        func_to_use = generate_decrypt_2()

    for x in temp_list:
        if x != temp_9:
            if random.randint(1,2) == 1:
                temp_12 = 'Q'
                for y in range(0, 43):
                    temp_12 += letters[random.randint(0, 61)]
                temp_11 += f'{x} = {temp}("{temp_12}", {temp_8})\n'
            else:
                temp_12 = random.randint(1, 255)
                temp_11 += f'{x} = {temp}({temp_12}, {temp_8})\n'
        else:
            temp_11 += f'{temp_9} = {temp}({rand_key}, {temp_8})\n'
    obfuscated_code = f'''import base64
from cryptography.fernet import Fernet
{temp_7} = "{base64_content}"

{func_to_use}

{temp_8} = base64.b64decode({temp_7}).decode("latin-1")
{temp_11}
rand_list = {str(temp_list).replace("'", "")}
for i in rand_list:
    try:
        exec(i)
    except:
        pass
'''
    with open(file_to_obfuscate, "w", encoding='utf-8') as new_file:
        new_file.write(obfuscated_code)
    print(f"File obfuscated to: {file_to_obfuscate} on pass {i} using {method}.")
