# Preview Model AI
🚀 A simple Streamlit interface for quickly testing and previewing AI agent services.

This application allows you to easily interact with different AI agent backends by configuring the model and API key directly through the user interface. It's designed for rapid testing and early-stage evaluation of AI models.

## ✨ Features
Simple UI: Intuitive interface to send requests and view responses from AI agents.

Direct Configuration: Set the API key and choose the model directly in the app.

Flexible Backend: Easily swap out the AI agent service by modifying a single service file.

## 🛠️ Installation
#### Clone the repository:

```
git clone <your-repository-url>
cd preview-model-ai
```

#### Install dependencies:

```
pip install -r requirements.txt

```


#### ▶️ Running the Application

Using Docker (Recommended)

```
docker compose up --build
```

execute the following command in conteiner Preview Model AI (Attach Shell)


```
streamlit run main.py
```


## ⚙️ How to Use
Once the application is running, you will see an interface where you can input:

Your API Key for the AI service.

The specific Model ID you wish to test.

Your Prompt or message for the AI agent.

Submit your request and view the agent's response directly in the UI.

## 🔄 Customization: Changing the AI Agent Service
The core logic for interacting with the AI agent is encapsulated in the AgentService class, typically found in a file like agent_service.py (often within a service/ directory).

To use a different AI model or service provider:

> Locate the service file: This is usually service/agent_service.py.


## References:
Inspired by a chatbot created in an Asimov Academy course.

## 🤝 Contributing
Contributions are welcome! If you have suggestions or improvements, please feel free to open an issue or submit a pull request.