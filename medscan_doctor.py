def load_doctors():
    """Returns a dict of {username: password} loaded from doctors.txt."""
    doctors = {}
    try:
        with open("doctors.txt", "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                stored_username, stored_password = line.split(",", 1)
                doctors[stored_username] = stored_password
    except FileNotFoundError:
        pass
    return doctors


def authenticate_doctor(username, password):
    doctors = load_doctors()
    return doctors.get(username) == password


def doctor_exists(username):
    return username in load_doctors()


def register_doctor(username, password):
    """
    Creates a new doctor account.
    Returns (success: bool, message: str).
    """
    username = username.strip()

    if not username or not password:
        return False, "Username and password are required."

    if " " in username or "," in username:
        return False, "Username cannot contain spaces or commas."

    if doctor_exists(username):
        return False, "That username is already taken."

    # Guard against appending onto a file that doesn't already end
    # with a newline (this is what caused entries to get mushed
    # together on one line).
    needs_leading_newline = False
    try:
        with open("doctors.txt", "rb") as file:
            file.seek(0, 2)  # end of file
            if file.tell() > 0:
                file.seek(-1, 2)
                needs_leading_newline = file.read(1) != b"\n"
    except FileNotFoundError:
        pass

    with open("doctors.txt", "a", encoding="utf-8") as file:
        if needs_leading_newline:
            file.write("\n")
        file.write(f"{username},{password}\n")

    return True, "Account created successfully. You can now log in."