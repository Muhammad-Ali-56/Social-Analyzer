import streamlit as st
import pandas as pd
import json
from importlib import import_module


st.set_page_config(page_title="Social Media Profile Analyzer", page_icon="🔍", layout="centered")
# Import social-analyzer dynamically
SocialAnalyzer = import_module("social-analyzer").SocialAnalyzer()

# Streamlit UI
st.title("🔍 Social Media Profile Analyzer")

# Input field for username
username = st.text_input("Enter the username:", "")

# Button to trigger search
if st.button("Search"):
    if username.strip():  # Ensure username is not empty
        st.info(f"Searching for user: {username} on Facebook...")

        # Run the analyzer
        results = SocialAnalyzer.run_as_object(username=username, websites='facebook', silent=True)

        # Check if profiles were detected
        if "detected" in results and isinstance(results["detected"], list) and results["detected"]:
            detected_profiles = results["detected"]

            # Display results
            st.success(f"✅ {len(detected_profiles)} Profile(s) Found!")
            for idx, profile in enumerate(detected_profiles, 1):
                st.subheader(f"📌 Profile {idx}")
                for key, value in profile.items():
                    st.write(f"**{key}:** {value}")

            # Convert detected profiles to DataFrame and save to CSV
            df = pd.DataFrame(detected_profiles)
            df.to_csv("data_scrape.csv", index=False, encoding="utf-8")

            st.download_button(label="📥 Download Results", data=df.to_csv(index=False), file_name="data_scrape.csv", mime="text/csv")

        else:
            st.error("❌ No profiles detected for the given username.")
        
        # Display raw JSON output
        st.text_area("📜 Raw Output", json.dumps(results, indent=4), height=300)

    else:
        st.warning("⚠️ Please enter a valid username.")

