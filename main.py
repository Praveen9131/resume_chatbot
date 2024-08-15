from flask import Flask, request, jsonify, render_template_string
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
@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.json
    question = data.get('question', '')

    if not question:
        return jsonify({'error': 'No question provided'}), 400

    # Build the API request
    api_request_json = {
        "messages": [
            {"role": "system", "content": "You are an AI assistant that answers questions based on a resume.,you have to answer instead of praveen,"},
            {"role": "user", "content": f"Here is the resumw: {resume_text}"},
            {"role": "user", "content": question},
        ],
        "stream": False,
    }

    # Execute the Request
    response = llama.run(api_request_json)

    # Extract and return the answer
    answer = response.json()['choices'][0]['message']['content']
    return jsonify({'answer': answer})

# Frontend HTML template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resume Chatbot</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .chat-container {
            width: 375px;
            max-width: 100%;
            background-color: white;
            border-radius: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }
        .chat-header {
            
            color: white;
            padding: 15px;
            text-align: center;
            font-size: 1.2rem;
            font-weight: bold;
        }
        .chat-messages {
            padding: 20px;
            height: 400px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
        }
        .message {
            margin-bottom: 15px;
            display: flex;
            align-items: flex-end;
        }
        .message.user {
            justify-content: flex-end;
        }
        .message.bot {
            justify-content: flex-start;
        }
        .message p {
            max-width: 70%;
            padding: 10px 15px;
            border-radius: 20px;
            background-color: #e4e6eb;
            margin: 0;
            font-size: 0.9rem;
        }
        .message.user p {
            background-color: #007bff;
            color: white;
        }
        .message.bot p {
            background-color: #f1f0f0;
            color: black;
        }
        .input-container {
            display: flex;
            padding: 10px;
            border-top: 1px solid #ddd;
        }
        input[type="text"] {
            flex: 1;
            padding: 10px;
            border-radius: 20px;
            border: 1px solid #ddd;
            outline: none;
        }
        button {
            background-color: #007bff;
            border: none;
            color: white;
            padding: 10px 20px;
            margin-left: 10px;
            border-radius: 20px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        
        <div class="chat-messages" id="chat-messages">
            <!-- Messages will appear here -->
        </div>
        <div class="input-container">
            <input type="text" id="question" placeholder="Ask a question about the resume...">
            <button onclick="askQuestion()">Send</button>
        </div>
    </div>

    <script>
        function createMessageElement(content, sender) {
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('message', sender);
            const messageText = document.createElement('p');
            messageText.textContent = content;
            messageDiv.appendChild(messageText);
            return messageDiv;
        }

        function askQuestion() {
            const question = document.getElementById('question').value;
            if (!question) return;

            const chatMessages = document.getElementById('chat-messages');

            // Add user message at the end
            const userMessage = createMessageElement(question, 'user');
            chatMessages.appendChild(userMessage);

            // Clear input
            document.getElementById('question').value = '';

            fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: question }),
            })
            .then(response => response.json())
            .then(data => {
                // Add bot response at the end
                const botMessage = createMessageElement(data.answer, 'bot');
                chatMessages.appendChild(botMessage);

                // Scroll to the bottom of the chat
                chatMessages.scrollTop = chatMessages.scrollHeight;
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        }

        // Listen for Enter key press
        document.getElementById('question').addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault(); // Prevent form submission
                askQuestion();
            }
        });
    </script>
</body>
</html>
'''

# Route to serve the frontend
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
