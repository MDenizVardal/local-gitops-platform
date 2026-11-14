# Working rules

**Design**
- Simple beats complex. Don't overengineer.
- No fallbacks. There is one correct path and no alternatives.
- Do each thing one way only.
- Clear code beats backward compatibility.
- Fail fast. Throw errors when preconditions aren't met, such as a missing env var, tool or CRD.
- No backups or "just in case" mechanisms. Trust the primary mechanism.
- Each function or file has one responsibility.

**Process**
- Work **one phase at a time**. At the end of each phase, list the verify commands. Then stop and wait for Deniz's go.
- Make surgical, minimal changes. Don't refactor things you weren't asked to touch.
- **Debug like a detective:** state a theory, collect evidence (logs, `kubectl describe`, events,
  minimal targeted logging), and only fix once the evidence proves the theory. No speculative fixes.
- Explain only when Deniz asks. Keep status updates short.
- Ask before installing anything on Deniz's machine.

**Git**
- Make small, descriptive commits. Commit at the end of each phase after Deniz approves.
- **Never add `Co-Authored-By: Claude` lines or any Claude/AI attribution to commits or PR descriptions.**
