import random
import base64

file_to_obfuscate = input("Give file path: ")
passes = int(input("How many times do you want your file to be encrypted? "))+1

def generate_decrypt_function():
    return '''def decrypt_caesar(key, message):
    return_message = ""
    for char in message:
        ascii_val = ord(char)
        shifted = (ascii_val - key) % 256
        return_message += chr(shifted)
    return return_message'''

for i in range(0,passes):
    def encrypt_caesar(key, message):
        return_message = ""
        for char in message:
            ascii_val = ord(char)
            shifted = (ascii_val + key) % 256
            return_message += chr(shifted)
        return return_message

    try:
        with open(file_to_obfuscate, "r", encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print("File not found!")
        exit()
    rand_key = random.randint(1, 255)
    encrypted_content = encrypt_caesar(rand_key, content)
    base64_content = base64.b64encode(encrypted_content.encode('latin-1')).decode('ascii')
    obfuscated_code = f'''import base64
encrypted_data = "{base64_content}"
key = {rand_key}
    
{generate_decrypt_function()}
    
decoded = base64.b64decode(encrypted_data).decode('latin-1')
original_code = decrypt_caesar(key, decoded)
exec(original_code)'''
    with open(file_to_obfuscate, "w", encoding='utf-8') as new_file:
        new_file.write(obfuscated_code)
    print(f"File obfuscated to: {file_to_obfuscate} on pass {i}.")
