# NutriContext AI - Interview Questions & Answers 📝

**Technical Deep Dive Q&A**  
*Based on ARCHITECTURE.md – Production-grade answers for FAANG+ interviews*

## 🎯 **Architecture & Design (High-Level)**

**Q1: Describe the overall system architecture?**  
A: **Event-driven SPA** with Streamlit monolith:  
- **Layers**: UI (app.py) → AI (ai_engine.py) → Logic (logic.py) → Data (database.py).  
- **Flow**: Photo upload triggers Gemini Vision → JSON parse → Rules → DB persist → Dashboard.  
- **State**: Session (ephemeral) + PostgreSQL (persistent).  
**Strength**: Rapid prototyping; **Tradeoff**: Horizontal scale needs refactoring.

**Q2: Why Streamlit over Flask/React?**  
A: **Pros**: Zero boilerplate (dataframes → charts), built-in auth/sidebar, auto-reload. **Cons**: Less control (custom routing/SSR). Ideal for AI demos/ML prototypes.

**Q3: Deployment strategy?**  
A: **Streamlit Cloud** (GitHub-integrated, secrets mgmt). Alt: Docker → Heroku/EC2. **Scaling**: Multiple replicas + Redis cache.

---

## 🤖 **AI/ML Integration**

**Q4: How does Gemini prompting work? Why JSON strict format?**  
A: Structured prompt with exact JSON schema → `json.loads(response.text)`. Strips markdown fences. **Benefits**: Parseable, no hallucinations in structure. **Edge**: Add Pydantic validation.

**Q5: Vision model choice? Cost/performance?**  
A: Gemini 2.5 Flash (fast, multimodal). ~$0.35/1M tokens. **Batch alt**: Vertex AI for scale. **Prompt tips**: Context injection (user goal/time).

**Q6: What if AI JSON fails? Production handling?**  
A: Try-except → fallback `{"error": e}`. **Prod**: Retry (exp backoff), fallback model (GPT-4o-mini), cache similar meals.

---

## 💾 **Data & Database**

**Q7: Why raw psycopg2 vs SQLAlchemy/ORM?**  
A: **Simplicity** (no migrations overhead), direct control. **Upgrade path**: Alembic + SQLAlchemy. Queries parametrized (`%s`) → no injection.

**Q8: Schema design? Indexes?**  
A: `users(id, username, goal, calories)`, `meals(user_id, timestamp, food_name, nutrition JSONB?, score)`. **Index**: `user_id, timestamp` for dashboard queries.

**Q9: Analytics queries complexity?**  
A: Pandas aggregations post-fetch (`df.groupby('date').sum()`). **Optimized**: DB views/materialized + Plotly Express.

---

## 🔐 **Security & Auth**

**Q10: Auth mechanism? Vulnerabilities?**  
A: bcrypt hash + username DB lookup. **Streamlit caveat**: Session state resets on refresh → stateless. **Fix**: JWT cookies or Supabase Auth.

**Q11: Secrets handling?**  
A: `.streamlit/secrets.toml` (gitignored). **Prod**: Env vars/AWS Secrets Manager.

**Q12: File upload security?**  
A: PIL `convert('RGB')`, Streamlit uploader limits. **Add**: Virus scan (ClamAV), size/type validation.

---

## ⚡ **Performance & Scaling**

**Q13: Cold starts? Caching strategy?**  
A: `@st.cache_data` for DB queries/AI (TTL=3600). **Gemini**: Cache embeddings of common foods.

**Q14: Concurrent users?**  
A: Streamlit single-threaded → Gunicorn workers. **Horizontal**: Separate API (FastAPI) + frontend.

**Q15: Image handling optimizations?**  
A: Resize (1280px max), thumbor/Cloudinary CDN.

---

## 🎨 **UI/UX & Frontend**

**Q16: Custom styling approach?**  
A: `st.markdown("""<style>...</style>""")` → Scoped CSS. Targets `.stMetric`, `.result-card`.

**Q17: Responsive design? Mobile?**  
A: `layout="wide"`, column grids. **Mobile**: Test + media queries.

---

## 🧪 **Testing & Monitoring**

**Q18: Test coverage? Types?**  
A: **Unit**: Pytest (prompt parsing, logic rules). **E2E**: Playwright (upload → DB). **AI**: Mock responses.

**Q19: Error tracking? Logging?**  
A: `st.error()`, Sentry integration. Logs to file/DB.

---

