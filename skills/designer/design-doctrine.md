# Design doctrine (read before every run)

Sources: the PIXELS Guide (5 GitHub design tools), `frontend-design`, the taste-skill pack,
`ui-ux-pro-max`, `design-motion-principles`, prior site builds, and the operator's
stated preferences. Where a rule comes from one of those, it says so.

## 1. Precedence when skills disagree

1. The user's explicit words in this request.
2. `DESIGN.md` in the site folder: colours, fonts, type scale, spacing, radius, shadows.
3. The brief (audience, feeling, one action, proof).
4. `ui-ux-pro-max`: page structure and section order only. Its colours and fonts are suggestions
   and lose to DESIGN.md.
5. The chosen taste sub-skill: layout, typography discipline, and killing generic patterns.
6. Motion rules: last, and only after layout is settled.

When one rule overrides another, say which in one line. (Guide, section 9.)

### Taste sub-skills vs a chosen DESIGN.md (read from the actual skill files, 2026-10-01)

None of the taste skills reads DESIGN.md. `design-taste-frontend` has defaults with override
clauses that trigger when the brand brief names a choice; the style skills have hard bans.

| Sub-skill | With a DESIGN.md | Why |
|---|---|---|
| `design-taste-frontend` | **Compatible, preferred.** Treat DESIGN.md as the brief | Its font, serif, colour and layout rules are defaults with "unless the brand brief names it" overrides. Its shape-consistency and one-accent locks agree with a coherent DESIGN.md. Watch: default `tracking-tighter` display, Tailwind v4 and Motion defaults are stack/typography defaults, not design choices; DESIGN.md wins. |
| `gpt-taste` | **Conflicts on type, partly on layout** | Forces a font from Satoshi / Cabinet Grotesk / Outfit / Geist, a random hero and a GSAP set. Use only for scroll-motion composition after waiving the font rule, or skip. |
| `high-end-visual-design` | **Usually conflicts** | Mandates double-bezel squircle cards, pill nav, button-in-button, blur fade-up reveals, bans 1px grey borders and Helvetica/Inter. Fits only a DESIGN.md that is soft and rounded. |
| `minimalist-ui` | **Conflicts on colour and radius** | Bans pure `#000000`, caps radius at 8 to 12px, warm monochrome palette. Fits only a warm, light, low-radius DESIGN.md. |
| `industrial-brutalist-ui` | **Conflicts on colour** | Mandates one red accent and avoids `#000000`. Fits only a DESIGN.md that is already brutalist. |
| `stitch-design-taste` | **Generator, not a builder** | It writes a DESIGN.md; use it at step 3, never after one is chosen. |
| `redesign-existing-projects` | **Compatible in preserve mode** | Extracts and keeps the existing brand tokens. |

Rule: the table decides the route. Where a sub-skill rule contradicts DESIGN.md the rule is
waived and logged in `design-log.md`, never blended. Example worked through: the Bugatti
DESIGN.md (pure `#000000`, 0px radius on everything but pill buttons, transparent outlined
buttons, serif body, 2 to 4px display tracking, no accent, no shadows) routes to
`design-taste-frontend` only. `high-end-visual-design` would round every card and add bezels,
`minimalist-ui` would ban its black and soften its corners, `industrial-brutalist-ui` would add a
red accent, `gpt-taste` would swap its fonts.

## 2. The AI-look list (name it to ban it)

Naming the cliché is what suppresses it; "make it premium" does not.

- Purple-to-pink gradient, floating gradient blob.
- Big centred headline over three identical icon cards.
- Every section the same height and the same rhythm.
- Warm cream + high-contrast serif + terracotta accent, when chosen as a default rather than a
  decision. Same for near-black + one acid accent, and broadsheet hairline rules with zero radius.
  (`frontend-design`: legitimate for some briefs, but they appear regardless of subject.)
- Template chrome: all-caps eyebrow on every section, arrow-suffixed CTAs, numbered markers
  (01 / 02 / 03) when the content is not a real sequence.
- Fade-and-slide-up on every section, hover growth on every card, pulsing dots, breathing CTAs,
  blur on every entrance, items popping in one by one for no reason.
