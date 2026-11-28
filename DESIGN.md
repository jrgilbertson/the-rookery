---
name: The Rookery
description: A cool-paper field system where corvids carry knowledge through a five-job delivery sequence and two distinct feedback currents.
colors:
  raven-navy: "#042458"
  route-cobalt: "#0050CC"
  mist-paper: "#E3E9F7"
  chalk-paper: "#F6F7FA"
  drafting-graphite: "#47577A"
  signal-orange: "#DC6C36"
  dispatch-paper: "#F0EBE5"
  night-paper: "#14161B"
  night-sheet: "#1B1E25"
  night-chalk-ink: "#ECEEF3"
  night-graphite: "#A7AFC0"
  night-cobalt: "#93AEEF"
  night-signal: "#E08A5E"
  night-dispatch: "#29251F"
  night-emphasis: "#34415C"
  white-sheet: "#FFFFFF"
  signal-ink: "#963E12"
  control-border: "#7C87A0"
  add: "#0B5D3B"
  add-wash: "#EAF3EE"
  del: "#8F2A1F"
  del-wash: "#F7E9E6"
  night-mist: "#242A36"
  night-signal-ink: "#F0A57E"
  night-control-border: "#686E7A"
  night-add: "#9BD3B5"
  night-add-wash: "#1C2A23"
  night-del: "#F0A99D"
  night-del-wash: "#33201D"
typography:
  display:
    fontFamily: "Didot, 'Bodoni 72', 'Bodoni MT', Georgia, serif"
    fontSize: "2.6rem"
    fontWeight: 400
    lineHeight: 1.08
    letterSpacing: "-0.01em"
  title:
    fontFamily: "Baskerville, 'Libre Baskerville', 'Baskerville Old Face', Georgia, serif"
    fontSize: "1.2rem"
    fontWeight: 600
    lineHeight: 1.3
  body:
    fontFamily: "Baskerville, 'Libre Baskerville', 'Baskerville Old Face', Georgia, serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: "0.72rem"
    fontWeight: 650
    lineHeight: 1.4
    letterSpacing: "0.04em"
  control:
    fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: "0.82rem"
    fontWeight: 400
    lineHeight: 1.5
  mono:
    fontFamily: "ui-monospace, 'SF Mono', Menlo, Consolas, monospace"
    fontSize: "0.8rem"
    fontWeight: 400
    lineHeight: 1.55
rounded:
  card: "2px"
  circle: "50%"
spacing:
  xs: "4px"
  sm: "8px"
  md: "12px"
  lg: "16px"
  xl: "24px"
  gutter: "28px"
  measure: "30rem"
components:
  card:
    backgroundColor: "{colors.white-sheet}"
    textColor: "{colors.raven-navy}"
    typography: "{typography.body}"
    rounded: "{rounded.card}"
    padding: "22px 24px 24px"
  control:
    backgroundColor: "{colors.white-sheet}"
    textColor: "{colors.raven-navy}"
    typography: "{typography.control}"
    rounded: "{rounded.card}"
    padding: "6px 12px"
    height: "36px"
  control-chosen:
    backgroundColor: "{colors.raven-navy}"
    textColor: "{colors.chalk-paper}"
    typography: "{typography.control}"
    rounded: "{rounded.card}"
    padding: "6px 12px"
    height: "36px"
  text-field:
    backgroundColor: "{colors.white-sheet}"
    textColor: "{colors.raven-navy}"
    typography: "{typography.control}"
    rounded: "{rounded.card}"
    padding: "10px 12px"
    height: "5em"
    width: "100%"
  chip:
    textColor: "{colors.drafting-graphite}"
    rounded: "{rounded.card}"
    padding: "1px 7px"
  factor-pill:
    textColor: "{colors.raven-navy}"
    rounded: "{rounded.card}"
  factor-pill-three:
    backgroundColor: "{colors.mist-paper}"
    textColor: "{colors.raven-navy}"
    rounded: "{rounded.card}"
  shortcut-help:
    backgroundColor: "{colors.white-sheet}"
    textColor: "{colors.raven-navy}"
    typography: "{typography.control}"
    rounded: "{rounded.card}"
  dispatch-note:
    backgroundColor: "{colors.dispatch-paper}"
    textColor: "{colors.raven-navy}"
    padding: "8px 12px"
  seal:
    backgroundColor: "{colors.signal-orange}"
    rounded: "{rounded.circle}"
    size: "10px"
  diff-added:
    backgroundColor: "{colors.add-wash}"
    textColor: "{colors.add}"
    typography: "{typography.mono}"
    padding: "2px 8px 2px 2.3em"
  diff-removed:
    backgroundColor: "{colors.del-wash}"
    textColor: "{colors.del}"
    typography: "{typography.mono}"
    padding: "2px 8px 2px 2.3em"
