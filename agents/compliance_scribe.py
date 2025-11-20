# NOTE: In a production ADK project, this would inherit from the Agent class.
from tools.nexus_legal_tools import NexusLegalTools
from typing import List, Dict, Any

class ComplianceScribe:
    """
    Agent C: ComplianceScribe. The final reporting agent.
    Generates the auditable Risk Report and the Redline Document.
    """

    def __init__(self, name: str = "ComplianceScribe"):
        self.name = name
        self.tools = NexusLegalTools()

    def run(self, a2a_results: List[Dict[str, Any]]) -> Dict[str, str]:
        """Receives A2A results and generates final outputs using Custom Tools."""
        print(f"[{self.name}] Final stage: Generating Risk Report and Redline Document.")
        
        # 1. Use Custom Tool to generate the redline document
        redline_doc = self.tools.generate_redline_document(a2a_results)
        
        # 2. Generate the structured risk report from the A2A data
        risk_report = "--- RISK ASSESSMENT REPORT ---\n"
        
        total_risk = sum(res['risk_score'] for res in a2a_results)
        
        risk_report += f"Total Aggregate Risk Score: {total_risk}/24 (Max Possible Risk)\n\n"
        
        for result in a2a_results:
            risk_report += (
                f"Topic: {result['clause_topic'].upper()}\n"
                f"  Risk Score: {result['risk_score']}\n"
                f"  Action Taken: {result['recommended_action']}\n"
                f"  Playbook Policy: {result['playbook_reference']}\n"
                f"  Original Text Excerpt: {result['clause_text'][:50]}...\n"
                f"---\n"
            )

        return {
            "risk_report": risk_report,
            "redline_document": redline_doc
        }