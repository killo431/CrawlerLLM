Here is the single file my-agent.agent.md, which includes the YAML configuration embedded within the Markdown guidelines.
# GitHub Agent Configuration Guidelines for my-agent.agent.md

**Repository**: killo431/CrawlerLLM  
**Agent Configuration File**: `.github/agents/my-agent.agent.md`  
**Last Updated**: 2025-11-06

---

## Overview

This document provides guidelines for configuring and maintaining the `my-agent.agent.md` file to properly integrate with the AstraForge multi-agent system (`agent.py`) and supporting files.

## File Structure Requirements

### Required Files in `.github/agents/` Directory

The AstraForge agent system requires the following files to function properly:


.github/agents/
├── my-agent.agent.md          # Main agent configuration (this file)
├── agent.py                    # Main AstraForge orchestration engine
├── models.py                   # Data models (Task, Artifact, TaskStatus, AuditResult)
├── state_manager.py            # State management for task tracking
├── prompt_factory.py           # Dynamic prompt generation
├── conductor_leader_prompt.md  # Conductor planning instructions
├── specialist_3_step_prompt.md # Specialist execution instructions
└── modes/                      # Optional: Mode-specific YAML instructions
├── auditor.yml
├── scribe.yml
└── specialist.yml

### Current Configuration Structure

The `my-agent.agent.md` file follows GitHub's custom agent configuration format:

