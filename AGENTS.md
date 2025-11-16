---
description: instructions for an agent to use or create new skills within this repo.
---

# Instructions

1. **Clarify the request**
   - Restate the user's goal in your own words to ensure you understand the outcome they want.
   - Note any constraints (file formats, tooling limits, domains, timelines).

2. **Review the skills catalog**
   - Open `\skillset\SKILLS_CATALOG.md` and scan the table of skills, use cases, and dependencies.
   - Shortlist any skills whose primary use case overlaps with the user's goal.
   - Capture dependency requirements so you can confirm the environment supports them.

3. **Inspect shortlisted skills**
   - For each candidate, read its `SKILL.md` to understand activation guidance, workflows, and bundled assets.
   - Verify that the required dependencies are available or can be satisfied.
   - If one skill matches clearly, proceed with it and stop here.

4. **Decide between existing vs. new skill**
   - If no existing skill fully addresses the goal, determine whether adapting the `template-skill/` or creating a new skill is warranted.
   - When in doubt, prefer extending an existing skill only if the changes are small and aligned with its documented scope.

5. **Consult the Agent Skills Spec**
   - Read `agent_skills_spec.md` to confirm the structural requirements for any new or updated skill (frontmatter fields, directory layout, optional metadata, etc.).
   - Use the spec as a checklist to ensure the skill folder remains compliant.

6. **Create or extend the skill**
   - If building a new skill, follow the guidance in `skill-creator/SKILL.md` (and run its helper scripts if applicable).
   - If extending an existing skill, update its `SKILL.md` and resources while staying within the documented best practices.
   - When starting from scratch, use `template-skill/` as the base and populate the YAML frontmatter + instructions per the spec.
   - Ensure that you update `SKILLS_CATALOG.md` with the new skill details before using the skill to achieve the user's goal

7. **Document the decision**
   - Record which skill you chose (or the rationale for creating a new one) before proceeding with implementation.
   - Note any outstanding dependency setup steps so they are handled before execution.
