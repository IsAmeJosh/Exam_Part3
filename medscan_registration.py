from medscan_patient import Patient
from medscan_storage import save_patient, generate_patient_id


def register_patient(name, sex, age, contact, allergies, surgeries):
    patient_id = generate_patient_id()
    patient = Patient(patient_id, name, sex, age, contact, allergies, surgeries)
    save_patient(patient)
    return patient_id