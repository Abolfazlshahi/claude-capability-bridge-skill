# Artifact Lifecycle

Treat an artifact as a deliverable with state, not merely the result of a creation call.

## Lifecycle

```text
INTENT / ACCEPTANCE
→ CREATE
→ RENDER / OPEN
→ INTERACT when applicable
→ VERIFY CONTENT / DATA / STATE
→ SAVE / VERSION
→ SHARE / ACCESS CHECK when requested
→ REPORT
```

## Updated artifact system

Current Cowork documentation says artifacts created on or after August 19, 2026 use the updated artifact system: they are saved to the account, can be shared within the organization, and open on the web. Older live artifacts retain their older behavior and are no longer editable in place.

Therefore do not assume all artifacts share the same lifecycle. Determine which artifact system/context applies.

## Verification rules

Creation success proves only that creation returned successfully.

Verify separately:

```text
rendered output
interactive controls
content/data correctness
persistent save/version state
share/access state when requested
```

If the artifact is supposed to be an interactive dashboard, tracker, comparison tool, or similar surface, exercise a representative interaction and verify the resulting state.

## Safety

Do not publish/share an artifact merely because it was created. Sharing is a consequential state transition and must be part of the requested acceptance criteria.
