# NOTE: In a production ADK project, this would inherit from the Agent class.
from tools.nexus_legal_tools import NexusLegalTools
from typing import Dict, List

class TextIngestor:
    """
    Agent A: TextIngestor. First agent in the Sequential flow.
    Uses the PyPDF2-enabled Custom Tool to handle real file ingress.
    """
    
    def __init__(self, name: str = "TextIngestor"):
        self.name = name
        self.tools = NexusLegalTools()

    def run(self, file_path: str) -> Dict[str, List[str]]:
        """Parses the document using a Custom Tool and returns segmented clauses."""
        print(f"[{self.name}] Initiating document analysis via Custom Tool...")
        
        segmented_clauses = self.tools.document_parsing_tool(file_path)
        
        print(f"[{self.name}] Successfully segmented document into {len(segmented_clauses)} key topics.")
        return segmented_clauses