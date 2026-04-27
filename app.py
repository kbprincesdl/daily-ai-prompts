import streamlit as st
from utils import generate_prompt, save_to_excel, load_data

st.set_page_config(page_title="Daily AI Prompts", layout="wide")

st.title("🤖 Daily AI Prompt Generator")

# Session state
if "current_prompt" not in st.session_state:
    st.session_state.current_prompt = ""

# Generate Prompt
if st.button("✨ Generate New Prompt"):
    st.session_state.current_prompt = generate_prompt()

# Display Prompt
if st.session_state.current_prompt:
    st.subheader("🧠 Today's Prompt")
    st.success(st.session_state.current_prompt)

    # Auto Save Button
    if st.button("💾 Save Prompt"):
        save_to_excel(st.session_state.current_prompt)
        st.success("Saved to Excel!")

# Dashboard Section
st.divider()
st.subheader("📊 Prompt History Dashboard")

data = load_data()

if not data.empty:
    st.dataframe(data, use_container_width=True)

    # Stats
    st.write(f"Total Prompts Saved: {len(data)}")

    # Download button
    with open("prompts.xlsx", "rb") as f:
        st.download_button(
            label="⬇️ Download Excel",
            data=f,
            file_name="prompts.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("No prompts saved yet.")
