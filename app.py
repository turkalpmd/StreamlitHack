import os
from dotenv import load_dotenv
import pymongo
from datetime import datetime
import streamlit as st

PAGE_TITLE = "Streamlit Hackhaton..."
PAGE_ICON = ":wave:"
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

# Load environment variables
load_dotenv()

class Database:
    def __init__(self):
        self.client = pymongo.MongoClient(st.secrets["MongoDB"]["MONGODB_CONNECTION_STRING"])
        self.db = self.client[st.secrets["MongoDB"]["MONGO_CLIENT"]]        
        self.collection = self.db[st.secrets["MongoDB"]["MONGO_DB"]]        


    def insert_data(self, data):
        self.collection.insert_one(data)
        
def validate_form_data(data):
    # Check if required fields are filled
    required_fields = ['Name', 'Surname', 'Phone', 'Email', 'Birth Date', 'Age', 'Weight', 'Gender']
    for field in required_fields:
        if not data.get(field):
            st.write(f"{field} is required.")
            return False

    # Check if age and weight are positive
    if data['Age'] <= 0 or data['Weight'] <= 0:
        st.write("Age and Weight must be positive.")
        return False

    # All validations passed
    return True

def main():
    # Database
    db = Database()
 
    st.title("Patient Information Form")
    
    st.info("""
        First of all, I'd like to praise the brilliance of Streamlit, especially for beginner developers, \
        it's as valuable as a rare gem. It allows for the rapid and easy creation of interactive and user-friendly web applications, \
        which is a great asset in data science and machine learning fields. As a doctor, I've created this sample project for a\
        telemedicine application. Telemedicine breaks down geographical barriers between patients and healthcare providers,\
        enabling quality healthcare services to be delivered regardless of time and location. This form, in particular, \
                assists in gathering a patient's medical information, enabling doctors to better comprehend the patient's condition and devise the most effective treatment strategies.

    """)
    st.success("""

                    For anyone interested in assessing the source codes, they can be found on my GitHub page: https://github.com/turkalpmd/StreamlitHack
                """)

    name = st.text_input("Name")
    secondname = st.text_input("Second Name")
    surname = st.text_input("Surname")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email Address")
    address = st.text_area("Home Address")
    birth_date = st.date_input("Birth Date")
    age = st.number_input("Age", min_value=0)
    weight = st.number_input("Weight (in kg)", min_value=0.0)
    gender = st.selectbox("Gender", ["Male", "Female", "Non-binary", "Prefer not to say"])
    race = st.text_input("Race")
    heart_rate = st.number_input("Heart Rate", min_value=0)
    respiratory_rate = st.number_input("Respiratory Rate", min_value=0)
    systolic_blood_pressure = st.number_input("Systolic Blood Pressure", min_value=0)
    temperature = st.number_input("Body Temperature", min_value=0.0)
    main_complaint = st.text_area("Main Complaint")

    if st.button("Submit"):
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        birth_date = str(birth_date)
        response = {
            'Submission time' : dt_string,
            'Name': name,
            'Second Name': secondname,
            'Surname': surname,
            'Phone': phone,
            'Email': email,
            'Address': address,
            'Birth Date': birth_date,
            'Age': age,
            'Weight': weight,
            'Gender': gender,
            'Race': race,
            'Heart Rate': heart_rate,
            'Respiratory Rate': respiratory_rate,
            'Systolic Blood Pressure': systolic_blood_pressure,
            'Temperature': temperature,
            'Main Complaint': main_complaint,
        }
        # Validate form data
        if validate_form_data(response):
            db.insert_data(response)
            st.write("Form Submitted Successfully. Please wait for a notification to meet with a suitable doctor.")
        else:
            st.write("Form data is invalid. Please correct the errors and try again.")
    
    st.info("""
        MongoDB, the NoSQL database used to manage the database operations of this application, 
        caters to the needs of modern applications with its features like flexible schema structure, 
        scalability, performance, and reliability. The data from this form is stored and processed 
        swiftly and securely, thanks to the high performance and reliability provided by MongoDB.
    """)

    st.info("""
        Streamlit, the Python library used to create the user interface of this application, 
        enables data scientists and developers to create interactive and user-friendly web applications. 
        This form was swiftly created thanks to Streamlit's ease of use and rapid prototyping capabilities. 
        Streamlit is an ideal tool for rapidly developing modern web applications.
    """)

if __name__ == "__main__":
    main()


