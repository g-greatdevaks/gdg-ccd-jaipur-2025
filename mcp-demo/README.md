# FastMCP Math Demo (GDG CCD Jaipur 2025)

A demo showing how to build and connect a local **MCP Server** and **MCP Client** using [FastMCP](https://gofastmcp.com/) for math operations and LLM-powered number-in-words explanations.  
This includes a Streamlit web app, a CLI client, and Gemini LLM integration.

---

## 📑 Table of Contents

- [FastMCP Math Demo (GDG CCD Jaipur 2025)](#fastmcp-math-demo-gdg-ccd-jaipur-2025)
- [📂 Directory Structure](#📂-directory-structure)
- [🚀 Quick Start](#🚀-quick-start)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Python Version and Dependencies](#2-python-version-and-dependencies)
  - [3. Set Up Python Virtual Environment](#3-set-up-python-virtual-environment)
  - [4. Install Dependencies](#4-install-dependencies)
  - [5. Configure Gemini API Key](#5-configure-gemini-api-key)
  - [6. Start the MCP Server](#6-start-the-mcp-server)
  - [7. Run the Streamlit Web App](#7-run-the-streamlit-web-app)
  - [8. Try the CLI MCP Client](#8-try-the-cli-mcp-client)
- [🧑‍💻 Demo Summary](#🧑‍💻-demo-summary)
- [📝 Notes and Disclaimer](#📝-notes-and-disclaimer)
- [☁️ Cloud Run Deployment](#️☁️-cloud-run-deployment)
- [📚 References](#📚-references)

---

## 📂 Directory Structure

```
mcp-demo/
│
├── .streamlit/
│ └── secrets.toml # Store Gemini API Key here.
│
├── clients/
│ └── math_client.py # CLI MCP client.
│
├── host-app/
│ └── app.py # Streamlit web application.
│
├── servers/
│ └── math_server.py # MCP server with math tools and LLM sampling.
│
└── requirements.txt # Python dependencies.
```

---

## 🚀 Quick Start

### 1. Clone the Repository

```
git clone https://github.com/g-greatdevaks/gdg-ccd-jaipur-2025.git
cd mcp-demo
```

---

### 2. Python Version and Dependencies

- **Python 3.9 or higher is required.**
- All required libraries are listed in `requirements.txt` and will be installed in the next step.

Check your Python version:

```
python3 --version
```

or, if `python3` is not available, try:

```
python --version
```

> **Note:**
> On some systems, especially macOS and Linux, you may need to use `python3` and `pip3` instead of `python` and `pip`.
> Replace `python` with `python3` and `pip` with `pip3` in the commands below if needed.

If you do not have Python 3.9+ installed, download it from [python.org](https://www.python.org/downloads/).

---

### 3. Set Up Python Virtual Environment

#### **Mac / Linux**

```
python3 -m venv venv
source venv/bin/activate
```

or, if `python3` is not available, try:

```
python -m venv venv
source venv/bin/activate
```

#### **Windows**

```
python3 -m venv venv
venv\Scripts\activate
```

or, if `python3` is not available, try:

```
python -m venv venv
venv\Scripts\activate
```

If you are using PowerShell:
```
.\venv\Scripts\Activate.ps1
```

> **Troubleshooting PowerShell Script Activation**
>
> If you see an error like:
>
> ```
> .\venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on this system.
> ```
>
> This means PowerShell’s execution policy is blocking script execution.  
> To allow activation scripts to run, open PowerShell and run:
>
> ```
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```
>
> You may need to confirm the change.  
> This command allows you to run scripts you create (like activating your virtual environment) while still protecting you from unsigned scripts downloaded from the internet.
>
> For more details, see [Microsoft Docs: about_Execution_Policies](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies).

---

### 4. Install Dependencies

```
pip3 install -r requirements.txt
```

or, if `pip3` is not available, try:

```
pip install -r requirements.txt
```

---

### 5. Configure Gemini API Key

#### **Recommended:**

Create `.streamlit/secrets.toml` in the root directory:

```
# .streamlit/secrets.toml
GEMINI_API_KEY = "your-gemini-api-key-here"
```

- Get your free Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

#### **Alternatively:**

Set the environment variable before running the app:

- **Mac/Linux:**

```
export GEMINI_API_KEY="your-gemini-api-key-here"
```

- **Windows (CMD):**

```
set GEMINI_API_KEY=your-gemini-api-key-here
```

- **Windows (PowerShell):**

```
$env:GEMINI_API_KEY="your-gemini-api-key-here"
```

---

### 6. Start the MCP Server

```
python3 servers/math_server.py
```

or, if `python3` is not available, try:

```
python servers/math_server.py
```

- The server will listen at `http://127.0.0.1:8080/mcp`.

---

### 7. Run the Streamlit Web App

```
streamlit run host-app/app.py
```

- Open the link shown in your terminal (typically `http://localhost:8501`).

> By default, Streamlit runs on port 8501. If port 8501 is already in use, Streamlit will automatically use the next available port (e.g., 8502, 8503, etc.).
> 
> You can also specify a port explicitly with:
>
> ```
> streamlit run host-app/app.py --server.port 8505
> ```
>
> or set it in `.streamlit/config.toml` as:
>
> ```
> [server]
> port = 8505
> ```

- Enter numbers, select operation, toggle "Express the result in words (LLM)" to see LLM-powered explanations, and choose "US" or "India" for the numbering system.

---

### 8. Try the CLI MCP Client

```
python3 clients/math_client.py 
```

or, if `python3` is not available, try:

```
python clients/math_client.py 
```

- This will run demo math operations and showcase error handling in the terminal.

---

## 🧑‍💻 Demo Summary

This project demonstrates:

- **MCP Server** (`servers/math_server.py`):  
  - Exposes math tools (`add` and `subtract`) and a tool (`explain_calculation`) that uses LLM sampling to convert numbers to words in US/Indian numbering systems.
- **MCP Client** (`clients/math_client.py`):  
  - Connects to the server and calls tools via the MCP protocol, with logging and error handling.
- **Streamlit Host App** (`host-app/app.py`):  
  - User-friendly web interface for math operations and LLM-powered explanations.
  - Integrates Gemini LLM via Google API for dynamic, country-aware number-in-words output.
- **All components run locally** for learning and demonstration purposes.

---

## 📝 Notes and Disclaimer

- The content and views presented during the session are the author’s own and not of any organizations they are associated with.
- **This code is for illustration and educational purposes only.**
    - Not production-grade; error handling, security, and scalability are not fully addressed.

---

## ☁️ Cloud Run Deployment

> **Coming Soon:**  
> Instructions for deploying the MCP Server to Google Cloud Run will be added here.

---

## 📚 References

- [FastMCP Documentation](https://gofastmcp.com/)
- [Google Gemini API](https://aistudio.google.com/app/apikey)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Python Documentation](https://docs.python.org/3/)