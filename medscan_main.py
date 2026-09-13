import streamlit as st
from medscan_doctor import authenticate_doctor, register_doctor, doctor_exists
from medscan_registration import register_patient
from medscan_lookup import lookup_patient
from medscan_notes import add_note
from medscan_access import request_access, get_access_status, set_access_status, get_requests_for_patient
from medscan_emergency import log_emergency_access
from medscan_storage import load_all_patients

st.set_page_config(page_title="MedScan", page_icon="🩺", layout="wide")

st.title("🩺 MedScan")
st.write("ID-Based Patient Medical Record Access System")
st.divider()

if "doctor_logged_in" not in st.session_state:
    st.session_state.doctor_logged_in = False
if "doctor_name" not in st.session_state:
    st.session_state.doctor_name = ""
if "allergy_list" not in st.session_state:
    st.session_state.allergy_list = []
if "surgery_list" not in st.session_state:
    st.session_state.surgery_list = []
if "current_patient" not in st.session_state:
    st.session_state.current_patient = None
if "emergency_unlocked" not in st.session_state:
    st.session_state.emergency_unlocked = False

# ------------------------------------------------------------
# Restore login after a browser refresh.
# A refresh starts a brand-new Streamlit session, so
# st.session_state is wiped every time — but the URL's query
# params survive a refresh, so we keep the logged-in doctor's
# username there and use it to log them back in automatically.
# ------------------------------------------------------------
if not st.session_state.doctor_logged_in:
    qp_doctor = st.query_params.get("doctor")
    if qp_doctor and doctor_exists(qp_doctor):
        st.session_state.doctor_logged_in = True
        st.session_state.doctor_name = qp_doctor

st.sidebar.title("MedScan Menu")
mode = st.sidebar.radio(
    "Select mode:",
    ["Patient Registration", "Manage Access", "Doctor Login"]
)

# ============================================================
# PATIENT REGISTRATION
# ============================================================
if mode == "Patient Registration":
    st.subheader("Register a New Patient")

    name = st.text_input("Full Name")

    sex = st.radio(
        "Sex / Gender",
        ["Male", "Female", "Non-binary", "Prefer not to say"]
    )

    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    contact = st.text_input("Contact Number", max_chars=11, placeholder="e.g. 09171234567")

    st.write("**Known Allergies**")
    col_a, col_b = st.columns([3, 1])
    with col_a:
        new_allergy = st.text_input(
            "Type an allergy and click Add",
            key="new_allergy_input",
            value=st.session_state.get("prefill_allergy", "")
        )
    with col_b:
        st.write("")
        st.write("")
        if st.button("Add Allergy"):
            if new_allergy.strip() != "":
                st.session_state.allergy_list.append(new_allergy.strip())
                st.session_state.prefill_allergy = ""
                st.rerun()

    if st.session_state.allergy_list:
        for i, item in enumerate(st.session_state.allergy_list):
            col_x, col_y, col_z = st.columns([3, 1, 1])
            col_x.write(f"- {item}")
            if col_y.button("Edit", key=f"edit_allergy_{i}"):
                st.session_state.prefill_allergy = item
                st.session_state.allergy_list.pop(i)
                st.rerun()
            if col_z.button("Remove", key=f"remove_allergy_{i}"):
                st.session_state.allergy_list.pop(i)
                st.rerun()
    else:
        st.caption("No allergies added yet.")

    st.write("**Past Surgeries**")
    col_c, col_d = st.columns([3, 1])
    with col_c:
        new_surgery = st.text_input(
            "Type a surgery and click Add",
            key="new_surgery_input",
            value=st.session_state.get("prefill_surgery", "")
        )
    with col_d:
        st.write("")
        st.write("")
        if st.button("Add Surgery"):
            if new_surgery.strip() != "":
                st.session_state.surgery_list.append(new_surgery.strip())
                st.session_state.prefill_surgery = ""
                st.rerun()

    if st.session_state.surgery_list:
        for i, item in enumerate(st.session_state.surgery_list):
            col_p, col_q, col_r = st.columns([3, 1, 1])
            col_p.write(f"- {item}")
            if col_q.button("Edit", key=f"edit_surgery_{i}"):
                st.session_state.prefill_surgery = item
                st.session_state.surgery_list.pop(i)
                st.rerun()
            if col_r.button("Remove", key=f"remove_surgery_{i}"):
                st.session_state.surgery_list.pop(i)
                st.rerun()
    else:
        st.caption("No surgeries added yet.")

    if st.button("Register Patient"):
        contact_digits = contact.strip()

        if name.strip() == "" or contact.strip() == "":
            st.error("Name and contact number are required.")
        elif not contact_digits.isdigit():
            st.error("Contact number must contain digits only.")
        elif len(contact_digits) < 10 or len(contact_digits) > 11:
            st.error("Contact number must be 10–11 digits long (e.g. 09171234567).")
        else:
            allergies_string = ", ".join(st.session_state.allergy_list) if st.session_state.allergy_list else "None"
            surgeries_string = ", ".join(st.session_state.surgery_list) if st.session_state.surgery_list else "None"
            patient_id = register_patient(name, sex, age, contact, allergies_string, surgeries_string)
            st.success("Patient registered successfully!")
            st.info(f"Your Patient ID is: **{patient_id}**")
            st.warning("Save this ID — you will need it for future clinic visits.")
            st.session_state.allergy_list = []
            st.session_state.surgery_list = []