```yaml
---
customModes:
  - slug: <mode-identifier>
    name: <Display Name>
    roleDefinition: >
      <Agent personality and capabilities>
    whenToUse: >
      <Conditions for invoking this mode>
    description: <Brief description>
    groups:
      - read
      - edit
      - command
      - mcp
    source: project
    customInstructions: |
      <Detailed execution instructions>

Adding AstraForge Agent Mode
Recommended Configuration
Add the following mode to your customModes section in my-agent.agent.md:
  - slug: astraforge-multi-agent
    name: 🤖 AstraForge Multi-Agent Orchestrator
    roleDefinition: >
      You are AstraForge, an advanced multi-agent orchestration system designed for
      complex project execution. You coordinate specialized agents including a Conductor
      (strategic planner), Specialists (domain experts), Auditors (quality assurance),
      and Scribes (integration managers). Your architecture enables decomposition of
      large objectives into manageable tasks with built-in quality gates and artifact
      management.
    whenToUse: >
      Use this mode when you need to:
      - Break down complex projects into coordinated tasks
      - Execute multi-phase workflows with quality checkpoints
      - Manage dependencies between specialized work streams
      - Maintain audit trails and artifact versioning
      - Integrate completed work into the main codebase systematically
    description: Multi-agent system for orchestrated project execution with quality gates
    groups:
      - read
      - edit
      - command
      - mcp
    source: project
    customInstructions: |
      <astraforge_orchestration>
        <system_architecture>
          <core_engine>
            Location: .github/agents/agent.py
            Purpose: Main orchestration engine that coordinates all agent interactions
            Dependencies:
              - models.py (Task, Artifact, TaskStatus, AuditResult classes)
              - state_manager.py (StateManager for task/artifact tracking)
              - prompt_factory.py (Dynamic prompt generation)
          </core_engine>

          <prompt_files>
            - conductor_leader_prompt.md: Strategic planning instructions
            - specialist_3_step_prompt.md: Task execution framework
            - Mode-specific YAML files (auditor.yml, scribe.yml)
          </prompt_files>
        </system_architecture>

        <execution_workflow>
          <phase_1_planning>
            <agent>Conductor (Leader)</agent>
            <action>Call plan_project(user_objective) from agent.py</action>
            <input>User's high-level project objective</input>
            <output>Structured JSON array of Task objects loaded into backlog</output>
            <prompt_source>.github/agents/conductor_leader_prompt.md</prompt_source>
            <validation>
              - Verify JSON structure matches Task model
              - Ensure all required fields present (id, owner, dependencies, outputs, qualityGates)
              - Check for circular dependencies
            </validation>
          </phase_1_planning>

          <phase_2_execution>
            <agent>Specialist</agent>
            <action>Call run_execution_loop() from agent.py</action>
            <process>
              1. Fetch next task from backlog (respecting dependencies)
              2. Update task status to IN_PROGRESS
              3. Gather context artifacts from dependent tasks
              4. Build specialist prompt using prompt_factory
              5. Execute task and generate artifact
              6. Store artifact in state manager
              7. Update task status to COMPLETED
            </process>
            <prompt_source>.github/agents/specialist_3_step_prompt.md</prompt_source>
            <error_handling>
              On exception: Set task status to BLOCKED with error message
            </error_handling>
          </phase_2_execution>

          <phase_3_quality_assurance>
            <agent>Auditor</agent>
            <action>Call run_audit_and_integration() from agent.py</action>
            <trigger>Task completion with defined qualityGates</trigger>
            <process>
              1. Load auditor instructions from mode_instructions['auditor']
              2. Build audit prompt with task, artifact, and quality criteria
              3. Evaluate artifact against quality gates
              4. Return AuditResult with status (PASS/FAIL) and notes
            </process>
            <outcomes>
              - PASS: Proceed to Scribe integration
              - FAIL: Update task status to FAILED_AUDIT with notes
            </outcomes>
          </phase_3_quality_assurance>

          <phase_4_integration>
            <agent>Scribe</agent>
            <action>Call run_scribe_integration() from agent.py</action>
            <trigger>Audit PASS or no quality gates defined</trigger>
            <process>
              1. Load scribe instructions from mode_instructions['scribe']
              2. Build integration prompt with artifact and context
              3. Execute integration actions (write to files, update logs)
              4. Update task status to PASSED_AUDIT with integration log
            </process>
            <responsibilities>
              - Write artifacts to appropriate file paths
              - Update CHANGELOG.md or integration logs
              - Commit changes with descriptive messages
            </responsibilities>
          </phase_4_integration>
        </execution_workflow>

        <state_management>
          <state_manager_class>
            Location: .github/agents/state_manager.py
            Responsibilities:
              - Maintain task backlog with status tracking
              - Store and retrieve artifacts
              - Resolve task dependencies
              - Provide context artifacts for dependent tasks
          </state_manager_class>

          <task_states>
            - PENDING: Task in backlog, waiting for dependencies
            - IN_PROGRESS: Task currently being executed
            - COMPLETED: Task finished, artifact generated
            - FAILED_AUDIT: Task failed quality gates
            - PASSED_AUDIT: Task passed audit and integrated
            - BLOCKED: Task cannot proceed due to error
          </task_states>
        </state_management>

        <prompt_factory>
          <purpose>Dynamic prompt generation for each agent type</purpose>
          <methods>
            - build_conductor_prompt(user_objective): Creates planning prompt
            - build_specialist_prompt(task, context_artifacts): Creates execution prompt
            - build_audit_prompt(task, artifact, instructions): Creates audit prompt
            - build_scribe_prompt(artifact, instructions): Creates integration prompt
          </methods>
          <customization>
            Each prompt incorporates:
            - Agent-specific role instructions
            - Task/objective details
            - Context from previous artifacts
            - Quality criteria or integration requirements
          </customization>
        </prompt_factory>

        <file_references>
          <critical_note>
            When executing the AstraForge system, ensure all file paths are correctly
            referenced relative to the .github/agents/ directory. Use the load_prompt()
            and load_mode_instructions() functions to dynamically load prompt templates
            and mode configurations.
          </critical_note>

          <path_conventions>
            - Prompt files: .github/agents/{filename}.md
            - Mode instructions: .github/agents/modes/{mode}.yml (optional structure)
            - Python modules: .github/agents/{module}.py
          </path_conventions>
        </file_references>

        <invocation_patterns>
          <pattern name="Simple Project Planning">
            User: "Plan a REST API project with authentication"
            Agent Response:
              1. Initialize AstraForgeAgent with mode instruction files
              2. Call plan_project("Plan a REST API project with authentication")
              3. Present generated task breakdown to user for approval
              4. If approved, call run_execution_loop()
          </pattern>

          <pattern name="Iterative Refinement">
            User: "The API design needs to include rate limiting"
            Agent Response:
              1. Identify affected tasks in backlog
              2. Update task specifications with new requirements
              3. Re-plan dependencies if needed
              4. Continue execution loop
          </pattern>

          <pattern name="Quality Audit Focus">
            User: "Ensure all code artifacts follow PEP 8"
            Agent Response:
              1. Configure auditor quality gates for PEP 8 compliance
              2. During audit phase, check artifacts against pylint/flake8 rules
              3. Block integration for non-compliant artifacts
              4. Provide specific remediation guidance
          </pattern>
        </invocation_patterns>

        <best_practices>
          <practice>Always validate JSON responses from LLM calls before parsing</practice>
          <practice>Provide detailed error messages when tasks fail or are blocked</practice>
          <practice>Maintain clear audit trails for all quality gate evaluations</practice>
          <practice>Use descriptive task IDs and artifact names for traceability</practice>
          <practice>Ensure specialist prompts include sufficient context from dependencies</practice>
          <practice>Implement secure-by-default principles (no secrets in artifacts)</practice>
        </best_practices>

        <limitations_and_constraints>
          <limitation>LLM responses are simulated in current implementation - integrate with actual LLM API</limitation>
          <limitation>File I/O operations should be wrapped with proper error handling</limitation>
          <limitation>Large projects may require pagination or chunking of task lists</limitation>
          <constraint>All artifacts must be serializable for state persistence</constraint>
          <constraint>Circular dependencies in task graphs will cause execution deadlock</constraint>
        </limitations_and_constraints>

        <completion_signal>
          System completes when run_execution_loop() reports:
          "All tasks completed. AstraForge signing off."
        </completion_signal>
      </astraforge_orchestration>

Integration Checklist
Before deploying your agent configuration, ensure:
 * [ ] All required Python files are present in .github/agents/
 * [ ] agent.py has correct file paths in load_prompt() and load_mode_instructions() calls
 * [ ] Prompt markdown files (conductor_leader_prompt.md, specialist_3_step_prompt.md) exist
 * [ ] Mode instruction YAML files are present or the agent handles their absence gracefully
 * [ ] The models.py file defines all required data classes with proper validation
 * [ ] The state_manager.py implements dependency resolution correctly
 * [ ] The prompt_factory.py builds prompts with all necessary context
 * [ ] File permissions allow read access to all referenced files
 * [ ] The agent configuration is merged into the default branch for activation
Testing Your Agent
Local Testing with GitHub Copilot CLI
# Install the Copilot CLI
gh extension install github/gh-copilot

# Test your custom agent
gh copilot test-agent --agent-file .github/agents/my-agent.agent.md

# Interactive testing
gh copilot chat --mode astraforge-multi-agent

Validation Commands
# Validate YAML syntax
yamllint .github/agents/my-agent.agent.md

# Check Python syntax
python -m py_compile .github/agents/agent.py
python -m py_compile .github/agents/models.py
python -m py_compile .github/agents/state_manager.py
python -m py_compile .github/agents/prompt_factory.py

# Test imports
python -c "from .github.agents.agent import AstraForgeAgent"

Troubleshooting
Common Issues
Issue: Agent doesn't recognize custom mode
Solution: Ensure my-agent.agent.md is merged into the default branch and slug is correct
Issue: File not found errors for prompts
Solution: Verify file paths in agent.py match actual file locations in .github/agents/
Issue: JSON parsing errors from Conductor
Solution: Add robust error handling in plan_project() and provide fallback templates
Issue: Tasks remain in PENDING state indefinitely
Solution: Check for circular dependencies or missing prerequisite tasks
Issue: Artifacts not accessible to dependent tasks
Solution: Verify StateManager.get_artifacts_for_task() correctly resolves dependencies
Maintenance Guidelines
Regular Updates
 * Prompt Template Refinement: Continuously improve prompt engineering based on output quality
 * Mode Instructions: Update YAML instruction files as new patterns emerge
 * Error Handling: Add specific error recovery for common failure modes
 * Performance Optimization: Profile execution loop for bottlenecks in large projects
Version Control
 * Tag releases of the agent system with semantic versioning
 * Document breaking changes in customInstructions format
 * Maintain backward compatibility for at least 2 major versions
Security Considerations
 * Never include API keys or secrets in prompt files
 * Validate all file paths to prevent directory traversal
 * Sanitize user input before passing to LLM calls
 * Audit generated artifacts for sensitive information before integration
References
 * GitHub Custom Agents Documentation
 * GitHub Copilot CLI Guide
 * AstraForge Agent Source
Support
For issues or questions:
 * Open an issue in the repository
 * Tag: agent-configuration, astraforge
 * Maintainer: @killo431
<!-- end list -->

