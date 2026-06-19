import streamlit as st
import requests
import os

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Digital Scientist",
    page_icon="🔬",
    layout="wide"
)

st.markdown("""
<style>
.main-title {
    font-size: 48px;
    font-weight: 800;
    color: #1f4e79;
}
.subtitle {
    font-size: 20px;
    color: #555;
}
.card {
    padding: 25px;
    border-radius: 15px;
    background-color: #f8f9fa;
    border: 1px solid #e0e0e0;
    margin-bottom: 20px;
}
.metric-box {
    padding: 20px;
    border-radius: 12px;
    background-color: #ffffff;
    border: 1px solid #ddd;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🔬 Digital Scientist</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">AI-powered hypothesis testing, research-paper analysis, and statistical dataset intelligence.</div>',
    unsafe_allow_html=True
)

st.divider()

left, right = st.columns([1, 2])

with left:
    st.markdown("### Project Modules")
    st.info("Research Claim Analyzer")
    st.info("Academic Paper Search")
    st.info("CSV Statistical Testing")
    st.info("Graph + PDF Report Generator")

with right:
    st.markdown("### What this system does")
    st.write(
        "Digital Scientist converts natural-language claims into research hypotheses, "
        "retrieves academic papers, analyzes evidence, and validates datasets statistically."
    )

st.divider()

tab1, tab2, tab3, tab4 = st.tabs(
    ["Research Assistant", "Dataset Scientist", "Research Chat", "Project Summary"]
)

with tab1:
    st.markdown("## Research Claim Analysis")

    claim = st.text_area(
        "Enter a research claim",
        placeholder="Example: Social media usage reduces academic performance",
        height=120
    )

    col1, col2 = st.columns([1, 3])

    with col1:
        analyze_btn = st.button("Analyze Claim", use_container_width=True)

    if analyze_btn:
        if not claim.strip():
            st.warning("Please enter a research claim.")
        else:
            with st.spinner("Digital Scientist is analyzing the claim..."):
                try:
                    response = requests.get(
                        f"{API_URL}/full-research",
                        params={"claim": claim},
                        timeout=60
                    )

                    if response.status_code == 200:
                        data = response.json()

                        st.success("Research analysis completed")

                        st.markdown("### Generated Hypothesis")
                        st.markdown(f"""
                        <div class="card">
                        {data.get("hypothesis", "No hypothesis generated.")}
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown("### Retrieved Research Papers")

                        papers = data.get("papers", [])

                        if papers:
                            for i, paper in enumerate(papers, start=1):
                                with st.expander(f"{i}. {paper.get('title', 'Untitled Paper')}"):
                                    st.write("Published:", paper.get("published", "N/A"))
                                    st.write("Link:", paper.get("link", "N/A"))
                                    st.write(paper.get("summary", "No summary available."))
                        else:
                            st.warning("No papers found.")

                        st.markdown("### Evidence Analysis")
                        st.markdown(f"""
                        <div class="card">
                        {data.get("evidence_analysis", "No evidence analysis available.")}
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown("### Similar Research Papers")

                        similar_papers = data.get("similar_papers", [])

                        if similar_papers:
                            for paper in similar_papers:
                                metadata = paper["metadata"]

                                with st.expander(metadata["title"]):
                                    st.write("Published:", metadata.get("published", "N/A"))
                                    st.write("Similarity Score:", metadata.get("similarity_score", "N/A"))
                                    st.write("Link:", metadata.get("link", "N/A"))
                                    st.write(paper["content"][:500])
                        else:
                            st.info("No similar papers found.")

                    else:
                        st.error("Backend returned an error.")

                except Exception as e:
                    st.error(f"Could not connect to backend: {e}")
                    
with tab2:
    st.markdown("## Dataset Statistical Analysis")

    col1, col2 = st.columns([1, 1])

    with col1:
        uploaded_file = st.file_uploader(
            "Upload CSV file",
            type=["csv"]
        )

    with col2:
        independent_col = st.text_input(
            "Independent Variable",
            placeholder="Example: sleep_hours"
        )

        dependent_col = st.text_input(
            "Dependent Variable",
            placeholder="Example: exam_score"
        )

    analyze_dataset_btn = st.button(
        "Analyze Dataset",
        use_container_width=True
    )

    if analyze_dataset_btn:
        if uploaded_file is None:
            st.warning("Please upload a CSV file.")
        elif not independent_col or not dependent_col:
            st.warning("Please enter both variable names.")
        else:
            with st.spinner("Analyzing dataset..."):
                try:
                    files = {
                        "file": uploaded_file
                    }

                    data = {
                        "independent_col": independent_col,
                        "dependent_col": dependent_col
                    }

                    response = requests.post(
                        f"{API_URL}/analyze-dataset",
                        files=files,
                        data=data,
                        timeout=60
                    )

                    result = response.json()

                    if "error" in result.get("analysis", {}):
                        st.error(result["analysis"]["error"])
                    else:
                        analysis = result["analysis"]

                        st.success("Dataset analysis completed")

                        m1, m2, m3, m4 = st.columns(4)

                        m1.metric("Correlation", analysis["correlation"])
                        m2.metric("P-Value", analysis["p_value"])
                        m3.metric("Rows", analysis["rows"])
                        m4.metric("Significance", analysis["significance"])

                        st.markdown("### Statistical Analysis")
                        st.json(analysis)

                        st.markdown("### Research Report")
                        st.markdown(f"""
                        <div class="card">
                        <pre>{result.get("research_report", "")}</pre>
                        </div>
                        """, unsafe_allow_html=True)

                        plot_file = result.get("plot_file")

                        if plot_file and os.path.exists(plot_file):
                            st.markdown("### Generated Scatter Plot")
                            st.image(plot_file, use_container_width=True)

                        pdf_file = result.get("pdf_report")

                        if pdf_file and os.path.exists(pdf_file):
                            with open(pdf_file, "rb") as pdf:
                                st.download_button(
                                    label="Download PDF Report",
                                    data=pdf,
                                    file_name="digital_scientist_report.pdf",
                                    mime="application/pdf",
                                    use_container_width=True
                                )

                except Exception as e:
                    st.error(f"Could not analyze dataset: {e}")

with tab3:
    st.markdown("## Research Chat")

    question = st.text_area(
        "Ask a question about stored research papers",
        placeholder="Example: What do the stored papers say about AI in education?",
        height=120
    )

    if st.button("Ask Research Assistant", use_container_width=True):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Searching stored papers..."):
                response = requests.get(
                    f"{API_URL}/research-chat",
                    params={"question": question},
                    timeout=60
                )

                if response.status_code == 200:
                    data = response.json()

                    st.success("Answer generated")

                    st.markdown("### Answer")
                    st.markdown(f"""
                    <div class="card">
                    {data.get("answer", "No answer generated.")}
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("### Sources")

                    for source in data.get("sources", []):
                        metadata = source["metadata"]

                        with st.expander(metadata["title"]):
                            st.write("Published:", metadata.get("published", "N/A"))
                            st.write("Similarity Score:", metadata.get("similarity_score", "N/A"))
                            st.write("Link:", metadata.get("link", "N/A"))
                            st.write(source["content"][:500])
                else:
                    st.error("Backend returned an error.")