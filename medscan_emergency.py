from datetime import datetime


def log_emergency_access(patient_id, doctor_username, reason):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("emergency_log.txt", "a", encoding="utf-8") as file:
        file.write(
            f"Timestamp: {timestamp}\n"
            f"Doctor: {doctor_username}\n"
            f"PatientID: {patient_id}\n"
            f"Reason: {reason}\n"
            f"---\n"
        )