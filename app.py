from flask import Flask, request, send_file, render_template, after_this_request
from pypdf import PdfWriter
import os
import uuid

app = Flask(__name__)

# Folder paths for storing temporary files
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

# Create folders if they don’t exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Home route → renders UI
@app.route('/')
def home():
    return render_template("index.html")

# Merge route → handles PDF merging
@app.route('/merge', methods=['POST'])
def merge():
    # Get uploaded files
    files = request.files.getlist('pdfs')

    # Validation: minimum 2 files required
    if len(files) < 2:
        return "Upload at least 2 PDFs to merge"

    if not files or files[0].filename == '':
        return "No files selected"

    merger = PdfWriter()
    temp_paths = []

    # Save files temporarily and add to merger
    for file in files:
        if not file.filename.lower().endswith('.pdf'):
            return "Only PDF files allowed"

        unique_name = str(uuid.uuid4()) + ".pdf"
        path = os.path.join(UPLOAD_FOLDER, unique_name)
        file.save(path)

        temp_paths.append(path)
        merger.append(path)

    # Create merged output file
    output_file = os.path.join(OUTPUT_FOLDER, str(uuid.uuid4()) + ".pdf")
    merger.write(output_file)

    # delete uploaded temp files
    for path in temp_paths:
        os.remove(path)

    # Delete merged file after sending it
    @after_this_request
    def cleanup(response):
        try:
            os.remove(output_file)
        except Exception:
            pass
        return response

    # Send merged PDF to user
    return send_file(output_file, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)