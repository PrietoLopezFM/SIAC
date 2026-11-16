#To hash
from argon2 import PasswordHasher

def HashPassword(key):
    ph = PasswordHasher()
    res = ph.hash(key)
    print(res)

#Verify
def VerifyPassword(hash, key):
    ph = PasswordHasher()
    hash = ""#ph.hash("sup") #Password to fetch from the db
    try:
        ph.verify(hash, key)
        print("Password match!")
    except Exception:
        print("Incorrect password.")


HashPassword("john")
VerifyPassword("sup")