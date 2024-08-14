from flask import Flask, request, jsonify
from llamaapi import LlamaAPI

# Initialize Flask app
app = Flask(__name__)

# Initialize the LlamaAPI SDK
llama = LlamaAPI("LL-GUoKRxfem5xvKwxOlTFX5uLvgt3JhbZBMw8dv60AOhg0K3OWAXx9hwdyveOMlTcV")

# Function to read the resume text from a file
def read_resume_text(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Path to your resume text file
resume_txt_path = "assets/a.txt"  # Update the path if necessary
resume_text = read_resume_text(resume_txt_path)

# API endpoint to handle questions
@app.route('/ask', methods=['GET', 'POST'])
def ask_question():
    if request.method == 'POST':
        data = request.json
        question = data.get('question', '')

        if not question:
            return jsonify({'error': 'No question provided'}), 400

    elif request.method == 'GET':
        question = request.args.get('question', '')

        if not question:
            return jsonify({'error': 'No question provided'}), 400

    # Build the API request
    api_request_json = {
        "messages": [
            {"role": "system", "content": "You are an AI assistant that answers questions based on a resume. You have to answer instead of Praveen."},
            {"role": "user", "content": f"Here is the resume: {resume_text}"},
            {"role": "user", "content": question},
        ],
        "stream": False,
    }

    # Execute the Request
    response = llama.run(api_request_json)

    # Extract and return the answer
    answer = response.json()['choices'][0]['message']['content']
    return jsonify({'answer': answer})

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
