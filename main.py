from flask import Flask, request, jsonify
import fitz  # PyMuPDF
import openai
import os

app = Flask(__name__)

# Load your OpenAI key (set in Railway variables)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load PDF and extract text once
def load_pdf_text(file_path):
    with fitz.open(file_path) as doc:
        return "\n".join([page.get_text() for page in doc])

pdf_text = load_pdf_text("synergybot.pdf")

@app.route("/", methods=["POST"])
def handle_question():
    try:
        data = request.json
        user_question = data.get("question", "")

        if not user_question:
            return jsonify({"error": "No question provided"}), 400

        messages = [
            {"role": "system", "content": "Answer ONLY using the following documentation:\n\n" + pdf_text},
            {"role": "user", "content": user_question}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
        )

        answer = response['choices'][0]['message']['content']
        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
        if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)

