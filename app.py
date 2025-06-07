import os
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("API key not found. Please add your OpenAI API key to the .env file.")
else:
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    # Streamlit app
    st.title("Meta Ad Caption Generator")

    st.markdown("""
    This app generates ad captions in a consistent, on-brand format using GPT-4.
    Fill in the product details below, and click **Generate Captions**.
    """)

    # Inputs
    product_name = st.text_input("Product Name / Brand", placeholder="e.g., Paul John Caffeine")
    hook = st.text_input("Catchy Hook (ends with ☕)", placeholder="e.g., Taste the richness only Indian coffee can deliver ☕")
    cta_keywords = st.text_input("CTA Keywords", placeholder="e.g., brew bold, stay grounded, sip with meaning")

    st.markdown("### USPs and Emojis")
    col1, col2 = st.columns(2)
    with col1:
        usp1 = st.text_input("USP 1", placeholder="e.g., Shade-grown in India – Infused with notes of lychee, citrus, and pepper")
        usp2 = st.text_input("USP 2", placeholder="e.g., Freshly roasted in the U.S. – Craft meets culture")
    with col2:
        emoji1 = st.text_input("Emoji for USP 1", placeholder="e.g., 🌿")
        emoji2 = st.text_input("Emoji for USP 2", placeholder="e.g., 🇺🇸")

    col3, col4 = st.columns(2)
    with col3:
        usp3 = st.text_input("USP 3", placeholder="e.g., Women-owned & kosher certified – Coffee with conscience")
        usp4 = st.text_input("USP 4", placeholder="e.g., A ritual for the soul – Your moment of stillness")
    with col4:
        emoji3 = st.text_input("Emoji for USP 3", placeholder="e.g., 👩🏽‍🌾")
        emoji4 = st.text_input("Emoji for USP 4", placeholder="e.g., 🧘🏽‍♀️")

    # Generate button
    if st.button("Generate Captions"):
        # Build the prompt
        prompt = f"""
You are an expert marketing copywriter who writes consistent, on-brand ad captions for Meta Ads. Please generate exactly 3 ad captions in the following strict format using the provided inputs.

FORMAT:
1️⃣ First line: Catchy, interesting hook ending with ☕
2️⃣ Second line: Mention brand name and product with a short description.
3️⃣ Four lines with ✅ bullet points, each with a short USP explanation followed by its specified emoji.
4️⃣ Final line: A closing sentence with a call to action.

Use the following inputs:
Brand Name and Product: {product_name}
USPs and Emojis:
1) {usp1} {emoji1}
2) {usp2} {emoji2}
3) {usp3} {emoji3}
4) {usp4} {emoji4}
Hook: {hook}
CTA Keywords: {cta_keywords}

IMPORTANT:
- Follow the structure exactly: hook line, brand line, 4 USPs with ✅ bullet points (each ending with its specified emoji), then final line with CTA.
- Do not add extra explanations, disclaimers, or headings like "Ad 1:" or "Ad 2:". Just output the captions, separated by a blank line.
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )

            captions = response.choices[0].message.content.strip()
            st.markdown("### Generated Ad Captions:")
            st.text_area("Captions", captions, height=400)
        except Exception as e:
            st.error(f"Error generating captions: {e}")
