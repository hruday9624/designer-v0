# Copy SOP (read at step 2, Strategy and copy)

This file distils the load-bearing copy checks that the designer pipeline applies when writing
real copy for a page. Apply them inline; no external copy tools or MCP servers are needed.

Four sources, attributed: Claude C. Hopkins' *Scientific Advertising* (public domain, 1923),
Donald Miller's SB7 framework (*Building a StoryBrand*), Harry Dry's copy method (Marketing
Examples), and Robert Cialdini's six principles (*Influence: The Psychology of Persuasion*).

## 1. Headline and claims (Hopkins)

- The headline's job is to **select the right reader, not to appeal to the most readers.** Name
  the audience or the problem in the headline; a vague headline wins impressions and loses the
  buyer.
- **Be specific.** "Cuts booking time in half" beats "saves you time". Any claim that can carry a
  number must carry one the client actually has. If the client has none, weaken the claim until it
  needs no number; never invent one.
- **Offer service, not a selfish appeal.** Lead with what the visitor gets, not with the company's
  pride ("we are the leading..."). Feature-by-outcome, in the visitor's words.
- **Advertising is salesmanship in print.** Every section earns the next; a page that amuses
  without moving the reader toward the one action has failed its job.
- **Test before betting:** for any headline choice that stays open after the checkpoint, say which
  of two headlines you would A/B test first, and what would settle it.

## 2. Page structure and who the hero is (Miller / SB7)

- **The customer is the hero. The brand is the guide.** Any draft where the brand solves the
  problem in its own voice ("we transform", "our revolutionary...") gets flagged and rewritten
  before other feedback. Empathy ("we know how it feels to...") plus authority (one proof line)
  is what makes a guide believable.
- Name the problem in three layers: **external** (the visible hassle), **internal** (how it makes
  them feel), and **philosophical** (why it is wrong that it happens). Copy that names all three
  reads like it was written for that reader.
- The page should show a simple **plan** (usually three steps: how it works / book / get the
  result) and a **call to action** that asks for the one action, clearly and once per
  screen-worth of copy.
- Frame cost of inaction: what failure looks like if nothing changes, without fear-mongering.
  **Never** manufacture the failure.

## 3. Line-level sharpening (Harry Dry)

Run the Three-Question Filter on every headline and sub-headline; if any answer is no, rewrite:

1. **Can I picture it?** (concrete image, not an abstraction)
2. **Can it be falsified?** (it says something real enough to be checked)
3. **Could nobody else say it?** (specific to this business; if a competitor could paste the same
   line on their page, it carries no weight)

Rewriting drill: replace abstractions with the concrete thing they stand for. "Enterprise-grade
platform" -> the actual thing: "your data stays in your AWS account".

## 4. Persuasion audit (Cialdini)

Check which of the six principles the page actually fires, and fire none of them without real
substance behind it:

- **Reciprocation:** a genuinely useful free thing (guide, audit, tool) earning the contact.
- **Commitment and consistency:** small yes first (checklist, quiz) before the bigger ask.
- **Social proof:** real counts, real names, real quotes only; a logo wall of clients you cannot
  name is banned.
- **Liking:** the operator's/client's own voice and face; similarity to the reader.
- **Authority:** credentials, media, real numbers; claimed authority without evidence reads worse
  than none.
- **Scarcity:** only when a real constraint exists and is stated honestly.

## Hard copy rules (apply to every draft)

- No fabricated proof: no invented testimonials, logos, review counts or statistics.
- No fabricated scarcity or urgency (countdowns, "only 3 spots") without a real constraint.
- No price, fee or guarantee the client's own documents do not state.
- No vague superlative ("best", "amazing", "world-class") without pushing the client for the real
  number; if there is none, cut the superlative.
- Self-reported numbers are labelled as the client's claim in `design-log.md`, never presented by
  you as verified.
- Placeholder copy (lorem ipsum, "Lorem Co.") never ships from this pipeline.

## When this SOP is not enough

This file is a distillation for one narrow job: writing and checking the copy of a page inside the
designer pipeline. For a full messaging strategy, offer architecture or negotiation support, the
operator can plug in their own dedicated copy tools instead of this file.
