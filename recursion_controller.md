# recursion_controller.md
## Recursion Control & Termination Logic

---

## Objective
Prevent uncontrolled recursion while maximizing solution quality gains from self-refinement.

---

## Controller Inputs

- Current solution (y_t)
- Structured critique from Critic Agent
- Recursion depth counter (t)
- Historical solutions {y_0 … y_t}
- Optional metrics:
  - Error count
  - Confidence score
  - Semantic similarity to previous iteration

---

## Control Signals

### 1. Error Severity Score
Derived from critic output:
- Critical errors (logical, factual, constraint violations)
- Minor issues (clarity, formatting, redundancy)

Mapped to a scalar severity score ∈ [0, 1].

---

### 2. Improvement Delta
Measures progress between iterations:
- Semantic similarity(y_t, y_{t-1})
- Reduction in error count
- Change in critic severity score

Low delta ⇒ diminishing returns.

---

### 3. Recursion Budget
- Maximum recursion depth: T_max = 5
- Hard stop if t ≥ T_max

---

## Decision Policy

The controller outputs one of:
- **CONTINUE**
- **HALT**

### HALT if any condition holds:
- Severity score < ε (no critical issues)
- Improvement delta < δ (no meaningful improvement)
- Recursion depth reached T_max
- Degeneration detected (quality regression)

### CONTINUE otherwise

---

## Degeneration Detection

Indicators:
- Increasing verbosity without error reduction
- Oscillation between similar solutions
- New errors introduced in refinement

If detected → HALT immediately.

---

## Design Rationale

- Ensures stability of recursive loops
- Makes recursion measurable and auditable
- Converts reflection from heuristic to controlled process

---