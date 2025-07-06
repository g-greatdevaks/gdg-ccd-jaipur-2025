# FastMCP Number-in-Words Demo (with Gemini LLM & Cloud Run-based Barcode Generator) (GDG CCD Jaipur 2025)

A demo showing how to build and connect **MCP Servers** and **MCP Clients** using [FastMCP](https://gofastmcp.com/) for Math operations, LLM-powered number-in-words explanations, and hybrid orchestration across local and cloud environments.

This project includes:
- A **Streamlit Web Application** for interactive exploration.
- A **CLI-based MCP Client** for command-line testing.
- **Gemini LLM integration** via FastMCP's sampling handler, enabling dynamic number-in-words explanations.
- A **serverless barcode generator tool** hosted on Google Cloud Run as a remote MCP Server.

The demo highlights how to compose and orchestrate tools across both local and remote MCP Servers, leveraging FastMCP’s standard protocol for secure, flexible, and Pythonic LLM agent workflows.

---

## 📑 Table of Contents

- [FastMCP Number-in-Words Demo (with Gemini LLM & Cloud Run-based Barcode Generator) (GDG CCD Jaipur 2025)](#fastmcp-number-in-words-demo-with-gemini-llm--cloud-run-based-barcode-generator-gdg-ccd-jaipur-2025)
- [📂 Directory Structure](#📂-directory-structure)
- [Prerequisite Installations](#prerequisite-installations)
- [🚀 End-to-End Quick Start (Local + Cloud Run)](#🚀-end-to-end-quick-start-local--cloud-run)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Python Version and Dependencies](#2-python-version-and-dependencies)
  - [3. Set Up Python Virtual Environment](#3-set-up-python-virtual-environment)
  - [4. Install Dependencies](#4-install-dependencies)
  - [5. Configure Gemini API Key](#5-configure-gemini-api-key)
  - [6. Start the MCP Server](#6-start-the-mcp-server)
  - [7. Build and Deploy the Cloud Run MCP Server (Barcode Generator)](#7-build-and-deploy-the-cloud-run-mcp-server-barcode-generator)
    - [A. GCP Project and Region Configuration](#a-gcp-project-and-region-configuration)
    - [B. Enable Required Google Cloud APIs](#b-enable-required-google-cloud-apis)
    - [C. Prepare Dockerfile](#c-prepare-dockerfile)
    - [D. Create Artifact Registry Repository (if not already)](#d-create-artifact-registry-repository-if-not-already)
    - [E. Build and Push Docker Image](#e-build-and-push-docker-image)
    - [F. Deploy to Cloud Run](#f-deploy-to-cloud-run)
    - [G. Grant Cloud Run Invoker Role](#g-grant-cloud-run-invoker-role)
  - [8. Install and Start the Cloud Run Proxy](#8-install-and-start-the-cloud-run-proxy)
  - [9. Try the CLI MCP Client](#9-try-the-cli-mcp-client)
  - [10. Run the Streamlit Web App](#10-run-the-streamlit-web-app)
  - [11. (Optional) Visualize with MCP Inspector](#11-optional-visualize-with-mcp-inspector)
- [🧑‍💻 Demo Summary](#🧑‍💻-demo-summary)
- [📝 Notes and Disclaimer](#📝-notes-and-disclaimer)
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
│ └── math_client.py # CLI MCP Client.
│
├── host-app/
│ └── app.py # Streamlit Web Application.
│
├── servers/
│ ├── math_server.py # MCP Server with math tools and LLM sampling.
│ └── cloudrun_server.py # MCP Server for barcode tool (Cloud Run).
│
├── Dockerfile # For Cloud Run MCP Server.
└── requirements.txt # Python dependencies.
```

---

## Prerequisite Installations

- Python 3.9 or higher.
- [Docker](https://docs.docker.com/get-docker/)
- [Google Cloud SDK (gcloud)](https://cloud.google.com/sdk/)
- [Node.js and npx](https://nodejs.org/) (for MCP Inspector, optional)
- Access to a Google Cloud Project with billing enabled.
  - **Tip:** If new to Google Cloud, one can avail up to [$300 in free GCP credits](https://cloud.google.com/free) when by signing up for a new account.

---

## 🚀 End-to-End Quick Start (Local + Cloud Run)

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

If Python 3.9+ is not installed, the same can be downloaded from [python.org](https://www.python.org/downloads/).

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

If using PowerShell:
```
.\venv\Scripts\Activate.ps1
```

> **Troubleshooting PowerShell Script Activation**
>
> If an error like the following is reported:
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
> Confirm the changes.  
> This command allows running the scripts created by the user (like activating your virtual environment) while enforcing protection against unsigned scripts downloaded from the internet.
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

#### **Recommended**

Create `.streamlit/secrets.toml` in the root directory:

```
# .streamlit/secrets.toml
GEMINI_API_KEY = "your-gemini-api-key-here"
```

- Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

#### **Alternatively**

Set the environment variable before running the app:

- **Mac/Linux**

```
export GEMINI_API_KEY="your-gemini-api-key-here"
```

- **Windows (CMD)**

```
set GEMINI_API_KEY=your-gemini-api-key-here
```

- **Windows (PowerShell)**

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

### 7. Build and Deploy the Cloud Run MCP Server (Barcode Generator)

#### **A. GCP Project and Region Configuration**

- Set the GCP Project and Region for all commands:
    ```
    export PROJECT_ID="gcp-project-id"
    export REGION=us-central1
    gcloud config set project $PROJECT_ID
    gcloud config set run/region $REGION
    ```

> Reference the [official documentation](https://cloud.google.com/run/docs/setup) for setting up the GCP environment for hosting Cloud Run-based MCP Server.
> 
> Additional references:
> 
> 1. [Host MCP Servers on Cloud Run](https://cloud.google.com/run/docs/host-mcp-servers#container-images)
> 2. [Build and Deploy a Remote MCP Server to Google Cloud Run in Under 10 Minutes](https://cloud.google.com/blog/topics/developers-practitioners/build-and-deploy-a-remote-mcp-server-to-google-cloud-run-in-under-10-minutes?e=48754805)

#### **B. Enable Required Google Cloud APIs**

Enable the following APIs:

```
gcloud services enable artifactregistry.googleapis.com run.googleapis.com cloudbuild.googleapis.com cloudresourcemanager.googleapis.com --project $PROJECT_ID
```

#### **C. Prepare Dockerfile**

Place this at the root of `mcp-demo/`:

```
FROM python:3.11-slim

WORKDIR /app

# Copy only requirements first to leverage Docker cache.
COPY requirements.txt .

# Install dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code.
COPY servers/cloudrun_server.py .

CMD ["python", "cloudrun_server.py"]
```

#### **D. Create Artifact Registry Repository (if not already)**

```
gcloud artifacts repositories create remote-mcp-servers \
  --repository-format=docker \
  --location=$REGION \
  --description="Repository for remote MCP servers" \
  --project=$PROJECT_ID
```

#### **E. Build and Push Docker Image**

```
docker build -t $REGION-docker.pkg.dev/$PROJECT_ID/remote-mcp-servers/mcp-cloudrun-server:latest .
gcloud auth configure-docker $REGION-docker.pkg.dev
docker push $REGION-docker.pkg.dev/$PROJECT_ID/remote-mcp-servers/mcp-cloudrun-server:latest
```

#### **F. Deploy to Cloud Run**

```
gcloud run deploy mcp-cloudrun-server \
  --image $REGION-docker.pkg.dev/$PROJECT_ID/remote-mcp-servers/mcp-cloudrun-server:latest \
  --region $REGION \
  --no-allow-unauthenticated \
  --port 8080 \
  --project $PROJECT_ID
```

- The `--no-allow-unauthenticated` flag ensures that the service is protected by IAM.

#### **G. Grant Cloud Run Invoker Role**

```
gcloud run services add-iam-policy-binding mcp-cloudrun-server \
  --region $REGION \
  --member="user:YOUR_EMAIL@example.com" \
  --role="roles/run.invoker" \
  --project $PROJECT_ID
```

---

### 8. Install and Start the Cloud Run Proxy

[Install gcloud CLI](https://cloud.google.com/sdk/docs/install) if not already installed.

```
gcloud run services proxy mcp-cloudrun-server --region=$REGION --port=8081 --project $PROJECT_ID
```

- This exposes the Cloud Run MCP Server securely at `http://localhost:8081/mcp`.

---

### 9. Try the CLI MCP Client

```
python3 clients/math_client.py 
```

or, if `python3` is not available, try:

```
python clients/math_client.py 
```

- This will run demo math operations and showcase error handling in the terminal.

---

### 10. Run the Streamlit Web App

```
streamlit run host-app/app.py
```

- Open the link shown in the terminal (typically `http://localhost:8501`).

> By default, Streamlit runs on port 8501. If port 8501 is already in use, Streamlit will automatically use the next available port (e.g., 8502, 8503, etc.).
> 
> If needed, a port can be specifiedexplicitly with:
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

- Enter numbers, select operation, and click "Calculate".
- Toggle "Express the result in words (LLM)" to see LLM-powered explanations.
- Toggle "Show Barcode using Cloud Run" to generate and display a barcode for the result.

---

### 11. (Optional) Visualize with MCP Inspector

> (Optional) Install Node.js/npx for MCP Inspector.
> If the MCP Inspector needs to be used, Node.js (which includes npx) needs to be installed.
> 
> Check if Node.js is installed:
> 
> ```
> node --version
> npx --version
> ```
> If not installed, download and install from the [official documentation](https://nodejs.org/).
> 
> Once installed, the `npx @modelcontextprotocol/inspector` command can be used for inspection purposes.

The [MCP Inspector](https://www.npmjs.com/package/@modelcontextprotocol/inspector) can be used to visually inspect any MCP Server (local or Cloud Run):

Inspecting Local MCP Server:

```
npx @modelcontextprotocol/inspector --url http://localhost:8080/mcp
```

or, inspecting Cloud Run MCP Server (Barcode Generator):

```
npx @modelcontextprotocol/inspector --url http://localhost:8081/mcp
```

This opens a web UI to browse available tools, resources, and try out calls interactively.

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
  - **Barcode generation via Cloud Run MCP server** (optional, secure, and serverless).
- **All components run locally by default**; barcode tool is cloud/serverless.

---

## 📝 Notes and Disclaimer

- The content and views presented during the session are the author’s own and not of any organizations they are associated with.
- **This code is for illustration and educational purposes only.**
    - Not production-grade; error handling, security, and scalability are not fully addressed.
- **Google Cloud services (including Cloud Run, Artifact Registry, and related resources) may incur costs beyond the free tier or trial credits.**  
  Always review [Google Cloud Pricing](https://cloud.google.com/pricing) and monitor the billing dashboard.

---

## 📚 References

- [FastMCP Documentation](https://gofastmcp.com/)
- [Google Cloud Run Docs](https://cloud.google.com/run/docs/)
- [Artifact Registry Docs](https://cloud.google.com/artifact-registry/docs/)
- [Cloud Build Docs](https://cloud.google.com/build/docs/)
- [Gemini API](https://aistudio.google.com/app/apikey)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Python Documentation](https://docs.python.org/3/)
- [MCP Inspector (npm)](https://www.npmjs.com/package/@modelcontextprotocol/inspector)