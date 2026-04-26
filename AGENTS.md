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

## Implementation Priority

Start with Inter credit card support
Do not implement other sources until Inter credit card is fully working
Avoid generic abstractions before having a working implementation

## Commands

Run tests: pytest