- "Stacked slides": each section generated in isolation so the page reads as unrelated slides.
  Require at least one persistent or morphing element across section boundaries (shared type
  treatment, a line or object that travels, a colour that shifts with scroll).
- Placeholder content: lorem ipsum, "Lorem Co.", invented testimonials, fake logo walls, made-up
  statistics.

## 3. Taste rules the operator has confirmed

- **Propose before restructuring.** Named bug or small clear fix: just do it. Layout, section
  treatment, multi-part effect set: recommendation plus one tradeoff first, build on the
  operator's answer.
- **Read the named design spec before proposing.** If the site has a DESIGN.md or spec, never
  propose changes that contradict it (moving figures off a locked mono display face or
  recolouring the accent both broke a real spec). "Use the same system, add your touch" means
  touches the spec itself licenses.
- **Motion replays.** Reveals reset when they leave the screen and replay on return in either
  direction; hover replays story pieces; scroll-linked effects run both ways. Stale sequences are
  cancelled with run-tokens. A still version exists for `prefers-reduced-motion`.
- **Plan then execute** for multi-effect work: a short per-section plan, then build in the same
  turn unless he says wait.
- **Hand-written CSS** for single-file local pages. No Tailwind play-CDN (it renders unstyled
  offline; a page built with it had to be reverted once).
- **Dark mode pairing:** in a dark theme, mute one of two saturated accents instead of running
  both at full strength.
- **Verify with measurements and screenshots**, not by reading the code. The operator notices
  misalignment and stray bands by eye.
- **Variants as routes** when the direction is uncertain: separate routes, one shared content file.

## 4. Motion rules (used when `design-motion-principles` is not installed)

- Frequency gate: rare interactions can be expressive; daily ones subtle and fast; constant ones
  (hundreds a day) and anything keyboard-initiated get no animation.
- Menus and popovers 150 to 250 ms; ease-out on entrance (arrive fast, settle slowly); nothing
  scales up from zero size; buttons do not bounce.
- Animate `transform` and `opacity` only; avoid layout-thrashing properties.
- Keyframes cannot retarget mid-flight; use state-driven transitions for anything a user can
  re-trigger quickly.
- Every animation honours `prefers-reduced-motion`.
- Start dials moderate (variance 6 or 7, motion 3 or 4); raise one at a time.
- One orchestrated signature moment beats scattered effects.

## 5. Writing a build prompt for another tool (PROMPT mode)

The 8-step formula, proven on a real brief:
1. Name the aspirational reference class (for example "Awwwards-level"), not a competitor.
2. List the generic failure modes for this category and forbid each by name.
3. Give real facts (names, people, numbers) before any creative direction.
4. Per section: literal copy, then a non-generic structure, then named animation behaviour.
5. Define a motion vocabulary once as a glossary; sections reference it tersely.
6. Name the "stacked slides" failure and require persistent or morphing elements across sections.
7. Fence ambition with hard rules: stack, exclusions, accessibility, performance.
8. End with a self-audit instruction ("cut anything that reads as a generic template") and a
   one-line statement of the real bar, placed last.
Highest-leverage pieces: step 2 and step 6. Check both before calling a prompt done.

## 6. Hard rules

- No fabricated proof: no invented testimonials, logos, review counts, case studies or statistics.
  If proof is missing, design without that section. Diagnostic material (what you found mapping
  similar problems) is expertise proof, never a delivered-results claim, unless there is a signed
  client and real numbers.
- No fabricated scarcity or urgency (countdowns, "only 3 spots") without a real constraint.
- No fee, price, or guarantee on a page that the offer docs do not state.
- Borrow the feel, never the brand: no copied logos, product photos, names or written copy.
- Do not disparage the user's own product in a hook or headline.
- Self-reported numbers on any page are labelled as the client's claim in the log, never
  presented by you as verified.
- Third-party skills and tools are read before they are installed. The motion skill and the
  Chrome extension come from small repos; use the official store listing for the extension.
- Do not dump private deal context (real prospect names, live-deal numbers) into a public page
  or example.
- A page is not done until the reviewer's Critical and Major list is empty or the open items are
  stated to the user.
