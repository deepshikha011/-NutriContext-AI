# NutriContext AI - Detailed File Architecture Guide 🏗️

**For Technical Interviews & Deep Dives**  
*Architecture breakdown of each file, responsibilities, key code patterns, & interactions*

## 📋 File Structure Overview
```
NutriContext-AI/
├── app.py              [Main Entry - MVC Controller]
├── ai_engine.py        [AI Layer - Gemini Vision]
├── database.py         [Data Layer - PostgreSQL CRUD]
├── auth.py             [Auth Layer - bcrypt/session]
├── logic.py            [Business Logic - Rules/Warnings]
├── dashboard.py        [UI Layer - Analytics/Charts]
├── requirements.txt    [Dependencies]
├── runtime.txt         [Heroku/Platform]
└── .streamlit/config.toml | secrets.toml [Streamlit Config]
```

---

## 1. `app.py` - **Main Application Controller** (MVC: Controller + Router)
**Purpose**: Entry point, page routing, session state, UI orchestration.

**Key Components**:
- **Config**: `st.set_page_config()`, custom dark CSS
- **Init**: `init_db()`, auth gate (`show_auth_page()` → session_state.user)
- **Sidebar**: User info, page radio (`Log Meal`/`Dashboard`/`Profile`), logout
- **Pages** (conditional rendering):
  | Page | Functionality |
  |------|---------------|
  | 🍽️ Log Meal | File upload → `analyze_meal()` → metrics → `log_meal()` → DB |
  | 📊 Dashboard | `show_dashboard(user)` → charts from DB |
  | ⚙️ Profile | Form → `update_profile()` → session sync |

**Architecture Pattern**: Single-file Streamlit SPA with sidebar navigation.
**Dependencies**: All other modules imported at top.

**Interview Q**: *How does state flow?* → File upload → ai_engine → logic → database → UI metrics.

---

## 2. `ai_engine.py` - **AI Intelligence Layer**
**Purpose**: Gemini Vision model integration for meal photo → nutrition JSON.

**Key Code**:
```python
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash", safety_settings=...)
```
- **Prompt Engineering**: Structured JSON output (food_name, calories, macros, health_score, verdict, smart_swap).
- **Error Handling**: JSON parse fallback → `{"error": "..."}`
- **Input**: PIL Image + user goal/context.
- **Output**: Dict (calories:int, protein_g:float, health_score:0-100, etc.)

**Strengths**: Zero-shot prompting, vision capabilities, safety filters.
**Interview Q**: *Rate limiting/retries?* → Production: Add exponential backoff.

---

## 3. `database.py` - **Data Persistence Layer**
**Purpose**: PostgreSQL ORM-less CRUD for users/meals.

**Key Functions**:
| Function | Params | Returns | Purpose |
|----------|--------|---------|---------|
| `init_db()` | - | - | Create tables (users, meals) |
| `log_meal(...)` | user_id, food_name, calories, ... | - | INSERT meal log |
| `update_profile(user_id, goal, calories)` | id, goal, calories | - | UPDATE users |
| Others: `get_user()`, `user_exists()`, `register_user()` | | | Auth helpers |

**Connection**: Global `conn = psycopg2.connect(...)` (env vars ideal).
**SQL**: Raw queries with param binding (`%s` placeholders, `execute()`).

**Interview Q**: *SQL Injection?* → Safe (parametrized). *Scaling?* → Add SQLAlchemy/indexes.

---

## 4. `auth.py` - **Authentication Layer**
**Purpose**: Simple username/password system.

**Key Functions**:
- `show_auth_page()`: Login/register forms → session_state validation.
- `hash_password(pwd)` / `check_password(pwd, hash)`: bcrypt.
- Flow: Form submit → DB check → `st.session_state.user = {...}` → `st.rerun()`.

**Security**: bcrypt (salt rounds default), no sessions/cookies (Streamlit ephemeral).
**Interview Q**: *OAuth/JWT upgrade?* → Yes, for production.

---

## 5. `logic.py` - **Business Rules Engine**
**Purpose**: Non-AI logic (warnings, context detection).

**Key Functions**:
- `get_meal_context()`: Time/activity-based (morning/workout/etc.)
- `get_warning(food, context, goal, cal, score)`: Rule-based alerts (e.g., high-carb post-workout).

**Pattern**: If-else rules → human-readable strings.
**Extensible**: Add ML models or more rules.

---

## 6. `dashboard.py` - **Analytics UI Layer**
**Purpose**: Charts/tables from DB queries.

**Functions**:
- `show_dashboard(user)`: Pandas queries → Plotly metrics (daily calories, avg score).

**Interview Q**: *Real-time?* → Cache queries, WebSockets upgrade.

---

## 🔄 **Data Flow Diagram**
```
User Upload (app.py) 
  ↓
Gemini AI (ai_engine.py) → JSON Nutrition
  ↓ 
Logic Rules (logic.py) → Warnings/Swaps
  ↓
DB Persist (database.py)
  ↓ 
Dashboard Charts (dashboard.py)
```

## 🎯 **Design Decisions**
- **Monolith**: Single Streamlit app (easy deploy).
- **JSON Strict**: AI output parsing (prompt engineering).
- **Ephemeral State**: Streamlit sessions (DB for persistence).
- **Dark Theme**: Custom CSS injection.

## 🚀 **Production Considerations**
- Env vars for DB/API keys
- Rate limiting (Gemini)
- Image preprocessing (resize/compress)
- Caching (`@st.cache_data`)
- Monitoring (Sentry)

**Perfect for interviews: Demonstrates full-stack AI app!** 🎤

