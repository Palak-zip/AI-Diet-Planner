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

# --- Expanded Mock Data Generators ---
breakfast_options = {
    "Vegetarian (Indian Standard)": [
        {"name": "Vegetable Poha with Roasted Peanuts & Lemon", "portion": "1 large bowl", "calories": 320},
        {"name": "Upma (Semolina) with Carrots, Peas & Cashews", "portion": "1 bowl", "calories": 300},
        {"name": "Idli with Sambar and Coconut Chutney", "portion": "3 idlis, 1 bowl sambar", "calories": 350},
        {"name": "Aloo Paratha with Low-Fat Curd", "portion": "1 paratha, 1/2 bowl curd", "calories": 380},
        {"name": "Methi Thepla with Mango Pickle & Yogurt", "portion": "2 theplas", "calories": 310},
        {"name": "Vermicelli (Sevai) Upma with Veggies", "portion": "1 bowl", "calories": 290},
        {"name": "Oats Idli with Tangy Tomato Chutney", "portion": "3 idlis", "calories": 280},
        {"name": "Moong Dal Chilla (Crepes) with Mint Chutney", "portion": "2 chillas", "calories": 280},
        {"name": "Dalia (Broken Wheat) Porridge with Milk & Almonds", "portion": "1 bowl", "calories": 270},
        {"name": "Besan Chilla stuffed with Paneer", "portion": "2 chillas", "calories": 350},
        {"name": "Sprouted Moong Salad with Lemon & Black Pepper", "portion": "1 large bowl", "calories": 200},
        {"name": "Ragi Dosa with Onion Tomato Chutney", "portion": "2 dosas", "calories": 310}
    ],
    "Non-Vegetarian": [
        {"name": "Masala Omelette with 2 Slices Brown Bread", "portion": "2 eggs", "calories": 350},
        {"name": "Chicken Sausage Stir-fry with Scrambled Eggs", "portion": "1 plate", "calories": 400},
        {"name": "Egg Bhurji (Scrambled) with 2 Wheat Rotis", "portion": "2 eggs", "calories": 380},
        {"name": "Hard Boiled Eggs with Avocado on Multigrain Toast", "portion": "2 eggs, 1 toast", "calories": 330},
        {"name": "Chicken Kheema stuffed Wheat Paratha", "portion": "1 paratha", "calories": 420},
        {"name": "Appam with Egg Roast (Kerala Style)", "portion": "2 appams", "calories": 390},
        {"name": "Egg Dosa with Sambar", "portion": "1 large dosa", "calories": 340}
    ],
    "Vegan": [
        {"name": "Moong Dal Chilla with Green Coriander Chutney", "portion": "2 chillas", "calories": 280},
        {"name": "Oats Porridge cooked in Almond Milk with Fruits", "portion": "1 bowl", "calories": 250},
        {"name": "Besan Chilla (Chickpea Flour) with Veggies", "portion": "2 chillas", "calories": 300},
        {"name": "Tofu Scramble with Turmeric & Whole Wheat Toast", "portion": "1 bowl tofu, 2 slices", "calories": 320},
        {"name": "Green Smoothie Bowl (Banana, Spinach, Chia Seeds)", "portion": "1 large bowl", "calories": 290},
        {"name": "Pesarattu (Green Gram Dosa) with Allam Chutney", "portion": "2 dosas", "calories": 310},
        {"name": "Vegan Poha with Extra Green Peas", "portion": "1 bowl", "calories": 280}
    ]
}

