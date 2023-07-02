from flask import Flask, request, jsonify
from flask_cors import CORS
from main import FaqBot
import re

app=Flask(__name__)

CORS(app, origins='http://127.0.0.1:5173', allow_headers=['Content-Type'])

COLLEGE_DOMAIN_PATTERN= r"@(iitism\.ac\.in)$"

email_verified= False

@app.post("/verify_email")
def verify_email():
    email=request.get_json().get("email")
    global email_verified
    if email and re.search(COLLEGE_DOMAIN_PATTERN,email):
        email_verified=True
        return jsonify({"message":"Thanks. Please help me with your mobile number too. I promise I won't spam."}),201
    else:
        return jsonify({"message":"Please provide your institute email id"}),401
    
    

@app.post("/predict")
def predict():
    if not email_verified:
        return 
    text=request.get_json().get("message")
    response=FaqBot(text)
    message={"answer":response}
    return jsonify(message)

if __name__=="__main__":
    app.run(debug=True)
