import streamlit as st
import threading
from pdf_reader import PDFReader
from pdf_summarizer import PDFSummarizer

DEFAULT_PROMPT_TEMPLATE_FINAL = "Please summarize and Highlight the main points and key takeaways following text use markdown format:"
DEFAULT_PROMPT_TEMPLATE = "Please summarize and Highlight the main points and key takeaways following text use markdown format:"
API_KEY = "your_actual_api_key_here"
OLLAMA_MODEL = 'llama3.1:8b'

def read_and_extract_text(pdf_file_path):
    """Read and extract text from a PDF file"""
    pdf_reader = PDFReader(pdf_file_path)
    extracted_text = pdf_reader.read_pdf()

    return extracted_text

def main():
    st.title("PDF Summarizer")

    # Initialize session state for cancel button
    if "cancel" not in st.session_state:
        st.session_state.cancel = False

    # Initialize session state for summarizer
    if "summarizer" not in st.session_state:
        st.session_state.summarizer = None

    # Initialize session state for thread
    if "thread" not in st.session_state:
        st.session_state.thread = None

    # Load the PDF file from disk
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"], key="pdf_uploader")

    if uploaded_file is not None:
        with st.spinner("Extracting text from PDF..."):
            document_text = read_and_extract_text(uploaded_file)
            filename = uploaded_file.name

        is_cust_promt = st.checkbox("Custmization of Prompt Template")
        if is_cust_promt:
            prompt_template_page = st.text_area("Enter prompt template by Page", value=DEFAULT_PROMPT_TEMPLATE)
            prompt_template_final = st.text_area("Enter prompt template in Final", value=DEFAULT_PROMPT_TEMPLATE_FINAL)
        else:
            prompt_template_page = DEFAULT_PROMPT_TEMPLATE
            prompt_template_final = DEFAULT_PROMPT_TEMPLATE_FINAL

        # Add checkbox for write to local
        # write_to_local = st.checkbox("Write summaries to local files")

        if st.button("Summarize Text"):
            st.session_state.cancel = False
            st.session_state.summarizer = PDFSummarizer(API_KEY, OLLAMA_MODEL, prompt_template_page, prompt_template_final)

            if st.button("Cancel"):
                st.session_state.summarizer.api_client.cancel()
                st.session_state.cancel = True
                st.stop()

            if st.session_state.thread and st.session_state.thread.is_alive():
                st.warning("A summarization process is already running. Please wait for it to finish.")
            else:
                st.session_state.thread = threading.Thread(target=st.session_state.summarizer.pdf_summary, args=(filename, document_text, False))
                st.session_state.thread.start()

            with st.spinner("Summarizing text..."):
                st.session_state.thread.join()

            if not st.session_state.cancel:
                summary = st.session_state.summarizer.result_queue.get()
                # Display a summary of the PDF file
                st.subheader("Summary of PDF")
                st.markdown(summary['final_summary'])

                st.subheader("Summary of PDF Slice")
                st.markdown("\n\n".join(summary['slice_summaries']))

                # Add download buttons
                st.download_button(
                    label="Download Final Summary",
                    data=summary['final_summary'],
                    file_name=f"{filename}_final_summary.md",
                    mime="text/markdown"
                )

                st.download_button(
                    label="Download Slice Summaries",
                    data="\n\n".join(summary['slice_summaries']),
                    file_name=f"{filename}_slice_summaries.md",
                    mime="text/markdown"
                )

        if st.button("Cancel"):
            st.session_state.cancel = True
            if st.session_state.summarizer:
                st.session_state.summarizer.api_client.cancel()
            if st.session_state.thread and st.session_state.thread.is_alive():
                st.session_state.thread.join()
            st.stop()

if __name__ == "__main__":
    main()