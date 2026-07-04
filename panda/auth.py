"""
Authentication for PandaVault access.

Passwords are stored as SHA-256 hexdigests, never in plaintext.
"""
import hashlib


def password():
    f = open('password.txt', 'w+')
    passw = input('P.A.N.D.A : Enter the password - ')
    f.write(hashlib.sha256(passw.encode()).hexdigest())
    print("P.A.N.D.A : Password created.", end=' ')
    print("Make sure you remember it. ")
    f.close()
    return


def _hash(raw_password):
    return hashlib.sha256(raw_password.encode()).hexdigest()


def check_password(typed_password):
    """
    Compares a freshly typed password against the stored hash.
    Returns True/False. Raises FileNotFoundError if no password has
    been set yet (caller should catch this and prompt password()).
    """
    with open('password.txt', 'r') as f:
        stored_hash = f.read()
    return stored_hash == _hash(typed_password)
