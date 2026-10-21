# designer-skill

A Claude Code skill that takes a web design request from the first question to a live, checked page.
It does not invent its own design rules. It runs a fixed nine-step pipeline and calls the optional
skills you have installed (layout, motion, SEO, deploy) in a set order, along with a bundled copy
SOP, stops where you need to decide, and uses a separate reviewer agent to check the result.

## The idea in one paragraph

Most AI-built pages look the same because each step is done by whoever answers first, with no order,
no checkpoint and no independent check. `designer` fixes the order. One file (`DESIGN.md`) decides
what the page looks like. A taste skill decides how it is laid out. A different agent, one that did
not build the page, looks at real screenshots and reports faults. The builder does not mark its own
homework.

## What is in this repo

| Path | What it is |
|---|---|
| `skills/designer/SKILL.md` | The pipeline. The executable source. |
| `skills/designer/design-doctrine.md` | Precedence rule, the AI-look list, confirmed taste rules, motion rules, hard rules. Read before every run. |
| `skills/designer/brief-template.md` | The five-line intake brief. |
| `skills/designer/commands.md` | Cheatsheet of phrases and what each does. |
| `skills/designer/workflow-guide.md` | The long reference: component inventory, reasoning, compatibility table, troubleshooting, change log. |
| `skills/designer/references/copy-sop.md` | Bundled copy checks (headlines, hero framing, line sharpening, persuasion audit). No external copy tools needed. |
| `skills/designer/qa/shoot.py` | Playwright capture used by the QA step. |
| `agents/design-reviewer.md` | The independent QA agent. Reports a ranked fault list and never edits. |

## How to use it

Say what you want in plain words, or type `/designer`.

| You say | Mode | What happens |
|---|---|---|
| "designer build me a landing page for X" | NEW | The full pipeline below |
| "designer redo this site" | REDO | One question first: polish (audit and fix) or rebuild (full pipeline) |
| "designer make it look like <site>" | CLONE-LOOK | Pull that site's look into a DESIGN.md, then build with your content |
| "designer add motion to this page" | MOTION | Motion plan, build, then QA |
| "designer review this page" | REVIEW | QA only. Fault list with screenshots, no edits |
| "designer write a prompt to build a <type> site" | PROMPT | Writes a build prompt for another tool (Lovable, etc.), builds nothing |
| "designer show me 3 versions" | NEW (variants) | Three style routes sharing one content file |
| "designer ship it" | Ship step | Asks first, then deploys and re-checks the live URL |

It states the mode in one line before starting, for example `designer -> NEW (landing page, fresh build)`.

## The workflow

```
 1 Intake                what is the business, who is it for, what action, what proof
   |
 2 Strategy and copy     page structure for the industry, real copy (no lorem ipsum)
   |
 3 The look              one DESIGN.md: colours, fonts, type scale, spacing, radius, do and don't
   |
 4 Direction checkpoint  STOP. Show the plan, wait for your go-ahead
   |
 5 Build                 taste-skill router picks the layout skill, DESIGN.md wins on look
   |
 6 Motion                per-section plan, replays on scroll-back, still version for reduced motion
   |
 7 Independent QA        design-reviewer shoots the page in real Chrome and reports faults
   |                     (fix Critical and Major, re-run, max three rounds)
 8 Ship                  ASK FIRST. Deploy, schema and SEO checks, re-shoot the live URL
   |
 9 Log                   design-log.md in the site folder
```

### 1. Intake
Fills a five-line brief: business, audience, feeling, the one action, and proof. It reads what it
can from your files and earlier messages and asks only for what is still missing, in one batch. Proof
must be real. If there is none, the page is designed without a proof section instead of inventing one.

### 2. Strategy and copy
Runs the `ui-ux-pro-max` design-system search for the industry (section order, style, palette, font
pair, anti-patterns), then `frontend-design` to pin down one subject, the page's single job and a
signature element. Real copy is written now. Messaging is checked against the bundled
`references/copy-sop.md`: hero framing (customer is the hero), headline specificity, line-level
sharpening, and a persuasion audit with no fake scarcity, social proof or authority.

### 3. The look: one DESIGN.md
One file is the source of truth for the look. It comes from one of these:
- a ready-made file: `npx getdesign@latest add <name>` (68 to choose from)
- a live site, via the DESIGN.md Style Extractor Chrome extension (you click it, Claude cannot)
- a design-system bundle with its own readme and tokens
- an original, written with `stitch-design-taste`, the default when the brand should be distinctive
- if there is no brand yet, `brandkit` first (needs an image-generation tool)

The rule: borrow the feel, never the brand. No copied logos, photos or text.