---

# Design System: The Rookery

## Overview

**Creative North Star: "The Returning Field Dispatch"**

The Rookery looks like a natural-history field manual laid over a working draft table. Cool mist-blue paper, engraved navy corvids, graphite mechanisms, and measured construction lines make the work feel studied and practical rather than mythical or corporate. The result should make the technical system clear while retaining the warmth and memory of a hand-kept field guide.

Every illustration explains an operation. Huginn and Muninn carry, inspect, install, select, or return knowledge; they do not pose beside an abstract idea. Routes and mechanisms show the order of work, where observation happens, and how feedback returns. One restrained orange signal marks the intervention, dispatch, or return that matters most. Scenes may change across repository-owned explanatory visuals. Each should show the same connected system, with evidence moving forward and distinct feedback paths improving future work.

**Key Characteristics:**

- Cool drafting paper with faint grain, registration marks, and construction geometry.
- Natural-history corvid engraving paired with graphite field mechanisms.
- Cobalt paths that distinguish delivery from feedback and a scarce orange signal that explains intervention or return.
- Wide, calm compositions with enough negative space to survive GitHub rendering at reduced sizes.
- Characters whose physical action carries the meaning of the explanation.

## Colors

Navy signals authority, cobalt shows the sequence, and blue-gray defines supporting structure. Reserve orange for the moment that changes the state of the work.

### Primary

- **Raven Navy:** Use for corvid engraving, dominant titles, strong outlines, and the darkest explanatory labels.
- **Route Cobalt:** Use for delivery paths, feedback currents, sequence arrows, stage numbers, and supporting banner copy. It should guide the eye, not become a broad decorative fill.

### Secondary

- **Signal Orange:** Use only for dispatch seals, active interventions, pressure points, and the return into another pass.
- **Signal Ink** (`#963E12`): The text ink for the words beside an orange mark. Signal Orange reaches only 3.1:1 on Chalk Paper, too little for text, so the words take Signal Ink, which reaches 6.5:1 on Chalk Paper and 7.0:1 on a white sheet.

### Neutral

- **Mist Paper:** The ground for illustrated scenes: the banners and corvid plates. It is the cool, lightly grained paper the Illo character pack draws on, so the value varies a little across a plate. Keep it pale enough that dark engraving remains crisp.
- **Chalk Paper:** The ground for charts, tables, and diagrams. It is Mist Paper lifted almost to white, so the data is the darkest thing in view and small labels stay readable inside a GitHub page. A 1px Drafting Graphite hairline at 32% opacity holds the plate on a white page.
- **Drafting Graphite:** Use for secondary mechanisms, hatching, folds, measurements, small labels, and quiet construction detail.
- **Dispatch Paper:** Use for carried notes, envelopes, and evidence artifacts that need to separate from the cool ground.
- **Control Border** (`#7C87A0`): The edge of an interactive control on a working page. It is Drafting Graphite at 70% over Chalk Paper, and it reaches 3.36:1 on Chalk Paper and 3.60:1 on a white sheet.

### Named Rules

**The Orange Means Intervention Rule.** Orange identifies the action, handoff, or return that changes the state of the workflow; it is never a general-purpose accent.

**The Ink Hierarchy Rule.** Raven Navy explains the subject, Route Cobalt explains movement, and Drafting Graphite explains supporting structure.

**The Two Papers Rule.** Mist Paper carries a scene; Chalk Paper carries data. A figure whose job is to be read, not looked at, goes on Chalk. Text inks must reach 4.5:1 on their paper, and Drafting Graphite does on both.

### Night Paper

