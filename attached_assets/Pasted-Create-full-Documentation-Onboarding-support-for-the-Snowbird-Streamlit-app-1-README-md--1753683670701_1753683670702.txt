Create full Documentation & Onboarding support for the Snowbird Streamlit app.

1. **README.md** (at project root)
   - Title & tagline
   - Project overview: what Snowbird does and who it’s for
   - Prerequisites & installation: Python version, `pip install -r requirements.txt`
   - Configuration: `.env` or Replit secrets setup
   - Running the app: `streamlit run main.py`
   - Testing: `pytest` instructions
   - CI/CD: link to GitHub Actions workflow
   - Theming, Analytics, Auth, Reporting—brief feature list
   - Contributing link

2. **CONTRIBUTING.md** (at project root)
   - Code style guidelines: Black, Flake8, docstring conventions
   - Branching workflow: `main` vs feature branches, PR process
   - How to write tests & run them
   - Issue templates: bug report & feature request (include markdown examples)
   - Code of conduct (optional)

3. **Inline Code Comments & Docstrings**
   - Go through `/utils/` and `/pages/` files
   - Add module-level docstrings summarizing purpose
   - Add function docstrings: `Args`, `Returns`, `Raises`
   - Add inline comments for non-obvious logic (e.g. tax threshold calculations, onboarding state)

4. **In-App Onboarding Carousel**  
   - Create a new file `utils/onboarding.py` with a list of steps:
     ```python
     STEPS = [
       {"title": "Welcome to Snowbird", "body": "Track days in each state, manage budgets, and get AI help."},
       {"title": "Log Your Days",    "body": "Tap to log today’s location and watch your tax risk."},
       {"title": "Manage Budgets",    "body": "Set utilities, insurance & HOA budgets for each home."},
       {"title": "Ask Snowbird AI",   "body": "Ask any financial question, anytime."},
     ]
     ```
   - In `main.py`, detect first-time users via `st.session_state.onboarded` flag:
     - If not set, display a Streamlit `st.beta_expander` or multi-page carousel:
       ```python
       import streamlit as st
       from utils.onboarding import STEPS

       if not st.session_state.get("onboarded", False):
           for step in STEPS:
               st.subheader(step["title"])
               st.write(step["body"])
               st.button("Next", key=step["title"])
           st.session_state.onboarded = True
           st.experimental_rerun()
       ```
   - Ensure it only shows once per user session

5. **Update README.md** to reference the onboarding flow and where to find documentation.

Result: a polished documentation suite and in-app welcome carousel so new users and contributors get up and running immediately.
