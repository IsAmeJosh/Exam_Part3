def authenticate_doctor(username, password):
    try:
        with open("doctors.txt", "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                stored_username, stored_password = line.split(",", 1)
                if stored_username == username and stored_password == password:
                    return True
        return False
    except FileNotFoundError:
        return False