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


## Commit, Push and Pull Request Workflow

When the user asks to implement a change and push,
or requests to "push", "commit", "commit and push", "create PR", or similar,
use a pull request workflow instead of pushing directly to the original branch.

1. Identify current branch
git branch --show-current

Store it as the base branch.

2. Create a feature branch
If a task number is provided, include it in the branch name
Otherwise, use a short descriptive codename

Examples:

task-123-output-csv
feature-output-csv
integration-tests-inter

Create the branch from the current branch.

3. Validate current changes
git status
git diff
4. Testing requirements
Ensure tests were added or updated for the change
Prefer unit tests for detailed behavior
Add or update integration tests when:
the change affects an end-to-end flow
a new file format is supported
5. Run tests
pytest
6. Handle failures
If tests fail:
Fix the issue
Run pytest again
Do not commit failing code
7. Create commits
Only proceed if tests pass
One logical change per commit
Do not mix unrelated changes
Use Conventional Commits when possible

Commit message format:

First line: short clear title
Body: bullet points describing relevant changes
8. Push branch
Push the feature branch using the configured SSH remote
9. Create Pull Request
Create a PR targeting the original branch
Use GitHub CLI if available:
gh pr create

PR requirements:

Title: short and descriptive
Body must include:
Summary of changes
Tests executed
Notes or limitations (if any)
10. Final step
Switch back to the original branch after creating the PR
11. Safety rules
Do not merge the PR unless explicitly requested
Do not force push unless explicitly requested

### Branch Naming Rule
Use kebab-case
Keep names short and meaningful
Avoid generic names like "fix" or "update"

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
→ Execute the full Commit, Push and Pull Request Workflow
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