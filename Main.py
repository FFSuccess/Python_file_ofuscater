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

def generate_random_string():
    string_to_return = 'Q'
    for x in range(0, random.randint(20,30)):
        string_to_return += letters[random.randint(0, 61)]
    return string_to_return

def generate_random_key():
    key_letters = letters + ["-", "="]
    string_to_return = ''
    for x in range(0, 43):
        string_to_return += key_letters[random.randint(0, 63)]
    return string_to_return

#begin offuscating recursively
for i in range(1, passes+1):
    #generate random variable names
    function_name = generate_random_string()
    parameter_name_1 = generate_random_string()
    parameter_name_2 = generate_random_string()
    return_variable_name = generate_random_string()
    charecter_variable_name = generate_random_string()
    index_of_char_variable = generate_random_string()
    random_base64_contence = generate_random_string()
    cipher_text_variable = generate_random_string()
    decryption_key_variable = generate_random_string()
    temp_list = []
    for x in range(0, 100):
        temp_list.append(generate_random_string())

    #hide key in list
    temp_list.append(decryption_key_variable)
    random.shuffle(temp_list)
    temp_11 = ''

    #introduce deoffuscation functions
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
        for {charecter_variable_name} in {parameter_name_2}:
            {index_of_char_variable} = ord({charecter_variable_name})
            {return_variable_name} += chr(({index_of_char_variable} - {parameter_name_1}) % 256)
        return {return_variable_name}
    except:
        pass
'''
    
    #read contence of target file
    try:
        with open(file_to_obfuscate, "r", encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print("File not found!")
        exit()
    if len(content) >= 1169782:
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

    #genarate dud keys
    for x in temp_list:
        if x != decryption_key_variable:
            if method == "encryption":
                temp_12 = generate_random_key()
                temp_11 += f'{x} = {function_name}("{temp_12}", {cipher_text_variable})\n'
            else:
                temp_12 = random.randint(1, 255)
                while temp_12 == rand_key:
                    temp_12 = random.randint(1, 255)
                temp_11 += f'{x} = {function_name}({temp_12}, {cipher_text_variable})\n'
        else:
            temp_11 += f'{decryption_key_variable} = {function_name}({rand_key}, {cipher_text_variable})\n'
            
    #determine final output string
    obfuscated_code = f'''import base64
from cryptography.fernet import Fernet
{random_base64_contence} = "{base64_content}"

{func_to_use}

{cipher_text_variable} = base64.b64decode({random_base64_contence}).decode("latin-1")
{temp_11}
rand_list = {str(temp_list).replace("'", "")}
for i in rand_list:
    try:
        exec(i)
    except:
        pass
'''
    #write to file
    with open(file_to_obfuscate, "w", encoding='utf-8') as new_file:
        new_file.write(obfuscated_code)
    print(f"File obfuscated to: {file_to_obfuscate} on pass {i} using {method}.")
