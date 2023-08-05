from cryptography.fernet import Fernet

def write_key(path):
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open(path, "wb") as key_file:
        key_file.write(key)

def load_key(path):
    """
    Loads the key from the current directory named `key.key`
    """
    
    return open(path, "rb").read()

def encrypt(filename, 
            key, 
            nametow = None):
    """
    Given a filename (str) and key (bytes), it encrypts the file and write it
    """
    f = Fernet(key)
    encrypted_data = f.encrypt(nametow)
    # write the encrypted file
    with open(filename, "wb") as file:
        file.write(encrypted_data)

def decrypt(filename,key):
    """
    Given a filename (str) and key (bytes), it decrypts the file and write it
    """
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()
    # decrypt data
    decrypted_data = f.decrypt(encrypted_data)
    return decrypted_data.decode("utf-8")
