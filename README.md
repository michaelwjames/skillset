# This repo is based on the open source skills from Claude AI / Anthropic, but made generic for any AI agent system. 

# Agent Skills

Skills are folders of instructions, scripts, and resources that AI agents load dynamically to improve performance on specialized tasks. Skills teach AI agents how to complete specific tasks in a repeatable way, whether that's creating documents with your company's brand guidelines, analyzing data using your organization's specific workflows, or automating personal tasks.

For more information, see the `agent_skills_spec.md` file in this repository.

# About This Repository

This repository contains example skills that demonstrate what's possible with AI agent skills systems. 

## Flagship Skill: `tax-assistant/`

The **tax-assistant** skill is our flagship workflow. It orchestrates multi-document tax preparation by combining OCR, institution-specific references, and country-level compliance guidance:

- Processes PDF/CSV statements with deterministic Groq OCR.
- Normalises institution outputs to the fiscal year and currency described in `tax-assistant/references/country_tax_details.md`.
- Maintains auditable spreadsheets under `tax-assistant/spreadsheets/` and produces a post-run `review.md`.

Start by reading `tax-assistant/README.md` for human setup steps, then load `tax-assistant/SKILL.md` in your agent to execute the full workflow.

Each skill is self-contained in its own directory with a `SKILL.md` file containing the instructions and metadata that AI agents use. Browse through these examples to get inspiration for your own skills or to understand different patterns and approaches.

The example skills in this repo are open source (Apache 2.0).

## Meta Skills

- **skill-creator** - Guide for creating effective skills that extend AI agent capabilities
- **template-skill** - A basic template to use as a starting point for new skills

# Using Skills with AI Agents

Skills can be integrated with various AI agent systems that support dynamic skill loading. The specific integration method depends on your AI agent platform.

## General Usage

To use skills from this repository:

1. Copy the skill folder to your AI agent's skills directory
2. Ensure the skill contains a properly formatted `SKILL.md` file with required YAML frontmatter
3. Reference the skill in your AI agent interactions according to your platform's documentation

See `agent_skills_spec.md` for the complete specification of the skill format.

# Creating a Basic Skill

Skills are simple to create - just a folder with a `SKILL.md` file containing YAML frontmatter and instructions. You can use the **template-skill** in this repository as a starting point:

```markdown
---
name: my-skill-name
description: A clear description of what this skill does and when to use it
---

# My Skill Name

[Add your instructions here that the AI agent will follow when this skill is active]

## Examples
- Example usage 1
- Example usage 2

## Guidelines
- Guideline 1
- Guideline 2
```

The frontmatter requires only two fields:

- `name` - A unique identifier for your skill (lowercase, hyphens for spaces)
- `description` - A complete description of what the skill does and when to use it

The markdown content below contains the instructions, examples, and guidelines that the AI agent will follow. For more details, see `agent_skills_spec.md`.

# Contributing

Contributions are welcome! If you've created useful skills that could benefit others, please consider submitting a pull request. Ensure your skills follow the specification in `agent_skills_spec.md`.