from cryptography.fernet import Fernet
import getpass

ENCRYPT_KEY = 'jYh6qnrTZYVvGWGjbpZuaXEux6wsoMWlTN_UZeL1H3A='
PASSWORD = 'hbAYwDm22A6RU0Xj'

class PasswordAuth():
    """ prompt for inputing password to authenticate the encryption """
    def auth(self):
        password = getpass.getpass()
        if password != PASSWORD:
            print("The password is incorrect. Exit.")
            exit(0)

class Crypt():
    """ encrypt or decrypt a given string """
    def __init__(self):
        self.crypt = Fernet(ENCRYPT_KEY)

    def encrypt(self, plain_text: str) -> str:
        cipher = self.crypt.encrypt(str(plain_text).encode())
        return cipher.decode()

    def decrypt(self, cipher: str) -> str:
        plain_text = self.crypt.decrypt(cipher.encode())
        return plain_text.decode()    
    
class FileEncryptor():
    """ encrypt or decrypt a given file """
    def __init__(self, file=None, auth=True):
        self.file = file
        self.password = PASSWORD
        self.crypt = Fernet(ENCRYPT_KEY)
        self.auth = auth
    
    def encrypt(self, file=None):
        """ encrypt the given file and generate an output [file].e """
        if file != None:
            self.file = file 
        # read the file
        with open(self.file, "rb") as f:
            file_data = f.read()
        print(f"Encrypt the given file [{self.file}] ...")
        
        # encrypt the file content
        if self.auth:
            PasswordAuth().auth()
        cipher = self.crypt.encrypt(file_data)
        
        # output the encrypted file
        with open(self.file+'.e', "wb") as f:
            f.write(cipher)
        print(f"Generate the encrypted file [{self.file+'.e'}]")
    
    def decrypt(self, file=None):
        """ decrypt a given file and return the decrypt result """
        if file == None:
            file = self.file + '.e'
        # read the encrypted data
        with open(file, "rb") as file:
            cipher = file.read()
        # decrypt
        plain_text = self.crypt.decrypt(cipher)
        
        return plain_text

