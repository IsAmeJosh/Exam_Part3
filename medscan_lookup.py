from medscan_storage import load_all_patients


def lookup_patient(patient_id):
    patients = load_all_patients()
    for patient in patients:
        if patient.patient_id == patient_id:
            return patient
    return None