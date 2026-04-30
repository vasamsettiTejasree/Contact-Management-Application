import sqlite3

DB_NAME = "contacts.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def setup_database():
    conn = get_connection()

    # create table (won't recreate if already exists)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            address TEXT,
            email TEXT UNIQUE,
            phone TEXT UNIQUE
        )
    """)

    conn.commit()
    conn.close()


def save_contact(first, last, addr, email, phone):
    conn = get_connection()

    try:
        conn.execute("""
            INSERT INTO contacts (first_name, last_name, address, email, phone)
            VALUES (?, ?, ?, ?, ?)
        """, (first, last, addr, email, phone))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        # happens if email or phone already exists
        return False

    finally:
        conn.close()


def fetch_contacts(search_text=None):
    conn = get_connection()
    cur = conn.cursor()

    if search_text:
        s = f"%{search_text}%"
        cur.execute("""
            SELECT * FROM contacts
            WHERE first_name LIKE ? OR last_name LIKE ?
               OR email LIKE ? OR phone LIKE ?
            ORDER BY first_name ASC
        """, (s, s, s, s))
    else:
        cur.execute("SELECT * FROM contacts ORDER BY first_name ASC")

    rows = cur.fetchall()
    conn.close()

    return rows


def delete_contact(contact_id):
    conn = get_connection()

    conn.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    conn.commit()
    conn.close()


def update_contact(contact_id, fn, ln, addr, email, phone):
    conn = get_connection()
    cur = conn.cursor()

    # check duplicate email (ignore same contact)
    cur.execute(
        "SELECT id FROM contacts WHERE email=? AND id!=?",
        (email, contact_id)
    )
    if cur.fetchone():
        conn.close()
        return "email_exists"

    # check duplicate phone
    cur.execute(
        "SELECT id FROM contacts WHERE phone=? AND id!=?",
        (phone, contact_id)
    )
    if cur.fetchone():
        conn.close()
        return "phone_exists"

    # update record
    cur.execute("""
        UPDATE contacts
        SET first_name=?, last_name=?, address=?, email=?, phone=?
        WHERE id=?
    """, (fn, ln, addr, email, phone, contact_id))

    conn.commit()
    conn.close()

    return "success"