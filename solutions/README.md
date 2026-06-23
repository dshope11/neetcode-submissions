# Curated solutions

This is the **curated, organized-by-pattern** home for solved problems - the
place to look one up or re-read it. It is maintained by hand (via the MindWall
`/neetcode` workflow), separate from the automated raw dump.

## Two zones, no clashes

| Zone | Path | Owner | Contents |
|---|---|---|---|
| Raw archive | `Data Structures & Algorithms/<neetcode-slug>/submission-N.py` | NeetCode GitHub Sync (automated) | David's verbatim accepted submissions, exactly as typed. Never hand-edited. Re-solves stack as `submission-1.py`, `submission-2.py`, ... |
| Curated | `solutions/<NN-pattern>/<LLLL-slug>.py` | MindWall `/neetcode` (manual) | One enriched file per problem: optimal solution + alternatives + style notes. |

NeetCode's Sync only ever writes under `Data Structures & Algorithms/`, so the
curated tree under `solutions/` never collides with the auto-push.

## Naming convention

```
solutions/
  <NN>-<pattern-slug>/        # NN = NeetCode roadmap order (01, 02, ...)
    <LLLL>-<problem-slug>.py  # LLLL = zero-padded LeetCode number
```

- Pattern folders sort in **roadmap (learning) order**.
- Files sort by **LeetCode number** within a pattern, and are greppable by both
  number and slug.

Example: `solutions/01-arrays-and-hashing/0049-group-anagrams.py`.

## File format

Each curated file carries, top to bottom:

1. **Header comment** - problem name + LC number + pattern + list; solve date,
   outcome (`solo` / `hint` / `looked-up`), and any **style notes** (naming /
   PEP 8 slips in the typed solution, noted rather than silently fixed).
2. **Optimal solution, active** - copied verbatim from the accepted submission
   so it stays a valid, runnable file and preserves what David actually typed.
3. **Alternative implementations, commented** - every other instructive approach
   (sorted-key, brute force, one-liner, O(1)-space variant, ...), each with a
   one-line time/space complexity annotation.

The durable *knowledge* layer (recognition triggers, templates, gotchas, solve
log) lives in the MindWall wiki concept pages; these files are the code archive.
