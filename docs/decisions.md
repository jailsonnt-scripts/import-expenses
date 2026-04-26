# Technical Decisions

## Why Python Standard Library

To minimize dependencies and keep the project simple and portable.

## Why src/ layout

Avoid import conflicts and follow modern Python packaging practices.

## Why no pandas

- Overkill for this use case
- Higher complexity
- Less control over parsing behavior

## Incremental Development

The project is built step-by-step using AI assistance to ensure:
- correctness
- simplicity
- test coverage