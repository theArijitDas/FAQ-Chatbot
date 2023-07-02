from flask import Flask, request, jsonify
from flask_cors import CORS
from main import FaqBot
import re
import random
from dotenv import load_dotenv
import os
import vonage


app = Flask(__name__)

CORS(app, origins='http://127.0.0.1:5173', allow_headers=['Content-Type'])

load_dotenv()

COLLEGE_DOMAIN_PATTERN = r"@(iitism\.ac\.in)$"

email_verified = False
phone_verified = False


@app.post("/verify_email")
def verify_email():
    email = request.get_json().get("email")
    global email_verified
    if email and re.search(COLLEGE_DOMAIN_PATTERN, email):
        email_verified = True
        return jsonify({"message": "Thanks. Please help me with your mobile number too. I promise I won't spam."}), 201
    else:
        return jsonify({"message": "Please provide your institute email id"}), 401


@app.post("/verify_phone")
def verify_phone():
    global phone_verified
    phoneNo = request.get_json().get("phone")
    phoneNo = "91"+phoneNo
    client = vonage.Client(key=os.environ["KEY"], secret=os.environ["SECRET"])
    sms = vonage.Sms(client)
    global otp
    otp=random.randint(1000,9999)
    # otp=2002
    responseData = sms.send_message(
        {
            "from": "Pearl Chatbot",
            "to": phoneNo,
            "text": "Your Otp:"+str(otp),
        }
    )
    if responseData["messages"][0]["status"] == "0":
        return jsonify({"message": "You must have received an OTP. Please enter the OTP !"}), 201


@app.post("/verify_otp")
def verify_otp():
    global otp_verified
    newOtp=request.get_json().get("otp")
    
    print(newOtp,otp)
    
    if newOtp==str(otp):
        otp_verified=True
        return jsonify({"message": "Account has been verified, please ask your doubts..."}), 201
    else:
        return jsonify({"message": "Invalid OTP!, please enter the correct OTP"}), 401

   
    


@app.post("/predict")
def predict():
    if not email_verified or not otp_verified:
        return
    text = request.get_json().get("message")
    response = FaqBot(text)
    message = {"answer": response}
    return jsonify(message)


if __name__ == "__main__":
    app.run(debug=True)
