import streamlit as st
import os
import pandas as pd
from groq import Groq

# Get Groq API key from Streamlit secrets
api_key = st.secrets["api_key"]

def calculate_bmi(weight, height):
    return weight / (height ** 2)

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def fetch_groq_recommendations(api_key, bmi_value, category):
    client = Groq(api_key=api_key)  # Initialize the Groq client

    # Construct the AI prompt
    prompt = f"You are a nutrition and fitness expert. Based on a BMI of {bmi_value} ({category} category), suggest a diet plan and workout routine that would be most effective."

    # Generate the AI response using Groq's Llama model
    message = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama3-8b-8192",  # Groq's model
    )

    # Return the AI's response
    return message.choices[0].message.content

# Streamlit app structure
st.title("BMI Calculator and AI-Powered Health Recommendations")

# Input fields
weight = st.number_input("Enter your weight (kg)", min_value=1.0, max_value=300.0, value=70.0)
height = st.number_input("Enter your height (m)", min_value=0.5, max_value=2.5, value=1.7)

# 6-digit password field
password = st.text_input("Enter 6-digit password to view results", type="password")

# Button to trigger BMI calculation and recommendations
if st.button("Calculate BMI and Get AI Recommendations"):
    if password != "salman":  # Replace with your desired password
        st.error("Incorrect password. Please enter the correct 6-digit password.")
    else:
        # Calculate BMI and categorize
        bmi = calculate_bmi(weight, height)
        category = get_bmi_category(bmi)

        # Display results
        st.subheader("Results")
        st.write(f"Your BMI: {bmi:.2f}")
        st.write(f"Category: {category}")

        # Get and display AI recommendations
        st.subheader("AI-Powered Recommendations")
        try:
            ai_recommendations = fetch_groq_recommendations(api_key, bmi, category)
            st.write(ai_recommendations)
        except Exception as e:
            st.error(f"Error fetching AI recommendations: {e}")

    # Display BMI categories table
    st.subheader("BMI Categories")
    bmi_categories = pd.DataFrame({
        "Category": ["Underweight", "Normal weight", "Overweight", "Obese"],
        "BMI Range": ["< 18.5", "18.5 - 24.9", "25 - 29.9", "≥ 30"]
    })
    st.table(bmi_categories)

st.write("Note: This app provides AI-generated recommendations. For personalized advice, please consult a healthcare professional.")
