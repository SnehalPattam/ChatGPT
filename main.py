from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo
import openai

# Set your OpenAI API key
openai.api_key = ""

app = Flask(__name__)

# Use the correct MongoDB URI
app.config["MONGO_URI"] = ""
mongo = PyMongo(app)

@app.route('/')
def home():
    chats = mongo.db.chats.find({})
    myChats = [chat for chat in chats]
    print(myChats)
    return render_template("index.html", myChats=myChats)

@app.route("/api", methods=["GET", "POST"])
def qa():
    if request.method == "POST":
        print(request.json)
        question = request.json.get("question")
        chat = mongo.db.chats.find_one({"question": question})
        print(chat)
        if chat:
            data = {"question": question, "answer": f"{chat['answer']}"}
            return jsonify(data)
        else:
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo",  # Ensure you use the correct model name
                messages=[{"role": "user", "content": question}],
                temperature=1,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            # Extract the content of the response
            answer = response.choices[0].message['content']
            # Insert the question and actual answer into MongoDB
            mongo.db.chats.insert_one({"question": question, "answer": answer})
            # Return the actual response data
            data = {"question": question, "answer": answer}
            return jsonify(data)
    
    # Handle GET requests or other cases
    data = {"result": "Thank you! I'm just a machine learning model designed to respond to questions and generate text based on my training data. Is there anything specific you'd like to ask or discuss?"}
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
