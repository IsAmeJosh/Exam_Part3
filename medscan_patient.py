class Patient:
    def __init__(self, patient_id, name, sex, age, contact, allergies, surgeries, notes=None):
        self.patient_id = patient_id
        self.name = name
        self.sex = sex
        self.age = age
        self.contact = contact
        self.allergies = allergies      # string, comma-separated
        self.surgeries = surgeries      # string, comma-separated
        self.notes = notes if notes else []  # list of strings, each a full note line

    def add_note(self, note_line):
        self.notes.append(note_line)

    def to_record_string(self):
        lines = [
            f"PatientID: {self.patient_id}",
            f"Name: {self.name}",
            f"Sex: {self.sex}",
            f"Age: {self.age}",
            f"Contact: {self.contact}",
            f"Allergies: {self.allergies}",
            f"Surgeries: {self.surgeries}",
        ]
        for note in self.notes:
            lines.append(f"Note: {note}")
        lines.append("---")
        return "\n".join(lines) + "\n"

    @staticmethod
    def from_record_lines(lines):
        data = {
            "patient_id": "", "name": "", "sex": "",
            "age": "", "contact": "", "allergies": "",
            "surgeries": "", "notes": []
        }
        for line in lines:
            line = line.strip()
            if line.startswith("PatientID:"):
                data["patient_id"] = line.replace("PatientID:", "").strip()
            elif line.startswith("Name:"):
                data["name"] = line.replace("Name:", "").strip()
            elif line.startswith("Sex:"):
                data["sex"] = line.replace("Sex:", "").strip()
            elif line.startswith("Age:"):
                data["age"] = line.replace("Age:", "").strip()
            elif line.startswith("Contact:"):
                data["contact"] = line.replace("Contact:", "").strip()
            elif line.startswith("Allergies:"):
                data["allergies"] = line.replace("Allergies:", "").strip()
            elif line.startswith("Surgeries:"):
                data["surgeries"] = line.replace("Surgeries:", "").strip()
            elif line.startswith("Note:"):
                data["notes"].append(line.replace("Note:", "").strip())

        return Patient(
            data["patient_id"], data["name"], data["sex"], data["age"],
            data["contact"], data["allergies"], data["surgeries"], data["notes"]
        )