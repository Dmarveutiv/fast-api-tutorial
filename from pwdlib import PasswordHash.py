from pwdlib import PasswordHash


def hash(password : str):
    password_hash = PasswordHash.recommended()
    user_password = password_hash.hash(password)
    return user_password

def verify(plain_password : str, hashed_password : str):
    password_hash = PasswordHash.recommended()
    user_password = password_hash.hash(plain_password)
    
    if user_password == hashed_password:
        return hashed_password
    else:
        return f'Wrong Password'
    

# p = verify('111', 
# '$argon2id$v=19$m=65536,t=3,p=4$JUYuSsFYtxJMeW1YFPRq8g$xJ23kpXv9TTkHWzQr7J4DzehObTzg0I5ENErXiAzU5k')
# print(p)

a = hash('111')
print(a)