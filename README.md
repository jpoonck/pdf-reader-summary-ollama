# pdf-reader-summary-ollama

This project is designed to read a PDF file containing content related to linear algebra and statistics, summarize the text, diagrams, and formulas, and provide a concise overview of the material.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd pdf-reader-summary-ollama
   ```

2. Install the required dependencies:
   ```E
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
streamlit run src/main.py
```

## Functionality

- **PDF Reading**: The application reads a PDF file and extracts relevant text, diagrams, and formulas using the `PDFReader` class.
- **Text Summarization**: It divides the extracted text into manageable slices and makes API calls to summarize each slice using the `OllamaAPIClient`.
- **Summary of Summaries**: Finally, it summarizes the collected summaries to provide a concise overview of the content.

## Dependencies

- `requests`: For making HTTP requests to the summarization API.
- `PyPDF2` or `pdfplumber`: For reading and extracting text from PDF files.
- `streamlit`: For creating the web interface.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.