An interactive page that people read at night, such as the review page the `reviewing-prs` skill ships, may follow the reader's dark setting. Night Paper keeps every role of the palette on a near-neutral graphite ground. Its ground is a near-neutral graphite (`#14161B`, with sheets at `#1B1E25`) and its main ink is Chalk (`#ECEEF3`). Drafting Graphite lifts to `#A7AFC0`, Route Cobalt to `#93AEEF`, Signal Orange to `#E08A5E`, and Signal Ink to `#F0A57E`. Dispatch Paper darkens to a warm `#29251F` and Mist Paper to `#242A36`. Control Border becomes `#686E7A`, Night Graphite at 55% over the sheet, which reaches 3.26:1 on the sheet and 3.53:1 on the ground. Each role keeps its meaning, and every text ink still reaches 4.5:1 on its paper. Saturation stays low, so the ground does not read as blue and orange stays scarce.

## Typography

**Display Font:** Didot for the primary title in repository-owned banners.

**Supporting Font:** Baskerville Semibold for subtitles and diagram labels; a compact bold sans-serif is acceptable only for dense explanatory labels where it is demonstrably easier to read.

**Character:** Type should feel printed into a field guide, not overlaid by a product interface. The repository's Markdown body remains native to GitHub; this typography guidance applies to repository-owned visual assets.

### Hierarchy

- **Display:** Large, high-contrast serif titles with compact line spacing. Use only for the identity or subject of a wide banner.
- **Subtitle:** Smaller, weightier serif text in Route Cobalt. Keep it declarative and short enough to read when the image is scaled down.
- **Diagram Label:** Compact, sturdy lettering placed directly beside its stage or mechanism. Numbering should reinforce the path rather than act as decoration.

### Named Rules

**The Printed-In Rule.** Lettering must share the illustration's ink hierarchy and perspective while remaining real typography; never ask the raster artwork layer to render essential copy.

**The Family Restraint Rule.** Use one display treatment and one explanatory treatment within an asset. Name an exact font family only when the editable source uses it.

**The Layered Type Rule.** Keep essential lettering as real typography over a text-free illustration plate, retain the editable source, and export the shipped raster losslessly.

The workflow banner keeps its illustration and typography in separate production layers. `docs/assets/the-rookery-workflows-banner-artwork.webp` holds the text-free ropeway, its delivery wire, and its two return lines. `docs/assets/the-rookery-workflows-banner.svg` adds the Didot title and the Baskerville supporting copy and labels. The shipped WebP is a lossless render of that editable source, so later copy changes should update the vector text layer rather than regenerate the illustration.

The README banner follows the same pattern. `docs/assets/the-rookery-readme-banner-artwork.webp` holds the text-free artwork, in which Huginn comes home to a treetop rookery with a sealed field note; `docs/assets/the-rookery-readme-banner.svg` adds the Didot title and the Baskerville tagline, "A field guide to how I build with AI." Its matching WebP is the lossless rendered asset used by the README.

One explanatory plate follows the banner pattern at 1664 × 936. `docs/assets/prioritization-leverage.svg` sets the leverage formula in italic Baskerville on the slate of `docs/assets/prioritization-leverage-artwork.webp`, where Huginn finishes the fraction bar in orange chalk; the SVG extends that bar to the width of the denominator. Its matching WebP is the lossless render the page uses.

The testing diagrams use self-contained HTML sources in `docs/assets/testing-flow.html` and `docs/assets/testing-safeguards.html`. Their matching SVGs carry the styles and real typography into the Markdown page. Both sit on Chalk Paper inside the same hairline as the charts. In the safeguards view a layer's top face is Chalk and its side faces step down through `#DEE2EC` to `#CED4E0`. The safeguards view embeds the approved Muninn artwork from `docs/assets/muninn-descending-delivery.png`: he brakes to land beside the testing layer with a learned check in his talons. Keep that artwork separate from the editable labels, and update the HTML source before exporting its SVG.

### Routing charts

`scripts/routing/evidence.py` generates the routing chart `docs/assets/routing-base.svg`, the frontier chart `docs/assets/routing-frontier.svg`, and the shareable table `docs/assets/routing-table.svg` from the data in `docs/routing/`. Regenerate them with the script and never edit them by hand.

