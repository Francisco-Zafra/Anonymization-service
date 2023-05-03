import pandas as pd
import numpy as np
import random
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, kdf
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
#needs 5mins to finish
#age dataset
df = pd.read_csv("AgeDataset-V3.csv",sep=",")
df = df.drop(df.columns[0], axis=1)
# Define the secret key
secret_key = b'souyana_amar'

salt = b'global' # This should be a unique value for each encryption operation
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
)
encryption_key = base64.urlsafe_b64encode(kdf.derive(secret_key))


# Define a function to encrypt data
def encrypt_id(id):
    f = Fernet(encryption_key)
    encrypted_data = f.encrypt(id.encode())
    return encrypted_data.decode()

# Define a function to decrypt data
def decrypt_id(id):
    f = Fernet(encryption_key)
    decrypted_data = f.decrypt(id.encode())
    return decrypted_data.decode()

# Define a function to encrypt data
def encrypt_name(key, name):
    f = Fernet(key)
    encrypted_data = f.encrypt(name.encode())
    return encrypted_data.decode()

# Define a function to decrypt data
def decrypt_name(key, name):
    f = Fernet(key)
    decrypted_data = f.decrypt(name.encode())
    return decrypted_data.decode()

print("Encrypting...")

for i, row in df.iterrows():
    salt = row[0].encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(secret_key))
    row[1] = encrypt_name(key,row[1])
    row[0] = encrypt_id(row[0])
    df.iloc[i] = row

df.to_csv("AgeDataset-V3-encrypted.csv", index=False)

print("Decrypting...")

for i, row in df.iterrows():
    row[0] = decrypt_id(row[0])
    salt = row[0].encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(secret_key))
    row[1] = decrypt_name(key,row[1])
    df.iloc[i] = row

df.to_csv("AgeDataset-V3-decrypted.csv", index=False)