lunch_options = {
    "Vegetarian (Indian Standard)": [
        {"name": "Dal Tadka, Jeera Rice, and Mix Veg Sabzi", "portion": "1 bowl dal, 1 cup rice, 1/2 cup sabzi", "calories": 550},
        {"name": "Rajma Chawal with Kachumber Salad", "portion": "1 big bowl", "calories": 600},
        {"name": "Paneer Butter Masala with 2 Whole Wheat Rotis", "portion": "1 bowl paneer, 2 rotis", "calories": 650},
        {"name": "Kadhi Pakora with Brown Rice", "portion": "1 bowl kadhi, 1 cup rice", "calories": 520},
        {"name": "Chole Bhature (Baked/Air-fried Bhature)", "portion": "1 bowl chole, 2 bhature", "calories": 580},
        {"name": "Vegetable Biryani with Cucumber Raita", "portion": "1 big bowl", "calories": 500},
        {"name": "Mushroom Matar Malai with 2 Phulkas", "portion": "1 bowl sabzi, 2 rotis", "calories": 520},
        {"name": "Soya Chunk Pulao with Mint Raita", "portion": "1 big plate", "calories": 480},
        {"name": "Aloo Gobi, 2 Rotis, and Sprout Salad", "portion": "1 bowl sabzi, 2 rotis", "calories": 450},
        {"name": "Sambhar, Brown Rice, and Cabbage Poriyal", "portion": "1 plate", "calories": 490}
    ],
    "Non-Vegetarian": [
        {"name": "Chicken Curry (Home-style) with Rice & Onion Salad", "portion": "1 bowl chicken, 1 cup rice", "calories": 600},
        {"name": "Fish Tikka Masala with 2 Whole Wheat Rotis", "portion": "1 bowl fish, 2 rotis", "calories": 550},
        {"name": "Mutton Rogan Josh with Basmati Rice", "portion": "1 bowl mutton, 1 cup rice", "calories": 700},
        {"name": "Egg Curry with Quinoa and Salad", "portion": "2 eggs in gravy, 1 cup quinoa", "calories": 520},
        {"name": "Chicken Biryani with Mirchi ka Salan", "portion": "1 medium plate", "calories": 650},
        {"name": "Malabar Fish Curry with Brown Rice", "portion": "1 bowl, 1 cup rice", "calories": 540},
        {"name": "Chicken Sukka with 2 Neer Dosas", "portion": "1 plate", "calories": 580}
    ],
    "Vegan": [
        {"name": "Chickpea Curry (Pindi Chole) with Brown Rice", "portion": "1 bowl chole, 1 cup rice", "calories": 500},
        {"name": "Tofu Matar with 2 Multigrain Rotis", "portion": "1 bowl tofu, 2 rotis", "calories": 480},
        {"name": "Soya Chunk Curry with Quinoa", "portion": "1 bowl soya, 1 cup quinoa", "calories": 450},
        {"name": "Bhindi Masala (Okra) with 2 Jowar Rotis", "portion": "1 bowl bhindi, 2 rotis", "calories": 400},
        {"name": "Lentil Soup (Yellow Dal) with Roasted Sweet Potato", "portion": "1 bowl dal, 1 potato", "calories": 420},
        {"name": "Vegetable Pulao with Roasted Papad", "portion": "1 plate", "calories": 380},
        {"name": "Baingan Bharta with 2 Bajra Rotis", "portion": "1 bowl bharta, 2 rotis", "calories": 410}
    ]
}

snack_options = [
    {"name": "Roasted Makhana (Fox Nuts) with Peri Peri", "portion": "1 small bowl", "calories": 120},
    {"name": "Sprout Salad with Lemon, Onion, Tomato & Chaat Masala", "portion": "1 bowl", "calories": 150},
    {"name": "Handful of Mixed Nuts (Almonds, Walnuts, Pistachios)", "portion": "30g", "calories": 180},
    {"name": "Fresh Fruit Bowl (Apple, Papaya, Guava, Pomegranate)", "portion": "1 large bowl", "calories": 100},
    {"name": "Masala Oats with finely chopped veggies", "portion": "1 small bowl", "calories": 160},
    {"name": "Roasted Chana (Chickpeas) with black salt", "portion": "1 small bowl", "calories": 140},
    {"name": "Boiled Sweet Corn Chaat with lemon and chili", "portion": "1 small cup", "calories": 110},
    {"name": "Buttermilk (Chaas) with roasted cumin powder", "portion": "1 tall glass", "calories": 70},
    {"name": "Green Tea with 2 Multigrain Digestive Biscuits", "portion": "1 cup", "calories": 90},
    {"name": "Bhel Puri (dry, no sweet chutney)", "portion": "1 small bowl", "calories": 160},
    {"name": "Roasted Peanut Salad (Peanut Chaat)", "portion": "1 small bowl", "calories": 190},
    {"name": "Sattu Drink (Roasted Gram Flour cooler)", "portion": "1 glass", "calories": 130}
]

