
import streamlit as st
import pandas as pd

st.set_page_config(page_title="NAMAF Claim Verifier", layout="wide")
st.title("🏥 NAMAF Claim Verification App")

rules_file = st.file_uploader("Upload NAMAF Rules CSV", type=["csv"])
claims_file = st.file_uploader("Upload Claims Excel File", type=["xlsx", "xls"])

if rules_file and claims_file:
    rules_df = pd.read_csv(rules_file)
    claims_df = pd.read_excel(claims_file)

    def verify_claim(row):
        reasons = []
        code = str(row['Item Code']).strip()
        amount = row['Claimed Amount']
        provider = str(row['Service Provider Type']).strip()
        invoice = row.get('Invoice Number', 'Unknown')
        service_date = row.get('Service Date', 'Unknown')

        match = rules_df[rules_df['Code'].astype(str).str.strip() == code]

        if match.empty:
            reasons.append("Invalid code")
        else:
            rule = match.iloc[0]
            if amount > rule['MaxAmount']:
                reasons.append(f"Overcharge: Claimed N${amount} > Max N${rule['MaxAmount']}")
            if provider not in rule['ProviderTypeAllowed'].split(','):
                reasons.append(f"Provider '{provider}' not allowed for Code {code}")

        # Duplicate check
        is_duplicate = ((claims_df['Item Code'] == row['Item Code']) & 
                        (claims_df['Claimed Amount'] == row['Claimed Amount']) & 
                        (claims_df['Service Date'] == row['Service Date']) & 
                        (claims_df['Invoice Number'] == row['Invoice Number'])).sum() > 1
        if is_duplicate:
            reasons.append(f"Duplicate: Same code, amount, date, invoice ({invoice})")

        return "✅ Verified" if not reasons else "❌ " + " | ".join(reasons)

    claims_df['Verification Result'] = claims_df.apply(verify_claim, axis=1)
    st.success("Verification complete!")
    st.dataframe(claims_df)

    st.download_button("📥 Download Verified Claims", data=claims_df.to_csv(index=False).encode('utf-8'),
                       file_name="verified_claims.csv", mime="text/csv")
