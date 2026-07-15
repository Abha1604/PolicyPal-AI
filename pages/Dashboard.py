import streamlit as st

from utils.integration import get_standard_clause_status

if "analysis" not in st.session_state:
    st.warning("No contract analyzed yet.")
    st.stop()

analysis = st.session_state.analysis
structured_contract = st.session_state.structured_contract
metadata = st.session_state.get("analysis_metadata", {})

critical_risks = [risk for risk in analysis.risks if risk.severity == "High"]
standard_clause_status = get_standard_clause_status(structured_contract)

st.title("Contract Analysis Dashboard")

if metadata:
    info_cols = st.columns(4)
    with info_cols[0]:
        st.caption("File")
        st.write(metadata.get("filename", "Unknown"))
    with info_cols[1]:
        st.caption("Analysis Type")
        st.write(metadata.get("analysis_type", "Full Analysis"))
    with info_cols[2]:
        st.caption("Contract Type")
        st.write(str(structured_contract.contract_type))
    with info_cols[3]:
        pages = metadata.get("num_pages")
        st.caption("Pages")
        st.write(pages if pages is not None else "N/A")

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Risk Score", f"{analysis.risk_score}/100")

with col2:
    st.metric("Risk Level", analysis.risk_level)

with col3:
    st.metric("Clauses Found", len(structured_contract.clauses))

with col4:
    st.metric("Critical Risks", len(critical_risks))

st.markdown("---")

if structured_contract.parties:
    st.subheader("Parties")
    party_cols = st.columns(min(len(structured_contract.parties), 3))
    for index, party in enumerate(structured_contract.parties):
        with party_cols[index % len(party_cols)]:
            st.markdown(f"**{party.name}**")
            st.caption(party.role)
    st.markdown("---")

if structured_contract.important_dates:
    st.subheader("Important Dates")
    for date in structured_contract.important_dates:
        st.markdown(
            f"- **{date.type}**: {date.value} "
            f"_(Section: {date.source_section})_"
        )
    st.markdown("---")

if structured_contract.financial_obligations:
    st.subheader("Financial Obligations")
    for obligation in structured_contract.financial_obligations:
        st.markdown(
            f"- **{obligation.type}**: {obligation.amount} "
            f"— {obligation.responsible_party} "
            f"_(Section: {obligation.source_section})_"
        )
    st.markdown("---")

st.subheader("Standard Clause Checklist")

checklist_cols = st.columns(min(len(standard_clause_status), 5) or 1)
for index, item in enumerate(standard_clause_status):
    with checklist_cols[index % len(checklist_cols)]:
        if item["found"]:
            st.success(f"Found: {item['label']}")
        else:
            st.error(f"Missing: {item['label']}")

st.markdown("---")

st.subheader("Extracted Clauses")

if structured_contract.clauses:
    for clause in structured_contract.clauses:
        with st.expander(
            f"{clause.clause_type} — {clause.source_section}",
            expanded=False,
        ):
            st.write(clause.original_text)
else:
    st.info("No clauses were extracted from this contract.")

st.markdown("---")

st.subheader("Key Risks")

if analysis.risks:
    for risk in analysis.risks:
        if risk.severity == "High":
            st.error(f"**{risk.category}**: {risk.description}")
        elif risk.severity == "Medium":
            st.warning(f"**{risk.category}**: {risk.description}")
        else:
            st.info(f"**{risk.category}**: {risk.description}")
else:
    st.success("No significant risks were flagged by the rule engine.")

st.markdown("---")

st.subheader("Executive Summary")
st.info(analysis.summary)

st.markdown("---")

question = metadata.get("question")
st.subheader("Answer to Your Question")
if question:
    st.caption(f"Question: {question}")
st.write(analysis.answer)

if structured_contract.party_obligations:
    st.markdown("---")
    st.subheader("Party Obligations")
    for obligation in structured_contract.party_obligations:
        mandatory = "Required" if obligation.mandatory else "Optional"
        st.markdown(
            f"- **{obligation.party}** ({mandatory}): {obligation.obligation} "
            f"_(Section: {obligation.source_section})_"
        )
