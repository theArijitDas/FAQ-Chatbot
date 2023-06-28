import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import React, { useEffect, useRef, useState } from "react";
import "./styles/app.css";
import logo from "./assets/chatbox-icon.svg";

const App = () => {
  const [state, setState] = useState(false);
  const [messages, setMessages] = useState([]);
  const [textInput, setTextInput] = useState("");
  const [minimize, setMinimize] = useState(false);
  const [loading, setLoading] = useState(false);
  const botGreetingMessage = ["Hey, I am Pearl, How can I help you?"];
  const chatboxRef = useRef(null);

  const toggleState = () => {
    setState((prev) => !prev);
    setMinimize(false);
  };

  const onSendButton = () => {
    if (textInput === "" || loading) {
      return;
    }

    const newMessage = { name: "User", message: textInput };
    setMessages((prevMessages) => [...prevMessages, newMessage]);
    setTextInput("");
    setLoading(true);

    setTimeout(() => {
      fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        body: JSON.stringify({ message: textInput }),
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          const responseMessage = { name: "Pearl", message: data.answer };
          setMessages((prevMessages) => [...prevMessages, responseMessage]);

          setLoading(false);
        })
        .catch((error) => {
          console.error("Error:", error);
          const errorMessage = {
            name: "Pearl",
            message: "I cannot process your query right now.",
          };
          setMessages((prevMessages) => [...prevMessages, errorMessage]);
          setLoading(false);
        });
    }, 1000); // Delay the fetch request by 1 second
  };

  const handleInputChange = (event) => {
    setTextInput(event.target.value);
  };

  const handleInputKeyPress = (event) => {
    if (event.key === "Enter") {
      onSendButton();
    }
  };

  const showSupportToast = () => {
    if (!toast.isActive("supportToast") && !state && !minimize) {
      toast.info("Need any help? Chat Support Available", {
        toastId: "supportToast",
      });
    }
  };

  const closeChatSupport = () => {
    setState(false);
    setMessages([]);
    setTextInput("");
  };

  const minimizeWindow = () => {
    setMinimize(true);
    setState(false);
  };

  const renderMessage = (message) => {
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    const parts =String(message).split(urlRegex);
  
    return parts.map((part, index) => {
      if (urlRegex.test(part)) {
        // Render URL as a clickable link
        return (
          <a href={part} target="_blank" rel="noopener noreferrer" key={index}>
            {part}
          </a>
        );
      } else {
        // Render plain text
        return <span key={index}>{part}</span>;
      }
    });
  };

  useEffect(() => {
    if (state && !minimize && messages.length === 0) {
      setTimeout(() => {
        const botMessage = { name: "Pearl", message: botGreetingMessage };
        setMessages((prevMessages) => [...prevMessages, botMessage]);
        setTimeout(() => {
          chatboxRef.current.scrollTop = chatboxRef.current.scrollHeight;
        }, 100);
      }, 1000);
    }
  }, [state, minimize, messages]);

  return (
    <div className="container">
      <ToastContainer
        progressStyle={{ backgroundColor: "#25D366" }}
        toastClassName="whatsapp-toast"
      />
      <div className={`chatbox ${state ? "chatbox--active" : ""}`}>
        <div className="chatbox__support">
          <div className="chatbox__header">
            <div className="chatbox__header--left">
              <div className="chatbox__image--header">
                <img
                  src="https://img.icons8.com/color/48/000000/circled-user-female-skin-type-5--v1.png"
                  alt="image"
                />
                <div className="online-symbol"></div>
              </div>
              <div className="chatbox__content--header">
                <h4 className="chatbox__heading--header">Chat support</h4>
                <p>online</p>
              </div>
            </div>
            <div className="chatbox__header--icons">
              <div
                className={`chatbox__header--icon minimize ${
                  minimize && "minimized"
                }`}
                onClick={minimizeWindow}
              >
                <i className="fas fa-window-minimize"></i>
              </div>
              <div
                className="chatbox__header--icon close"
                onClick={closeChatSupport}
              >
                <i className="fas fa-times"></i>
              </div>
            </div>
          </div>
          <div className="chatbox__messages">
            {loading && (
              <div className="messages__item messages__item--visitor">
                <div className="loading-animation">
                  <span className="loading-dot"></span>
                  <span className="loading-dot"></span>
                  <span className="loading-dot"></span>
                </div>
              </div>
            )}
            {messages
              .slice()
              .reverse()
              .map((message, index) => (
                <div
                  key={index}
                  className={`messages__item ${
                    message.name === "Pearl"
                      ? "messages__item--visitor"
                      : "messages__item--operator"
                  }`}
                >
                  {message.name === "Pearl" ? (
                    <div className="chatbox__message-container">
                      <div className="chatbox__avatar">
                        <img
                          src={`https://img.icons8.com/color/48/000000/circled-user-female-skin-type-5--v1.png`}
                          alt="Chatbot Avatar"
                        />
                      </div>
                      <div className="chatbox__message">{renderMessage(message.message)}</div>
                    </div>
                  ) : (
                    message.message
                  )}
                </div>
              ))}
          </div>
          <div className="chatbox__footer">
            <input
              type="text"
              placeholder="Ask your doubt..."
              value={textInput}
              onChange={handleInputChange}
              onKeyDown={handleInputKeyPress}
            />
            <button
              className="chatbox__send--footer send__button"
              onClick={onSendButton}
            >
              <i className="fa fa-paper-plane"></i>
            </button>
          </div>
        </div>
        {!state && (
          <div className="chatbox__button">
            <button onClick={toggleState} onMouseEnter={showSupportToast}>
              <img src={logo} alt="chat icon" />
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
