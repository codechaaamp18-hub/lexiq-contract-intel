import streamlit as st
import re

# Set up the web page title
st.set_page_config(page_title="LexIQ Contract Intelligence", layout="wide")
st.title("⚖️ LexIQ: Legal Contract Analyzer")
st.write("A simplified Second-Year engineering prototype for extracting legal information.")

# 1. Input Section: Paste a sample contract
st.header("📄 Step 1: Input Contract Text")
sample_text = """This Non-Disclosure Agreement (the "Agreement") is entered into on August 15, 2026, 
by and between Alpha Tech Solutions (the "Disclosing Party") and Beta Consultants LLC (the "Receiving Party"). 
The parties agree to a financial liability limit of $50,000 for any breach of confidentiality."""

contract_text = st.text_area("Paste your legal agreement below:", value=sample_text, height=150)

# 2. Processing Engine (Using simple regular expressions)
def analyze_contract(text):
    # Rule-based matching for dates, companies, and money
    date_match = re.search(r'(?:on\s)([A-Z][a-z]+\s\d{1,2},\s\d{4})', text)
    parties = re.findall(r'([A-Z][a-zA-Z0-9\s]+(?:\sLtd|\sLLC|\sSolutions|\sInc))', text)
    amount_match = re.search(r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?', text)
    
    return {
        "Date": date_match.group(1) if date_match else "Not found",
        "Parties Involved": list(set(parties)) if parties else ["Not found"],
        "Liability Limit": amount_match.group(0) if amount_match else "Not found"
    }

# 3. Output Dashboard
if st.button("Analyze Contract"):
    st.header("🔍 Step 2: Extracted Information (Intelligence)")
    results = analyze_contract(contract_text)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Effective Date", value=results["Date"])
    with col2:
        st.metric(label="Liability Value", value=results["Liability Limit"])
    with col3:
        st.write("**Extracted Entities (Nodes):**")
        for party in results["Parties Involved"]:
            st.write(f"🏢 {party}")
            
    # 4. Simulating the Knowledge Graph Connections
    st.header("🕸️ Step 3: Simulated Knowledge Graph Connections")
    if len(results["Parties Involved"]) >= 2:
        p1, p2 = results["Parties Involved"][0], results["Parties Involved"][1]
        st.success(f"🔗 **Relationship Found:** [{p1}] ──(SIGNED_AGREEMENT_WITH)──> [{p2}]")
        st.caption(f"Graph Property: [Date: {results['Date']}, Limit: {results['Liability Limit']}]")
    else:
        st.info("Add more company indicators like 'LLC' or 'Inc' to map connections.")
