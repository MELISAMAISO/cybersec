# BSCIT-05-0080/24
# Mokeira Maiso

import hashlib
import secrets
import re
import hmac
from getpass import getpass

# CLASS 1: User
# Represents classsystem user.
# Stores username, salt, hashed password and failed login attempts, and lock status.

class User:

    def __init__(self, username, salt, hashed_password):
        self.username = username
        self.salt = salt
        self.hashed_password = hashed_password
        self.failed_tries = 0
        self.is_locked = False

# CLASS 2: PasswordManager
# Handles password security operations such as Password validation,Salt generation and  PBKDF2 hashing

class PasswordManager:

    def generate_hash(self, password, salt=None): #this function generates a secure password hash using
        #PBKDF2 which has 120000 iterations that slow brute-force attacks.
        
        if salt is None:
            salt = secrets.token_bytes(16)#salt ensures identical passwords do not produce the same hash

        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode(),
            salt,
            120000
        )

        return salt, key

    def validate_password(self, password): #this function validates password strength.
       
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        return re.match(pattern, password)

# CLASS 3: AuthenticationSystem
# this class handles, Registration, Login, Access control and Account lock after 3 failed attempts

class AuthenticationSystem:

    def __init__(self):
        self.user_db = {}
        self.max_attempts = 3
        self.password_manager = PasswordManager()

    
    # ACCOUNT REGISTRATION
    def create_account(self):
        print("\n CREATE AN ACCOUNT")

        # USERNAME VALIDATION LOOP
        while True:
            username = input("Enter username: ").strip().lower()

            if not username:
                print("Username cannot be empty.")
            elif username in self.user_db:
                print("Username already exists.")
            else:
                break

        # PASSWORD VALIDATION LOOP
        while True:
            password = input("Enter password: ")

            if not self.password_manager.validate_password(password):
                print("Weak password. Use 8+ chars, upper, lower, digit, and symbol.")
            else:
                break

        # HASH PASSWORD BEFORE STORAGE
        salt, hashed_pw = self.password_manager.generate_hash(password)

        # STORE SECURELY (NO PLAIN TEXT)
        user = User(username, salt, hashed_pw)
        self.user_db[username] = user

        print(f"User '{username}' successfully registered.")

    # USER AUTHENTICATION
    def authenticate_user(self):
        print("\n LOGIN ")
        username = input("Enter your Username: ").strip().lower()

        if username not in self.user_db:
            print("Access Denied: User record not found.")
            return

        user = self.user_db[username]

        # CHECK IF ACCOUNT IS LOCKED
        if user.is_locked:
            print("This account is locked due to multiple failed attempts.")
            return

        # PASSWORD ATTEMPT LOOP
        while True:
            password = input("Password: ")#Account is locked after 3 failed attempts to prevent guessing.
            _, attempt_hash = self.password_manager.generate_hash(password, user.salt)

            if hmac.compare_digest(attempt_hash, user.hashed_password):
                print(f"Access Granted. (: Welcome back, {username}!")
                user.failed_tries = 0
                break
            else:
                user.failed_tries += 1
                remaining = self.max_attempts - user.failed_tries

                print(f"Invalid Password. {remaining} attempts left.")

                if user.failed_tries >= self.max_attempts:
                    user.is_locked = True
                    print("Account locked due to security policy.")
                    break

# APPLICATION ENTRY POINT

if __name__ == "__main__":
    system = AuthenticationSystem()

    while True:
        print("\n Welcome To Simple Authentication System")
        print("\n 1. Register")
        print("\n 2. Login")
        print("\n 3. Exit")

        cmd = input("Select Option: ")

        if cmd == '1':
            system.create_account()
        elif cmd == '2':
            system.authenticate_user()
        elif cmd == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid Choice.")
