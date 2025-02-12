A brief description of the project and instructions to run it.

markdown
Copy
Edit
# Resume Analyzer

This project is a Streamlit application that:
- Uploads a CSV containing student details and resume links.
- Extracts text from PDF resumes.
- Stores resume details in an SQLite database.
- Uses a pre-trained SentenceTransformer to compute semantic embeddings.
- Matches resumes against a job description based on similarity.

## Project Structure

resume_analyzer/ 
├── app.py # Main Streamlit application 
├── database.py # Database operations (SQLite) 
├── pdf_extraction.py # PDF extraction logic 
├── embeddings.py # Semantic matching and embedding caching 
├── requirements.txt # Required packages 
└── README.md # Project documentation

markdown
Copy
Edit

## Setup and Run

1. **Clone the repository and navigate to the project directory:**
    ```bash
    git clone <repository_url>
    cd resume_analyzer
    ```

2. **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```

5. **Use the web interface to upload CSV files, filter candidates, and match job descriptions.**
