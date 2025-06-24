import random
import base64
from cryptography.fernet import Fernet

file_to_obfuscate = input("Give file path: ")
Number_wanted = True
while Number_wanted:
    try:
        passes = int(input("How many times do you want your file to be encrypted? "))
        Number_wanted = False
    except ValueError:
        print("Please enter a number.")
MAX_FILE_CONTENTS = 1169782
MAX_NUM_OF_FAKE_KEYS = 100
MIN_NUM_OF_FAKE_KEYS = 80
MIN_VARIABLE_LENGTH = 20
MAX_VARIABLE_LENGTH = 30


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

def generate_random_string():
    string_to_return = 'Q'
    for p in range(1, random.randint(MIN_VARIABLE_LENGTH,MAX_VARIABLE_LENGTH)):
        string_to_return += letters[random.randint(0, len(letters)-1)]
    return string_to_return

def generate_random_key():
    key_letters = letters + ["-", "="]
    string_to_return = ''
    for q in range(1, 44): #because key size is 44 chars
        string_to_return += key_letters[random.randint(0, len(key_letters)-1)]
    return string_to_return

#begin obfuscation recursively
for i in range(1, passes+1):
    #generate random variable names
    function_name = generate_random_string()
    parameter_name_1 = generate_random_string()
    parameter_name_2 = generate_random_string()
    return_variable_name = generate_random_string()
    character_variable_name = generate_random_string()
    index_of_char_variable = generate_random_string()
    random_base64_contents = generate_random_string()
    cipher_text_variable = generate_random_string()
    decryption_key_variable = generate_random_string()
    list_of_keys_random_name = generate_random_string()
    keys_in_list_random_name = generate_random_string()

    #generate fake key variable names
    list_of_keys = []
    for x in range(1, random.randint(MIN_NUM_OF_FAKE_KEYS,MAX_NUM_OF_FAKE_KEYS)):
        list_of_keys.append(generate_random_string())

    #add actual key to list of fakes and shuffle
    list_of_keys.append(decryption_key_variable)
    random.shuffle(list_of_keys)

    #introduce deobfuscation functions
    def generate_decrypt_2():
        return f'''def {function_name}({parameter_name_1}, {parameter_name_2}):
    try:
        {return_variable_name} = Fernet({parameter_name_1}.encode('utf-8'))
        return {return_variable_name}.decrypt({parameter_name_2}.encode('utf-8')).decode('utf-8')
    except:
        pass
'''
    def generate_caesar_function():
        return f'''def {function_name}({parameter_name_1}, {parameter_name_2}):
    try:
        {return_variable_name} = ""
        for {character_variable_name} in {parameter_name_2}:
            {index_of_char_variable} = ord({character_variable_name})
            {return_variable_name} += chr(({index_of_char_variable} - {parameter_name_1}) % 256)
        return {return_variable_name}
    except:
        pass
'''
    
    #read contents of target file
    try:
        with open(file_to_obfuscate, "r", encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print("File not found!")
        exit()
    if len(content) >= MAX_FILE_CONTENTS:
        print("File too big, terminating!")
        exit()

    #choose encryption function at random
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

    #genarate dud keys, assign variable, and format
    string_to_declare_keys = ''
    for key_in_list in list_of_keys:
        if key_in_list != decryption_key_variable:
            if method == "encryption":
                random_key = generate_random_key()
                string_to_declare_keys += f'{key_in_list} = {function_name}("{random_key}", {cipher_text_variable})\n'
            else:
                random_key = random.randint(1, 255)
                while random_key == rand_key:
                    random_key = random.randint(1, 255)
                string_to_declare_keys += f'{key_in_list} = {function_name}({random_key}, {cipher_text_variable})\n'
        else:
            string_to_declare_keys += f'{key_in_list} = {function_name}({rand_key}, {cipher_text_variable})\n'
            
    #format final output string
    obfuscated_code = f'''import base64
from cryptography.fernet import Fernet
{random_base64_contents} = "{base64_content}"

{func_to_use}

{cipher_text_variable} = base64.b64decode({random_base64_contents}).decode("latin-1")
{string_to_declare_keys}
{list_of_keys_random_name} = {str(list_of_keys).replace("'", "")}
for {keys_in_list_random_name} in {list_of_keys_random_name}:
    try:
        exec({keys_in_list_random_name})
    except:
        pass
'''
    #write obfuscated code to file
    with open(file_to_obfuscate, "w", encoding='utf-8') as new_file:
        new_file.write(obfuscated_code)
    print(f"File obfuscated to: {file_to_obfuscate} on pass {i} using {method}.")
