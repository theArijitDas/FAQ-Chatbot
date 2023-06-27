import React, { useState } from 'react';
import './styles/app.css';
import logo from "./assets/chatbox-icon.svg"

const App = () => {
  const [state, setState] = useState(false);
  const [messages, setMessages] = useState([]);
  const [textInput, setTextInput] = useState('');

  const toggleState = () => {
    setState(!state);
  };

  const onSendButton = () => {
    if (textInput === '') {
      return;
    }

    const newMessage = { name: 'User', message: textInput };
    setMessages([...messages, newMessage]);

    fetch('http://127.0.0.1:5000/predict', {
      method: 'POST',
      body: JSON.stringify({ message: textInput }),
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json',
      },
    }) ✖
      .then((response) => response.json())
      .then((data) => {
        const responseMessage = { name: 'Sam', message: data.answer };
        setMessages([...messages, responseMessage]);
        setTextInput('');
      })
     
      .catch((error) => {
        console.error('Error:', error);
        setTextInput('');
      });
  };

  const handleInputChange = (event) => {
    setTextInput(event.target.value);
  };

  return (
    <div className="container">
      <div className={`chatbox ${state ? 'chatbox--active' : ''}`}>
        <div className="chatbox__support">
          <div className="chatbox__header">
            <div className="chatbox__image--header">
              <img
                src="https://img.icons8.com/color/48/000000/circled-user-female-skin-type-5--v1.png"
                alt="image"
              />
            </div>
            <div className="chatbox__content--header">
              <h4 className="chatbox__heading--header">Chat support</h4>
              <p className="chatbox__description--header">
                Hi. My name is Sam. How can I help you?
              </p>
            </div>
          </div>
          <div className="chatbox__messages">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`messages__item ${
                  message.name === 'Sam'
                    ? 'messages__item--visitor'
                    : 'messages__item--operator'
                }`}
              >
                {message.message}
              </div>
            ))}
          </div>
          <div className="chatbox__footer">
            <input
              type="text"
              placeholder="Write a message..."
              value={textInput}
              onChange={handleInputChange}
            />
            <button className="chatbox__send--footer send__button" onClick={onSendButton}>
              Send
            </button>
          </div>
        </div>
        <div className="chatbox__button">
          <button onClick={toggleState}>
            <img src={logo} alt="chat icon" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default App;
