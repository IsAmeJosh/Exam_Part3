from medscan_patient import Patient


def load_all_patients():
    patients = []
    try:
        with open("patients.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        return patients

    current_block = []
    for line in lines:
        stripped = line.strip()
        if stripped == "---":
            if current_block:
                patients.append(Patient.from_record_lines(current_block))
                current_block = []
        else:
            current_block.append(line)

    return patients


def save_patient(patient):
    with open("patients.txt", "a", encoding="utf-8") as file:
        file.write(patient.to_record_string())


def overwrite_all_patients(patients):
    with open("patients.txt", "w", encoding="utf-8") as file:
        for patient in patients:
            file.write(patient.to_record_string())


def generate_patient_id():
    patients = load_all_patients()
    next_number = len(patients) + 1001
    return f"P{next_number}"