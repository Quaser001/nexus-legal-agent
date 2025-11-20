# Nexus Legal Agent ⚖️

**Track:** Enterprise Agents  
**Status:** Prototype (Submission Ready)

## 📜 Project Overview
Nexus Legal Agent is a sequential multi-agent system designed to automate the high-risk review of third-party vendor contracts. By leveraging an authoritative **Long-Term Memory (Legal Playbook)** and the **Gemini 1.5 Flash LLM**, it reduces contract review time while ensuring 100% policy compliance.

## 🎯 Problem Statement
Manual contract review is slow, expensive, and prone to human error. Legal teams waste hours comparing vendor terms against internal policies line-by-line. This bottleneck slows down business deals and exposes companies to regulatory risk.

## 💡 Solution Architecture
The system employs a **Sequential Multi-Agent Architecture**:

1.  **TextIngestor Agent:** Uses `PyPDF2` to ingest real PDF contracts and segment them into key clauses.
2.  **GeminiRiskEvaluator:** A generic reasoning agent powered by **Gemini 1.5 Flash**. It retrieves the correct policy from the **Memory Bank** (RAG) and evaluates the contract clause for risk.
3.  **ComplianceScribe:** Receives structured data via the **A2A Protocol** and generates a final Risk Report and Redline Document.

## 🛠️ Key Features & Concepts used
| Concept | Implementation |
| :--- | :--- |
| **Multi-Agent System** | Sequential flow (Ingestor -> Evaluator -> Scribe) orchestrated by a central manager. |
| **Custom Tools** | `document_parsing_tool` (PDF Reading) and `get_playbook_clause` (Memory Retrieval). |
| **Sessions & Memory** | Simulates an `InMemorySessionService` to track state and uses a JSON-based **Memory Bank** for long-term policy storage. |
| **A2A Protocol** | Strict JSON schema enforces communication between the Evaluator and Scribe agents. |
| **Gemini API** | Powers the risk analysis logic to understand legal nuance. |

## 🚀 How to Run

### Prerequisites
* Python 3.10+
* A Google Gemini API Key

### Installation
1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install google-generativeai pypdf2
    ```
3.  **API Setup:** Open `agents/risk_evaluator.py` and paste your Gemini API key into the `API_KEY` variable.

### Execution
Run the orchestrator with a target PDF file:

```bash
python main_orchestrator.py contract.pdf