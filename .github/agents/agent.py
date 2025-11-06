import json
from models import Task, Artifact, TaskStatus, AuditResult
from state_manager import StateManager
from prompt_factory import PromptFactory
from typing import Dict, List

def load_prompt(file_path: str) -> str:
    with open(file_path, 'r') as f:
        return f.read()

def load_mode_instructions(yaml_files: List[str]) -> Dict[str, str]:
    instructions = {}
    for path in yaml_files:
        slug = path.split('.')[0]
        with open(path, 'r') as f:
            instructions[slug] = f.read()
    return instructions

def call_llm(prompt: str) -> str:
    print(f"\n--- LLM CALL (Simulated) ---\n{prompt[:500]}...\n--- END CALL ---\n")
    if "auditor" in prompt.lower():
        return '{ "status": "PASS", "notes": "Audit simulation passed." }'
    if "scribe" in prompt.lower():
        return "Integration log: Simulated write to CHANGELOG.md"
    return "Simulated specialist artifact content."

class AstraForgeAgent:
    def __init__(self, mode_instruction_files: List[str]):
        self.state = StateManager()
        self.mode_instructions = load_mode_instructions(mode_instruction_files)
        self.prompt_factory = PromptFactory(
            leader_prompt=load_prompt("conductor_leader_prompt.md"),
            specialist_prompt=load_prompt("specialist_3_step_prompt.md"),
            mode_instructions=self.mode_instructions
        )

    def plan_project(self, user_objective: str):
        print("Calling Conductor to plan project...")
        prompt = self.prompt_factory.build_conductor_prompt(user_objective)
        response_json_str = call_llm(prompt)
        try:
            task_data = json.loads(response_json_str)
            tasks = [Task(**data) for data in task_data]
            self.state.load_backlog(tasks)
            print(f"Project plan created. {len(tasks)} tasks loaded into backlog.")
        except json.JSONDecodeError as e:
            print(f"FATAL: Conductor failed to return valid JSON. Error: {e}")
            print(f"Received: {response_json_str}")

    def run_execution_loop(self):
        while True:
            next_task = self.state.get_next_task()
            if not next_task:
                print("All tasks completed. AstraForge signing off.")
                break
            print(f"\n--- EXECUTING TASK: {next_task.id} (Owner: {next_task.owner}) ---")
            self.state.update_task_status(next_task.id, TaskStatus.IN_PROGRESS)
            try:
                context_artifacts = self.state.get_artifacts_for_task(next_task)
                prompt = self.prompt_factory.build_specialist_prompt(next_task, context_artifacts)
                artifact_content = call_llm(prompt)
                artifact = Artifact(
                    id=next_task.id,
                    owner_task_id=next_task.id,
                    content=artifact_content,
                    format=next_task.outputs.get("format", "markdown")
                )
                self.state.add_artifact(artifact)
                self.state.update_task_status(next_task.id, TaskStatus.COMPLETED)
                print(f"Task {next_task.id} COMPLETED. Artifact stored.")
                self.run_audit_and_integration(next_task, artifact)
            except Exception as e:
                print(f"Task {next_task.id} FAILED with exception: {e}")
                self.state.update_task_status(next_task.id, TaskStatus.BLOCKED, str(e))

    def run_audit_and_integration(self, task: Task, artifact: Artifact):
        if not task.qualityGates:
            print(f"Task {task.id} has no quality gates. Passing to Scribe.")
            self.run_scribe_integration(task, artifact)
            return
        print(f"Auditing task {task.id} for gates: {task.qualityGates}...")
        audit_instructions = self.mode_instructions.get('auditor')
        audit_prompt = self.prompt_factory.build_audit_prompt(task, artifact, audit_instructions)
        audit_result_str = call_llm(audit_prompt)
        try:
            audit_data = json.loads(audit_result_str)
            audit_result = AuditResult(**audit_data)
            if audit_result.status == "PASS":
                print(f"Audit PASSED for task {task.id}.")
                self.run_scribe_integration(task, artifact)
            else:
                print(f"Audit FAILED for task {task.id}: {audit_result.notes}")
                self.state.update_task_status(task.id, TaskStatus.FAILED_AUDIT, audit_result.notes)
        except Exception as e:
            print(f"Auditor failed to return valid JSON. Error: {e}")
            self.state.update_task_status(task.id, TaskStatus.FAILED_AUDIT, "Auditor response malformed.")

    def run_scribe_integration(self, task: Task, artifact: Artifact):
        print(f"Integrating artifact for task {task.id}...")
        scribe_instructions = self.mode_instructions.get('scribe')
        scribe_prompt = self.prompt_factory.build_scribe_prompt(artifact, scribe_instructions)
        integration_log = call_llm(scribe_prompt)
        print(f"Integration log: {integration_log}")
        self.state.update_task_status(task.id, TaskStatus.PASSED_AUDIT, integration_log)