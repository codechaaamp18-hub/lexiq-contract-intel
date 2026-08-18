import streamlit as st
import json
from groq import Groq
from supabase import create_client, Client

# Set up page configurations
st.set_page_config(page_title="LexIQ Contract Intelligence", layout="wide")
st.title("⚖️ LexIQ: AI Contract Intelligence & Knowledge Graph")
st.write("An advanced LLM-powered legal data analysis system with a database backend.")

# --- AUTOMATIC CREDENTIALS CONFIGURATION ---

GROQ_API_KEY = "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"
SUPABASE_URL = "https://guxmowzxflvwmbclirrf.supabase.co"
SUPABASE_KEY = "sb_publishable_m3_8bIaqewBJFhopXf6FCg_CwtQ8JI_"

# Complex multi-clause real-world legal draft sample
complex_sample = """AMENDED MASTER SERVICES & INTELLECTUAL PROPERTY COVENANT

This master strategic collaboration architecture is compiled, finalized, and executed into statutory effectiveness on this twenty-fourth day of February, two thousand twenty-seven. This framework establishes an explicit legal nexus between Oscorp Industries, incorporating operations out of New York City, hereinafter referred to as the 'Disclosing Party', and Cyberdyne Systems Ltd, managing production across localized facilities in Tokyo, Japan, hereinafter designated as the 'Receiving Party'.

WHEREAS, the executing organizations seek to minimize mutual operational exposure, it is definitively stipulated under Clause 14.7 (Indemnification Allocations) that the total financial liability exposure ceiling resulting from data breaches, cross-border compliance omissions, or intellectual property leakage shall be firmly capped at an absolute max limitation of nine hundred fifty thousand USD ($950,000). Furthermore, the agreement mandates an explicit executive overview summarizing all core corporate operational operational boundaries and liabilities.
"""

contract_text = st.text_area("📄 Paste Complex Legal Draft Contract:", value=complex_sample, height=220)

if st.button("🚀 Analyze Complex Contract & Sync To Backend"):
    if "PASTE_" in GROQ_API_KEY or "PASTE_" in SUPABASE_KEY:
        st.error("Stop! Please replace the placeholder strings at the top of your code with your real API keys first.")
    else:
        with st.spinner("AI Engine is executing reasoning extraction and generating summaries..."):
            try:
                # 1. Instantiate cloud framework clients
                client = Groq(api_key=GROQ_API_KEY)
                supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
                
                # 2. Refined Engineering System Prompt forcing explicit extraction and rich text summaries
                system_prompt = (
                    "You are an elite legal AI extraction algorithm. Analyze the input contract text and output ONLY a valid raw JSON object. "
                    "Do not include markdown tags, chat commentary, or code blocks. Follow this strict schema architecture:\n"
                    '{"effective_date": "string", "liability_limit": "string", "party_a": "string", "party_b": "string", "executive_summary": "string"}'
                )
                
                # Query the open-source migration model
                completion = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": contract_text}
                    ],
                    temperature=0.1
                )
                
                # --- SAFE PARSING FIX ---
                # Check if the response is a dictionary or a list to avoid attribute errors
                if isinstance(completion, dict):
                    raw_output = completion["choices"][0]["message"]["content"].strip()
                elif hasattr(completion, "choices") and len(completion.choices) > 0:
                    choice = completion.choices[0]
                    if isinstance(choice, dict):
                        raw_output = choice["message"]["content"].strip()
                    else:
                        raw_output = choice.message.content.strip()
                else:
                    raw_output = str(completion)
                    
                data = json.loads(raw_output)

                
                # 3. Cloud Database Integration Layer
                db_payload = {
                    "party_a": data.get("party_a"),
                    "party_b": data.get("party_b"),
                    "effective_date": data.get("effective_date"),
                    "liability_limit": data.get("liability_limit"),
                    "contract_text": contract_text
                }
                supabase.table("contracts").insert(db_payload).execute()
                st.toast("⚡ Cloud Backend Database Updated Successfully!")
                
                # 4. Rendering the UI Elements
                st.header("🔍 Extracted Contract Metadata Attributes")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label="🗓️ Interpreted ISO Date", value=data.get("effective_date", "Not found"))
                with col2:
                    st.metric(label="💰 Financial Liability Ceiling", value=data.get("liability_limit", "Not found"))
                
                # Executive Summarization Block
                st.header("📝 Executive Legal Digest")
                st.info(data.get("executive_summary", "No deep summary could be synthesized by the system model."))
                
                # Visual Semantic Network Graph Rendering
                st.header("🕸️ Semantic Legal Knowledge Graph Visualizer")
                p1 = data.get("party_a", "First Party")
                p2 = data.get("party_b", "Second Party")
                st.success(f"🏢 [{p1}] ───( ESTABLISHED_AGREEMENT_PARTNER )───> 🏢 [{p2}]")
                
                # Technical Node properties structure layout
                st.subheader("📊 Graph Database Structure Layout (Nodes & Attributes Mapping)")
                graph_schema_viz = {
                    "Graph Database Paradigm": "Property Graph Schema Mapping",
                    "Nodes (Entities)": [
                        {"Label": "Organization", "Properties": {"Name": p1, "Role": "Disclosing Entity"}},
                        {"Label": "Organization", "Properties": {"Name": p2, "Role": "Receiving Entity"}}
                    ],
                    "Edge (Semantic Relationship)": {
                        "Type": "MUTUAL_STRATEGIC_COVENANT",
                        "Properties": {
                            "Temporal_Activation": data.get("effective_date"),
                            "Financial_Risk_Cap": data.get("liability_limit")
                        }
                    }
                }
                st.json(graph_schema_viz)
                
            except Exception as e:
                st.error(f"Execution Error encountered during computation processing: {e}")

# --- BACKEND HISTORY VIEWER ---
st.header("📂 Historical Cloud Storage Logs (Real-Time Backend View)")
if "PASTE_" not in SUPABASE_KEY:
    try:
        sb = create_client(SUPABASE_URL, SUPABASE_KEY)
        history_response = sb.table("contracts").select("*").order("created_at", descending=True).execute()
        if history_response.data:
            st.dataframe(history_response.data)
        else:
            st.info("No saved records found in the database table yet.")
    except Exception:
        pass
