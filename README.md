
# NAMAF Claim Verifier App

This Streamlit app verifies medical claims against NAMAF rules, checking for:
- Invalid or unlisted codes
- Overcharges above NAMAF tariffs
- Wrong provider types
- Duplicate claims

## 🚀 How to Run

### 🔹 Option 1: Local Machine
1. Install requirements:
```
pip install -r requirements.txt
```
2. Run the app:
```
streamlit run app.py
```

### 🔹 Option 2: Free Hosting on Streamlit Cloud
1. Push this folder to a public GitHub repository.
2. Go to https://streamlit.io/cloud and link the repo.
3. Launch the app for free!

## 📂 Required Files
- `namaf_rules.csv` — extracted NAMAF code rules
- `sample_claims.xlsx` — claims to verify
