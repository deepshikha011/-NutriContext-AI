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
