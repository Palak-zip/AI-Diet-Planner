import streamlit as st
import google.generativeai as genai
import os
import json

st.set_page_config(page_title="AI Diet Planner", page_icon="🥗", layout="wide")

st.title("🥗 AI-Powered 7-Day Indian Diet Planner")
st.markdown("Get a personalized, authentic Indian diet plan tailored to your body and goals.")

# --- Sidebar Inputs ---
st.sidebar.header("Your Profile")
name = st.sidebar.text_input("Name", "Aarav Sharma")
age = st.sidebar.number_input("Age", min_value=10, max_value=100, value=26)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
height_cm = st.sidebar.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=174.0)
weight_kg = st.sidebar.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
activity = st.sidebar.selectbox("Activity Level", ["Sedentary", "Light", "Moderate", "Active", "Very Active"], index=2)
goal = st.sidebar.selectbox("Goal", ["Weight Loss", "Maintenance", "Weight Gain", "Muscle Gain"])
diet_preference = st.sidebar.selectbox("Dietary Preference", [
    "Vegetarian (Indian Standard)",
    "Non-Vegetarian",
    "Vegan",
    "Jain",
    "Keto / Low-Carb Indian",
    "High Protein Indian"
])

# --- Nutrition Calculator ---
def calculate_bmi(weight, height):
    if height == 0:
        return 0
    height_m = height / 100
    return round(weight / (height_m ** 2), 1)

def calculate_calorie_needs(weight, height, age, gender, activity, goal):
    # Mifflin-St Jeor equation
    bmr = 10 * weight + 6.25 * height - 5 * age
    if gender == 'Male':
        bmr += 5
    else:
        bmr -= 161
    
    activity_factors = {
        "Sedentary": 1.2,
        "Light": 1.375,
        "Moderate": 1.55,
        "Active": 1.725,
        "Very Active": 1.9
    }
    tdee = bmr * activity_factors.get(activity, 1.2)
    
    if goal == 'Weight Loss':
        target_calories = max(1200, tdee - 500)
    elif goal == 'Weight Gain':
        target_calories = tdee + 500
    elif goal == 'Muscle Gain':
        target_calories = tdee + 300
    else:
        target_calories = tdee

    return round(bmr), round(tdee), round(target_calories)

bmi = calculate_bmi(weight_kg, height_cm)
bmr, tdee, target_calories = calculate_calorie_needs(weight_kg, height_cm, age, gender, activity, goal)

col1, col2, col3, col4 = st.columns(4)
col1.metric("BMI", bmi)
col2.metric("BMR", f"{bmr} kcal")
col3.metric("TDEE", f"{tdee} kcal")
col4.metric("Target Daily Calories", f"{target_calories} kcal")

st.divider()

# --- AI Generation ---
api_key = st.text_input("Enter your Google Gemini API Key:", type="password")

if st.button("Generate My 7-Day Diet Plan", type="primary"):
    if not api_key:
        st.error("Please enter a valid Gemini API Key.")
    else:
        with st.spinner("Analyzing your profile and crafting your authentic Indian diet plan..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""
                You are an expert Indian clinical nutritionist. Generate an authentic, delicious 7-DAY BALANCED INDIAN DIET PLAN for this user:
                - Name: {name}
                - Age: {age}
                - Gender: {gender}
                - Height: {height_cm} cm
                - Weight: {weight_kg} kg
                - Activity Level: {activity}
                - Goal: {goal}
                - Dietary Preference: {diet_preference}
                - Target Daily Calories: approx {target_calories} kcal

                CRITICAL INSTRUCTIONS:
                - Every meal MUST BE AUTHENTIC INDIAN CUISINE.
                - DO NOT USE HINDI SCRIPT. ALL TITLES AND DESCRIPTIONS MUST BE IN CLEAN, PROFESSIONAL ENGLISH.
                - Express portions in clean measurements.

                Provide a strictly valid JSON response with the following structure:
                {{
                  "summary": "Short 2-sentence encouraging summary of the 7-day approach",
                  "hydrationGoalLiters": 2.5,
                  "days": [
                    {{
                      "dayNumber": 1,
                      "dayName": "Day 1 (Monday)",
                      "focus": "Digestive Reset",
                      "totalCalories": 2000,
                      "meals": {{
                        "breakfast": {{"name": "...", "portion": "...", "calories": 300}},
                        "lunch": {{"name": "...", "portion": "...", "calories": 600}},
                        "snack": {{"name": "...", "portion": "...", "calories": 200}},
                        "dinner": {{"name": "...", "portion": "...", "calories": 500}}
                      }}
                    }}
                  ],
                  "groceryList": [
                    {{"category": "Fresh Vegetables", "items": ["Spinach", "Tomatoes"]}}
                  ]
                }}
                Return ONLY valid JSON.
                """

                response = model.generate_content(prompt)
                response_text = response.text.replace("```json", "").replace("```", "").strip()
                plan_data = json.loads(response_text)
                
                st.success("Your diet plan is ready!")
                
                st.subheader("Plan Overview")
                st.write(plan_data.get("summary", ""))
                st.info(f"💧 Daily Hydration Goal: {plan_data.get('hydrationGoalLiters', 2.5)} Liters")
                
                st.subheader("Weekly Meal Plan")
                for day in plan_data.get("days", []):
                    with st.expander(f"{day.get('dayName', 'Day')} - {day.get('focus', '')} ({day.get('totalCalories', 0)} kcal)"):
                        meals = day.get("meals", {})
                        
                        m_col1, m_col2 = st.columns(2)
                        with m_col1:
                            st.markdown(f"**Breakfast:** {meals.get('breakfast', {}).get('name', '')}")
                            st.caption(f"Portion: {meals.get('breakfast', {}).get('portion', '')} | {meals.get('breakfast', {}).get('calories', '')} kcal")
                            
                            st.markdown(f"**Lunch:** {meals.get('lunch', {}).get('name', '')}")
                            st.caption(f"Portion: {meals.get('lunch', {}).get('portion', '')} | {meals.get('lunch', {}).get('calories', '')} kcal")
                            
                        with m_col2:
                            st.markdown(f"**Snack:** {meals.get('snack', {}).get('name', '')}")
                            st.caption(f"Portion: {meals.get('snack', {}).get('portion', '')} | {meals.get('snack', {}).get('calories', '')} kcal")
                            
                            st.markdown(f"**Dinner:** {meals.get('dinner', {}).get('name', '')}")
                            st.caption(f"Portion: {meals.get('dinner', {}).get('portion', '')} | {meals.get('dinner', {}).get('calories', '')} kcal")
                
                st.subheader("Grocery List")
                for category in plan_data.get("groceryList", []):
                    st.markdown(f"**{category.get('category', 'Items')}**")
                    items = category.get('items', [])
                    if items:
                        st.write(", ".join([item if isinstance(item, str) else item.get('name', '') for item in items]))

            except Exception as e:
                st.error(f"Error generating plan: {str(e)}")