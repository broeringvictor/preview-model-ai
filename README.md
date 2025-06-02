# AI Model & Agent Preview Interface

**A Streamlit-based frontend application designed for rapid testing, demonstration, and validation of AI models and agent services. This interface enables developers and teams to quickly connect with and interact with various AI backends, fostering efficient evaluation—including user acceptance testing for Minimum Viable Products (MVPs)—without the overhead of custom UI development.**

This application provides an intuitive chatbot-style interface, chosen for its widespread familiarity and ease of use. Users can directly configure API keys and select models via the UI, enabling seamless interaction with various backend AI agent services. It is engineered for swift prototyping, early-stage assessment, and showcasing AI capabilities to both technical and non-technical stakeholders.

## ✨ Core Features

* **Intuitive Chat Interface:** A user-friendly, chat-based UI for sending prompts and receiving responses from AI agents.
* **Dynamic Backend Configuration:** Easily set API keys and specify model IDs directly within the application, allowing for on-the-fly switching between different AI services.
* **Flexible Service Integration:** Designed to connect with various AI agent backends by modifying a single, clearly defined service class. This modularity supports diverse AI models and providers.
* **Rapid Prototyping & MVP Testing:** Accelerates the development cycle by providing a ready-to-use interface for testing AI functionalities and gathering feedback on MVPs.
* **Simplified Deployment:** Offers straightforward setup and execution, including a Dockerized option for consistency and ease of deployment.

## 🛠️ Installation

### Prerequisites
* Python 3.8+
* Pip
* Git
* Docker (Recommended for containerized deployment)

### Steps

1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd preview-model-ai
    ```

2.  **Install Dependencies:**
    Using a virtual environment is highly recommended.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

## ▶️ Running the Application

### Option 1: Using Docker (Recommended)

This method ensures a consistent environment and simplifies dependency management.

1.  **Build and Run the Docker Container:**
    From the project's root directory:
    ```bash
    docker compose up --build
    ```
    This command builds the Docker image (if not already present) and starts the container.

2.  **Access the Application:**
    Once the container is running, the Streamlit application is typically accessible via `http://localhost:8501` in your web browser. The `docker-compose.yml` file might specify a different port if modified.

    *Note: The original instructions mentioned attaching to the container and running Streamlit manually. With a well-configured `Dockerfile` and `docker-compose.yml`, Streamlit should start automatically. If manual start is still intended within the container:*

    *To execute commands inside the running container (e.g., for debugging):*
    ```bash
    # Find your container ID or name
    docker ps
    # Attach to the container (replace <container_id_or_name>)
    docker exec -it <container_id_or_name> /bin/bash
    # Then, if needed (though ideally it starts automatically):
    # streamlit run main.py
    ```

### Option 2: Running Locally (Without Docker)

1.  **Ensure all dependencies are installed** as detailed in the "Installation" section above.
2.  **Navigate to the Application Directory:**
    ```bash
    cd preview-model-ai
    ```
3.  **Run the Streamlit Application:**
    ```bash
    streamlit run main.py
    ```
4.  **Access the Application:**
    Streamlit will typically provide a local URL (e.g., `http://localhost:8501`) in your terminal. Open this URL in your web browser.

## ⚙️ How to Use

Once the application is running:

1.  **API Key Configuration:** Enter the API key for the target AI service.
2.  **Model Selection:** Enter the specific Model ID or name you wish to test.
3.  **Prompt Submission:** Type your message, query, or instruction for the AI agent in the designated input field.
4.  **Interaction:** Submit your prompt. The AI agent's response will be displayed directly in the chat interface.

This workflow allows for immediate feedback and iterative testing of the connected AI model or agent.

## 🔄 Customization: Integrating Your AI Agent Service

The application is designed for flexibility, allowing you to connect it to your custom AI agent or a different third-party service. The primary point of integration is the `AgentService` class.

1.  **Locate the Service File:**
    The interaction logic with the AI backend is encapsulated within a service class, typically found in `service/agent_service.py` or a similarly named file within a `service` directory.

2.  **Understand the `AgentService` Interface:**
    Examine the existing `AgentService` class to understand its methods (e.g., a method to send a prompt and receive a response). It will likely take parameters such as the API key, model ID, and user prompt.

3.  **Implement Your Custom Logic:**
    * **Modify Existing Class:** If your new AI service is conceptually similar, you might modify the methods within `agent_service.py` to call your backend. This could involve changing API endpoints, request/response formats, or authentication mechanisms.
    * **Create a New Service Class:** For significantly different services, you might create a new class that adheres to the expected interface or adapt the main application logic to use your new class. Ensure your new service class handles:
        * Initialization (e.g., with API keys).
        * Sending requests to your AI agent's endpoint.
        * Processing responses from your agent.
        * Error handling.

4.  **Update Application References:**
    Ensure that the main application script (`main.py`) correctly imports and instantiates your modified or new `AgentService`.

By abstracting AI interactions into a dedicated service class, this application facilitates straightforward adaptation to various AI backends without requiring modifications to the core UI components.

## 📚 References
* This project was inspired by a chatbot concept from an Asimov Academy course.

## 🤝 Contributing
Contributions are highly valued and welcome! If you have suggestions for improvements, new features, or bug fixes, please feel free to:
1.  Open an issue to discuss the proposed changes.
2.  Fork the repository, make your changes, and submit a pull request.

Please ensure your contributions align with the project's coding standards and objectives.
