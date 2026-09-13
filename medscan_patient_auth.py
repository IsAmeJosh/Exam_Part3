def load_patient_auth():
    """Returns a dict of {patient_id: password} loaded from patient_auth.txt."""
    records = {}
    try:
        with open("patient_auth.txt", "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                patient_id, password = line.split(",", 1)
                records[patient_id] = password
    except FileNotFoundError:
        pass
    return records


def authenticate_patient(patient_id, password):
    records = load_patient_auth()
    return records.get(patient_id) == password


def patient_auth_exists(patient_id):
    return patient_id in load_patient_auth()


def register_patient_auth(patient_id, password):
    """
    Creates login credentials for a patient (either right after
    registration, or later via "Set Up Account" for patients who
    were registered before accounts existed).
    Returns (success: bool, message: str).
    """
    patient_id = patient_id.strip()

    if not patient_id or not password:
        return False, "Patient ID and password are required."

    if patient_auth_exists(patient_id):
        return False, "This Patient ID already has a password set."

    # Same newline guard as doctors.txt, so entries never get
    # mushed together on one line.
    needs_leading_newline = False
    try:
        with open("patient_auth.txt", "rb") as file:
            file.seek(0, 2)  # end of file
            if file.tell() > 0:
                file.seek(-1, 2)
                needs_leading_newline = file.read(1) != b"\n"
    except FileNotFoundError:
        pass

    with open("patient_auth.txt", "a", encoding="utf-8") as file:
        if needs_leading_newline:
            file.write("\n")
        file.write(f"{patient_id},{password}\n")

    return True, "Account created successfully."