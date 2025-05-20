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
        background-color: rgba(255, 255, 255, 0.6);  /* translucent overlay */
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

/* White background specifically for output area */
.report-section {
    background-color: #ffffff !important;
    border-radius: 16px;
    padding: 25px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin-top: 20px;
}
.expander-white [data-testid="stExpander"] > div {
    background-color: #ffffff !important;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
            

/* Also target expanders for fallback */
[data-testid="stExpander"] > div {
    background-color: #ffffff !important;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
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

        # --- White background wrapper for results ---
        with st.container():
            st.markdown('<div class="report-section">', unsafe_allow_html=True)
            st.subheader("🧠 Interaction Report")

            # --- Parse Output ---
            parsed = {"risks": "", "interactions": "", "conclusion": ""}
            sections = re.split(r"###\s*\d\.\s*", result)

            if len(sections) >= 4:
                parsed["risks"] = sections[1].strip()
                parsed["interactions"] = sections[2].strip()
                parsed["conclusion"] = sections[3].strip()
            else:
                parsed["interactions"] = result.strip()

            st.markdown('<div class="expander-white">', unsafe_allow_html=True)
            with st.expander("💊 Risks / Side Effects", expanded=True):
                st.markdown(parsed["risks"] or "No specific risks found.")
            st.markdown('</div>', unsafe_allow_html=True)


            with st.expander("🔄 Drug Interactions", expanded=True):
                st.markdown(parsed["interactions"] or "No interaction data found.")

            with st.expander("✅ Conclusion / Recommendations", expanded=True):
                st.markdown(parsed["conclusion"] or "No specific conclusion found.")
            st.markdown('</div>', unsafe_allow_html=True)

# --- Footer ---
st.markdown("---")
st.markdown("<footer>Powered by OpenAI & LangChain</footer>", unsafe_allow_html=True)
