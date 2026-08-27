# beads (bd) — conlang

Task tracking is **bd**. Do not use TodoWrite, TaskCreate, or markdown TODO lists.

**Daily:** `bd ready` · `bd show <id>` · `bd update <id> --claim` · `bd close <id>`
`bd create --title="..." --description="..." --type=task|bug|feature --priority=0-4`

**Less obvious, worth knowing:** `bd blocked` · `bd dep add <issue> <depends-on>` ·
`bd search <q>` · `bd stale` · `bd orphans` · `bd defer <id> --until=<date>` ·
`bd supersede <id> --with=<id>` · `bd human <id>` (flag for a human decision) ·
`bd remember "insight"` / `bd memories <keyword>` (persistent notes, not MEMORY.md).
Avoid `bd edit` — it opens `$EDITOR` and blocks the agent.

## Landing work

Two remotes: `origin` (crew landing target) and `github` (public mirror,
github.com/heated/conlang — PUBLIC, nothing sensitive). Work lands on
`origin/main` and is mirrored:

```bash
git rebase main                  # in the worktree, main moves under you
git -C <main-checkout> merge --ff-only <branch>
bd dolt push && git push origin main && git push github main
```

Close finished beads before pushing. File beads for anything left over.
