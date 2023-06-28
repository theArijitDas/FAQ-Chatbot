from flask import Flask, request, jsonify
from flask_cors import CORS
from main import FaqBot

app=Flask(__name__)

CORS(app, origins='http://127.0.0.1:5173', allow_headers=['Content-Type'])

@app.get("/")
def sayHello():
    message={"answer":"Hello"}
    return jsonify(message)

@app.post("/predict")
def predict():
    text=request.get_json().get("message")
    response=FaqBot(text)
    message={"answer":response}
    return jsonify(message)

if __name__=="__main__":
    app.run(debug=True)
