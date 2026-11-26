# Copilot SDLC Agents

This directory contains repository-customized GitHub Copilot agent definitions
for the Agentic SDLC pipeline.

## Agent Sequence

1. `sdlc-orchestrator.agent.md`
2. `requirements.agent.md`
3. `architecture.agent.md`
4. `design-review.agent.md`
5. `implementation-planning.agent.md`
6. `implementer.agent.md`
7. `code-reviewer.agent.md`
8. `verifier.agent.md`
9. `pull-request.agent.md`

## Human Approval Gates

- Requirements approval
- Architecture and design approval
- Implementation approval
- PR merge approval

## Usage

Select the appropriate agent from the VS Code Copilot Chat custom-agent picker,
or begin with `sdlc-orchestrator` and specify the current SDLC stage.

All agents must respect `.github/copilot-instructions.md` and the repository
artifacts in `requirements.md`, `architecture.md`, `design-review.md`,
`impl-plan.md`, `code-review.md`, and `PR_DESCRIPTION.md`.
