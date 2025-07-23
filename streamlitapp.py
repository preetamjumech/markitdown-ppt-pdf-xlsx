import streamlit as st
from markitdown import MarkItDown
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import base64

st.set_page_config(page_title="MarkItDown Insights: Smart File Q&A", page_icon="📄", layout="centered")

st.markdown(
    """
    <h1 style='text-align: center; color: #1A5276; font-family: Arial; letter-spacing:2px;'>MarkItDown Insights</h1>
    <p style='text-align: center; font-size: 20px; color: #555; font-family: Arial;'>
        Smart File Q&A: Upload your PDF, PPT, or Excel file, preview it, and get instant insights from your documents.
    </p>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    uploaded_file = st.file_uploader(
        "Choose a file (.pdf, .ppt, .pptx, .xls, .xlsx)", 
        type=["pdf", "ppt", "pptx", "xls", "xlsx"], 
        help="Supported formats: PDF, PowerPoint, Excel"
    )

if uploaded_file:
    file_ext = uploaded_file.name.split('.')[-1].lower()
    st.markdown(f"<div style='text-align:center;'><b>File uploaded:</b> {uploaded_file.name}</div>", unsafe_allow_html=True)
    
    if file_ext == "pdf":
        st.markdown("<div style='text-align:center;'><b>Preview:</b></div>", unsafe_allow_html=True)
        temp_pdf_path = f"temp_preview.pdf"
        with open(temp_pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        with open(temp_pdf_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f"""
            <div style='display: flex; justify-content: center;'>
                <iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="500" style="border:1px solid #ccc;"></iframe>
            </div>
        """
        st.markdown(pdf_display, unsafe_allow_html=True)
    else:
        st.markdown("<div style='text-align:center;'><i>Preview not available for this file type.</i></div>", unsafe_allow_html=True)

    st.markdown("<div style='text-align:center; margin-top:30px;'>", unsafe_allow_html=True)
    question = st.text_input(
        "Ask a question about this file:",
        value="What is the total amount on this invoice?",
        help="Type your question here."
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Get Answer"):
        with st.spinner("Extracting content and querying Gemini..."):
            temp_path = f"temp.{file_ext}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            md = MarkItDown()
            result = md.convert(temp_path)
            llm = ChatGoogleGenerativeAI(
                google_api_key=os.getenv("GEMINI_API_KEY"),
                model="gemini-2.0-flash",
                max_output_tokens=2048,
                temperature=0,
            )
            prompt = f"{result.text_content}\n\nQuestion: {question}"
            answer = llm.invoke(prompt)
            
            st.markdown(
                f"""
                <div style='background-color: #F9EBEA; padding: 24px; border-radius: 12px; margin-top: 24px; text-align:center; box-shadow: 0 2px 8px #ccc;'>
                    <h3 style='color: #884EA0; font-family: Arial; letter-spacing:1px;'>Insightful Response</h3>
                    <p style='font-size: 22px; color: #333; font-family: Arial;'>{answer.content}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )