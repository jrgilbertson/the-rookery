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

### Neutral

- **Mist Paper:** The ground for illustrated scenes: the banners and corvid plates. It is the cool, lightly grained paper the Illo character pack draws on, so the value varies a little across a plate. Keep it pale enough that dark engraving remains crisp.
- **Chalk Paper:** The ground for charts, tables, and diagrams. It is Mist Paper lifted almost to white, so the data is the darkest thing in view and small labels stay readable inside a GitHub page. A 1px Drafting Graphite hairline at 32% opacity holds the plate on a white page.
- **Drafting Graphite:** Use for secondary mechanisms, hatching, folds, measurements, small labels, and quiet construction detail.
- **Dispatch Paper:** Use for carried notes, envelopes, and evidence artifacts that need to separate from the cool ground.

### Named Rules

**The Orange Means Intervention Rule.** Orange identifies the action, handoff, or return that changes the state of the workflow; it is never a general-purpose accent.

**The Ink Hierarchy Rule.** Raven Navy explains the subject, Route Cobalt explains movement, and Drafting Graphite explains supporting structure.

**The Two Papers Rule.** Mist Paper carries a scene; Chalk Paper carries data. A figure whose job is to be read, not looked at, goes on Chalk. Text inks must reach 4.5:1 on their paper, and Drafting Graphite does on both.

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

The README banner follows the same pattern. `docs/assets/the-rookery-readme-banner-artwork.webp` holds the text-free artwork, in which Huginn comes home to a treetop rookery with a sealed field note; `docs/assets/the-rookery-readme-banner.svg` adds the Didot title and the Baskerville tagline, “A field guide to how I build with AI.” Its matching WebP is the lossless rendered asset used by the README.

The routing charts, `docs/assets/routing-base.svg`, `docs/assets/routing-base-providers.svg`, `docs/assets/routing-base-suites.svg`, and the shareable table `docs/assets/routing-table.svg`, are generated by `scripts/routing/evidence.py` from the data in `docs/routing/`. Regenerate them with the script and never edit them by hand. They use the Didot title and Baskerville labels as real SVG text on Chalk Paper, inside its graphite hairline. Each provider has one colour, taken from its logo and set in `docs/routing/chart.json`: Anthropic terracotta (`#C15F3C`), Google blue (`#2F6FDB`), and xAI black (`#050505`). OpenAI's logo is black like xAI's, so OpenAI takes a green (`#0E8F6E`). The terracotta, blue, and green are darkened from their brand values until each line reaches at least 3:1 against Chalk Paper. These colours depart from the house palette on purpose, so a reader recognises each provider, and all four separate on Chalk Paper for normal and colour-blind vision. A dash tells one provider's models apart, and every line is labelled with its model. Each effort has its own marker shape, named once in a key under the subtitle, so no point needs an effort label. Every label sits at the nearest spot clear of lines, points, and other labels, with a thin leader when it has to move away. Drafting Graphite draws the other providers' models faintly as context and carries the chart's structure. Names and labels are set in navy text beside a sample of the line, never in the line's own ink. A model's best-value effort sits in a soft tint of its line's colour, edged with a 1px ring of the same colour, so the mark belongs to its model rather than adding a navy layer over the lines. The tint goes under every line and point and the ring over them. The key shows the same mark in Raven Navy.

Two explanatory plates follow the banner pattern at 1664 × 936. `docs/assets/prioritization-leverage.svg` sets the leverage formula in italic Baskerville on the slate of `docs/assets/prioritization-leverage-artwork.webp`, where Huginn finishes the fraction bar in orange chalk; the SVG extends that bar to the width of the denominator. `docs/assets/coordinating-work.svg` labels the lock in `docs/assets/coordinating-work-artwork.webp`: small pale rooks are the workers, Huginn is the Team lead at the gate, and the flagged boat beside the bell is the change held for the operator. Workers are drawn smaller and lighter than Huginn so the lead stays the darkest figure. Each matching WebP is the lossless render the page uses.

The testing diagrams use self-contained HTML sources in `docs/assets/testing-flow.html` and `docs/assets/testing-safeguards.html`. Their matching SVGs carry the styles and real typography into the Markdown page. Both sit on Chalk Paper inside the same hairline as the charts. In the safeguards view a layer's top face is Chalk and its side faces step down through `#DEE2EC` to `#CED4E0`. The safeguards view embeds the approved Muninn artwork from `docs/assets/muninn-descending-delivery.png`: he brakes to land beside the testing layer with a learned check in his talons. Keep that artwork separate from the editable labels, and update the HTML source before exporting its SVG.

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
- **Don't** reuse the unfolded field map as the default composition for unrelated visuals.
- **Don't** pose a raven beside an idea it is not performing; removing the bird should break the explanation.
- **Don't** use broad orange fills, multiple competing accents, glossy gradients, or interface-style shadows.
- **Don't** drift into novelty mascot art or Norse-fantasy ornament that overwhelms the technical mechanism.
- **Don't** imply that the system learns autonomously; the return mythology supports the operator's deliberate learning loop.
