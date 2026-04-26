# Project: import-expenses

## Goal
Convert bank and credit card CSV files into a normalized CSV for Minhas Finanças.

## Scope
- Handle checking account and credit card transactions
- Support multiple CSV formats via configuration

## Rules
- Use Python standard library when possible
- Do not ignore invalid data silently
- Keep functions small and testable
- Prefer simple solutions over complex abstractions

## Workflow
- Implement one feature at a time
- Always run tests before finishing a task
- Do not refactor unrelated code

## Commands
- Run tests: pytest

# Project: import-expenses


## Goal

Convert bank account and credit card CSV files into CSV formats compatible with Minhas Finanças.

## Scope

Handle checking account transactions
Handle credit card transactions
Support multiple CSV input formats
Support different output formats depending on transaction type
Inter must be supported for both checking account and credit card

## Rules

Use Python standard library when possible
Do not ignore invalid data silently
Keep functions small and testable
Prefer simple solutions over complex abstractions
Do not implement AI-based classification in the initial version

## Workflow

Implement one feature at a time
Always run tests before finishing a task
Do not refactor unrelated code

## Testing Policy
Every code change must include or update tests.
Unit tests are the default and should be more numerous than integration tests.
Unit tests must cover both success and failure scenarios.
Integration tests must validate end-to-end behavior for each supported file type.
Integration tests should focus mostly on successful flows.
Add integration failure tests only for critical risks, such as:
invalid file format
missing required columns
data loss risk
invalid amount parsing
Do not create trivial tests just to satisfy coverage.
Tests must validate real behavior and relevant edge cases.
Test Organization
Unit tests should be placed under tests/unit/.
Integration tests should be placed under tests/integration/.
Shared test fixtures should be placed under tests/fixtures/.
Sample files used for integration tests should be small and explicit.
Commands
Run all tests: pytest
Run unit tests: pytest tests/unit
Run integration tests: pytest tests/integration


## Commit and Push Workflow

When the user requests to "push", "commit", "commit and push", or similar:

Check current changes:
git status
git diff
Confirm tests were added or updated for code changes:
Prefer unit tests for detailed behavior
Add or update integration tests when the change affects an end-to-end flow or a supported file type
Run all tests:
pytest
Only proceed if tests pass.
If tests fail:
Fix the issue
Run pytest again
Do not commit failing code
Create focused commits:
One logical change per commit
Do not mix unrelated changes
Use Conventional Commits when possible
Commit message format:
First line: short clear title
Body: bullet points describing relevant changes
Push using the configured SSH remote.
Do not force push unless explicitly requested.

## Prompt Documentation Policy
Update docs/prompts.md only for meaningful, reusable prompts
Do not log trivial or repetitive prompts
Focus on prompts that define structure, workflow, or strategy

## Implementation Priority

Start with Inter credit card support
Do not implement other sources until Inter credit card is fully working
Avoid generic abstractions before having a working implementation

## Commands

Run tests: pytest

## Workflow Triggers

If the user says "push", "commit and push", or "save changes":
→ Execute the full commit and push workflow
If the user says "implement X and push":
→ Implement X, run tests, then commit and push

## Prompt Documentation Trigger
When a change introduces:
a new workflow
a new architectural decision
a new testing strategy
a reusable pattern

→ Update docs/prompts.md accordingly

Do not update prompts.md for trivial or small changes