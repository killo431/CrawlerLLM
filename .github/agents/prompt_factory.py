from models import Task, Artifact
from typing import Dict

class PromptFactory:
    def __init__(self, leader_prompt: str, specialist_prompt: str, mode_instructions: Dict[str, str]):
        self.leader_prompt = leader_prompt
        self.specialist_prompt = specialist_prompt
        self.mode_instructions = mode_instructions

    def build_conductor_prompt(self, objective: str) -> str:
        return f"{self.leader_prompt}\n\nUser Objective: \"{objective}\""

    def build_specialist_prompt(self, task: Task, context_artifacts: Dict[str, Artifact]) -> str:
        base_prompt = self.specialist_prompt
        base_prompt = base_prompt.replace("<Specialist Agent>", task.owner.capitalize())
        base_prompt = base_prompt.replace("<TASK_ID from Conductor>", task.id)
        base_prompt = base_prompt.replace("<TASK_ID>", task.id)
        base_prompt = base_prompt.replace("<concise actionable goal>", task.objective)
        base_prompt = base_prompt.replace("<performance, security, compliance, style>", "N/A" if not task.risk else f"Risk: {task.risk}")
        base_prompt = base_prompt.replace("<acceptance criteria>", "\n".join(f"- {a}" for a in task.acceptance))
        base_prompt = base_prompt.replace("[list]", ", ".join(task.qualityGates) or "None")
        context_str = ""
        for id, artifact in context_artifacts.items():
            context_str += f"--- CONTEXT ARTIFACT: {id} ---\n{artifact.content}\n--- END ARTIFACT ---\n\n"
        base_prompt = base_prompt.replace("<prior artifacts / assumptions>", context_str or "No prior artifacts.")
        mode_instructions = self.mode_instructions.get(task.owner, f"No specific instructions for role {task.owner}.")
        return f"{base_prompt}\n\n--- {task.owner.upper()} INSTRUCTIONS ---\n{mode_instructions}"

    def build_audit_prompt(self, task: Task, artifact: Artifact, audit_instructions: str) -> str:
        prompt = audit_instructions
        prompt = prompt.replace("<task_id>", task.id)
        prompt = prompt.replace("[<gate_id_1>, <gate_id_2>]", str(task.qualityGates))
        prompt = prompt.replace("<content_of_artifact_to_review>", artifact.content)
        return prompt

    def build_scribe_prompt(self, artifact: Artifact, scribe_instructions: str) -> str:
        prompt = scribe_instructions
        prompt = prompt.replace("<ARTIFACT_TO_INTEGRATE>", artifact.content)
        return prompt