

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

def fetch_anthropic_recommendations(api_key, bmi_value, category):
    client = anthropic.Anthropic(api_key=api_key)  # Initialize the client with the API key
    
    # Construct the AI prompt
    prompt = f"You are a nutrition and fitness expert. Based on a BMI of {bmi_value} ({category} category), suggest a diet plan and workout routine that would be most effective."

    # Generate the AI response
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=500,
        temperature=0.7,  # You can adjust the creativity of responses using temperature
        system="You are a nutrition and fitness expert. Respond with detailed and actionable advice.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )
    
    # Return the AI's response
    #return message["content"]
    raw_context = message.content
    itinery = raw_context[0].text
    return itinery

# Streamlit app structure
st.title("BMI Calculator and AI-Powered Health Recommendations")

# Input fields
api_key = st.text_input("Enter your Anthropic API Key", type="password")
#age = st.number_input("Enter your age", min_value=1, max_value=120, value=30)
weight = st.number_input("Enter your weight (kg)", min_value=1.0, max_value=300.0, value=70.0)
height = st.number_input("Enter your height (m)", min_value=0.5, max_value=2.5, value=1.7)

# Button to trigger BMI calculation and recommendations
if st.button("Calculate BMI and Get AI Recommendations"):
    if not api_key:
        st.error("Please enter your Anthropic API key.")
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
            ai_recommendations = fetch_anthropic_recommendations(api_key, bmi, category)
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
