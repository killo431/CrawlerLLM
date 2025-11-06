from agent import AstraForgeAgent

def main():
    mode_instruction_files = ["auditor.yaml", "scribe.yaml"]
    agent = AstraForgeAgent(mode_instruction_files=mode_instruction_files)
    # Example objective (customize as desired)
    user_objective = "Design and implement a secure REST API service with full documentation and audit trails."
    agent.plan_project(user_objective)
    agent.run_execution_loop()
    print("Finished.")

if __name__ == "__main__":
    main()