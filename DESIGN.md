---
name: The Rookery
description: A cool-paper field system where corvids carry knowledge through a five-job delivery sequence and two distinct feedback currents.
colors:
  raven-navy: "#042458"
  route-cobalt: "#0050CC"
  mist-paper: "#DEE2EC"
  drafting-graphite: "#596A8B"
  signal-orange: "#DC6C36"
  dispatch-paper: "#F0EBE5"
---

# Design System: The Rookery

## Overview

**Creative North Star: "The Returning Field Dispatch"**

The Rookery looks like a natural-history field manual laid over a working draft table. Cool mist-blue paper, engraved navy corvids, graphite mechanisms, and measured construction lines make the work feel studied and practical rather than mythical or corporate. The result should make the technical system clear while retaining the warmth and memory of a hand-kept field guide.

Every illustration explains an operation. Huginn and Muninn carry, inspect, install, select, or return knowledge; they do not pose beside an abstract idea. Routes and mechanisms make sequence, observation, and return causally legible, while one restrained orange signal marks the intervention, dispatch, or return that matters most. The exact scene may change across repository-owned explanatory visuals, but the world remains one connected system in which evidence moves forward and distinct forms of feedback make future work more useful.

**Key Characteristics:**

- Cool drafting paper with faint grain, registration marks, and construction geometry.
- Natural-history corvid engraving paired with graphite field mechanisms.
- Cobalt paths that distinguish delivery from feedback and a scarce orange signal that explains intervention or return.
- Wide, calm compositions with enough negative space to survive GitHub rendering at reduced sizes.
- Characters whose physical action carries the meaning of the explanation.

## Colors

The palette is a disciplined blue field system: navy holds authority, cobalt carries sequence, blue-gray builds structure, and orange is reserved for the moment that changes the state of the work.

### Primary

- **Raven Navy:** Use for corvid engraving, dominant titles, strong outlines, and the darkest explanatory labels.
- **Route Cobalt:** Use for delivery paths, feedback currents, sequence arrows, stage numbers, and supporting banner copy. It should guide the eye, not become a broad decorative fill.

### Secondary

- **Signal Orange:** Use only for dispatch seals, active interventions, pressure points, and the return into another pass.

### Neutral

- **Mist Paper:** The default ground for repository-owned illustrations. Keep it cool and lightly textured so dark engraving remains crisp.
- **Drafting Graphite:** Use for secondary mechanisms, hatching, folds, measurements, and quiet construction detail.
- **Dispatch Paper:** Use for carried notes, envelopes, and evidence artifacts that need to separate from the cool ground.

### Named Rules

**The Orange Means Intervention Rule.** Orange identifies the action, handoff, or return that changes the state of the workflow; it is never a general-purpose accent.

**The Ink Hierarchy Rule.** Raven Navy explains the subject, Route Cobalt explains movement, and Drafting Graphite explains supporting structure.

## Typography

**Display Font:** Didot for the primary title in repository-owned banners.

**Supporting Font:** Baskerville Semibold for subtitles and diagram labels; compact bold sans is acceptable only for dense explanatory labeling where it is demonstrably more legible.

**Character:** Type should feel printed into a field guide, not overlaid by a product interface. The repository's Markdown body remains native to GitHub; this typography guidance applies to repository-owned visual assets.

### Hierarchy

- **Display:** Large, high-contrast serif titles with compact line spacing. Use only for the identity or subject of a wide banner.
- **Subtitle:** Smaller, weightier serif text in Route Cobalt. Keep it declarative and short enough to read when the image is scaled down.
- **Diagram Label:** Compact, sturdy lettering placed directly beside its stage or mechanism. Numbering should reinforce the path rather than act as decoration.

### Named Rules

**The Printed-In Rule.** Lettering must share the illustration's ink hierarchy and perspective while remaining real typography; never ask the raster artwork layer to render essential copy.

**The Family Restraint Rule.** Use one display treatment and one explanatory treatment within an asset. Name an exact font family only when the editable source uses it.

**The Layered Type Rule.** Keep essential lettering as real typography over a text-free illustration plate, retain the editable source, and export the shipped raster losslessly.

The workflow banner keeps its illustration and typography in separate production layers. `docs/assets/the-rookery-workflows-banner-artwork.webp` is the regenerated text-free illustration plate with complete routes and mechanisms, and `docs/assets/the-rookery-workflows-banner.svg` adds the title in Didot and the supporting copy and labels in Baskerville Semibold. The SVG contains no corrective artwork patches. The shipped WebP is a lossless render of that editable source, so later copy changes should update the vector text layer rather than regenerate the illustration.

## Layout

Repository banners use a wide landscape canvas (1600 × 640). They depend on large silhouettes, sparse text, and generous negative space so the image retains a clear reading when GitHub scales it to the content column. Future explanatory visuals should resolve their dimensions from their reading context rather than inherit a removed asset format.

Banners establish hierarchy in the first glance: a clear title zone, a dominant corvid action, and a route or mechanism that crosses the remaining field. Other explanatory visuals should concentrate on one job or relationship at a time. The mechanism should be readable before the texture, and the subject should face or move into the next meaningful area of the composition.

The approved workflow banner uses field-map composition C: a large serif title and cobalt subtitle occupy the upper-left while an unfolded diagonal map fills the field. One raven anchors Research and another descends to retrieve the verified dispatch at Ship. Research runs through Plan, Design, Build, and Ship above two quiet return ribbons, without a redundant label over the numbered delivery sequence. A solid cobalt Maintain ribbon passes through a compact repair-and-binding press, while a solid orange Learn ribbon passes through an open field notebook and feather. The ribbons deliberately abstract their detailed inputs and outcomes; the adjacent prose explains how Maintain creates repository memory and Learn returns a better question to Research. This topology is specific to the workflow explanation, not a universal template for future assets.

**The Causal System Rule.** Show the five delivery jobs as an ordered sequence and each feedback process as its own path to the stages or input it changes. Never force distinct feedback loops into a false serial sequence, and never flatten the system into repeated equal containers.

**The Reduced-Size Test.** At ordinary GitHub content width, the five-job delivery order, repository-wide improvement path, and return of a better question to Research must remain understandable before a reader zooms into the engraving detail.

## Elevation & Depth

The system is flat by interface standards and dimensional by illustration standards. It uses no glossy card shadows, bloom, or floating UI layers. Depth comes from engraved hatching, paper folds, perspective, overlap, line-weight changes, and the contrast between dark subjects and pale field geometry.

**The Drawn Depth Rule.** Create depth with physical overlap, perspective, and line density; do not simulate it with product-UI drop shadows or glow.

## Shapes

Organic corvid silhouettes break against precise field geometry. Circular route nodes, seals, apertures, calibration rings, and return loops act as recurring state markers; rectilinear jigs, gates, frames, and folded paper make each abstract job physical. Corners belong to the depicted material: cut paper may soften, wood and metal stay constructed, and no generic rounded-card radius unifies the scene.

**The Mechanism Has Consequence Rule.** Every aperture, gate, jig, ring, or bridge must make the stage's operation clearer; remove decorative machinery that does not change the explanation.

## Do's and Don'ts

### Do:

- **Do** give Huginn or Muninn a load-bearing action such as carrying a dispatch, operating a mechanism, inspecting a handoff, or returning a signal.
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
