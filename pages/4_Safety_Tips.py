import streamlit as st

st.set_page_config(page_title="Job Safety Tips", layout="wide")

st.markdown("<h1 style='color:#00C6FF;'>🛡️ Career Safety Center: Avoid Job Scams</h1>", unsafe_allow_html=True)
st.markdown("Stay alert. Stay safe. Here's how to protect yourself while searching for jobs.")
st.markdown("---")

with st.expander("💡 Top Job Scam Prevention Tips", expanded=True):
    st.markdown("""
    ### 🔍 1. Research the Employer
    - Verify the company through LinkedIn, Glassdoor, or official websites.
    - Avoid jobs from companies with no online presence.

    ### 🧾 2. Never Pay to Apply
    - **Legitimate employers never ask for application or training fees.**
    - Scam recruiters often use words like “refundable deposit” — don’t fall for it.

    ### 📧 3. Watch Out for Fake Emails
    - Professional companies use domains like `@company.com` — not Gmail or Yahoo.
    - Be cautious if the recruiter’s email looks suspicious.

    ### 💬 4. Be Wary of Instant Offers
    - No interview? No verification? 🚩 Big red flag.
    - Real companies **take time** to vet candidates.

    ### 📝 5. Check Job Descriptions
    - Vague job roles, unrealistic salaries, and urgent hiring = often fake.
    - Real job descriptions are clear, detailed, and well-structured.

    ### 🔗 6. Use Official Platforms
    - Apply only through platforms like Naukri, LinkedIn, or verified company portals.
    - Avoid random WhatsApp groups, Telegram DMs, or Facebook posts.

    ### 🚨 7. Report Suspicious Jobs
    - Help others stay safe — use our **Report Scam** page to log fake listings.
    - The more we share, the safer we all become!
    """)

st.markdown("---")
st.info("Need more help? Visit [cybercrime.gov.in](https://cybercrime.gov.in/) to report fraud in India.")
