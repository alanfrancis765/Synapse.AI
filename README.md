![banner](src/Home.png)
# Synapse.AI

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Firebase](https://img.shields.io/badge/Firebase-FFCA28?style=for-the-badge&logo=firebase&logoColor=black)](https://firebase.google.com/)
[![Groq](https://img.shields.io/badge/Groq-000000?style=for-the-badge&logo=openai&logoColor=white)](https://groq.com/)
[![GitHub stars](https://img.shields.io/github/stars/alanfrancis765/Synapse.AI?style=for-the-badge)](https://github.com/alanfrancis765/Synapse.AI/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/alanfrancis765/Synapse.AI?style=for-the-badge)](https://github.com/alanfrancis765/Synapse.AI/network/members)
[![GitHub issues](https://img.shields.io/github/issues/alanfrancis765/Synapse.AI?style=for-the-badge)](https://github.com/alanfrancis765/Synapse.AI/issues)
[![GitHub last commit](https://img.shields.io/github/last-commit/alanfrancis765/Synapse.AI?style=for-the-badge)](https://github.com/alanfrancis765/Synapse.AI/commits/main)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/github/license/alanfrancis765/Synapse.AI?style=for-the-badge)](https://github.com/alanfrancis765/Synapse.AI/blob/main/LICENSE)

---

## 📑 Table of Contents

- [Description](#description)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Key Dependencies](#key-dependencies)
- [Project Structure](#project-structure)
- [Development Setup](#development-setup)
- [Contributing](#contributing)
- [License](#license)

## 📝 Description

***Synapse.AI*** is a secure, AI-powered conversational web application. Core objective of the platform is to deliver lightning-fast, intelligent chat interactions while maintaining rigorous enterprise-grade security standards and data persistence. Rather than executing heavy language models on local hardware, Synapse.AI leverages Groq Cloud's Language Processing Units (LPUs) to run Meta's open-source Llama large language model at ultra-low latency.

To turn a standard stateless LLM into a fully functional product, the application integrates a robust backend powered by Firebase. It features a secure login/registration system using Firebase Authentication via REST APIs and preserves user context across sessions by dynamically streaming and updating history logs inside a dedicated Google Cloud Firestore NoSQL database.

## 🛠️ Tech Stack

### 🛠️ Tech Stack & Architecture

* 🐍 **Python** — The core programming language used to develop the entire application.
* 🎈 **Streamlit** — The frontend framework utilized to build the interactive user interface. 
* 🔥 **Firebase Authentication** — Used to manage user registration and secure logins.
* 📦 **Google Cloud Firestore** — The NoSQL cloud database.
* ⚡ **Groq Cloud (LPU)** — The ultra-low latency inference engine infrastructure.
* 🦙 **Meta Llama** — The open-source Large Language Model (LLM) serving as the core "AI brain".


## ⚡ Quick Start

```bash

# 1. Clone the repository
git clone [https://github.com/alanfrancis765/Synapse.AI.git](https://github.com/alanfrancis765/Synapse.AI.git)

# 2. Create & activate a virtualenv
python -m venv venv && source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

## 📦 Key Dependencies

```
streamlit: 1.35.0
groq: 0.9.0
python-dotenv: latest
firebase-admin: latest
requests: latest
```

## 📁 Project Structure

```
.
├── .devcontainer
│   └── devcontainer.json
├── LICENSE
├── LLM.py
├── app.py
├── backend
│   ├── __init__.py
│   └── auth_backend.py
└── requirements.txt
```

## 🛠️ Development Setup

### Python
1. Install Python (v3.10+ recommended)
2. `python -m venv venv && source venv/bin/activate`  (Windows: `venv\Scripts\activate`)
3. `pip install -r requirements.txt`

## 👥 Contributing

Contributions are welcome! Here's the standard flow:

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/alanfrancis765/Synapse.AI.git`
3. **Branch**: `git checkout -b feature/your-feature`
4. **Commit**: `git commit -m 'feat: add some feature'`
5. **Push**: `git push origin feature/your-feature`
6. **Open** a pull request

Please follow the existing code style and include tests for new behavior where applicable.

## 📜 License

This project is licensed under the **MIT** License.

---
*This README was generated with ❤️ by [ReadmeBuddy](https://readmebuddy.com)*
