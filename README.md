
# ✦ AIRA AI – Intelligent AI Chatbot

AIRA AI is an intelligent conversational chatbot developed using Python, Streamlit, LangChain, and Groq API. It provides users with a simple and interactive platform to communicate with an AI assistant, ask questions, explore ideas, and receive helpful responses in real time.

The application features a modern dark-themed interface, conversation history management, and AI-powered response generation.

## ✨ Features

- **AI-powered conversations:** Get intelligent responses using Groq's language models.
- **Real-time streaming:** View responses as they are generated.
- **Modern user interface:** Clean and responsive dark-themed design.
- **Chat history:** Automatically save conversations using SQLite.
- **New conversations:** Start multiple independent chats.
- **Search conversations:** Find previous chats easily.
- **Rename and delete chats:** Organize your conversation history.
- **Regenerate responses:** Request another answer from AIRA.
- **Export conversations:** Download chat history in Markdown format.
- **Suggested prompts:** Explore example questions and tasks.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web application |
| LangChain | LLM integration and conversation handling |
| Groq API | AI response generation |
| SQLite | Conversation and message storage |
| Python-dotenv | Secure environment variable management |

## 📁 Project Structure

```text
AIRA-AI-Chatbot/
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
└── chatbot.db
```

**Note:** The `.env` and `chatbot.db` files are excluded from GitHub for security and privacy.

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/AIRA-AI-Chatbot.git
```

### 2. Navigate to the project folder

```bash
cd AIRA-AI-Chatbot
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure your Groq API key

Create a `.env` file in the project directory and add:

```env
GROQ_API_KEY=your_groq_api_key
```

Get your API key from:

https://console.groq.com/keys

Never share your API key or commit your `.env` file.

### 5. Run the application

```bash
python -m streamlit run app.py
```

The application will open in your browser, usually at:

```text
http://localhost:8501
```

## 🖥️ Application Highlights

AIRA AI provides a conversational interface where users can ask questions, receive AI-generated responses, and manage their previous conversations.

Add your application screenshots here:

```text
assets/
├── aira-home.png
└── aira-chat.png
```

## 🔐 Security

- API credentials are stored in environment variables.
- The `.env` file is excluded through `.gitignore`.
- Local conversation data is stored in SQLite.
- Database files are excluded from the public repository.

## 🚀 Future Enhancements

- Voice-based interaction.
- Conversation export in PDF format.
- User authentication.
- Customizable AI personalities.
- Deployment for public access.


⭐ If you find this project interesting, consider giving the repository a star!