dinner_options = {
    "Vegetarian (Indian Standard)": [
        {"name": "Palak Paneer with 2 Whole Wheat Rotis", "portion": "1 bowl palak, 2 rotis", "calories": 500},
        {"name": "Moong Dal Khichdi with a dollop of Ghee & Pickle", "portion": "1 plate", "calories": 450},
        {"name": "Lauki (Bottle Gourd) Ki Sabzi with 2 Rotis", "portion": "1 bowl sabzi, 2 rotis", "calories": 350},
        {"name": "Aloo Gobi with 2 Phulkas and Dal", "portion": "1 bowl sabzi, 1 bowl dal, 2 phulkas", "calories": 480},
        {"name": "Stuffed Bell Peppers (Capsicum) with 1 Roti", "portion": "2 pieces, 1 roti", "calories": 380},
        {"name": "Mixed Vegetable Soup and Grilled Paneer Tikka", "portion": "1 bowl soup, 4 pieces tikka", "calories": 360},
        {"name": "Dal Makhani (low cream) with 2 Missi Rotis", "portion": "1 bowl dal, 2 rotis", "calories": 510}
    ],
    "Non-Vegetarian": [
        {"name": "Grilled Chicken Breast with Sautéed Broccoli & Carrots", "portion": "1 breast, 1 cup veg", "calories": 450},
        {"name": "Light Egg Curry with 2 Rotis", "portion": "2 eggs, 2 rotis", "calories": 500},
        {"name": "Baked Fish (Pomfret/Bhetki) with Cucumber Tomato Salad", "portion": "1 fillet, 1 bowl salad", "calories": 400},
        {"name": "Chicken Tikka (Dry, Tandoori style) with Mint Chutney", "portion": "6 big pieces", "calories": 350},
        {"name": "Mutton Keema with 1 Roti and Onion Rings", "portion": "1 small bowl, 1 roti", "calories": 550},
        {"name": "Prawn Curry (Coconut milk base) with Brown Rice", "portion": "1 bowl prawn, 1/2 cup rice", "calories": 490}
    ],
    "Vegan": [
        {"name": "Mixed Dal (Panchratna) with 2 Rotis", "portion": "1 bowl dal, 2 rotis", "calories": 400},
        {"name": "Baingan Bharta (Roasted Eggplant) with Bajra Roti", "portion": "1 bowl bharta, 1 roti", "calories": 380},
        {"name": "Vegetable Dalia (Savoury Broken Wheat)", "portion": "1 big bowl", "calories": 350},
        {"name": "Creamy Pumpkin Soup with Sautéed Tofu Cubes", "portion": "1 bowl soup, 100g tofu", "calories": 320},
        {"name": "Mushroom Matar with 2 Ragi Rotis", "portion": "1 bowl sabzi, 2 rotis", "calories": 410},
        {"name": "Cabbage and Peas Stir-fry with 2 Rotis", "portion": "1 large bowl, 2 rotis", "calories": 370}
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

# --- State Management ---
if "diet_plan" not in st.session_state:
    st.session_state.diet_plan = None

# --- Smart Planner ---
if st.button("Generate My 7-Day Diet Plan", type="primary"):
    with st.spinner("Analyzing your profile and crafting a unique authentic Indian diet plan..."):
        time.sleep(1.5) # Fake AI loading time
        
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        generated_plan = []
        
        for i, day_name in enumerate(days_of_week):
            day_focus = random.choice(["Metabolism Boost", "Digestive Reset", "High Energy", "Recovery", "Balanced Nutrition", "Gut Health"])
            day_calories = target_calories + random.randint(-150, 150)
            
            b_opts = get_options_by_pref(diet_preference, breakfast_options)
            l_opts = get_options_by_pref(diet_preference, lunch_options)
            d_opts = get_options_by_pref(diet_preference, dinner_options)
            
            # Select random meals for the day
            b_meal = random.choice(b_opts)
            l_meal = random.choice(l_opts)
            s_meal = random.choice(snack_options)
            d_meal = random.choice(d_opts)
            
            generated_plan.append({
                "day_name": day_name,
                "focus": day_focus,
                "calories": day_calories,
                "meals": {
                    "breakfast": b_meal,
                    "lunch": l_meal,
                    "snack": s_meal,
                    "dinner": d_meal
                }
            })
            
        st.session_state.diet_plan = generated_plan

# --- Display Plan ---
if st.session_state.diet_plan:
    st.success("Your diet plan is ready!")
    
    st.subheader("Plan Overview")
    st.write(f"This personalized plan focuses on {goal.lower()} while keeping your meals purely Indian and delicious. It averages around {target_calories} kcal per day.")
    st.info("💧 Daily Hydration Goal: 2.5 to 3.0 Liters")
    
    st.subheader("Weekly Meal Plan")
    
    for i, day in enumerate(st.session_state.diet_plan):
        with st.expander(f"Day {i+1} ({day['day_name']}) - {day['focus']} (~{day['calories']} kcal)"):
            m_col1, m_col2 = st.columns(2)
            
            meals = day['meals']
            
            with m_col1:
                st.markdown(f"**Breakfast:** {meals['breakfast']['name']}")
                st.caption(f"Portion: {meals['breakfast']['portion']} | ~{meals['breakfast']['calories']} kcal")
                
                st.markdown(f"**Lunch:** {meals['lunch']['name']}")
                st.caption(f"Portion: {meals['lunch']['portion']} | ~{meals['lunch']['calories']} kcal")
                
            with m_col2:
                st.markdown(f"**Snack:** {meals['snack']['name']}")
                st.caption(f"Portion: {meals['snack']['portion']} | ~{meals['snack']['calories']} kcal")
                
                st.markdown(f"**Dinner:** {meals['dinner']['name']}")
                st.caption(f"Portion: {meals['dinner']['portion']} | ~{meals['dinner']['calories']} kcal")
    
    st.subheader("Grocery List")
    st.markdown("**Fresh Vegetables & Fruits**")
    st.write("Spinach, Tomatoes, Onions, Potatoes, Apples, Papaya, Lemon, Green Chillies, Coriander, Cucumber, Capsicum")
    st.markdown("**Pantry & Dairy**")
    st.write("Rice, Whole Wheat Atta, Toor Dal, Moong Dal, Poha, Oats, Milk, Curd, Paneer (if applicable)")
    st.markdown("**Spices & Nuts**")
    st.write("Turmeric, Cumin, Garam Masala, Almonds, Walnuts, Peanuts, Makhana, Roasted Chana")
