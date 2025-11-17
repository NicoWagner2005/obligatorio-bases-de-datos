import bcrypt

def hash_password(password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(14)).decode()
    return hashed

