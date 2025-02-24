import os

def process_all_pdfs_in_folder():
    """Process all PDFs in the folder."""
    results = []
    color = 'green'
    if not os.path.exists(folder_path):
        return (['Error: Data folder not found.'], 'red')
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith('.pdf'):
            pdf_path = os.path.join(folder_path, file_name)
            result, status_color = process_pdf_and_generate_json(pdf_path)
            results.extend(result)
            if status_color != 'green':
                color = 'red'
    return (results if results else ['No valid PDF files found in folder.'], color)