- **Type and paper.** The Didot title and Baskerville labels are real SVG text on Chalk Paper, inside its graphite hairline. Drafting Graphite carries the chart's structure.
- **Provider colors.** Each provider has one color, taken from its logo and set in `docs/routing/chart.json`: Anthropic terracotta (`#C15F3C`), Google blue (`#2F6FDB`), and xAI black (`#050505`). OpenAI's logo is black like xAI's, so OpenAI takes a green (`#0E8F6E`). The terracotta, blue, and green are darkened from their brand values until each line reaches at least 3:1 against Chalk Paper.
- **A deliberate departure.** These colors depart from the house palette on purpose, so a reader recognizes each provider, and all four separate on Chalk Paper for normal and color-blind vision.
- **Models and efforts.** A dash tells one provider's models apart, and every line is labeled with its model. Each effort has its own marker shape, named once in a key under the subtitle, so no point needs an effort label.
- **Labels.** Every label sits at the nearest spot clear of lines, points, and other labels, with a thin leader when it has to move away. Names and labels are set in navy text beside a sample of the line, never in the line's own ink.
- **Best-value mark.** A model's best-value effort sits in a soft tint of its line's color, edged with a 1px ring of the same color, so the mark belongs to its model rather than adding a navy layer over the lines. The tint goes under every line and point and the ring over them. The key shows the same mark in Raven Navy.
- **Frontier chart.** The frontier chart marks the frontier instead of best-value efforts: a soft Raven Navy band with a dashed navy line runs under every line and point, and a 1.6px navy ring circles each setting on it. Models the routing page routes keep their provider colors; every other model is a Drafting Graphite dotted line, keyed as not routed here. A name is bold when its model has a setting on the frontier.

## Layout

The README introduces Huginn and Muninn with the card-cabinet scene in `docs/assets/huginn-and-muninn.svg`. Huginn waits with one more field note while Muninn pulls open a drawer in an overstuffed cabinet to make room for it. The SVG embeds `docs/assets/huginn-and-muninn-artwork.png` and keeps their names, roles, and caption as editable Baskerville text. Update the vector text for copy changes and preserve the separate artwork plate.

The README banner uses a wide landscape canvas (1600 × 640). The workflow banner is 1600 × 704 to give its tagline and delivery labels more vertical space. They depend on large silhouettes, sparse text, and generous negative space so the image retains a clear reading when GitHub scales it to the content column. Choose dimensions for future explanatory visuals based on where people will view them. Do not reuse dimensions from a removed asset format by default.

A banner should make its main elements clear at first glance. Give the title a clear area, make the corvid's action dominant, and place a route or mechanism across the remaining space. Other explanatory visuals should concentrate on one job or relationship at a time. The mechanism should be readable before the texture, and the subject should face or move into the next meaningful area of the composition.

The approved workflow banner uses an aerial ropeway. Five posts carry one instrument each for Research, Plan, Design, Build, and Ship from left to right, joined by a delivery wire with a single arrowhead. Huginn clips a dispatch satchel onto the wire at the left while Muninn winds a reel at the right. The labels sit on clear paper above the instruments. A cobalt line returns improvements to the posts, and a separate orange line runs through the learning notebook to the first post. The adjacent prose explains how Maintain creates repository memory and Learn returns a better question to Research. This arrangement is specific to the workflow explanation, not a template for every future asset.

**The Causal System Rule.** Show the five delivery jobs as an ordered sequence and each feedback process as its own path to the stages or input it changes. Never force distinct feedback loops into a false serial sequence, and never flatten the system into repeated equal containers.

**The Reduced-Size Test.** At ordinary GitHub content width, the five-job delivery order, repository-wide improvement path, and return of a better question to Research must remain understandable before a reader zooms into the engraving detail.

## Elevation & Depth

The illustrations show physical depth without glossy card shadows, bloom, or floating UI layers. Depth comes from engraved hatching, paper folds, perspective, overlap, line-weight changes, and the contrast between dark subjects and pale field geometry.

**The Drawn Depth Rule.** Create depth with physical overlap, perspective, and line density; do not simulate it with product-UI drop shadows or glow.

## Shapes

