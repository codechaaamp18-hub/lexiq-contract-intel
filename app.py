import streamlit as st
import json
from groq import Groq

# Set up page configurations
st.set_page_config(page_title="LexIQ Contract Intelligence", layout="wide")
st.title("⚖️ LexIQ: AI Contract Intelligence & Knowledge Graph")
st.write("An advanced LLM-powered legal data analysis system.")

# Get API key securely from user input
groq_key = st.sidebar.text_input("Enter Groq API Key:", type="password")

# Sample complex contract text
complex_sample = """MEMORANDUM OF UNDERSTANDING
Concluded this day between the enterprise known as Stark Industries, operating out of California, 
and the organization designated as Wayne Enterprises. 

It is mutually understood that the final termination of these mutual obligations will be executed 
fully by the final calendar day of December in the year 2029. Should any data leak transpire, 
the financial penalty damages are capped at a maximum ceiling sum of fifty thousand USD."""

contract_text = st.text_area("Paste complex legal agreement below:", value=complex_sample, height=200)

if st.button("Run AI Intelligence Analysis"):
    if not groq_key:
        st.error("Please enter your Groq API Key in the sidebar to run the AI model.")
    else:
        with st.spinner("AI is analyzing complex structures..."):
            try:
                # Initialize the free Groq client
                client = Groq(api_key=groq_key)
                
                # Setup a strict system prompt to force the LLM to output clean JSON data
                system_prompt = (
                    "You are a legal data extraction engine. Analyze the contract and output ONLY a valid JSON object. "
                    "Do not include any conversational text, backticks, or markdown. Use this exact schema:\n"
                    '{"effective_date": "string", "liability_limit": "string", "party_a": "string", "party_b": "string"}'
                )
                
                # Query the open-source Llama 3 model
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": contract_text}
                    ],
                    temperature=0.1 # Low temperature means consistent, accurate extraction
                )
                
                # Parse the response string directly into Python data structures
                raw_response = completion.choices[0].message.content.strip()
                data = json.loads(raw_response)
                
                # --- UI Dashboard Output ---
                st.header("🔍 Extracted Contract Metadata")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label="🗓️ Identified Date", value=data.get("effective_date", "Not found"))
                with col2:
                    st.metric(label="💰 Liability Limit Value", value=data.get("liability_limit", "Not found"))
                
                # --- Visualizing the Knowledge Graph Data Structure ---
                st.header("🕸️ Semantic Legal Knowledge Graph")
                p1 = data.get("party_a", "Party A")
                p2 = data.get("party_b", "Party B")
                
                # Display the visual representation of Nodes and Edges
                st.success(f"🏢 [{p1}] ───( AGREEMENT_PARTNER )───> 🏢 [{p2}]")
                
                # Show details inside a neat technical layout
                st.subheader("📊 Graph Graph Database Properties (Nodes & Attributes)")
                graph_data = {
                    "Nodes": [
                        {"Type": "Organization", "Name": p1},
                        {"Type": "Organization", "Name": p2}
                    ],
                    "Edge (Relationship)": {
                        "Type": "CONCLUDED_AGREEMENT_WITH",
                        "Properties": {
                            "Expiry": data.get("effective_date"),
                            "Financial Liability Ceiling": data.get("liability_limit")
                        }
                    }
                }
                st.json(graph_data)
                
            except Exception as e:
                st.error(f"An processing error occurred: {e}")
