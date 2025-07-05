import re
from utils import load_data, save_data

class User:
    users_file = "users.json"

    def __init__(self, first_name, last_name, email, password, mobile):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.mobile = mobile

    @staticmethod
    def is_valid_email(email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email)

    @staticmethod
    def is_valid_egyptian_mobile(mobile):
        pattern = r'^(010|011|012|015)\d{8}$'
        return re.match(pattern, mobile)

    @classmethod
    def register(cls):
        print("\n=== User Registration ===")
        first_name = input("First name: ")
        last_name = input("Last name: ")
        email = input("Email: ")

        if not cls.is_valid_email(email):
            print("Invalid email format.")
            return None

        users = load_data(cls.users_file)
        for user in users:
            if user["email"] == email:
                print("Email already registered.")
                return None

        password = input("Password: ")
        confirm_password = input("Confirm password: ")
        if password != confirm_password:
            print("Passwords do not match.")
            return None

        mobile = input("Mobile phone (Egypt only): ")
        if not cls.is_valid_egyptian_mobile(mobile):
            print("Invalid Egyptian mobile number.")
            return None

        new_user = cls(first_name, last_name, email, password, mobile)
        users.append(new_user.__dict__)
        save_data(cls.users_file, users)
        print("Registration successful!")
        return new_user

    @classmethod
    def login(cls):
        print("\n=== User Login ===")
        email = input("Email: ")
        password = input("Password: ")

        users = load_data(cls.users_file)
        for user in users:
            if user["email"] == email and user["password"] == password:
                print(f"Welcome, {user['first_name']}!")
                return cls(
                    user["first_name"],
                    user["last_name"],
                    user["email"],
                    user["password"],
                    user["mobile"]
                )
        print("Invalid email or password.")
        return None