Organic corvid silhouettes break against precise field geometry. Circular route nodes, seals, apertures, calibration rings, and return loops repeatedly mark the state of the work. Straight-edged jigs, gates, frames, and folded paper give each abstract job a physical form. Corners follow the depicted material. Cut paper may soften; wood and metal keep constructed edges. Do not apply one generic rounded-card radius throughout the scene.

**The Mechanism Has Consequence Rule.** Every aperture, gate, jig, ring, or bridge must make the stage's operation clearer; remove decorative machinery that does not change the explanation.

## Components

These components belong to working pages. A working page is an interactive page someone uses to decide something, such as the review page the `reviewing-prs` skill ships. It keeps the plates' palette, type families, and paper roles; the rules below cover the parts a plate does not have.

### Papers and type

- **Papers.** Chalk Paper is the ground, and each section sits on a white sheet held by a Drafting Graphite hairline. Dispatch Paper carries notes someone wrote, such as an agent's read, a note across items, or review feedback. Data that needs attention does not use Dispatch Paper.
- **Reading measure.** Prose takes one width, `--measure` (30rem, about 75 characters of body text): the lede, the key under the filters, a card's summary, the sentence about the hold line, notes on Dispatch Paper, panel paragraphs, and a table's legend. Blocks stacked in one column therefore end at the same edge. The measure is set in rem, not ch, because a width in ch follows each block's own font and gives two type sizes two widths. Tables, code diffs, screenshots, the two-column grid, and controls are not capped; a paragraph in a column narrower than the measure ends at its column.
- **Type.** Didot sets the page headline and numerals at 1rem or larger only, because its hairlines thin out at small sizes and on Night Paper. Baskerville sets body text and titles. A compact system sans sets labels, buttons, and metadata, never smaller than 0.7rem (11px). A working page loads no web fonts, so the Georgia fallback for both serifs is intended.

### Controls

- **Parts.** Containers and controls take a 2px radius, the corner of cut card stock; circles are kept for route nodes, ranks, and seals. A segmented control shows its chosen option as a Raven Navy fill with Chalk text, reversed at night. Focus is a 2px Route Cobalt ring. Controls are at least 36px tall, and 44px on narrow screens. Nothing casts a shadow.
- **Control borders.** A button, segmented control, filter, toggle, text field, or disclosure button is edged in Control Border, so a reader can find it by its edge alone. Control Border reaches at least 3:1 against the paper behind it: `#7C87A0` is 3.36:1 on Chalk Paper and 3.60:1 on a white sheet, and at night `#686E7A` is 3.26:1 on Night Sheet and 3.53:1 on Night Paper. The Drafting Graphite hairline reaches only 1.63:1 on Chalk Paper, so it holds sheets, dividers, and other parts nobody operates, and never a control.

### Cards

- **Card.** A card is a white sheet with a hairline edge, a 2px radius, and no shadow. It carries one item to decide: a rank in a circle, a Baskerville title, metadata chips, and the controls that record the decision.
- **Summary.** A card that carries a plain-language summary opens its body with it, above the sentence that explains the hold line. It is Baskerville body text in the main ink on the card's own sheet, held to the reading measure under a sans label. It takes no box and no Dispatch Paper, so the notes on a card stay distinct from it. A card without a summary draws nothing in its place.
- **Verdict notes.** The notes field is a multi-line text field on its own row across the card, under the title and the segmented control. It shows three lines, resizes vertically only, and sits on the card's own sheet with the Control Border, while the read-only verdicts box takes Chalk Paper, so the field you type in is the white one. Its text is the sans at 0.9rem, and 1rem on narrow screens so a phone does not zoom when it takes focus. The hint that a note needs a verdict sits left-aligned under the field. A collapsed card hides the field with the segmented control.
- **Active card.** The page has one active card at a time, the card its keyboard shortcuts act on. `<main>` marks it with a 2px Route Cobalt border in place of the hairline, and the rail marks the same card as current. Cobalt shows where the reader is on the route; it does not mean the card needs attention.
- **Collapsible routine cards.** A routine card starts collapsed: one under the hold line or from a dependency bot, with no hold and no violation. Its title, rank, metadata, and recalled-verdict badge stay visible outside the toggle. A card that is held or carries a violation never starts collapsed, and any link or shortcut that goes to a collapsed card opens it. The toggle is a control with a small Drafting Graphite chevron that turns when the card opens, without animation when the reader asks for reduced motion.
- **Factor pills.** `.card-factors` shows an item's leverage factors as a row of small pills: a 2px radius, a hairline edge, and a sans figure. Each pill carries a visually hidden label that names its factor. A factor that scores three takes the `.three` highlight, a Mist Paper fill with a Drafting Graphite edge and a bolder figure, so the fill never carries the meaning alone.