### 4. Direction checkpoint
The skill stops here and waits. It shows the section order with a headline for each, the look, the
signature element, the build route (single file or Next.js, and whether to try 2 or 3 variants), one
tradeoff it wants decided, and a motion plan per section. For visually important pages it can also
offer design images per section to approve before any code. A named small fix ("white band in the
footer") skips the stop. Anything structural gets it.

### 5. Build
The `taste-skill` router picks the layout skill. Because those skills do not know DESIGN.md exists,
there is a **design contract**: DESIGN.md decides what the page looks like, the taste skill decides how
it is composed. If a taste rule contradicts DESIGN.md, the rule is waived (not blended) and written
into `design-log.md`. Default stack for one page is a single `index.html` with hand-written CSS.
Multi-page or heavy motion goes to Next.js with one shared content file.

### 6. Motion
Uses `design-motion-principles` if installed, otherwise the motion rules in `design-doctrine.md`.
Motion replays on scroll-back and on hover and resets when it leaves the screen. One bold moment, no
fade-and-slide on every section, no hover growth on every card.

### 7. Independent QA
The `design-reviewer` agent runs `qa/shoot.py` (Chrome at 390, 768 and 1440 px, five scroll depths, a
reduced-motion pass, overflow, console errors, alt text, tap targets), reads the screenshots, and
returns a ranked list: **Critical**, **Major**, **Minor**. The builder fixes Critical and Major and
re-runs, up to three rounds, then reports what is left. The builder also does its own screenshot pass
first, but that never replaces the reviewer.

### 8. Ship
Local files need no confirmation. A public deploy or a published artifact is asked about first. Then
deploy, add schema and run an SEO audit, and shoot the live URL once more.

### 9. Log
`design-log.md` records the brief, the mode, where DESIGN.md came from, what was tried and rejected,
QA rounds and what they fixed, waived rules and open items. The next request on the same site starts
from this file and DESIGN.md.

## When two rules disagree

Highest wins, and the skill says in one line which rule won:

1. Your explicit words in this request
2. `DESIGN.md`
3. The brief (audience, feeling, one action, proof)
4. `ui-ux-pro-max` for page structure and section order only
5. The chosen taste skill: layout and typography discipline
6. Motion rules, last

## The AI-look list

`design-doctrine.md` names the clichés so they can be banned by name: purple-to-pink gradients, a
centred headline over three identical icon cards, every section the same height, template chrome (an
all-caps eyebrow on every section, numbered 01/02/03 markers on non-sequences), fade-and-slide-up on
everything, "stacked slides" where each section is generated in isolation, and placeholder content.

## Hard rules

- No fabricated proof: no invented testimonials, logos, review counts or statistics.
- No fabricated scarcity or urgency.
- No price, fee or guarantee the offer docs do not state.
- Borrow the feel, never the brand.
- Self-reported numbers are labelled as the client's claim, never presented as verified.

## Install

The repo is deliberately dependency-light. Exactly one thing is a hard requirement:

### Hard requirement (QA step)

1. **Python + Playwright** — https://github.com/microsoft/playwright
   ```
   pip install playwright
   playwright install chrome
   ```
   (`qa/shoot.py` tries real Chrome first, then Edge, then bundled Chromium.)

### Bundled, nothing to install

2. **Copy SOP** — `skills/designer/references/copy-sop.md` distils the copy checks
   (Hopkins-style headlines, StoryBrand hero framing, Harry Dry line sharpening, Cialdini
   persuasion audit) so no external copy tools or MCP servers are needed.

### Optional skills (each step degrades gracefully without them)

3. **`ui-ux-pro-max`** — design-system search database (industry structure, palettes, font pairs):
   https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
   ```
   /plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill
   /plugin install ui-ux-pro-max@ui-ux-pro-max-skill
   ```
4. **`design-motion-principles`** — motion expert (create + audit modes):
   https://github.com/kylezantos/design-motion-principles
   ```
   npx skills add kylezantos/design-motion-principles -g -a claude-code -y
   ```
5. **Taste-skill pack** (13 anti-slop layout skills + the `/taste-skill` router):
   https://github.com/leonxlnx/taste-skill
6. **DESIGN.md Style Extractor (TypeUI, Bergside)** — the Chrome extension for CLONE-LOOK mode
   (only the user can click it):
   https://github.com/bergside/design-md-chrome or the Chrome Web Store listing:
   https://chromewebstore.google.com/detail/designmd-style-extractor/ogpdnchdjiibhobphelbbkemnnemkfma
7. **`getdesign`** — 68 ready-made DESIGN.md files, run per project, nothing to install:
   `npx getdesign@latest add <name>`
8. **`frontend-design`, `site-architecture`, `schema`, `seo-audit`, `seo-aeo`, `vercel:*`** —
   Claude Code skills/plugins; install from your own skill library or marketplace if you use them.
   Each does a smaller, ordinary job that the pipeline completes by hand when they are absent.

### Skill and agent files themselves

Copy the folders into your Claude Code user directory, then restart Claude Code (agents load at
session start):

```
skills/designer/            ->  ~/.claude/skills/designer/
agents/design-reviewer.md   ->  ~/.claude/agents/design-reviewer.md
```

Until the restart, the reviewer is not callable by name. Launch a general-purpose agent and tell it to
read `design-reviewer.md` as its instructions.

## Known limits

- The taste rules in `design-doctrine.md` are the author's own, not general design law. Edit section 3
  to match yours.
- Copy checks in `references/copy-sop.md` are a distillation for one narrow job (page copy inside
  this pipeline), not a full copywriting course.
- Some steps need tools not every machine has: an image-generation tool (brandkit, design images), the
  Chrome extension (looks from a live site), Higgsfield credits (scroll-scrubbed video worlds). The
  skill says plainly when a step could not run.
- For the long version with the compatibility table, troubleshooting and change log, read
  `skills/designer/workflow-guide.md`.
