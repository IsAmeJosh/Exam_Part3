from datetime import datetime
from medscan_storage import load_all_patients, overwrite_all_patients


def add_note(patient_id, doctor_name, note_text):
    patients = load_all_patients()

    for patient in patients:
        if patient.patient_id == patient_id:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            full_note = f"{timestamp} | {doctor_name} | {note_text}"
            patient.add_note(full_note)
            overwrite_all_patients(patients)
            return True

    return False