import google.generativeai as genai
import json
import os
from tools.nexus_legal_tools import NexusLegalTools
from typing import Dict, List, Any


API_KEY = "YOUR_KEY_HERE" 

class GeminiRiskEvaluator:
    """
    Agent B: GeminiRiskEvaluator.
    Uses the REAL Gemini API to perform reasoning and risk assessment
    against the Long-Term Memory (Playbook).
    """

    def __init__(self, name: str = "GeminiRiskEvaluator"):
        self.name = name
        self.tools = NexusLegalTools()
        
        # Configure Gemini
        if not API_KEY or "PASTE_YOUR" in API_KEY:
             print(f"[{self.name}] ERROR: Gemini API Key is missing inside agents/risk_evaluator.py")
             self.model = None
        else:
             try:
                 # We add # type: ignore to stop Pylance false positives
                 genai.configure(api_key=API_KEY) # type: ignore
                 
                 # Using Gemini 1.5 Flash for speed and efficiency
                 self.model = genai.GenerativeModel('gemini-1.5-flash') # type: ignore
             except Exception as e:
                 print(f"[{self.name}] ERROR: Failed to configure Gemini: {e}")
                 self.model = None

    def run(self, segmented_clauses: Dict[str, List[str]]) -> List[Dict[str, Any]]:
        """Analyzes clauses using Gemini and outputs A2A Protocol data."""
        print(f"[{self.name}] Connecting to Gemini API for policy-grounded analysis...")
        a2a_results = []
        
        if not self.model:
            print(f"[{self.name}] CRITICAL: No AI Model loaded. Check API Key.")
            return []
        
        for topic, texts in segmented_clauses.items():
            
            # 1. Query the Long-Term Memory 
            # We normalize the topic to match keys in the JSON file
            clean_topic = topic.upper().replace("_CAP", "").replace("_FOR_CONVENIENCE", "")
            playbook_data = self.tools.get_playbook_clause(clean_topic)
            
            if playbook_data is None:
                print(f"[{self.name}] WARNING: No policy found for {topic}. Skipping AI analysis.")
                continue

            clause_text = " ".join(texts)
            
            # 2. Construct the Prompt for Gemini
            prompt = f"""
            ACT AS: Expert Legal Compliance Auditor.
            
            TASK: Compare the 'CONTRACT CLAUSE' against the 'INTERNAL POLICY'.
            
            INTERNAL POLICY (The Standard):
            "{playbook_data['standard_text']}"
            Forbidden Phrases: {playbook_data.get('forbidden_phrases', [])}
            
            CONTRACT CLAUSE (The Input):
            "{clause_text}"
            
            INSTRUCTIONS:
            1. Determine if the CONTRACT CLAUSE violates the INTERNAL POLICY.
            2. Assign a Risk Score (1-10). 10 is a severe violation (e.g., using forbidden phrases).
            3. If Risk Score > 5, the Recommended Action must be "REPLACE". Otherwise "FLAG_ACCEPT".
            
            OUTPUT FORMAT (JSON ONLY):
            {{
                "risk_score": <int>,
                "recommended_action": "<string>",
                "reasoning": "<short explanation>"
            }}
            """
            
            # 3. Call the Gemini API
            try:
                # Adding type ignore here as well just in case Pylance complains about the model object
                response = self.model.generate_content(prompt) # type: ignore
                
                # Clean up response to ensure we get valid JSON
                clean_json = response.text.replace("```json", "").replace("```", "").strip()
                ai_analysis = json.loads(clean_json)
                
                print(f"[{self.name}] Gemini Analysis for {topic}: Risk={ai_analysis['risk_score']} ({ai_analysis['recommended_action']})")
                
                # 4. Construct A2A Output using AI Data
                a2a_output = {
                    "clause_topic": topic,
                    "clause_text": clause_text,
                    "risk_score": ai_analysis['risk_score'],
                    "recommended_action": ai_analysis['recommended_action'],
                    "standard_playbook_text": playbook_data['standard_text'],
                    "playbook_reference": playbook_data['policy_id'],
                    "ai_reasoning": ai_analysis.get('reasoning', 'No reasoning provided.')
                }
                a2a_results.append(a2a_output)
                
            except Exception as e:
                print(f"[{self.name}] ERROR: Gemini API call failed: {e}")
                a2a_results.append({
                    "clause_topic": topic,
                    "clause_text": clause_text,
                    "risk_score": 10,
                    "recommended_action": "MANUAL_REVIEW",
                    "standard_playbook_text": playbook_data['standard_text'],
                    "playbook_reference": playbook_data['policy_id'],
                    "ai_reasoning": "API Error - Defaulting to High Risk"
                })
            
        return a2a_results