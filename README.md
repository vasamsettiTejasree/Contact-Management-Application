# Contact-Management-Application
A simple and user-friendly Contact Management App built using Python and Streamlit.
This application allows users to store, view, update, and delete contacts easily.

Features:
- Add new contacts
- View all contacts
- Search contacts by name, email, or phone
- Edit existing contacts
- Delete contacts
- Input validation (email & phone)
- Prevent duplicate email and phone
- Tech Stack
  
Frontend: Streamlit

Backend: Python

Database: SQLite

Libraries Used:
streamlit
sqlite3
re

 Project Structure
Contact-Management-App/

├── app.py          # Main Streamlit app

├── database.py     # Database operations (CRUD)

├── contacts.db     # SQLite database (auto-created)

└── README.md       # Project documentation

⚙️ How to Run the Project

1. Clone the repository
git clone [https://github.com/your-username/contact-management-app.git](https://github.com/vasamsettiTejasree/Contact-Management-Application)
cd contact-management-app

3. Install dependencies
pip install streamlit

5. Run the app
streamlit run app.py

7. Open in browser
http://localhost:8501

1) How It Works
- The app uses Streamlit for the UI.

- User inputs are validated before storing.

- Data is stored in a SQLite database.
  
- Duplicate emails and phone numbers are restricted.
  
- Edit functionality uses session_state to manage updates.

2) Validation Rules
- First Name, Email, and Phone are required
  
- Email must be in valid format
  
- Phone must be at least 10 digits
  
- Email and Phone must be unique

3) Challenges Faced
   
- Handling duplicate entries during update
- Managing edit state in Streamlit
- Styling buttons and layout using custom CSS

4) Future Improvements
- Add login/authentication
- Export contacts (CSV/PDF)
- Cloud database integration
- Better UI enhancements


 Note:
This project was built as part of a learning task to understand full-stack development using Python.
