"""

Smart Resume Screening and Candidate Ranking Tool 

"""


import pandas as pd
import streamlit as st

from resume_parser import extract_text, extract_contact_info
from ranker import rank_candidates, DEFAULT_SKILLS


st.set_page_config(
    page_title = "Smart Resume Screening & Ranking Tool",
    layout = "wide"
)


def load_candidates(uploaded_files):
    candidates = []
    errors = []

    for f in uploaded_files:
        try:
            file_bytes = f.read()
            text = extract_text(f.name, file_bytes)

            if not text.strip():
                errors.append(f"{f.name}: no extractable text found.")
                continue
            contact = extract_contact_info(text, f.name)

            candidates.append({
                "filename": f.name,
                "text": text,
                **contact,
            })

        except Exception as e:
            errors.append(f'{f.name}: {e}')

    return candidates, errors


def main():
    st.title("Smart Resume Screening & Candidate Ranking Tool")
    st.caption(
        "Paste job description, upload resumes and get a rank shortlist based on keywords similarity and skill matches."
    )

    with st.sidebar:
        st.header("Settings")
        top_n = st.slider("Show top N candidates", min_value = 1, max_value = 50, value = 10)
        min_score = st.slider("Minimum match score (%)", 0, 100, 0)

        st.subheader("Skill List")
        st.caption("Edit or extend the list to search in the resume.")
        skills_input = st.text_area(
            "Skills",
            value = ",".join(DEFAULT_SKILLS),
            height = 150
        )
        skills = [s.strip() for s in skills_input.split(",") if s.strip()]
    col1, col2 = st.columns([1,1])
    
    with col1:
        st.subheader("1. Job Description")
        job_description = st.text_area(
            "Paste the Job Description here",
            height = 280,
            placeholder = "EX: We are looking for a Python Developer with experience"
                          "in machine learning, rest APIs, and cloud deployment..."
        )

    with col2:
        st.subheader("2. Upload Resumes")
        uploaded_files = st.file_uploader(
            "Upload one or more resume (PDF, DOCX)",
            type = ["pdf", "docx"],
            accept_multiple_files = True
        )

        if uploaded_files:
            st.write(f" {len(uploaded_files)} file(s) uploaded")

    st.divider()


    run = st.button("Screen & Rank Candidates", type = "primary", use_container_width = True)


    if run:
        if not job_description.strip():
            st.error("Please paste the Job Description first.")
            return
        if not uploaded_files:
            st.error("Please upload atleast one resume.")
            return
    
        with st.spinner("Parsing Resumes..."):
            candidates, errors = load_candidates(uploaded_files)

        for err in errors:
            st.warning(err)

        if not candidates:
            st.error("No resume could be parsed. Please check the files and try again.")
            return


        with st.spinner("Scoring & Ranking Candidates..."):
            ranked = rank_candidates(job_description, candidates, skills=skills)

        ranked = [c for c in ranked if c["match_score"] >= min_score] [: top_n]


        if not ranked:
            st.info("No candidates met the minimum score threshold.")
            return
    
        st.subheader(f"Ranked Candidates ({len(ranked)})")


        table_rows = []
        for i, c in enumerate(ranked, start=1):
            table_rows.append({
                "Rank" : i,
                "Name" : c["name"],
                "File" : c["filename"],
                "Email" : c["email"],
                "Phone" : c["phone"],
                "Match Score (%)" : c["match_score"],
                "Matched Skills" : ",".join(c["matched_skills"]) if c["matched_skills"] else "-",
                "# Skills" : c["skill_count"]
        })
            

        df = pd.DataFrame(table_rows)
        st.dataframe(df, use_container_width = True, hide_index = True)

        st.subheader("Score Comparison")
        chart_df = df.set_index("Name") [["Match Score (%)"]]
        st.bar_chart(chart_df)
        
        st.subheader("Candidate Details")
        for c in ranked:
            with st.expander(f"{c['name']} - {c['match_score']}% match"):
                st.write(f"**File:** {c['filename']}")
                st.write(f"**Email:** {c['email'] or 'Not Found'}")
                st.write(f"**Phone:** {c['phone'] or 'Not Found'}")
                st.write(f"**Matched Skills:** {','.join(c['matched_skills']) if c ['matched_skills'] else 'None Found'}")
                st.text_area(
                    "Extracted resume text (preview)",
                    value = c["text"][:2000] + ("..." if len(c["text"]) > 2000 else ""),
                    height = 150,
                    key = f"preview_{c['filename']}"
                )


if __name__ == "__main__":
    main()






