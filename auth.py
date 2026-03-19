import bcrypt
import streamlit as st
from database import create_user, get_user


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


def show_auth_page():
    st.markdown("<h1 style='text-align:center;'>🥗 NutriContext AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:gray;'>Your AI-powered nutrition companion</p>", unsafe_allow_html=True)
    st.divider()

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        _login_form()

    with tab2:
        _signup_form()


def _login_form():
    with st.form("login_form"):
        st.subheader("Welcome Back")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login", use_container_width=True)

    if submitted:
        if not username or not password:
            st.error("Please fill in all fields.")
            return
        user = get_user(username)
        if user and verify_password(password, user["password_hash"]):
            st.session_state.user = user
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password.")


def _signup_form():
    with st.form("signup_form"):
        st.subheader("Create Account")
        username = st.text_input("Choose a Username")
        password = st.text_input("Choose a Password", type="password")
        confirm  = st.text_input("Confirm Password", type="password")
        goal     = st.selectbox("Your Goal", ["Weight Loss", "Muscle Gain", "Keto", "Maintenance"])
        calories = st.number_input("Daily Calorie Target (kcal)", min_value=500, max_value=5000, value=2000, step=50)
        submitted = st.form_submit_button("Create Account", use_container_width=True)

    if submitted:
        if not username or not password:
            st.error("Please fill in all fields.")
            return
        if password != confirm:
            st.error("Passwords do not match.")
            return
        if len(password) < 6:
            st.error("Password must be at least 6 characters.")
            return
        hashed = hash_password(password)
        success = create_user(username, hashed, goal, calories)
        if success:
            st.success("Account created! Please log in.")
        else:
            st.error("Username already taken. Try another.")
