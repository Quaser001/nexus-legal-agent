# Nexus Legal Agent ⚖️

**Track:** Enterprise Agents  
**Status:** Functional Prototype (Live Gemini AI Integration)

## 📜 Project Overview
Nexus Legal Agent is a **sequential multi-agent system** designed to automate the high-risk review of third-party vendor contracts. Unlike simple text matching tools, Nexus leverages the **Gemini 1.5 Flash LLM** to perform reasoning against an authoritative **Long-Term Memory (Legal Playbook)**. It reduces contract review time while ensuring 100% policy compliance.

## 🎯 Problem Statement
Manual contract review is a bottleneck in enterprise operations. Legal teams waste hours performing rote comparisons of vendor terms against internal policies. This slows down business deals (Time-to-Contract) and exposes companies to regulatory risk due to human error.

## 💡 Solution Architecture
The system employs a deterministic **Sequential Multi-Agent Architecture** to ensure auditability:



1.  **TextIngestor Agent:** Uses `PyPDF2` to ingest real PDF contracts, extract text, and segment it into key legal clauses.
2.  **GeminiRiskEvaluator:** The core intelligence. It uses **Gemini 1.5 Flash** to reason about the contract text, comparing it against specific policies retrieved from the **Memory Bank** (JSON Vector Store). It assigns a numerical risk score (1-10).
3.  **ComplianceScribe:** A reporting agent that consumes the structured **A2A Protocol** data to generate a final Risk Assessment Report and a Draft Redline Document.

## 🛠️ Key Features
| Concept | Implementation |
| :--- | :--- |
| **Multi-Agent System** | Sequential flow (Ingestor -> Evaluator -> Scribe) with State Management. |
| **Live AI (Gemini)** | Uses `google-generativeai` to perform semantic analysis of legal risk. |
| **Custom Tools** | `document_parsing_tool` (Real PDF Processing) and `get_playbook_clause` (RAG/Memory). |
| **Sessions & Memory** | Simulates `InMemorySessionService` for state tracking; uses JSON-based Long-Term Memory. |
| **A2A Protocol** | Strict JSON schema enforces communication, preventing hallucinated outputs. |

## 🚀 How to Run

### Prerequisites
* Python 3.10+
* A Google Gemini API Key (Get one [here](https://aistudio.google.com/))

### Installation
1.  Clone the repository:
    ```bash
    git clone [https://github.com/](https://github.com/)[YOUR_USERNAME]/nexus-legal-agent.git
    cd nexus-legal-agent
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration
1.  Open `agents/risk_evaluator.py`.
2.  Locate the `API_KEY` variable.
3.  Paste your Gemini API Key (or set it via Environment Variable `GEMINI_API_KEY`).

### Execution
Run the orchestrator by passing the path to your target PDF contract:

```bash
python main_orchestrator.py contract.pdf