# ============================================================
# MANAGE ACCESS (Patient side)
# ============================================================
elif mode == "Manage Access":
    st.subheader("Manage Doctor Access")
    st.write("Enter your Patient ID to review and control which doctors can access your record.")

    patient_id_input = st.text_input("Your Patient ID")

    if st.button("View Access Requests"):
        patient = lookup_patient(patient_id_input)
        if not patient:
            st.error("Patient ID not found.")
        else:
            st.session_state.access_patient_id = patient_id_input

    if st.session_state.get("access_patient_id"):
        requests = get_requests_for_patient(st.session_state.access_patient_id)

        if not requests:
            st.info("No doctors have requested access yet.")
        else:
            for r in requests:
                col1, col2, col3 = st.columns([2, 1, 1])
                col1.write(f"**Dr. {r['doctor']}** — status: `{r['status']}`")

                if r["status"] != "approved":
                    if col2.button("Approve", key=f"approve_{r['doctor']}"):
                        set_access_status(st.session_state.access_patient_id, r["doctor"], "approved")
                        st.rerun()

                if r["status"] != "denied":
                    if col3.button("Deny", key=f"deny_{r['doctor']}"):
                        set_access_status(st.session_state.access_patient_id, r["doctor"], "denied")
                        st.rerun()


# ============================================================
# DOCTOR LOGIN
# ============================================================
elif mode == "Doctor Login":

    if not st.session_state.doctor_logged_in:
        login_tab, signup_tab = st.tabs(["🔑 Log In", "🆕 Sign Up"])

        # --- Log In ---
        with login_tab:
            st.subheader("Doctor Login")
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")

            if st.button("Log In"):
                if authenticate_doctor(username, password):
                    st.session_state.doctor_logged_in = True
                    st.session_state.doctor_name = username
                    st.query_params["doctor"] = username  # survives a page refresh
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

        # --- Sign Up ---
        with signup_tab:
            st.subheader("Create a Doctor Account")
            new_username = st.text_input("Choose a Username", key="signup_username")
            new_password = st.text_input("Choose a Password", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")

            if st.button("Sign Up"):
                if new_username.strip() == "" or new_password == "":
                    st.error("Username and password are required.")
                elif new_password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    success, message = register_doctor(new_username, new_password)
                    if success:
                        st.success(message)
                        st.info("Switch to the Log In tab to sign in with your new account.")
                    else:
                        st.error(message)

    else:
        st.subheader(f"Welcome, Dr. {st.session_state.doctor_name}")

        if st.button("Log Out"):
            st.session_state.doctor_logged_in = False
            st.session_state.doctor_name = ""
            st.session_state.current_patient = None
            st.session_state.emergency_unlocked = False
            if "doctor" in st.query_params:
                del st.query_params["doctor"]
            st.rerun()

        st.divider()

        tab1, tab2 = st.tabs(["🔍 Patient Lookup", "📋 All Patients"])

        # --- Tab 1: Lookup by ID ---
        with tab1:
            patient_id = st.text_input("Enter Patient ID")

            if st.button("Look Up Patient"):
                patient = lookup_patient(patient_id)
                if patient:
                    st.session_state.current_patient = patient
                    st.session_state.emergency_unlocked = False
                else:
                    st.session_state.current_patient = None
                    st.error("Patient not found.")

        # --- Tab 2: All Patients list ---
        with tab2:
            all_patients = load_all_patients()

            if not all_patients:
                st.info("No patients registered yet.")
            else:
                for p in all_patients:
                    col1, col2, col3, col4 = st.columns([2, 3, 1, 1])
                    col1.write(f"**{p.patient_id}**")
                    col2.write(p.name)
                    col3.write(p.sex)
                    col4.write(p.age)
                    if st.button("View Profile", key=f"view_{p.patient_id}"):
                        st.session_state.current_patient = p
                        st.session_state.emergency_unlocked = False
                        st.rerun()

        # --- Shared record display (used by both tabs) ---
        if st.session_state.current_patient:
            patient = st.session_state.current_patient
            doctor_name = st.session_state.doctor_name

            access_status = get_access_status(patient.patient_id, doctor_name)
            has_access = (access_status == "approved") or st.session_state.emergency_unlocked

            st.divider()
            st.write(f"### Record: {patient.name} ({patient.patient_id})")

            if has_access:
                col1, col2, col3 = st.columns(3)
                col1.metric("Name", patient.name)
                col2.metric("Sex", patient.sex)
                col3.metric("Age", patient.age)

                st.write(f"**Contact:** {patient.contact}")
                st.write(f"**Allergies:** {patient.allergies}")
                st.write(f"**Past Surgeries:** {patient.surgeries}")

                if st.session_state.emergency_unlocked and access_status != "approved":
                    st.warning("⚠️ Viewing under Emergency Access — this action has been logged.")

                st.write("#### Consultation History")
                if patient.notes:
                    for note in patient.notes:
                        st.text(note)
                else:
                    st.info("No previous notes on record.")

                st.write("#### Add New Note")
                new_note = st.text_area("Consultation notes for this visit")

                if st.button("Save Note"):
                    if new_note.strip() == "":
                        st.error("Note cannot be empty.")
                    else:
                        add_note(patient.patient_id, doctor_name, new_note)
                        st.success("Note saved successfully!")
                        st.session_state.current_patient = lookup_patient(patient.patient_id)
                        st.rerun()

                st.divider()
                st.write("#### Refer to Another Doctor")
                st.caption("Since you have access to this record, you can grant access to a colleague.")
                referred_doctor = st.text_input("Doctor's username to grant access")

                if st.button("Grant Access to Doctor"):
                    if referred_doctor.strip() == "":
                        st.error("Enter a doctor's username.")
                    else:
                        set_access_status(patient.patient_id, referred_doctor.strip(), "approved")
                        st.success(f"Access granted to Dr. {referred_doctor.strip()}.")

            else:
                st.warning("You do not have approved access to this patient's record.")

                if access_status == "pending":
                    st.info("Access request sent. Waiting for patient approval.")
                elif access_status == "denied":
                    st.error("This patient has denied your access request.")
                else:
                    if st.button("Request Access"):
                        request_access(patient.patient_id, doctor_name)
                        st.rerun()

                st.divider()
                st.write("#### Emergency Access")
                st.caption("Use only for urgent situations. This will be logged with your reason.")
                reason = st.text_area("Reason for emergency access (required)")

                if st.button("Unlock via Emergency Access"):
                    if reason.strip() == "":
                        st.error("A reason is required to use emergency access.")
                    else:
                        log_emergency_access(patient.patient_id, doctor_name, reason)
                        st.session_state.emergency_unlocked = True
                        st.rerun()