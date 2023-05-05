import pandas as pd
import numpy as np
import random
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, kdf
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import concurrent.futures
#needs 5mins to finish
#Richest dataset
df = pd.read_csv("500 richest people 2021.csv",sep=";")
df = df.drop(df.columns[7:11],axis=1)
df = df.drop(index= df.iloc[499:503].index.tolist())

def generate_ids(num):
    #generate unique ids without replacement
    ids = random.sample(range(100000, 999999), num)
    return ids
# Write the updated DataFrame back to a CSV file
ids = generate_ids(499)
df["id"] = ids
df = df[df.columns[[-1,0,1,2,3,4,5,6]]]
df.to_csv("500 richest people 2021 with IDs.csv", index=False)


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
    encrypted_data = f.encrypt(str(id).encode())
    return encrypted_data.decode()

# Define a function to decrypt data
def decrypt_id(id):
    f = Fernet(encryption_key)
    decrypted_data = f.decrypt(id.encode())
    return int(decrypted_data.decode())

# Define a function to encrypt data
def encrypt_name(id, name):
    salt = str(id).encode()
    kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(secret_key))
    f = Fernet(key)
    encrypted_data = f.encrypt(name.encode())
    return encrypted_data.decode()

# Define a function to decrypt data
def decrypt_name(id, name):
    salt = str(id).encode()
    kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(secret_key))
    f = Fernet(key)
    decrypted_data = f.decrypt(name.encode())
    return decrypted_data.decode()

print("Encrypting...")

# for i, row in df.iterrows():
#     salt = str(row[0]).encode()
#     kdf = PBKDF2HMAC(
#         algorithm=hashes.SHA256(),
#         length=32,
#         salt=salt,
#         iterations=100000,
#     )
#     key = base64.urlsafe_b64encode(kdf.derive(secret_key))
#     row[2] = encrypt_name(key,row[2])
#     row[0] = encrypt_id(row[0])
#     df.iloc[i] = row
def encrypt_row(row):
    new_row = list(row[:])
    new_row[2] = encrypt_name(row[0], row[2])
    new_row[0] = encrypt_id(row[0])
    return new_row

# df[2] = df.apply(lambda row: encrypt_name(row[0], row[2]), axis=1)
# df[0] = df[0].apply(encrypt_id)
# parralelize
with concurrent.futures.ThreadPoolExecutor() as executor: #iterate with multiple threads
    results = list(executor.map(encrypt_row, df.itertuples(index=False)))

df = pd.DataFrame(results, columns=df.columns)
df.to_csv("500 richest people 2021 encrypted2.csv", index=False)

print("Decrypting...")

# for i, row in df.iterrows():
#     row[0] = decrypt_id(row[0])
#     salt = str(row[0]).encode()
#     kdf = PBKDF2HMAC(
#         algorithm=hashes.SHA256(),
#         length=32,
#         salt=salt,
#         iterations=100000,
#     )
#     key = base64.urlsafe_b64encode(kdf.derive(secret_key))
#     row[2] = decrypt_name(key,row[2])
#     df.iloc[i] = row

# df[0] = df[0].apply(decrypt_id)
# df[2] = df.apply(lambda row: decrypt_name(row[0], row[2]), axis=1)
def decrypt_row(row):
    new_row = list(row[:])
    new_row[0] = decrypt_id(row[0])
    new_row[2] = decrypt_name(new_row[0], row[2])
    return new_row
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = list(executor.map(decrypt_row, df.itertuples(index=False)))
df = pd.DataFrame(results, columns=df.columns)

df.to_csv("500 richest people 2021 decrypted2.csv", index=False)
