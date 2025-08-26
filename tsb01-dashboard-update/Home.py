import streamlit as st
import streamlit as st
import os

def add_pdf_download_sidebar():
    """Add PDF download functionality to sidebar"""
    st.sidebar.markdown("---")  # Add separator line
    st.sidebar.markdown("### 📄 Download Resources")
    
    # Define your PDF files (add your PDF files to a 'pdfs' folder in your project directory)
    pdf_files = {
        "Project Documentation": "pdfs/CCDS_HIL_Giz.pdf",
    }
    
    # Create download buttons for each PDF
    for pdf_name, pdf_path in pdf_files.items():
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as pdf_file:
                pdf_data = pdf_file.read()
                
                st.sidebar.download_button(
                    label=f"📥 Download {pdf_name}",
                    data=pdf_data,
                    file_name=f"{pdf_name.replace(' ', '_').lower()}.pdf",
                    mime="application/pdf",
                    help=f"Click to download {pdf_name}"
                )
        else:
            st.sidebar.error(f"❌ {pdf_name} not found")
    
    # Alternative: Single file upload and download
    st.sidebar.markdown("### 📤 Upload & Share PDF")
    uploaded_file = st.sidebar.file_uploader(
        "Upload a PDF to share", 
        type=['pdf'],
        help="Upload a PDF file that others can download"
    )
    
    if uploaded_file is not None:
        st.sidebar.download_button(
            label="📥 Download Uploaded PDF",
            data=uploaded_file.read(),
            file_name=uploaded_file.name,
            mime="application/pdf"
        )
def main():

    st.set_page_config(
    page_title="Welcome DIU",
    page_icon=":material/home:"
    )  
    # Main page introduction
    st.title("Welcome to 2nd Batch of Swinfy RGUKT Basara")
    st.sidebar.success("Select above any project.")
    add_pdf_download_sidebar()




 
    st.info("Use the sidebar to navigate through different dashboards and explore various metrics.")
    st.markdown("## Getting Started")
    st.markdown("""
    1. **Navigate**: Use the sidebar to select different dashboards.
    """)



if __name__=='__main__':
    main()


