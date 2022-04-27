import os
from cryptography.fernet import Fernet


class CryptographyToken:
    FILE_NAME="key_file.txt"
    def __init__(self) -> None:
        self.key = self.__get_key__()

    def __get_key__(self):
        if not os.path.exists(CryptographyToken.FILE_NAME):
            private_key = Fernet.generate_key()
            with open("key_file.txt", "w") as key_file_w:
                key_file_w.write(str(private_key, encoding="utf-8"))
        else:
            with open("key_file.txt", "r") as key_file:
                private_key = key_file.read()
        return private_key

    def encrypt_token(self, token_raw : str):
        f = Fernet(self.key)
        token = f.encrypt(bytes(token_raw, encoding="utf-8"))
        return str(token, encoding="utf-8")
    
    def decrypt_token(self, token_encrypt : str):
        f = Fernet(self.key)
        token = f.decrypt(bytes(token_encrypt, encoding="utf-8"))
        return str(token, encoding="utf-8")
    

    # def decrypt_token(token):
    #     key = Fernet.generate_key()
    #     f = Fernet(key)
    #     return  f.decrypt(token)
