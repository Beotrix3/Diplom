from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
from flask_mysqldb import MySQL

# Генерация пары ключей RSA и сохранение их в файлы
def generate_and_save_rsa_keys(private_key_file, public_key_file):
    key = RSA.generate(2048)  # Генерация ключа длиной 2048 бит
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    with open(private_key_file, 'wb') as f:
        f.write(private_key)
    
    with open(public_key_file, 'wb') as f:
        f.write(public_key)

# Чтение ключей RSA из файлов
def read_rsa_keys(private_key_file, public_key_file):
    with open(private_key_file, 'rb') as f:
        private_key = f.read()
    
    with open(public_key_file, 'rb') as f:
        public_key = f.read()
    
    return private_key, public_key

# Шифрование симметричного ключа AES
def encrypt_aes_key(aes_key, public_key):
    rsa_public_key = RSA.import_key(public_key)
    cipher_rsa = PKCS1_OAEP.new(rsa_public_key)
    encrypted_key = cipher_rsa.encrypt(aes_key)
    return encrypted_key

def decrypt_aes_key(encrypted_aes_key, private_key):
    rsa_private_key = RSA.import_key(private_key)
    cipher_rsa = PKCS1_OAEP.new(rsa_private_key)
    decrypted_key = cipher_rsa.decrypt(encrypted_aes_key)
    return decrypted_key

# Основной код
if __name__ == '__main__':
    # Генерация ключей RSA и сохранение их в файлы
    private_key_file = "private_key.pem"
    public_key_file = "public_key.pem"
    #generate_and_save_rsa_keys(private_key_file, public_key_file)

    # Чтение ключей RSA из файлов
    private_key, public_key = read_rsa_keys(private_key_file, public_key_file)

    # Генерация симметричного ключа AES
    #aes_key = get_random_bytes(32)  # Пример 256-битного ключа для AES
    aes_key = b'\xd6\x18L\x16K\xe8\xd8\xcd\xcf\x06nL\x10\x83y(A\xc5[_*\xb0\xd2!y\xd6&\x0b\xca\xedAs'

    # Шифрование ключа AES
    encrypted_aes_key = encrypt_aes_key(aes_key, public_key)

    # Сохранение зашифрованного AES ключа в файл
    with open("encrypted_aes_key.bin", 'wb') as f:
        f.write(encrypted_aes_key)

    # Закрытый ключ сохранён в переменной private_key
    # Чтение зашифрованного AES ключа из файла
    with open("encrypted_aes_key.bin", 'rb') as f:
        encrypted_aes_key = f.read()

    # Расшифровка ключа AES
    print(encrypted_aes_key)
    decrypted_aes_key = decrypt_aes_key(encrypted_aes_key, private_key)
    print(f"Decrypted AES Key: {decrypted_aes_key}")
    
    print("***")
    print("Key:", aes_key.hex())
    print("Enc:", encrypted_aes_key.hex())
    print("Dec:", decrypted_aes_key.hex())