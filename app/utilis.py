from pwdlib import PasswordHash

def hash(password : str):
    password_hash = PasswordHash.recommended()
    user_password = password_hash.hash(password)
    return user_password