## 🚀 **Deployment & CI/CD**

**Q20: Streamlit Cloud workflow?**  
A: GitHub webhook → auto-deploy. Secrets injected UI. **Custom**: GitHub Actions → Docker → Railway.

**Q21: Domain/SSL?**  
A: Streamlit subdomain free. **Custom**: Cloudflare → app.streamlit.io.

---

## 🔮 **Future Enhancements**

**Q22: V2 Features?**  
- Computer Vision alternatives (YOLO + NutritionNet).
- User trends ML (anomaly detection).
- Multi-language prompts.
- Wearable integration (calories from Fitbit).

**Perfect interview prep: Code walkthrough + whiteboard architecture!** 🎯

## 📁 **Per-File Deep Dives + Interview Q&A**

### 1. `app.py` - Main Controller (~250 lines)
**Detailed Explanation**:
- **Lines 1-10**: Imports (Streamlit, PIL, all modules).
- **12-25**: Page config + dark CSS injection (scoped selectors like `[data-testid="stAppViewContainer"]`).
- **27**: `init_db()` ensures schema.
- **30-35**: Auth gate - if no `session_state.user`, show login → `st.stop()`.
- **Sidebar (38-50)**: Dynamic user info from session + page selector.
- **Log Meal Page**: File uploader → `analyze_meal(image)` → display metrics (st.columns/st.metric) → `log_meal()` → success.
- **State Mutations**: `st.session_state.user` updates trigger `st.rerun()`.

**Key Pattern**: Conditional page rendering based on sidebar radio.

**Q23: Why `st.rerun()` after auth/profile update?**  
A: Forces full page refresh to reflect session changes (Streamlit reactivity limitation).

**Q24: How handle concurrent uploads/sessions?**  
A: Streamlit locks per-session; production → async queues (Celery).

**Q25: Custom CSS limitations?**  
A: Scoped only (no global styles). Alt: `components.html()` or React.

### 2. `ai_engine.py` - Gemini AI Core (~50 lines)
**Detailed Explanation**:
- **Global model**: `GenerativeModel('gemini-2.5-flash')` with safety (BLOCK_MEDIUM_AND_ABOVE).
- **Prompt**: 20-line template with JSON schema + dynamic `{goal}`/ `{context}` injection.
- **Generate**: `[prompt, image]` multimodal → text strip ```json → `json.loads()`.
- **Fallback**: Comprehensive except covering JSONDecodeError/IndexError.

**Key Pattern**: JSON-forcing to avoid LLM hallucinations in structure.

**Q26: Why not function calling/tools?**  
A: Gemini structured outputs unstable; JSON prompt more reliable for vision.

**Q27: Token usage optimization?**  
A: Short prompt, image auto-compressed. Monitor via `response.usage_metadata`.

**Q28: Multi-model fallback?**  
A: Configurable; Claude/GPT as backup if Gemini rate-limited.

### 3. `database.py` - Postgres Layer
**Detailed Explanation**:
- **Global conn**: `psycopg2.connect(DSN)` (hardcoded → env refactor).
- **init_db()**: `CREATE TABLE IF NOT EXISTS` for users (id SERIAL PK, username UNIQUE) + meals (user_id FK, JSON nutrition?).
- **CRUD**: Param lists `%s`, `executemany()` batches possible.
- No transactions explicit → add for profile+log atomicity.

**Q29: Connection pooling?**  
A: psycopg2.ConnectionPool. Streamlit → `@st.cache_resource`.

**Q30: Migration strategy?**  
A: Alembic/Flyway. Current: Manual SQL in init_db.

### 4. `auth.py`, `logic.py`, `dashboard.py` - Helpers
**auth.py**: bcrypt wrapper + form handlers → DB ops.
**logic.py**: Timezone-aware context (`datetime.now()`) + if-else warnings.
**dashboard.py**: `pd.read_sql()` → `plotly.express` (bar/line for trends).

**Q31: Why separate logic.py? SRP?**  
A: Yes, app.py not bloated. Testable pure functions.

**Q32: Dashboard perf for 10k logs?**  
A: Paginate, DB aggregates (`GROUP BY date`), Vega-Lite.

## 🎓 **Interview Mastery Tips**
- Demo live: `streamlit run app.py` + upload meal.
- Whiteboard: Draw data flow + bottlenecks.
- Tradeoffs: Every choice explained (speed vs scale).

**Now 30+ Qs – FAANG-ready!** 🚀
