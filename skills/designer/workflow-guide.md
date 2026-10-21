# The designer workflow: end-to-end guide

Written 2026-10-01. For the operator, or any agent that needs to run, audit or extend the
`designer` skill. `SKILL.md` is the executable pipeline; this file is the full explanation, with
the reasoning, the component inventory, the decision tables and the known limits. If the two ever
disagree, `SKILL.md` and `design-doctrine.md` win and this file needs updating.

Origin: the PIXELS Guide (Google Doc, "5 free GitHub tools that make Claude design like a studio,
not like an AI", doc id `1DxvG_MchxYjdQm_Xl1-QomcoCSiqaiiJaj9CLP7GMIU`, read 2026-10-01) plus
prior site builds and the operator's stated design preferences.

---

## 1. What it is, and what it is not

`designer` owns a web design request from the first question to the live link. It is an
**orchestrator skill**, not a design method and not a graph "digital employee". The design rules
live in the skills it calls. Its own job is order, precedence, checkpoints and proof that the page
works.

- It is a skill (runs in the main session) so it can stop at checkpoints and talk to the operator.
- Only the QA step runs as a subagent (`design-reviewer`), in a fresh context, so the builder never
  grades its own work.
- It is user-scope, so it works from any folder.

Why Claude produces boring sites without it: Claude can design, but with no brief it picks the
safest average of every site it has seen. Each tool below supplies one layer of the missing
brief: what suits the industry, what to avoid, which exact colours and fonts, what to borrow,
how things move.

## 2. Component inventory

| Role | Component | Where | Status |
|---|---|---|---|
| Orchestrator | `designer` skill | `~/.claude/skills/designer/` | built 2026-10-01 |
| Independent QA | `design-reviewer` agent | `~/.claude/agents/design-reviewer.md` | built, validated, registered |
| Browser capture | `qa/shoot.py` (Playwright, real Chrome, Edge fallback) | `designer/qa/shoot.py` | tested on a flawed page |
| Strategy and layout | `ui-ux-pro-max` plugin | plugin cache | optional (see Dependencies in the README) |
| Anti-slop build rules | taste-skill pack, 13 skills + `/taste-skill` router | `~/.claude/skills/` | optional (see Dependencies in the README) |
| Ready-made looks | `getdesign` (68 DESIGN.md files) | `npx getdesign@latest add <name>`, per project | no install (guide Tool 3) |
| Look from a live site | DESIGN.md Style Extractor, Chrome extension (Bergside) | Chrome Web Store | user click (guide Tool 4) |
| Motion | `design-motion-principles` | `~/.claude/skills/design-motion-principles/` | optional, falls back to doctrine section 4 |
| Subject grounding | `frontend-design` plugin | plugin cache | optional |
| Page structure | `site-architecture` skill | skills folder | optional, multi-page sites |
| Copy | `references/copy-sop.md` (bundled) | this skill folder | bundled, no install |
| SEO and markup | `seo-aeo`, `schema`, `seo-audit` | skills | optional |
| Deploy | `vercel:*` skills | plugin | optional |
| Heavy scroll film | `scroll-world` plugin | plugin | optional, rendering needs Higgsfield credits |

Taste-pack members: `design-taste-frontend` (default, v2), `design-taste-frontend-v1`,
`high-end-visual-design`, `minimalist-ui`, `industrial-brutalist-ui`, `gpt-taste`,
`stitch-design-taste`, `redesign-existing-projects`, `image-to-code`, `imagegen-frontend-web`,
`imagegen-frontend-mobile`, `brandkit`, `full-output-enforcement`. The router's table lists them;
update the router when one is added or removed.

## 3. The pipeline at a glance

```
0 Mode check -> 1 Intake -> 2 Strategy+copy -> 3 Look (DESIGN.md) -> 4 CHECKPOINT (stop)
   -> 5 Build -> 6 Motion -> 7 Independent QA (loop <=3) -> 8 Ship (confirm) -> 9 Log
```

Order rationale (from the guide, section 9): strategy, then the look, then the build, then the
motion, then the review, the way a studio works. Each tool has one job, and precedence settles
disputes.

## 4. Precedence when skills disagree

1. The user's explicit words in this request.
2. `DESIGN.md` in the site folder: colours, fonts, type scale, spacing, radius, shadows, do/don't.
3. The brief (audience, feeling, one action, proof).
4. `ui-ux-pro-max`: page structure and section order only.
5. The chosen taste sub-skill: layout, typography discipline, anti-slop.
6. Motion rules, last.

When a rule overrides another, say which in one line.

## 5. Step by step

### Step 0: Mode check
State the understood mode in one line.

| Request | Mode | Path |
|---|---|---|
| New page or site | NEW | steps 1 to 9 |
| "redo", "improve", "fix" an existing site | REDO | ask once: polish (`redesign-existing-projects`, audit then fix) or rebuild (full pipeline) |
| "make it look like <site>" | CLONE-LOOK | step 3 via extraction, then the rest |
| Only motion | MOTION | step 6, then 7 |
| "review this page" | REVIEW | step 7 only, report, no edits unless asked |
| "write me a prompt to build a site" | PROMPT | the 8-step formula in `design-doctrine.md` section 5; do not build |

The redo question exists because "redo" was ambiguous on an earlier site (polish vs fresh
build) and a wrong guess costs real rework.

### Step 1: Intake
Fill the five-line brief (template in `brief-template.md`): Business, Audience, Feeling (three
words), One action, Proof. Fill from what the user said, any brand/context files in the
workspace, and memory. Ask **only the blanks, in one message**: new vs redo,
one page or several, reference sites and what exactly is liked about them, brand assets, voice,
stack and hosting, constraints, real content available. If proof is missing, design without a proof
section rather than inventing one. Write the filled brief as the first section of `design-log.md`.

### Step 2: Strategy and copy
- `ui-ux-pro-max`: design-system search for the industry (structure, style, palette, font pair,
  anti-patterns). Use `site-architecture` for multi-page sites.
- `frontend-design`: pin one concrete subject, the page's single job, and a signature element.
- Write real copy now, never lorem ipsum. For messaging checks, read `references/copy-sop.md`
  (bundled) and apply its checks: hero framing (customer is the hero, brand is the guide),
  headline specificity and claim testing, line-level sharpening, and the persuasion audit
  (no fake scarcity, social proof or authority). No MCP servers or external copy tools needed.
- Voice: pages follow the client's voice; ask for it (voice notes, banned words, tone rules).

### Step 3: The look, one DESIGN.md
A DESIGN.md is one plain text file describing a whole visual style: exact colours with hex codes,
type scale, how buttons and cards look, spacing, shadows, do's and don'ts, responsive behaviour.
It is a brand book written for the AI. Pick one source:

1. **Ready-made.** `npx getdesign@latest add <name>` in the project folder (`... list` shows the 68
   names; `--force` replaces on purpose; a second add lands in a sub-folder). The files are
   independent interpretations of each brand, not official brand files.
2. **From a live site.** The Chrome extension. Claude cannot click it: the user opens the site,
   clicks the extension, Generate DESIGN.md, Download. Then move the newest `DESIGN.md` from
   Downloads into the project, read it, and report which values were taken. Sparse, animated or
   image-only sites extract thinly; try the pricing or features page.
3. **A design-system bundle** (zip with readme and `theme.json`, like the Modernist one): read the
   readme's Do and Don't first, then the tokens, then the closest template.
4. **Original.** Write it from the `frontend-design` plan (4 to 6 named hex values, type roles,
   layout concept, signature), using `stitch-design-taste` as the generator so the file carries
   the pack's anti-generic rules. Default when the brand must look distinctive.

No brand identity yet (no logo, palette, guidelines): offer `brandkit` to generate an identity
board first, then derive DESIGN.md from the approved board. Needs an image tool; say so if absent.

Always: borrow the feel, never the brand. Change logo, name, copy and ideally the main accent.
Never copy another company's logo, photos or written text. One DESIGN.md per project.

What a real file contains (worked example, Bugatti, 28 KB): a YAML token header (colours, typography
roles, radius, spacing, about 20 named components), then Overview, Colors, Typography, Layout,
Elevation, Shapes, Components, Do's and Don'ts, Responsive, Iteration Guide and Known Gaps. Its
own Known Gaps section lists what it could not capture (hover and animation timing, licensed
fonts unavailable for the web). Read that section for any file you adopt.

### Step 4: Direction checkpoint (stop and wait)
Show a short plan, then wait:
- section order with the headline for each section
- the look (palette, type pair, why it fits)
- the signature element
- the build route: which taste sub-skill and why, single file or Next.js, whether to build 2 or 3
  variants as separate routes
- one tradeoff that needs a decision
- a per-section motion plan (what moves, what stays still)
- optional: visual references first, `imagegen-frontend-web` (one design image per section,
  approved before any code), then build with `image-to-code`. Needs an image tool; offer, never force.

Skip the stop only for a named small fix ("white band in the footer"). Structural changes, a new
section treatment or a multi-effect set always get the checkpoint, because layout and rhythm are
the operator's taste call.

### Step 5: Build
**Design contract.** The taste skills do not know DESIGN.md exists, and some carry hard rules that
contradict a chosen look. So:
- DESIGN.md decides WHAT the page looks like: every token and component rule, including radius,
  shadows, button style, tracking and photography treatment, not only colours and fonts.
- The taste skill decides HOW it is composed and engineered: layout rhythm, hierarchy, anti-slop
  discipline, performance, accessibility.
- Before loading the sub-skill, treat DESIGN.md as "the brand brief that explicitly names these
  choices". That is the exact trigger the taste skills' own override clauses wait for.

Compatibility (read from the skill files, 2026-10-01):

| Sub-skill | With a DESIGN.md |
|---|---|
| `design-taste-frontend` | Compatible, preferred. Defaults carry "unless the brand brief names it" overrides |
| `gpt-taste` | Conflicts on type (forces Satoshi, Cabinet Grotesk, Outfit or Geist), partly on layout |
| `high-end-visual-design` | Usually conflicts (squircle double-bezel cards, pill nav, blur reveals, bans 1px grey borders) |
| `minimalist-ui` | Conflicts on colour and radius (bans `#000000`, caps radius at 12px) |
| `industrial-brutalist-ui` | Conflicts on colour (mandates a red accent) |
| `stitch-design-taste` | A generator for step 3, never a builder after a DESIGN.md is chosen |
| `redesign-existing-projects` | Compatible in preserve mode (extracts existing brand tokens) |

Rules: pick the route from this table; any sub-skill rule that contradicts DESIGN.md is waived,
not blended; record each waived rule in `design-log.md`; the sub-skill's pre-flight items that flag
DESIGN.md-licensed choices count as passing; if the user wants a clashing style, say so at the
checkpoint and let them choose to keep the file or drop it. Worked example: the Bugatti file
(pure black, 0px radius except pill buttons, transparent outlined buttons, serif body, 2 to 4px
display tracking, no accent, no shadows) routes to `design-taste-frontend` only.

Build details:
- Route through the `/taste-skill` router; run the sub-skill's own settings and its pre-flight
  check before showing anything, and report what it caught. Mobile app screens go to
  `imagegen-frontend-mobile`. Long single-pass pages also load `full-output-enforcement`.
- Stack: one page with no build tooling is a single `index.html` with hand-written CSS (works
  offline, no CDN framework). Multi-page, shared content or heavy scroll motion is Next.js with one
  shared content file (per-page routes import from it). Say which at the checkpoint.
- Real copy and real facts, mobile first, visible keyboard focus.
- Variants live as separate routes sharing one content file.
- Save to the current project folder (one folder per site). DESIGN.md at the site root.

### Step 6: Motion
- `design-motion-principles` in Create mode. Weight Jakub and Jhey for marketing pages, Emil for
  forms and navigation. Fallback if it is missing: `design-doctrine.md` section 4.
- Standing rules: motion replays on scroll-back and on hover (resets on leave, run-tokens cancel
  stale sequences), a still version for `prefers-reduced-motion`, plan then execute for
  multi-effect work, spend boldness in one place.
- Banned: per-section fade-and-slide-up, hover growth on every card, looping pulses, blur on every
  entrance, one-shot animations that never replay.
- Frequency gate: rare interactions may be expressive; daily subtle and fast; constant or
  keyboard-initiated none.
- Heavy scroll-scrubbed video worlds: only on request, via `scroll-world`; rendering needs
  Higgsfield credits, so say so before promising it.

### Step 7: Independent QA
The taste pre-flight is the builder's own check and does not replace this. Do your own screenshot
loop first (stray bands and misalignment are noticed by eye). Then spawn the `design-reviewer`
agent with the page path or URL, the DESIGN.md path and the brief. If the agent is not registered
(new agents load at the next Claude Code start), launch a `general-purpose` agent and tell it to
read `~/.claude/agents/design-reviewer.md` as its instructions.

The reviewer runs `python qa\shoot.py <page-or-url> <out-dir>` (set `PYTHONIOENCODING=utf-8`; use a
scratch out-dir): real Chrome at 390, 768 and 1440 px, viewport shots at five scroll depths plus a
full-page shot per width, and a reduced-motion pass at the widest width. It records horizontal
overflow, console errors, failed requests, h1 count, images without alt, missing viewport meta,
text under 12px, tap targets under 40px (mobile), and infinite animations still running under
reduced motion. It reads `report.json` and the screenshots, then reports.

Severity: CRITICAL = overflow at any width, page-breaking console errors, a hard-rule violation,
unreadable or hidden content, DESIGN.md ignored wholesale. MAJOR = visible quality problems,
missing alt, wrong h1 count, text under 12px, animation ignoring reduced motion, AI-look hits,
contrast below AA, placeholder copy. MINOR = polish, naming, metadata.

Report format: `VERDICT: SHIP / FIX FIRST / REBUILD`, then numbered CRITICAL / MAJOR / MINOR items,
each with `where | evidence | fix`, then WHAT HOLDS UP (max 3 lines) and NOT CHECKED. The reviewer
never edits. The designer fixes every Critical and Major, re-runs, up to three rounds, then
reports what is left. Run the motion audit from `design-motion-principles` here too.

### Step 8: Ship (confirm first)
Local files need no confirmation. A public deploy or an Artifact publish is outward-facing: ask
first. Then `vercel:*` skills to deploy, `schema` and `seo-audit` for markup and metadata,
`seo-aeo` if the page should be cited by LLMs. Re-run `shoot.py` against the live URL.

### Step 9: Log
Write `design-log.md` in the site folder: the brief, mode, DESIGN.md source, taste skill and
variants tried, **waived taste rules**, what the user rejected and why, QA rounds and fixes, open
items. The next request on the same site starts from this file and the DESIGN.md.

## 6. Hard rules (full list in `design-doctrine.md` section 6)

- No fabricated proof: no invented testimonials, logos, review counts, case studies or statistics.
  Discovery-call material is expertise proof, never delivered-results proof, without a signed
  client and real numbers.
- No fabricated scarcity or urgency. No price, fee or guarantee the offer docs do not state.
- Borrow the feel, never the brand. No copied logos, photos, names or written copy.
- Do not disparage the user's own product in a hook or headline.
- Self-reported numbers are labelled as the client's claim in the log, never presented as verified.
- Read third-party skills and tools before installing them. Use the official store listing for the
  Chrome extension.
- No private deal context (real prospect names, live-deal numbers) on a public page.
- A page is not done until the reviewer's Critical and Major list is empty or the open items are
  stated to the user.

## 7. Confirmed taste rules (operator-confirmed; edit to yours)

Propose before restructuring (named bug: just fix). Read the named design spec before proposing.
Motion replays. Plan then execute for multi-effect work. Hand-written CSS for single-file pages
(no Tailwind play-CDN). In dark themes mute one of two saturated accents. Verify with measurements
and screenshots, not by reading code. Variants as routes when the direction is uncertain.

## 8. Files the skill reads and writes

Skill folder (`~/.claude/skills/designer/`): `SKILL.md`, `design-doctrine.md`,
`brief-template.md`, `commands.md`, `workflow-guide.md` (this file), `references/copy-sop.md`,
`qa/shoot.py`.
Agent: `~/.claude/agents/design-reviewer.md`.
Per site: `DESIGN.md` (the look, source of truth) and `design-log.md` (brief, decisions, QA, waivers).

## 9. Troubleshooting

| Symptom | Cause and fix |
|---|---|
| `design-reviewer` "agent type not found" | Registry loads at session start. Restart Claude Code, or launch a `general-purpose` agent told to read the agent file |
| `shoot.py` cannot launch a browser | It tries Chrome, then Edge, then bundled Chromium. Install Chrome, or `python -m playwright install chromium` |
| Console prints garbled characters | Set `PYTHONIOENCODING=utf-8` |
| `npx skills add` denied | The auto-mode classifier blocks third-party code installs. The user runs it with the `!` prefix |
| `getdesign add` wrote DESIGN.md somewhere random | It writes to the current folder. `cd` into the project first |
| Taste skill overrode DESIGN.md | The sub-skill is incompatible per section 5 table. Re-route to `design-taste-frontend` or waive the rule and log it |
| Image-based steps fail | No image-generation tool or credits available. Skip `brandkit`, `imagegen-frontend-web`, `image-to-code` and say so |
| Extracted DESIGN.md is thin | Site is animated or image-only. Extract from its pricing or features page |

## 10. Known limits (as of 2026-10-01)

- The full pipeline has not been run on a real site. Tested: `shoot.py` and the reviewer, on a
  deliberately flawed page (all planted faults caught).
- The taste-versus-DESIGN.md contract is written guidance for the model, not code that enforces
  it. `design-taste-frontend` is about 1,200 lines of its own rules, so drift is possible; the
  reviewer's DESIGN.md fidelity check is the safety net.
- The image steps are unverified in this environment.
- `shoot.py` takes stills; it does not tab through the page, so keyboard focus order and hover
  states are read from CSS, not exercised.
- Star counts and tool claims from the PIXELS Guide were checked by its author on 2026-09-26 and
  not independently re-verified here.

## 11. Maintenance

- Adding or removing a taste sub-skill: update the `/taste-skill` router table and the
  compatibility table in `design-doctrine.md` section 1 and in this guide, section 5.
- After the first real run, tune the step 4 checkpoint wording and record what changed in
  `design-log.md` and your own session notes.
- Keep `SKILL.md` as the single executable source; this guide explains it.

## 12. Change log

- 2026-10-01: built from the PIXELS Guide. Added the QA agent and capture script (validated),
  installed `design-motion-principles`, wired in the taste-pack skills (`stitch-design-taste` at
  step 3, `brandkit`, `imagegen-frontend-web` and `image-to-code` as optional steps, the router
  and pre-flight at step 5), and added the DESIGN.md design contract with the compatibility table.
