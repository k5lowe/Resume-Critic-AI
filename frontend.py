import streamlit as st
from backend import main_function
import os
import tempfile

st.title("Software Resume AI Critic")

resume = st.file_uploader("Upload your resume", type=["pdf"])

job_description = st.text_area("Enter the job description")


if st.button("Analyze") and resume is not None and job_description:
    st.success("Resume uploaded successfully")

    # file_path = os.path.join("temp", resume.name)
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        
        tmp_file.write(resume.getbuffer())  # Write uploaded content to the temp file
        tmp_file_path = tmp_file.name


        score, feedback = main_function(tmp_file_path, job_description)

        st.markdown("<h2><b>Resume Score:</b></h2>", unsafe_allow_html=True)
        


        color = f"rgb({255 - int(score * 2.55)}, {int(score * 2.55)}, 0)"

        # Custom HTML to create a circle with bold text and color
        circle_html = f"""
            <div style="display: flex; justify-content: center; align-items: center; 
                        width: 100%;">
                <div style="display: flex; justify-content: center; align-items: center;
                            width: 150px; height: 150px; border-radius: 50%; 
                            background-color: {color}; font-size: 40px; color: white; 
                            font-weight: bold;">
                    {score}
                </div>
            </div>
        """

        # Display the custom HTML in Streamlit
        st.markdown(circle_html, unsafe_allow_html=True)


        st.markdown(f"<h2><b>Feedback:</b></h2>\n {feedback}", unsafe_allow_html=True)




elif resume is None:
    st.warning("Please upload a resume file.")
elif not job_description:
    st.warning("Please enter a job description.")