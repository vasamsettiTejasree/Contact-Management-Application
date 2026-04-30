import streamlit as st
import database as db
import re

# make sure DB is ready
db.setup_database()

st.set_page_config(page_title="Tejasree's Contact Book", layout="wide")


# ------------------ STYLE ------------------
st.markdown("""
<style>

/* sidebar */
[data-testid="stSidebar"] {
    background-color: #111827 !important;
}
[data-testid="stSidebar"] * {
    color: white !important;
}

/* buttons */
.stButton > button {
    border-radius: 8px;
    width: 100%;
    font-weight: 500;
}

/* primary - blue */
button[kind="primary"] {
    background-color: #2563eb !important;
    color: white !important;
    border: none !important;
}

/* secondary - red */
button[kind="secondary"] {
    background-color: #dc2626 !important;
    color: white !important;
    border: none !important;
}

/* hover */
button[kind="primary"]:hover {
    background-color: #1d4ed8 !important;
}
button[kind="secondary"]:hover {
    background-color: #b91c1c !important;
}

/* avatar circle */
.avatar-circle {
    width: 45px;
    height: 45px;
    background-color: #e0e7ff;
    color: #4338ca;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)


# ------------------ VALIDATION ------------------
def validate_data(fname, email, phone):
    if not fname or not email or not phone:
        return False, "Required fields missing"

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False, "Invalid email format"

    if not phone.isdigit() or len(phone) < 10:
        return False, "Phone must be at least 10 digits"

    return True, ""


# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.title("📂 Contact Book")
    menu = st.radio("MENU", ["View Contacts", "Add Contact"])


# ================== VIEW ==================
if menu == "View Contacts":

    # -------- EDIT MODE --------
    if "editing_id" in st.session_state and st.session_state.editing_id:

        st.header("📝 Edit Contact")
        data = st.session_state.edit_data

        with st.form("edit_form"):
            c1, c2 = st.columns(2)

            fn = c1.text_input("First Name *", value=data["first_name"])
            ln = c2.text_input("Last Name", value=data["last_name"])
            addr = st.text_area("Address", value=data["address"])
            em = st.text_input("Email *", value=data["email"])
            ph = st.text_input("Phone *", value=data["phone"])

            submitted = st.form_submit_button("Update Contact")

            if submitted:
                valid, msg = validate_data(fn, em, ph)

                if not valid:
                    st.error(msg)
                else:
                    res = db.update_contact(data["id"], fn, ln, addr, em, ph)

                    if res == "email_exists":
                        st.error("Email already exists")
                    elif res == "phone_exists":
                        st.error("Phone already exists")
                    elif res == "success":
                        st.success("Updated successfully")
                        st.session_state.editing_id = None
                        st.rerun()

        if st.button("Cancel"):
            st.session_state.editing_id = None
            st.rerun()

    # -------- LIST MODE --------
    else:
        st.header("📋 Contact List")

        search = st.text_input("", placeholder="Search name, email...")
        contacts = db.fetch_contacts(search)

        st.write(f"Total Contacts: {len(contacts)}")
        st.divider()

        for person in contacts:

            col1, col2, col3, col4 = st.columns([0.8, 5, 1.2, 1.2])

            # avatar
            initials = f"{person['first_name'][0]}{person['last_name'][0]}".upper()
            col1.markdown(
                f'<div class="avatar-circle">{initials}</div>',
                unsafe_allow_html=True
            )

            # details
            with col2:
                st.markdown(f"**{person['first_name']} {person['last_name']}**")
                st.caption(f"📧 {person['email']}  |  📞 {person['phone']}")

                if person["address"]:
                    st.markdown(
                        f"<span style='color:gray;'>🏠 {person['address']}</span>",
                        unsafe_allow_html=True
                    )

            # edit
            if col3.button("Edit", key=f"edit_{person['id']}", type="primary"):
                st.session_state.editing_id = person["id"]
                st.session_state.edit_data = dict(person)
                st.rerun()

            # delete
            if col4.button("Delete", key=f"del_{person['id']}", type="secondary"):
                db.delete_contact(person["id"])
                st.rerun()

            st.divider()


# ================== ADD ==================
else:
    st.header("➕ Add Contact")

    with st.form("add_form", clear_on_submit=True):

        c1, c2 = st.columns(2)

        fn = c1.text_input("First Name *")
        ln = c2.text_input("Last Name")
        addr = st.text_area("Address")
        em = st.text_input("Email *")
        ph = st.text_input("Phone *")

        submit = st.form_submit_button("Save Contact")

        if submit:
            valid, msg = validate_data(fn, em, ph)

            if not valid:
                st.error(msg)
            else:
                ok = db.save_contact(fn, ln, addr, em, ph)

                if ok:
                    st.success("Contact saved successfully")
                else:
                    st.error("Duplicate email or phone")