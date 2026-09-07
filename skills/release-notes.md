---
name: release-notes
description: "Generate user-facing release notes from tickets, PRDs, or changelogs. Creates clear, engaging summaries organized by category (new features, improvements, fixes). Use when writing release notes, creating changelogs, announcing product updates, or summarizing what shipped."
---

## Release Notes Generator

Transform technical tickets, PRDs, or internal changelogs into polished, user-facing release notes.

### Instructions

1. **Gather raw material**: Read all provided tickets, changelogs, or descriptions. Extract:
   - What changed (feature, improvement, or fix)
   - Who it affects (which user segment)
   - Why it matters (the user benefit)

2. **Categorize changes**:
   - **New Features**: Entirely new capabilities
   - **Improvements**: Enhancements to existing features
   - **Bug Fixes**: Issues resolved
   - **Breaking Changes / Attention**: Anything that requires user action (migrations, API changes, uncontextual commits)

3. **Write each entry** following these principles:
   - Lead with the user benefit, not the technical change
   - Use plain language — avoid jargon, internal codenames, or ticket numbers
   - Keep each entry to 1-3 sentences

   **Example transformations**:
   - Technical: "Implemented Redis caching layer for dashboard API endpoints"
   - User-facing: "Dashboards now load up to 3x faster, so you spend less time waiting and more time analyzing."

   - Technical: "Fixed race condition in concurrent checkout flow"
   - User-facing: "Fixed an issue where some orders could fail during high-traffic periods."

4. **Structure the release notes**:

   ```markdown
   # [Product Name] — [Version / Date]

   ## New Features
   - **[Feature name]**: [1-2 sentence description of what it does and why it matters]

   ## Improvements
   - **[Area]**: [What got better and how it helps]

   ## Bug Fixes
   - Fixed [issue description in user terms]

   ## Breaking Changes / Attention (if any)
   - **Action required**: [What users need to do or review]
   ```

5. **Adjust tone** to match the product's voice — professional for B2B, friendly for consumer, developer-focused for APIs.
