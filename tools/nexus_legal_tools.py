import json
import datetime
import PyPDF2 
from typing import List, Dict, Any, Optional

class NexusLegalTools:
    """
    Custom Tools for the Nexus Legal Agent. This class simulates external service 
    integrations, memory retrieval (RAG), and document manipulation.
    """

    @staticmethod
    def document_parsing_tool(file_path: str) -> Dict[str, List[str]]:
        """
        Custom Tool: Reads a PDF document and segments its text into mock clauses.
        This performs real text extraction using PyPDF2.
        """
        trace_id = "TRACE-" + str(hash(file_path))[:6]
        print(f"|TRACE| {datetime.datetime.now().isoformat()} | START | PARSING_TOOL | TraceID={trace_id}")
        
        full_text = ""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    # Extract text, handling potential None or empty strings
                    extracted = page.extract_text()
                    if extracted:
                        full_text += extracted + "\n"
        except FileNotFoundError:
            print(f"|ERROR| {datetime.datetime.now().isoformat()} | PARSING_TOOL | File not found at {file_path}. Using fallback mock data.")
            # Fallback for demonstration if the file path is bad
            full_text = "MOCK: LIABILITY clause contained herein. Indemnify and hold harmless. Termination must be mutual."
        except Exception as e:
            print(f"|ERROR| {datetime.datetime.now().isoformat()} | PARSING_TOOL | Parsing failed: {e}. Using fallback mock data.")
            full_text = "MOCK: Failed to parse document. Liability clause is too high. Indemnify."


        # --- CLAUSE SEGMENTATION SIMULATION ---
        # We simulate segmentation by searching for keywords within the extracted text.
        segmented_clauses = {}
        
        if "liability" in full_text.lower():
             segmented_clauses["liability_cap"] = [
                "The core LIABILITY section was extracted from the document for analysis."
            ]
        
        if "indemnify" in full_text.lower():
             segmented_clauses["indemnification"] = [
                "The INDEMNIFICATION section was successfully extracted."
            ]
             
        if "terminate" in full_text.lower():
             segmented_clauses["termination_for_convenience"] = [
                "The TERMINATION clause was identified and extracted."
            ]
            
        if not segmented_clauses:
             # Use a generic set if no keywords were found, ensuring the evaluation agent runs
             segmented_clauses = {
                "liability_cap": ["No specific liability clause found, using fallback text."],
                "indemnification": ["No specific indemnification clause found, using fallback text."]
             }
        
        print(f"|TRACE| {datetime.datetime.now().isoformat()} | END | PARSING_TOOL | Segments identified: {len(segmented_clauses)}")
        return segmented_clauses

    @staticmethod
    def get_playbook_clause(clause_topic: str) -> Optional[Dict[str, Any]]:
        """
        Custom Tool: Queries the Long-Term Memory (Playbook) for the standard text.
        """
        trace_id = "MEM-" + str(hash(clause_topic))[:6]
        print(f"|TRACE| {datetime.datetime.now().isoformat()} | START | MEMORY_QUERY | TraceID={trace_id} | Topic={clause_topic}")
        
        try:
            with open('legal_data/playbook_clauses.json', 'r') as f:
                playbook = json.load(f)
        except FileNotFoundError:
            print(f"|ERROR| {datetime.datetime.now().isoformat()} | MEMORY_QUERY | File not found.")
            return None

        for clause in playbook:
            if clause['clause_topic'] == clause_topic:
                print(f"|TRACE| {datetime.datetime.now().isoformat()} | SUCCESS | MEMORY_QUERY | Policy={clause['policy_id']}")
                return clause
        
        print(f"|TRACE| {datetime.datetime.now().isoformat()} | FAIL | MEMORY_QUERY | Policy not found.")
        return None

    @staticmethod
    def generate_redline_document(a2a_results: List[Dict[str, Any]]) -> str:
        """
        Custom Tool: Generates the final mock redline document based on A2A input.
        """
        print(f"|TRACE| {datetime.datetime.now().isoformat()} | START | REDLINE_TOOL | ResultCount={len(a2a_results)}")
        redline_output = "--- DRAFT REDLINE AGREEMENT MANDATED BY POLICY ---\n"
        
        for result in a2a_results:
            if result.get("recommended_action") == "REPLACE":
                redline_output += (
                    f"\n[SECTION: {result['clause_topic'].upper()}]\n"
                    f"  [ORIGINAL (DELETED): {result['clause_text']}]\n"
                    f"  [REPLACEMENT (POLICY MANDATED - {result['playbook_reference']}): {result['standard_playbook_text']}]\n"
                )
            elif result.get("recommended_action") == "FLAG_ACCEPT":
                 redline_output += (
                    f"\n[SECTION: {result['clause_topic'].upper()}]\n"
                    f"  [STATUS: ACCEPTED (RISK SCORE: {result['risk_score']})]\n"
                )

        print(f"|TRACE| {datetime.datetime.now().isoformat()} | END | REDLINE_TOOL")
        return redline_output