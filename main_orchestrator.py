import datetime
import sys
from typing import Dict, Any, Optional

from agents.text_ingestor import TextIngestor
from agents.risk_evaluator import GeminiRiskEvaluator
from agents.compliance_scribe import ComplianceScribe

class ContractReviewOrchestrator:
    """
    The central orchestrator for the Sequential Multi-Agent System (Nexus Legal Agent).
    Implements Session & State Management logic to track workflow progress.
    """

    def __init__(self, document_path: str):
        # 1. Initialize Agents (The specialized team)
        self.ingestor_agent = TextIngestor()
        self.evaluator_agent = GeminiRiskEvaluator()
        self.scribe_agent = ComplianceScribe()
        
        # 2. Set up Initial State/Session (Simulating Inmemory Session Service)
        self.document_path = document_path
        self.session_data: Dict[str, Any] = {"file_path": document_path, "status": "INITIALIZED"}

    def log_session_update(self, stage: str, status: str, data_key: Optional[str] = None):
        """Logs the session state update after a sequential agent runs."""
        timestamp = datetime.datetime.now().isoformat()
        self.session_data['status'] = status
        
        print(f"\n|SESSION| {timestamp} | STAGE: {stage} | STATUS: {status}")
        if data_key:
             print(f"|SESSION| {timestamp} | DATA UPDATED: Added '{data_key}' to state.")

    def run_review(self) -> Dict[str, str]:
        """
        Executes the mandatory sequential flow (Ingestor -> Evaluator -> Scribe).
        This fixed workflow ensures legal steps are always completed in order.
        """
        print("--- NEXUS LEGAL AGENT: CONTRACT REVIEW STARTED ---")
        print(f"--- Processing Document: {self.document_path} ---") 
        
        # 1. Step: TextIngestor (Uses Custom Tool)
        print("\n[Orchestrator] Delegating to TextIngestor Agent...")
        segmented_clauses = self.ingestor_agent.run(self.document_path)
        
        # Log Session Update (State Management)
        self.session_data['parsed_data'] = segmented_clauses 
        self.log_session_update("INGESTION", "PARSE_COMPLETE", "parsed_data")
        
        # 2. Step: GeminiRiskEvaluator (Multi-Agent, Memory, A2A Protocol, Gemini)
        print("\n[Orchestrator] Delegating to GeminiRiskEvaluator for A2A Generation...")
        a2a_results = self.evaluator_agent.run(segmented_clauses)
        
        # Log Session Update (State Management)
        self.session_data['a2a_data'] = a2a_results 
        self.log_session_update("EVALUATION", "ANALYSIS_COMPLETE", "a2a_data")
        
        # 3. Step: ComplianceScribe (Receives A2A Data, Uses Custom Tool)
        print("\n[Orchestrator] Delegating to ComplianceScribe for Final Output...")
        final_outputs = self.scribe_agent.run(a2a_results)
        
        self.log_session_update("REPORTING", "REVIEW_COMPLETE")
        print("\n--- NEXUS LEGAL AGENT: REVIEW COMPLETE ---")
        
        return final_outputs

if __name__ == "__main__":
    # Execution Start: Handles command-line input 
    if len(sys.argv) < 2:
        print("ERROR: Please provide the path to the PDF document as a command line argument.")
        print("Usage: python main_orchestrator.py [path/to/your/document.pdf]")
        sys.exit(1) # Exit if argument is missing
    
    INPUT_DOCUMENT_PATH = sys.argv[1]
    
    orchestrator = ContractReviewOrchestrator(INPUT_DOCUMENT_PATH)
    results = orchestrator.run_review()
    
    # Print Final Results
    print("\n FINAL OUTPUT: RISK ASSESSMENT REPORT")
    print(results['risk_report'])
    
    print("\n FINAL OUTPUT: DRAFT REDLINE DOCUMENT")
    print(results['redline_document'])