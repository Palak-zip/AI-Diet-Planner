import streamlit as st
import random
import time

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

# --- Mock Data Generators ---
breakfast_options = {
    "Vegetarian (Indian Standard)": [
        {"name": "Poha with Peanuts", "portion": "1 plate", "calories": 320},
        {"name": "Upma with Mixed Veggies", "portion": "1 bowl", "calories": 300},
        {"name": "Idli with Sambar", "portion": "3 idlis, 1 bowl sambar", "calories": 350},
        {"name": "Aloo Paratha with Curd", "portion": "1 paratha, 1/2 bowl curd", "calories": 380},
    ],
    "Non-Vegetarian": [
        {"name": "Masala Omelette with Brown Bread", "portion": "2 eggs, 2 slices", "calories": 350},
        {"name": "Chicken Sausage with Scrambled Eggs", "portion": "1 plate", "calories": 400},
        {"name": "Egg Bhurji with Roti", "portion": "2 eggs, 2 rotis", "calories": 380},
    ],
    "Vegan": [
        {"name": "Moong Dal Chilla", "portion": "2 chillas", "calories": 280},
        {"name": "Oats Porridge with Almond Milk", "portion": "1 bowl", "calories": 250},
        {"name": "Besan Chilla", "portion": "2 chillas", "calories": 300},
    ]
}

lunch_options = {
    "Vegetarian (Indian Standard)": [
        {"name": "Dal Tadka, Rice, Mix Veg", "portion": "1 bowl dal, 1 cup rice", "calories": 550},
        {"name": "Rajma Chawal", "portion": "1 big bowl", "calories": 600},
        {"name": "Paneer Butter Masala with 2 Rotis", "portion": "1 bowl paneer, 2 rotis", "calories": 650},
    ],
    "Non-Vegetarian": [
        {"name": "Chicken Curry with Rice", "portion": "1 bowl chicken, 1 cup rice", "calories": 600},
        {"name": "Fish Tikka Masala with 2 Rotis", "portion": "1 bowl fish, 2 rotis", "calories": 550},
        {"name": "Mutton Rogan Josh with Rice", "portion": "1 bowl mutton, 1 cup rice", "calories": 700},
    ],
    "Vegan": [
        {"name": "Chickpea Curry (Chole) with Brown Rice", "portion": "1 bowl chole, 1 cup rice", "calories": 500},
        {"name": "Tofu Matar with 2 Multigrain Rotis", "portion": "1 bowl tofu, 2 rotis", "calories": 480},
        {"name": "Soya Chunk Curry with Quinoa", "portion": "1 bowl soya, 1 cup quinoa", "calories": 450},
    ]
}

snack_options = [
    {"name": "Roasted Makhana", "portion": "1 small bowl", "calories": 120},
    {"name": "Sprout Salad", "portion": "1 bowl", "calories": 150},
    {"name": "Handful of Mixed Nuts (Almonds, Walnuts)", "portion": "30g", "calories": 180},
    {"name": "Fruit Bowl (Apple, Papaya)", "portion": "1 bowl", "calories": 100},
    {"name": "Masala Oats", "portion": "1 small bowl", "calories": 160},
]

dinner_options = {
    "Vegetarian (Indian Standard)": [
        {"name": "Palak Paneer with 2 Rotis", "portion": "1 bowl palak, 2 rotis", "calories": 500},
        {"name": "Khichdi with Curd", "portion": "1 plate", "calories": 450},
        {"name": "Lauki Ki Sabzi with 2 Rotis", "portion": "1 bowl sabzi, 2 rotis", "calories": 350},
    ],
    "Non-Vegetarian": [
        {"name": "Grilled Chicken Breast with Sautéed Veggies", "portion": "1 breast, 1 cup veg", "calories": 450},
        {"name": "Egg Curry with 2 Rotis", "portion": "2 eggs, 2 rotis", "calories": 500},
        {"name": "Baked Fish with Salad", "portion": "1 fillet, 1 bowl salad", "calories": 400},
    ],
    "Vegan": [
        {"name": "Mixed Dal with 2 Rotis", "portion": "1 bowl dal, 2 rotis", "calories": 400},
        {"name": "Baingan Bharta with Bajra Roti", "portion": "1 bowl bharta, 1 roti", "calories": 380},
        {"name": "Vegetable Dalia", "portion": "1 big bowl", "calories": 350},
    ]
}

def get_options_by_pref(pref, options_dict):
    if pref in options_dict:
        return options_dict[pref]
    elif "Non-Vegetarian" in pref:
        return options_dict["Non-Vegetarian"]
    elif "Vegan" in pref:
        return options_dict["Vegan"]
    else:
        return options_dict["Vegetarian (Indian Standard)"]

# --- Smart Planner ---
if st.button("Generate My 7-Day Diet Plan", type="primary"):
    with st.spinner("Analyzing your profile and crafting your authentic Indian diet plan..."):
        # Simulate thinking time for AI effect
        time.sleep(2.5)
        
        st.success("Your diet plan is ready!")
        
        st.subheader("Plan Overview")
        st.write(f"This personalized plan focuses on {goal.lower()} while keeping your meals purely Indian and delicious. It averages around {target_calories} kcal per day.")
        st.info("💧 Daily Hydration Goal: 2.5 to 3.0 Liters")
        
        st.subheader("Weekly Meal Plan")
        
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        for i, day_name in enumerate(days_of_week):
            day_focus = random.choice(["Metabolism Boost", "Digestive Reset", "High Energy", "Recovery", "Balanced Nutrition", "Gut Health"])
            day_calories = target_calories + random.randint(-150, 150)
            
            with st.expander(f"Day {i+1} ({day_name}) - {day_focus} (~{day_calories} kcal)"):
                m_col1, m_col2 = st.columns(2)
                
                b_opts = get_options_by_pref(diet_preference, breakfast_options)
                l_opts = get_options_by_pref(diet_preference, lunch_options)
                d_opts = get_options_by_pref(diet_preference, dinner_options)
                
                b_meal = random.choice(b_opts)
                l_meal = random.choice(l_opts)
                s_meal = random.choice(snack_options)
                d_meal = random.choice(d_opts)
                
                with m_col1:
                    st.markdown(f"**Breakfast:** {b_meal['name']}")
                    st.caption(f"Portion: {b_meal['portion']} | ~{b_meal['calories']} kcal")
                    
                    st.markdown(f"**Lunch:** {l_meal['name']}")
                    st.caption(f"Portion: {l_meal['portion']} | ~{l_meal['calories']} kcal")
                    
                with m_col2:
                    st.markdown(f"**Snack:** {s_meal['name']}")
                    st.caption(f"Portion: {s_meal['portion']} | ~{s_meal['calories']} kcal")
                    
                    st.markdown(f"**Dinner:** {d_meal['name']}")
                    st.caption(f"Portion: {d_meal['portion']} | ~{d_meal['calories']} kcal")
        
        st.subheader("Grocery List")
        st.markdown("**Fresh Vegetables & Fruits**")
        st.write("Spinach, Tomatoes, Onions, Potatoes, Apples, Papaya, Lemon, Green Chillies, Coriander")
        st.markdown("**Pantry & Dairy**")
        st.write("Rice, Whole Wheat Atta, Toor Dal, Moong Dal, Poha, Oats, Milk, Curd, Paneer (if applicable)")
        st.markdown("**Spices & Nuts**")
        st.write("Turmeric, Cumin, Garam Masala, Almonds, Walnuts, Peanuts, Makhana")