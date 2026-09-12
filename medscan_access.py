def load_access_records():
    records = []
    try:
        with open("access.txt", "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) == 3:
                    records.append({
                        "patient_id": parts[0],
                        "doctor": parts[1],
                        "status": parts[2]
                    })
    except FileNotFoundError:
        pass
    return records


def save_access_records(records):
    with open("access.txt", "w", encoding="utf-8") as file:
        for r in records:
            file.write(f"{r['patient_id']},{r['doctor']},{r['status']}\n")


def request_access(patient_id, doctor_username):
    records = load_access_records()
    for r in records:
        if r["patient_id"] == patient_id and r["doctor"] == doctor_username:
            return r["status"]
    records.append({"patient_id": patient_id, "doctor": doctor_username, "status": "pending"})
    save_access_records(records)
    return "pending"


def get_access_status(patient_id, doctor_username):
    records = load_access_records()
    for r in records:
        if r["patient_id"] == patient_id and r["doctor"] == doctor_username:
            return r["status"]
    return None


def set_access_status(patient_id, doctor_username, status):
    records = load_access_records()
    for r in records:
        if r["patient_id"] == patient_id and r["doctor"] == doctor_username:
            r["status"] = status
            save_access_records(records)
            return True
    # No existing record — create one (used for referrals)
    records.append({"patient_id": patient_id, "doctor": doctor_username, "status": status})
    save_access_records(records)
    return True


def get_requests_for_patient(patient_id):
    records = load_access_records()
    return [r for r in records if r["patient_id"] == patient_id]