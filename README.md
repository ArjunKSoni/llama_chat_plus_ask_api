
LLM Chat Application
====================

This repository contains a FastAPI application for chatting and question answering using a Large Language Model (LLM). The application supports conversational interactions with memory as well as simple Q&A without conversation history.

Features
--------

*   **Chat with history**: Interact with the model while maintaining a conversation history.
*   **Simple Q&A**: Ask questions and get answers without maintaining a conversation history.
*   **Streaming Responses**: Receive responses in a streaming fashion.

Routes
------

### `/chat`

*   **Method**: `POST`
*   **Description**: Chat with the model while maintaining conversation history.
*   **Request Body**:
    *   `input` (string): The input message from the user.
*   **Response**: Streaming response of the model's reply.

### `/ask`

*   **Method**: `POST`
*   **Description**: Ask a question and get a response without maintaining conversation history.
*   **Request Body**:
    *   `input` (string): The input question from the user.
*   **Response**: Streaming response of the model's answer.

Getting Started
---------------

### Prerequisites

*   Python 3.7+
*   Docker (optional, for containerized deployment)
*   A valid `GROQ_API_KEY` (from Groq API)

### Installation

1.  **Clone the repository**:
    
        git clone https://github.com/your-username/llm-chat-app.git
        cd llm-chat-app
    
2.  **Create a virtual environment and activate it**:
    
        python -m venv venv
        source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    
3.  **Install the dependencies**:
    
        pip install -r requirements.txt
    
4.  **Create a `.env` file and add your `GROQ_API_KEY`**:
    
        echo "GROQ_API_KEY=your_groq_api_key" > .env
    

### Running the Application

1.  **Start the FastAPI server**:
    
        uvicorn main:app --reload
    
2.  **The application will be available at** `http://127.0.0.1:8000`.

### Using the Application

You can interact with the application using tools like `curl`, Postman, or directly from your frontend application.

#### Example Requests

**Chat with History**:

    curl -X POST "http://127.0.0.1:8000/chat" -H "Content-Type: application/json" -d '{"input": "Hello, how are you?"}'

**Simple Q&A**:

    curl -X POST "http://127.0.0.1:8000/ask" -H "Content-Type: application/json" -d '{"input": "What is the capital of France?"}'

### Testing

For testing purposes, you can use the base URL `https://llamachat-ipea.onrender.com/`.

**Chat with History**:

    curl -X POST "https://llamachat-ipea.onrender.com/chat" -H "Content-Type: application/json" -d '{"input": "Hello, how are you?"}'

**Simple Q&A**:

    curl -X POST "https://llamachat-ipea.onrender.com/ask" -H "Content-Type: application/json" -d '{"input": "What is the capital of France?"}'

### Docker Deployment (Optional)

To run the application in a Docker container:

1.  **Build the Docker image**:
    
        docker build -t llm-chat-app .
    
2.  **Run the Docker container**:
    
        docker run -d -p 8000:8000 --env-file .env llm-chat-app
    

The application will be available at `http://127.0.0.1:8000`.

