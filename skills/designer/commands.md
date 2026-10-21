# designer: command cheatsheet

Invoke with `/designer` or by name. Say what you want in plain words; the skill picks the mode.

| You say | Mode | What happens |
|---|---|---|
| "designer build me a landing page for <business>" | NEW | Full pipeline: intake, strategy and copy, DESIGN.md, checkpoint, build, motion, QA, ship, log |
| "designer redo this site" | REDO | One question: polish (audit and fix) or rebuild (full pipeline) |
| "designer make it look like <site>" | CLONE-LOOK | Extract the site's DESIGN.md (you run the Chrome extension), then build with your content |
| "designer add motion to this page" | MOTION | Per-section motion plan, build, then QA |
| "designer review this page" | REVIEW | Independent QA only: ranked fault list with screenshots, no edits |
| "designer write a prompt to build <type> site" | PROMPT | Applies the 8-step prompt formula for another builder tool, no build |
| "designer show me 3 versions" | NEW (variants) | Three style routes sharing one content file |
| "designer ship it" | Ship step | Asks first, then deploys and checks the live URL |

## Files

- `SKILL.md`: the pipeline
- `design-doctrine.md`: precedence, AI-look list, confirmed taste rules, motion rules, hard rules
- `workflow-guide.md`: the full end-to-end guide (read this first when extending or auditing)
- `brief-template.md`: intake format
- `references/copy-sop.md`: bundled copy checks (replaces external copy tools)
- `qa/shoot.py`: Playwright capture (390 / 768 / 1440, five scroll depths, reduced motion)
- `~/.claude/agents/design-reviewer.md`: the QA agent (registers on next Claude Code start)

## Per-site files it creates

- `DESIGN.md`: the look, source of truth
- `design-log.md`: brief, decisions, rejected options, QA rounds, open items

## Dependencies

- `design-motion-principles` (motion expert skill): optional. If missing, the skill falls back to
  the motion rules in `design-doctrine.md`. Install:
  `npx skills add kylezantos/design-motion-principles -g -a claude-code -y`
  (https://github.com/kylezantos/design-motion-principles)
- All other optional skills and their pinned sources: see the README's Install and Dependencies
  sections.