### Shortcut help

- **Disclosure panel.** A `?` button opens `#shortcut-help`, a non-modal panel that lists each keyboard shortcut, explains each verdict in one line, and holds a key to the page's marks. It is a white sheet with a hairline edge and a 2px radius, with no shadow and no scrim, and the page behind it stays usable. Escape closes it and returns focus to the `?` button.
- **Keys.** Each key sits in a small monospace cap with a 2px radius. The toggle that turns shortcuts on or off is a control, and shows its pressed state the way a segmented control shows its chosen option.
- **Page key.** The same panel explains the page's own marks: each value of the `Described?` column, the score factors with the hold line and the leverage formula, what orange marks, and the four groups. A term that the page draws with a seal, a ring, or a route dot carries the same mark in the key, and the words beside an orange seal take Signal Ink. The key holds one seal for each thing the page seals, so orange stays scarce.
- **Layout.** At 1200px and wider the panel sets three parts side by side, divided by a soft hairline: shortcuts and verdicts, then `Described?` and scores, then orange marks and groups. Below that it is one 440px column that scrolls inside itself, so it never grows wider than the screen. The panel takes keyboard focus while it is open, so the arrow keys scroll it.

### Signals

- **Orange.** A small Signal Orange seal marks what needs the operator: behavior a change did not describe, a change a revert cannot undo, a notice that leaves the work incomplete, anything that shipped without the operator's decision or changed after it, and a style outside the design system in a redrawn screen. Orange never fills an area and never marks an empty state; an empty group takes the graphite ring. Each orange mark also says what it means in words, set in Signal Ink.
- **Movement.** Route Cobalt marks what a change moved: a ring around a changed element and a heavier border on the changed step of a path.
- **Diff colors.** Code diffs use green and red, a deliberate departure like the routing chart's provider colors, because readers expect them. Added lines are `#0B5D3B` on `#EAF3EE` and removed lines `#8F2A1F` on `#F7E9E6`; at night they are `#9BD3B5` on `#1C2A23` and `#F0A99D` on `#33201D`. Each pair reaches 7:1.
- **Emphasis at night.** An emphasized cell uses Night Emphasis (`#34415C`) at night, because Mist Paper's night value sits too close to the sheet to read as a step.

## Do's and Don'ts

### Do:

- **Do** give Huginn or Muninn an action essential to the explanation, such as carrying a dispatch, operating a mechanism, inspecting a handoff, or returning a signal.
- **Do** use Route Cobalt and shape or direction together, so paths remain understandable without color.
- **Do** distinguish the Delivery Sequence, Repository Learning Loop, and Personal Learning Loop by position, labels, direction, and mechanism as well as color.
- **Do** keep Signal Orange scarce and attach it to one meaningful intervention or return.
- **Do** preserve calm negative space and a strong silhouette before adding paper grain, coordinates, hatching, or registration marks.
- **Do** write meaningful alt text that states the mechanism, sequence, and return represented by the image.

### Don't:

- **Don't** turn the workflow into a generic equal-card flowchart or consulting-deck diagram.
- **Don't** present Research, Plan, Design, Build, Ship, Maintain, and Learn as one seven-step serial loop; Maintain and Learn are distinct feedback loops with different destinations.
- **Don't** pose a raven beside an idea it is not performing; removing the bird should break the explanation.
- **Don't** use broad orange fills, multiple competing accents, glossy gradients, or interface-style shadows.
- **Don't** drift into novelty mascot art or Norse-fantasy ornament that overwhelms the technical mechanism.
- **Don't** imply that the system learns autonomously; the return mythology supports the operator's deliberate learning loop.
