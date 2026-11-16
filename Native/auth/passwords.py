from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError

_password_hasher = PasswordHasher()

def hash_password(password):
    #Return an Argon2 hash to store in the database.
    return _password_hasher.hash(password)


def verify_password(stored_hash, password):
    #Return whether the password matches the stored hash.
    try:
        return _password_hasher.verify(stored_hash, password)
    except (VerifyMismatchError, InvalidHashError):
        return False


# Test 1
stored_hash = hash_password("john")  # Save this hash in the database.
matches = verify_password(stored_hash, "john")

print(matches)  # True

# Test 2