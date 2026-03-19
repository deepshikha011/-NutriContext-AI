import streamlit as st
from PIL import Image
from database import init_db, log_meal, update_profile
from auth import show_auth_page
from ai_engine import analyze_meal
from logic import get_meal_context, get_warning
from dashboard import show_dashboard

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NutriContext AI",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Dark Mode Styling ─────────────────────────────────────────────────────────
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background-color: #0e1117; }
    [data-testid="stSidebar"] { background-color: #161b22; }
    .stMetric { background-color: #161b22; border-radius: 10px; padding: 10px; }
    .result-card {
        background-color: #161b22;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        border-left: 4px solid #00d4aa;
    }
    .warning-card {
        background-color: #2d1b1b;
        border-radius: 12px;
        padding: 15px;
        border-left: 4px solid #ff6b6b;
    }
    .swap-card {
        background-color: #1b2d1b;
        border-radius: 12px;
        padding: 15px;
        border-left: 4px solid #00d4aa;
    }
</style>
""", unsafe_allow_html=True)

# ── Init DB ───────────────────────────────────────────────────────────────────
init_db()

# ── Auth Gate ─────────────────────────────────────────────────────────────────
if "user" not in st.session_state:
    show_auth_page()
    st.stop()

user = st.session_state.user

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"### 👤 {user['username']}")
    st.markdown(f"**Goal:** {user['goal']}")
    st.markdown(f"**Target:** {user['target_calories']} kcal/day")
    st.divider()
    page = st.radio("Navigate", ["🍽️ Log Meal", "📊 Dashboard", "⚙️ Profile"])
    st.divider()
    if st.button("🚪 Logout", use_container_width=True):
        del st.session_state.user
        st.rerun()

# ── Pages ─────────────────────────────────────────────────────────────────────

if page == "🍽️ Log Meal":
    st.markdown("## 🍽️ Log Your Meal")
    st.markdown("Upload a photo of your meal and let AI analyze it for you.")

    uploaded = st.file_uploader("Upload Meal Image", type=["jpg", "jpeg", "png", "webp"])

    if uploaded:
        image = Image.open(uploaded).convert("RGB")
        col1, col2 = st.columns([1, 1])

        with col1:
            st.image(image, caption="Your Meal", use_column_width=True)
            meal_context = get_meal_context()
            st.info(f"🕐 Detected Context: **{meal_context}**")

        with col2:
            if st.button("🔍 Analyze with AI", use_container_width=True, type="primary"):
                with st.spinner("Analyzing your meal with Gemini AI..."):
                    result = analyze_meal(image, user["goal"], meal_context)

                if "error" in result:
                    st.error(f"AI Error: {result['error']}")
                else:
                    warning = get_warning(
                        result["food_name"], meal_context,
                        user["goal"], result["calories"], result["health_score"]
                    )
                    smart_swap = result.get("smart_swap")

                    # Display result card
                    st.markdown(f"""
                    <div class="result-card">
                        <h3>🍴 {result['food_name']}</h3>
                        <p>{result.get('verdict', '')}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("🔥 Calories", f"{result['calories']} kcal")
                    m2.metric("💪 Protein", f"{result['protein_g']}g")
                    m3.metric("🌾 Carbs", f"{result['carbs_g']}g")
                    m4.metric("🧈 Fats", f"{result['fats_g']}g")

                    score = result["health_score"]
                    score_color = "#00d4aa" if score >= 70 else "#ffd93d" if score >= 40 else "#ff6b6b"
                    st.markdown(f"**Health Score:** <span style='color:{score_color}; font-size:1.4em;'>{score}/100</span>", unsafe_allow_html=True)

                    if warning:
                        st.markdown(f'<div class="warning-card">{warning}</div>', unsafe_allow_html=True)

                    if smart_swap:
                        st.markdown(f'<div class="swap-card">💡 <b>Smart Swap:</b> {smart_swap}</div>', unsafe_allow_html=True)

                    # Save to DB
                    log_meal(
                        user_id=user["id"],
                        food_name=result["food_name"],
                        calories=result["calories"],
                        protein=result["protein_g"],
                        carbs=result["carbs_g"],
                        fats=result["fats_g"],
                        health_score=result["health_score"],
                        meal_context=meal_context,
                        warning=warning,
                        smart_swap=smart_swap
                    )
                    st.success("✅ Meal logged successfully!")


elif page == "📊 Dashboard":
    show_dashboard(user)


elif page == "⚙️ Profile":
    st.markdown("## ⚙️ Update Profile")
    with st.form("profile_form"):
        goal     = st.selectbox("Goal", ["Weight Loss", "Muscle Gain", "Keto", "Maintenance"], index=["Weight Loss", "Muscle Gain", "Keto", "Maintenance"].index(user["goal"]))
        calories = st.number_input("Daily Calorie Target (kcal)", min_value=500, max_value=5000, value=user["target_calories"], step=50)
        saved    = st.form_submit_button("Save Changes", use_container_width=True)

    if saved:
        update_profile(user["id"], goal, calories)
        st.session_state.user["goal"] = goal
        st.session_state.user["target_calories"] = calories
        st.success("Profile updated!")
        st.rerun()
