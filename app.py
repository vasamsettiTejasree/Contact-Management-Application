import streamlit as st
import database as db
import re

db.setup_database()

st.set_page_config(page_title="Tejasree's Contact Book", layout="wide")

st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: #111827 !important;
}
[data-testid="stSidebar"] * {
    color: white !important;
}
.stButton > button {
    border-radius: 8px;
    width: 100%;
    font-weight: 500;
}
button[kind="primary"] {
    background-color: #2563eb !important;
    color: white !important;
    border: none !important;
}
button[kind="secondary"] {
    background-color: #dc2626 !important;
    color: white !important;
    border: none !important;
}
button[kind="primary"]:hover { background-color: #1d4ed8 !important; }
button[kind="secondary"]:hover { background-color: #b91c1c !important; }
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


def check_inputs(first_name, email, phone):
    if not first_name or not email or not phone:
        return False, "Please fill in all required fields"
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False, "That email doesn't look right"
    if not phone.isdigit() or len(phone) < 10:
        return False, "Phone number should be at least 10 digits"
    return True, ""


with st.sidebar:
    st.title("📂 Contact Book")
    menu = st.radio("MENU", ["View Contacts", "Add Contact"])


if menu == "View Contacts":

    if "editing_id" in st.session_state and st.session_state.editing_id:
        st.header("📝 Edit Contact")
        contact = st.session_state.edit_data

        with st.form("edit_form"):
            col1, col2 = st.columns(2)
            first = col1.text_input("First Name *", value=contact["first_name"])
            last = col2.text_input("Last Name", value=contact["last_name"])
            address = st.text_area("Address", value=contact["address"])
            email = st.text_input("Email *", value=contact["email"])
            phone = st.text_input("Phone *", value=contact["phone"])

            if st.form_submit_button("Update Contact"):
                ok, msg = check_inputs(first, email, phone)
                if not ok:
                    st.error(msg)
                else:
                    result = db.update_contact(contact["id"], first, last, address, email, phone)
                    if result == "email_exists":
                        st.error("That email is already taken by another contact")
                    elif result == "phone_exists":
                        st.error("That phone number is already taken by another contact")
                    else:
                        st.success("Contact updated!")
                        st.session_state.editing_id = None
                        st.rerun()

        if st.button("Cancel"):
            st.session_state.editing_id = None
            st.rerun()

    else:
        st.header("📋 Contact List")
        query = st.text_input("", placeholder="Search name, email...")
        contacts = db.fetch_contacts(query)

        st.write(f"Total Contacts: {len(contacts)}")
        st.divider()

        for person in contacts:
            col1, col2, col3, col4 = st.columns([0.8, 5, 1.2, 1.2])

            initials = (person['first_name'][0] + person['last_name'][0]).upper()
            col1.markdown(f'<div class="avatar-circle">{initials}</div>', unsafe_allow_html=True)

            with col2:
                st.markdown(f"**{person['first_name']} {person['last_name']}**")
                st.caption(f"📧 {person['email']}  |  📞 {person['phone']}")
                if person["address"]:
                    st.markdown(f"<span style='color:gray;'>🏠 {person['address']}</span>", unsafe_allow_html=True)

            if col3.button("Edit", key=f"edit_{person['id']}", type="primary"):
                st.session_state.editing_id = person["id"]
                st.session_state.edit_data = dict(person)
                st.rerun()

            if col4.button("Delete", key=f"del_{person['id']}", type="secondary"):
                db.delete_contact(person["id"])
                st.rerun()

            st.divider()

else:
    st.header("➕ Add Contact")

    with st.form("add_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        first = col1.text_input("First Name *")
        last = col2.text_input("Last Name")
        address = st.text_area("Address")
        email = st.text_input("Email *")
        phone = st.text_input("Phone *")

        if st.form_submit_button("Save Contact"):
            ok, msg = check_inputs(first, email, phone)
            if not ok:
                st.error(msg)
            elif db.save_contact(first, last, address, email, phone):
                st.success("Contact saved!")
            else:
                st.error("A contact with that email or phone already exists")
