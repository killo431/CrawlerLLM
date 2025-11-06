# AstraForge Autonomous Agent

Production-ready framework for multi-agent code systems. Drop the files into your repo and run:

```bash
pip install -r requirements.txt
python astra_agent.py
```

**Repository Layout**:

- `models.py`: Data models for Task, Artifact, AuditResult
- `state_manager.py`: Task/artifact state logic
- `prompt_factory.py`: Prompt builder logic
- `agent.py`: Main agent class and loop
- `astra_agent.py`: Entrypoint for the agent
- `conductor_leader_prompt.md`, `specialist_3_step_prompt.md`: System prompt templates
- `auditor.yaml`, `scribe.yaml`: YAML role definitions

**How to use**:
- Run `astra_agent.py` to test the full autonomous workflow.
- Modify the `user_objective` in `astra_agent.py` to change the project goal.

**LLM Integration**:
- `call_llm()` in `agent.py` is a stub — replace with your API for Gemini/Claude/OpenAI.

**Extend**:
- Add more specialist roles via YAML and inject into `PromptFactory`.