# architecture.md
## Recursive Self-Refinement Agent Architecture

---

## System Overview

The system implements an inference-time recursive agent architecture where
an LLM iteratively improves its own outputs through structured feedback loops.

Recursion is treated as a first-class control mechanism, not an emergent behavior.

---

## Core Components

### 1. Generator Agent
- Produces an initial candidate solution
- Optimized for speed and coverage
- No self-reflection

### 2. Critic Agent
- Performs structured evaluation
- Identifies correctness, reasoning, and constraint issues
- Outputs machine-readable critique

### 3. Refiner Agent
- Revises the solution strictly based on critique
- Preserves valid content
- Avoids uncontrolled rewriting

### 4. Controller Agent
- Governs recursion depth and termination
- Balances quality improvement vs cost
- Prevents infinite or degenerative loops

---

## Data Flow (Single Iteration)

Input Task  
→ Generator → Candidate Solution  
→ Critic → Structured Critique  
→ Refiner → Revised Solution  
→ Controller → {CONTINUE | HALT}

---

## Recursive Execution

If CONTINUE:
- Revised solution becomes next iteration input
- Critic and Refiner are re-invoked

If HALT:
- Current solution is returned as final output

---

## Architectural Properties

- Model-agnostic (black-box LLM compatible)
- Inference-time only (no fine-tuning)
- Deterministic control over recursion
- Compatible with graph-based execution engines (e.g., LangGraph)

---

## Design Goals

- Improve reliability of agentic LLMs
- Enable empirical study of recursion depth vs performance
- Provide a reusable blueprint for self-improving AI systems

---