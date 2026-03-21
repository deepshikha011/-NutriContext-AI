# NutriContext AI - COMPLETE Line-by-Line Code Tutorial 👨‍💻

**From Scratch for Absolute Beginners**  
*Every line explained. No prior knowledge needed. Run `streamlit run app.py` after reading!*

## 🤔 **What is this project?**
A web app where you upload meal photos → AI tells calories/protein/health score → warns if bad for your diet goal → shows dashboard. **Magic?** No – just Python + AI API.

## 📂 **Prerequisites**
1. Install Python 3.10+
2. `pip install streamlit google-generativeai psycopg2-binary bcrypt pillow pandas plotly python-dotenv`
3. Get free [Gemini API key](https://aistudio.google.com/app/apikey) → `.streamlit/secrets.toml`
4. PostgreSQL DB (use Neon.tech free tier)

**Run**: `streamlit run app.py`

---

## 1. `app.py` - The Main App (Main Door 🚪)

**Purpose**: User interface. Like a website but in Python.

```
Line 1: import streamlit as st
# st = Streamlit library for web apps (no HTML/CSS/JS needed!)

Lines 2-6: from [module] import [function]
# Imports pieces from other files. app.py is "boss" calling workers.

Lines 9-11: st.set_page_config(...)
# Sets tab name "NutriContext AI", salad emoji icon, wide layout, sidebar open.

Lines 14-39: st.markdown("""<style>...</style>""")
# Injects custom dark CSS colors/borders for pretty "cards" (result/warning).

Line 42: init_db()
# Calls database.py to create tables (runs once).

Lines 45-48: if "user" not in st.session_state: show_auth_page(); st.stop()
# st.session_state = browser memory. No login? Show login, STOP app.

Line 50: user = st.session_state.user
# Logged-in user data {id:1, username:'bob', goal:'Loss'...}

Lines 53-66: with st.sidebar: ...
# Left sidebar: Shows user info, radio buttons for pages, logout button.
# del st.session_state.user + st.rerun() = restart fresh.

Lines 70-170: if page == "🍽️ Log Meal": ...
# BIG SECTION: File upload → AI → show results → save DB.
# - st.file_uploader(): Photo input
# - Image.open().convert("RGB"): Safe image processing
# - col1/col2: Split screen (photo | results)
# - st.button() → analyze_meal(image, goal, context)
# - st.metric(): Big numbers (calories etc.)
# - Custom HTML cards for verdict/warning/swap
# - log_meal(...): Save all data
```

**Beginner Tip**: Streamlit auto-updates UI when variables change!

---

## 2. `ai_engine.py` - AI Brain 🧠 (Gemini Magic)

**Purpose**: Sends photo to Google AI → gets nutrition numbers.

```
Line 1-3: imports
Line 5: genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
# Connects to Google's AI (your free API key from secrets.toml)

Lines 6-14: model = genai.GenerativeModel(...)
# Creates AI model, blocks harmful content.

Lines 16-50: def analyze_meal(image, goal, context):
# Main function. Input: photo + your diet info. Output: dict of numbers.
# - f""" prompt """: Long instruction telling AI "output ONLY JSON"
# - model.generate_content([prompt, image]): AI sees TEXT + PHOTO
# - text.strip(): Clean response
# - ``` stripping: AI adds code blocks sometimes
# - json.loads(): Turns text → Python dict {'calories': 450}
# - except: If JSON bad → error dict

**Key**: AI "sees" image + understands "Weight Loss goal = low calorie good".
```

---

## 3. `database.py` - Data Storage 🗄️ (Like Excel in Postgres)

**Purpose**: Save/load users/meals. Persistent memory.

```
Lines 1-3: imports
Lines 6-20: def get_connection():
# Secure DB connect using secrets.toml (host/port/user/pass)

Lines 23-49: def init_db():
# CREATE TABLE users/meals if missing. Runs first time.

Lines 52-67: def create_user(...):
# INSERT new user. Try-catch UNIQUE username conflict.

Lines 70-78: def get_user(username):
# SELECT user data by name.

Lines 81-89: def update_profile(...)
# UPDATE goal/calories.

Lines 92-104: def log_meal(...)
# INSERT meal row with ALL nutrition data.

Lines 107+: Query helpers (today meals, 7-day trends).
**SQL**: %s = safe parameters (no hacking).
```

---

## 4. `auth.py` - Login/Signup 🔐

```
Lines 1-2: bcrypt (password encryption), st
Line 5: hash_password(): Scramble password irreversibly
Line 9: verify_password(): Check scramble matches

Lines 12-16: show_auth_page(): Tabs Login/Signup

Line 18+: _login_form():
# st.form(): Group inputs + submit button
# get_user() + verify → session_state.user = login!

Line 36+: _signup_form():
# Extra checks (password match, length>6)
# hash + create_user → success message
```

---

## 5. `logic.py` - Smart Rules 🧮

```
Lines 3-21: get_meal_context(): Hour → "Breakfast"/"Dinner"
Lines 24-42: get_warning(...):
# If-else rules: Late snack + low score → warning string
# Goal-specific (Keto = low carb good)

Lines 45+: calculate_daily_health_score(): Blend calories vs target + avg meal score
```

---

## 6. `dashboard.py` - Charts 📊

```
Lines 1-5: Imports Pandas/Plotly for graphs
Lines 8+: show_dashboard(user):

Line 15-22: st.metric(): Today's calories vs target
Lines 25+: get_last_7_days() → Pandas df → charts

_calorie_trend_chart(): px.line() + target line
_health_score_chart(): Color-coded bars
_macro_breakdown_chart(): Stacked protein/carbs/fats
_pattern_insights(): Evening snack warnings
_today_meals_table(): Dataframe table

**Magic**: Pandas → Plotly auto-charts!
```

## 🎉 **How it ALL Works Together**
1. Open app.py → login → sidebar "Log Meal"
2. Upload photo → ai_engine → numbers
3. logic warns → database saves → dashboard shows trends

**secrets.toml**:
```
GEMINI_API_KEY = "AIza..."
database = {host=..., port=5432, ...}  # Neon DB
```

**Total LOC**: ~800. **Power**: Production AI app!

**Practice**: Change CSS colors, add new warnings. Run → upload your lunch photo! 🍲

**Now YOU understand every line!** 🎓

