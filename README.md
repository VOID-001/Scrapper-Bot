# Scrapper-Bot 🤖
_A RAG x LLM-powered URL Scrapper Bot_

![GitHub top language](https://img.shields.io/github/languages/top/VOID-001/Scrapper-Bot?color=%2334D058)
![GitHub license](https://img.shields.io/github/license/VOID-001/Scrapper-Bot?color=%23007EC6)
![GitHub stars](https://img.shields.io/github/stars/VOID-001/Scrapper-Bot?style=social)

---

## 🌟 Features
- 🚀 **Efficient URL Scraping**: Extracts data from websites using RAG and LLM technologies.
- 🤖 **AI-Powered Backend**: Processes and answers questions with advanced AI capabilities.
- ⚡ **Fast and Scalable**: Built with TypeScript, Python, and Docker for seamless performance.

---

## 📖 Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [API Endpoints](#api-endpoints)
4. [Technologies Used](#technologies-used)
5. [Contributing](#contributing)
6. [License](#license)

---

## 💻 Installation
### Using Docker
1. Clone the repository:
   ```bash
   git clone https://github.com/VOID-001/Scrapper-Bot.git
   cd Scrapper-Bot
   ```

2. Build and run the Docker container:
   ```bash
   docker-compose up --build
   ```

3. Access the application via:
   - **Frontend**: `http://localhost:3000`
   - **Backend**: `http://localhost:8000`

---

## 🚀 Usage
### Frontend
- **URL Acceptor**: Enter a URL in the text field and submit.
- **Question Acceptor**: Enter your question in the text field and submit.
- **Reset Button**: Clears embeddings data.

### Backend (API)
Use the following curl commands to interact with the backend:

1. **Ingest URL**:
   ```bash
   curl -X 'POST' \
   'http://localhost:8000/ingest-url/?url=https%3A%2F%2Fquotes.toscrape.com%2F&max_depth=1' \
   -H 'accept: application/json' \
   -d ''
   ```

2. **Ask Question**:
   ```bash
   curl -X 'POST' \
   'http://localhost:8000/ask-question/?question=“Imperfection is beauty...”' \
   -H 'accept: application/json' \
   -d ''
   ```

3. **Reset Embeddings**:
   ```bash
   curl -X 'DELETE' \
   'http://localhost:8000/reset-embeddings/' \
   -H 'accept: application/json'
   ```

---

## 🛠 Technologies Used
![TypeScript](https://img.shields.io/badge/TypeScript-81.8%25-blue)
![Python](https://img.shields.io/badge/Python-15.3%25-yellow)
![CSS](https://img.shields.io/badge/CSS-2.5%25-purple)

- **Frontend**: TypeScript, CSS
- **Backend**: Python, RAG, LLM
- **Containerization**: Docker, Docker Compose

---

## ✨ Animations & Visuals
![Demo Animation](https://github.com/VOID-001/Scrapper-Bot/assets/demo.gif)

---

## 💬 Contact
For support or questions, open an [issue](https://github.com/VOID-001/Scrapper-Bot/issues) in the repository.
