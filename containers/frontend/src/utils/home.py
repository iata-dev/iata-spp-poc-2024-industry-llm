from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, render_template_string
from werkzeug.utils import secure_filename
import os

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template_string('\n            <div style="text-align:center; font-family: Arial, sans-serif; color: #ff4d4d;">\n                <h1>No file part in the request!</h1>\n                <a href="/" style="color: #007bff;">Go back</a>\n            </div>\n            ')
        file = request.files['file']
        if file.filename == '':
            return render_template_string('\n            <div style="text-align:center; font-family: Arial, sans-serif; color: #ff4d4d;">\n                <h1>No selected file!</h1>\n                <a href="/" style="color: #007bff;">Go back</a>\n            </div>\n            ')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            if filename.lower().endswith('.pdf'):
                results, color = process_pdf_and_generate_json(file_path)
            else:
                results = ['Image processing is not fully supported yet.']
                color = 'orange'
            return render_template_string('\n            <!DOCTYPE html>\n            <html lang="en">\n            <head>\n                <meta charset="UTF-8">\n                <meta name="viewport" content="width=device-width, initial-scale=1.0">\n                <title>Upload Successful</title>\n                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css">\n                <style>\n                    body { background-color: #121212; color: #fff; font-family: Arial, sans-serif; }\n                    .container { margin-top: 50px; }\n                    .card { background-color: #1f1f1f; }\n                    a { color: #007bff; text-decoration: none; }\n                    .small-message { font-size: 18px; color: #fff; }\n                    .large-success { font-size: 24px; color: #28a745; font-weight: bold; }\n                </style>\n            </head>\n            <body>\n                <div class="container text-center">\n                    <div class="card p-4 shadow-lg">\n                        <p class="small-message">File uploaded successfully!</p>\n                        <p class="large-success">{{ results[0] }}</p>\n                        <ul class="list-group mt-3">\n                        {% for result in results[1:] %}\n                            <li class="list-group-item bg-dark text-light">{{ result }}</li>\n                        {% endfor %}\n                        </ul>\n                        <a href="/" class="btn btn-primary mt-3">Go Back</a>\n                    </div>\n                </div>\n            </body>\n            </html>\n            ', results=results, color=color)
    return render_template_string('\n    <!DOCTYPE html>\n    <html lang="en">\n    <head>\n        <meta charset="UTF-8">\n        <meta name="viewport" content="width=device-width, initial-scale=1.0">\n        <title>VALIDOC Submission Dashboard</title>\n        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css">\n        <style>\n            body { background-color: #121212; color: #fff; font-family: Arial, sans-serif; }\n            .container { margin-top: 50px; }\n            .card { background-color: #1f1f1f; }\n            input[type="file"] { background-color: #333; color: #fff; }\n            input[type="file"]::-webkit-file-upload-button {\n                background-color: #007bff; color: white; border: none; padding: 5px 10px; cursor: pointer;\n            }\n            input[type="file"]::-webkit-file-upload-button:hover {\n                background-color: #0056b3;\n            }\n            a { color: #007bff; text-decoration: none; }\n        </style>\n    </head>\n    <body>\n        <div class="container text-center">\n            <div class="card p-4 shadow-lg">\n                <h1 class="text-primary">VALIDOC Submission Dashboard</h1>\n                <p>Upload a PDF or Image file to process it and view results.</p>\n                <form method="POST" enctype="multipart/form-data" class="mt-4">\n                    <input type="file" name="file" class="form-control mb-3" required>\n                    <button type="submit" class="btn btn-success">Upload</button>\n                </form>\n                <p class="mt-4">Visit the <a href="/dashboard/">Dashboard</a> to view real-time updates.</p>\n            </div>\n        </div>\n    </body>\n    </html>\n    ')

