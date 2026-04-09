import sys
import os

sys.path.append("/data/.openclaw/workspace/achelion_arms/src")

from engine.sentinel_workflow import sentinel_workflow

def run_test():
    print("Testing SENTINEL v2.0 Workflow Initialization...")
    try:
        sentinel_workflow.initiate_thesis("ARM", "Cat B")
        sentinel_workflow.run_automated_gates("ARM", "RISK_ON", "NORMAL->NORMAL")
        
        path = "/data/.openclaw/workspace/achelion_arms/src/achelion_arms/state/sentinel_records_v2.json"
        if os.path.exists(path):
            with open(path, "r") as f:
                print(f.read())
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    run_test()
