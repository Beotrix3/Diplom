from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

# Генерация ключа (для примера, его нужно хранить и использовать снова)
#key = os.urandom(32)  # AES-256
#key = b'$\x89\r\xde<\x8b\xdd\xa2\x12r\x99\xc0\nsUy'
key = b'\xd6\x18L\x16K\xe8\xd8\xcd\xcf\x06nL\x10\x83y(A\xc5[_*\xb0\xd2!y\xd6&\x0b\xca\xedAs'
print(f"Key (before encryption): {key.hex()}")
print(f"Key (before encryption): {key}")

# Шифрование ключа
def encrypt_data(data):
    cipher = AES.new(key, AES.MODE_CBC)  # Используем key для шифрования данных
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    iv = cipher.iv
    return iv + ct_bytes  # Возвратите IV вместе с зашифрованным сообщением

# Расшифровка ключа
def decrypt_data(encrypted_data):
    iv = encrypted_data[:16]  # Первый 16 байт - это IV
    ct = encrypted_data[16:]   # Остальные байты - это зашифрованное сообщение
    cipher = AES.new(key, AES.MODE_CBC, iv)  # Создание шифра с тем же ключом и IV
    decrypted = unpad(cipher.decrypt(ct), AES.block_size)  # Расшифровка и удаление отступов
    return decrypted  # Возвращаем байты

# Пример шифрования и расшифровки
#key_to_encrypt = b'$\x89\r\xde<\x8b\xdd\xa2\x12r\x99\xc0\nsUy'  # Изначальный ключ для шифрования
key_to_encrypt = b'\xd6\x18L\x16K\xe8\xd8\xcd\xcf\x06nL\x10\x83y(A\xc5[_*\xb0\xd2!y\xd6&\x0b\xca\xedAs'
print(f"Key to encrypt: {key_to_encrypt.hex()}")

# Зашифруем ключ
encrypted_key = encrypt_data(key_to_encrypt)
print(f"Encrypted Key (hex): {encrypted_key.hex()}")

# Теперь расшифруем ключ
decrypted_key = decrypt_data(encrypted_key)
print(f"Decrypted Key: {decrypted_key}")  # Это будет строка байт
print(f"Decrypted Key (hex): {decrypted_key.hex()}")

# Проверка: подтвердим, что расшифрованный ключ совпадает с исходным
print(f"Is decrypted key same as original: {decrypted_key == key_to_encrypt}")

# Пример шифрования строки
string_to_encrypt = 'vkru egkp rloz xpow'
encrypted_string = encrypt_data(string_to_encrypt.encode())  # Преобразуем строку в байты
print(f"Encrypted String (hex): {encrypted_string.hex()}")