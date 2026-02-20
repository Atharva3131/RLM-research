# agent_roles.md
## Recursive Self-Refinement Agent Roles

---

## 1. Generator Agent

**Purpose**
- Produce an initial solution to the given task.

**Inputs**
- User query / task specification
- Optional context or constraints

**Outputs**
- Candidate solution (text, code, or action plan)
- Optional self-reported confidence score

**Responsibilities**
- Maximize task completion given current information
- Avoid self-critique or overthinking
- Act as a fast, first-pass solver

---

## 2. Critic Agent

**Purpose**
- Evaluate the Generator’s output for errors, gaps, and violations.

**Inputs**
- Original task specification
- Generator output
- Optional rubric or constraints

**Outputs**
- Structured critique:
  - Detected errors
  - Missing steps or logic gaps
  - Constraint violations
  - Ambiguities or uncertainties

**Responsibilities**
- Be adversarial and conservative
- Focus on correctness, not style
- Avoid rewriting the solution

---

## 3. Refiner Agent

**Purpose**
- Improve the solution based on the Critic’s feedback.

**Inputs**
- Generator output (current version)
- Structured critique from Critic Agent

**Outputs**
- Revised solution
- Summary of changes applied

**Responsibilities**
- Fix only what is flagged
- Preserve correct parts of the solution
- Avoid introducing new, unrelated changes

---

## 4. Controller Agent

**Purpose**
- Decide whether to continue recursion or terminate.

**Inputs**
- Current solution
- Critique severity metrics
- Recursion depth counter
- Historical solution states (optional)

**Outputs**
- Control decision:
  - CONTINUE (next recursion step)
  - HALT (finalize solution)

**Responsibilities**
- Enforce maximum recursion depth
- Detect diminishing returns or degeneration
- Prevent infinite loops
- Balance performance gain vs cost

---

## 5. Recursive Loop Summary

**Flow**
1. Generator produces solution (y₀)
2. Critic evaluates solution
3. Refiner revises solution
4. Controller decides:
   - If CONTINUE → repeat Critic → Refiner
   - If HALT → output final solution

**Termination Conditions**
- No critical errors detected
- Improvement below threshold
- Maximum recursion depth reached

---