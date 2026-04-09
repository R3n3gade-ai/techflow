import json
import datetime
from src.engine.systematic_scan import _fetch_documents, _calculate_gate3_score, ScanCandidate
from src.intelligence.llm_wrapper import llm_wrapper

def run_test_scan():
    print(f"--- ARMS Systematic Scan Engine: Integration Test Sweep ---")
    
    test_universe = ["ALAB", "PLTR"]
    candidates = []
    
    for ticker in test_universe:
        print(f"\n[Scan] Processing {ticker}...")
        
        # 1. Fetch public documents
        docs = _fetch_documents(ticker)
        print(f"  -> Fetched SEC EDGAR data: {len(docs)} characters.")
        
        # 2. Run SENTINEL Gate 1 & 2 Analysis via Gemini API
        prompt = f"""
        You are the ARMS SENTINEL Gate 1 & 2 Analyst.
        - Gate 1: Is this a civilizational shift, not a product cycle?
        - Gate 2: Is this company non-optional (cannot be routed around)?
        
        Analyze the following context for {ticker} based strictly on these SEC filings, and return ONLY valid JSON.
        JSON format: {{'gate1_pass': bool, 'gate2_pass': bool, 'rationale': 'str'}}
        
        CONTEXT:
        {docs}
        """
        
        response_json = llm_wrapper.call(
            task_type='sentinel_scan',
            prompt=prompt,
            knowledge_base_query=f'{ticker} SENTINEL analysis'
        )
        
        # Strip markdown if present
        if response_json.startswith("```json"):
            response_json = response_json[7:-3].strip()
        elif response_json.startswith("```"):
            response_json = response_json[3:-3].strip()
            
        try:
            res = json.loads(response_json)
            print(f"  -> Gate 1: {res.get('gate1_pass')} | Gate 2: {res.get('gate2_pass')}")
            print(f"  -> Rationale: {res.get('rationale')}")
            
            if res.get('gate1_pass') and res.get('gate2_pass'):
                g3_score = _calculate_gate3_score(ticker)
                
                candidate = ScanCandidate(
                    ticker=ticker,
                    gate1_pass=True,
                    gate2_pass=True,
                    gate3_score=g3_score,
                    rationale=res.get('rationale', 'No rationale provided.')
                )
                candidates.append(candidate)
                print(f"  -> Candidate Found: {ticker} (Score: {g3_score})")
                
        except (json.JSONDecodeError, KeyError) as e:
            print(f"  [Error] Failed to parse AI response for {ticker}: {e}")

    print(f"\n--- Scan Complete. {len(candidates)} candidate(s) identified. ---")

if __name__ == '__main__':
    run_test_scan()
