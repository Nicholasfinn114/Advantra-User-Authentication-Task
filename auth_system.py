import re

users = {}
next_user_id = 1  # To assign unique IDs to new users

def register(email: str, name: str, password: str) -> dict:
    """
    Registers a new user with the given email, name, and password.

    Validations:
    - Email must contain '@'.
    - Password must be at least 8 characters long and contain at least one digit.
    - Email must be unique (no duplicate users).

    Args:
        email (str): The user's email address.
        name (str): The user's full name.
        password (str): The chosen password.

    Returns:
        dict: A dictionary indicating the status of the registration.
              Example: {"status": "success", "message": "User registered successfully", "user_id": 1}
              Example: {"status": "error", "message": "Invalid email format"}
              Example: {"status": "error", "message": "Password must be at least 8 characters long and contain at least one digit."}
              Example: {"status": "error", "message": "User email already taken"}
    """
    global next_user_id

    # 1. Email validation
    if '@' not in email:
        return {"status": "error", "message": "Invalid email format"}

    # 2. Password validation
    if len(password) < 8 or not any(char.isdigit() for char in password):
        return {"status": "error", "message": "Password must be at least 8 characters long and contain at least one digit."}

    # 3. Email uniqueness validation
    for user_id, user_data in users.items():
        if user_data["email"] == email:
            return {"status": "error", "message": "User email already taken"}

    # If all validations pass, create a new user
    new_user = {
        "email": email,
        "name": name,
        "password": password,  # plaintext for now
        "is_admin": False
    }

    users[next_user_id] = new_user
    user_id = next_user_id
    next_user_id += 1

    return {"status": "success", "message": "User registered successfully", "user_id": user_id}

def login(email: str, password: str) -> dict:
    """
    Checks if a user exists and verifies their password.

    Args:
        email (str): The user's email address.
        password (str): The user's password.

    Returns:
        dict: A dictionary indicating the status of the login.
              Example: {"status": "success", "message": "Login successful", "user_id": 1}
              Example: {"status": "error", "message": "Invalid email or password"}
    """
    for user_id, user_data in users.items():
        if user_data["email"] == email and user_data["password"] == password:
            return {"status": "success", "message": "Login successful", "user_id": user_id}
    return {"status": "error", "message": "Invalid email or password"}

def remove_user(user_id: int) -> dict:
    """
    Removes a user by their ID.

    Args:
        user_id (int): The unique ID of the user to be removed.

    Returns:
        dict: A dictionary indicating the status of the removal.
              Example: {"status": "success", "message": "User removed successfully"}
              Example: {"status": "error", "message": "User not found"}
    """
    if user_id in users:
        del users[user_id]
        return {"status": "success", "message": "User removed successfully"}
    return {"status": "error", "message": "User not found"}


# Bonus Challenge 1: list_users()
def list_users() -> dict:
    """
    Returns a dictionary of all users' ID, email, and name (but never passwords).

    Returns:
        dict: A dictionary where keys are user IDs and values are dictionaries
              containing 'email' and 'name'.
              Example: {1: {'email': 'test@example.com', 'name': 'Test User'}}
    """
    user_list = {}
    for user_id, user_data in users.items():
        user_list[user_id] = {
            "email": user_data["email"],
            "name": user_data["name"]
        }
    return user_list

# Bonus Challenge 2: update_password()
def update_password(user_id: int, old_password: str, new_password: str) -> dict:
    """
    Validates the old password, applies the same security checks to the new password,
    and updates the password if valid.

    Args:
        user_id (int): The ID of the user whose password is to be updated.
        old_password (str): The user's current password.
        new_password (str): The new password to set.

    Returns:
        dict: A dictionary indicating the status of the password update.
              Example: {"status": "success", "message": "Password updated successfully"}
              Example: {"status": "error", "message": "User not found"}
              Example: {"status": "error", "message": "Incorrect old password"}
              Example: {"status": "error", "message": "Password must be at least 8 characters long and contain at least one digit."}
    """
    if user_id not in users:
        return {"status": "error", "message": "User not found"}

    if users[user_id]["password"] != old_password:
        return {"status": "error", "message": "Incorrect old password"}

    # Apply new password validation
    if len(new_password) < 8 or not any(char.isdigit() for char in new_password):
        return {"status": "error", "message": "Password must be at least 8 characters long and contain at least one digit."}

    users[user_id]["password"] = new_password
    return {"status": "success", "message": "Password updated successfully"}

