import streamlit as st
from PIL import Image
from agent import analyze_drug_interaction
import base64
import re
import os

st.set_page_config(page_title="Drug Interaction Checker", layout="wide")

# --- Background Image Setup ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

try:
    bin_str = get_base64_of_bin_file("background.png")
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        background-attachment: fixed;
    }}
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        height: 100%;
        width: 100%;
        background-color: rgba(255, 255, 255, 0.6);
        z-index: -1;
    }}
    </style>
    """, unsafe_allow_html=True)
except Exception as e:
    st.warning(f"Could not load background image: {e}")

# --- Custom CSS Styling ---
st.markdown("""
<style>
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
h1, h2, h3, h4 {
    color: #00796b;
}
.stButton > button {
    color: white;
    background-color: #00796b;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 16px;
}
.stTextInput>div>div>input,
textarea {
    padding: 10px;
    border-radius: 8px;
}
.stMarkdown {
    font-size: 17px;
}
footer {
    text-align: center;
    padding: 10px;
    font-size: 14px;
    color: #888888;
}

/* Report section wrapper */
.report-section {
    background-color: #ffffff !important;
    border-radius: 16px;
    padding: 25px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin-top: 10px;
}

/* Expander style */
.expander-white [data-testid="stExpander"] {
    background-color: #ffffff !important;
    border-radius: 12px;
    border: 1px solid #ddd;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    margin-bottom: 16px;
    padding: 0;
}
.expander-white [data-testid="stExpander"] > div:first-child {
    background-color: #ffffff !important;
    border-radius: 12px 12px 0 0;
    padding: 15px 20px;
    font-weight: 600;
    color: #333;
}
.expander-white [data-testid="stExpander"] > div:nth-child(2) {
    background-color: #ffffff !important;
    border-radius: 0 0 12px 12px;
    padding: 20px;
}
</style>
""", unsafe_allow_html=True)

# --- Logo (Optional) ---
try:
    logo = Image.open("logo.png")
    st.image(logo, width=150)
except:
    pass

# --- App Title & Inputs ---
st.title("🧪 Drug Interaction Checker")
st.markdown("Enter at least two drugs (name + optional dosage):")

drug_1 = st.text_input("Drug 1", placeholder="e.g., Metformin 500mg")
drug_2 = st.text_input("Drug 2", placeholder="e.g., Lisinopril 10mg")
more_drugs = st.text_area("Add More Drugs (one per line)", height=100)

# --- Action Button ---
if st.button("Check Interaction"):
    drug_list = [drug_1.strip(), drug_2.strip()] + [d.strip() for d in more_drugs.splitlines() if d.strip()]
    valid_drugs = [d for d in drug_list if d]

    if len(valid_drugs) < 2:
        st.warning("⚠️ Please enter at least two drug names.")
    else:
        with st.spinner("🔍 Analyzing drug interactions..."):
            result = analyze_drug_interaction(valid_drugs)

        # --- Parse Output ---
        parsed = {"risks": "", "interactions": "", "conclusion": ""}
        sections = re.split(r"###\s*\d\.\s*", result)

        if len(sections) >= 4:
            parsed["risks"] = sections[1].strip()
            parsed["interactions"] = sections[2].strip()
            parsed["conclusion"] = sections[3].strip()
        else:
            parsed["interactions"] = result.strip()

        # --- Report Section ---
        st.subheader("🧠 Interaction Report")

        # --- Risks
        with st.expander("💊 Risks / Side Effects", expanded=True):
            st.markdown(parsed["risks"] or "No specific risks found.")
        st.markdown('</div>', unsafe_allow_html=True)

        # --- Interactions
        st.markdown('<div class="expander-white">', unsafe_allow_html=True)
        with st.expander("🔄 Drug Interactions", expanded=True):
            st.markdown(parsed["interactions"] or "No interaction data found.")
        st.markdown('</div>', unsafe_allow_html=True)

        # --- Conclusion
        st.markdown('<div class="expander-white">', unsafe_allow_html=True)
        with st.expander("✅ Conclusion / Recommendations", expanded=True):
            st.markdown(parsed["conclusion"] or "No specific conclusion found.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)  # Close report-section

# --- Footer ---
st.markdown("---")
st.markdown("<footer>Powered by OpenRouter & LangChain</footer>", unsafe_allow_html=True)
