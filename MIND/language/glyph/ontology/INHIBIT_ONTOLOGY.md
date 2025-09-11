# Inhibit Ontology

## Principle

**Inhibit** edges represent braking or constraint in the Mandala graph.  
They dampen salience, slow loops, and act as guardrails.  
Inhibit is the *brake* — the counterforce that prevents runaway activation.

## Law

- Inhibit is a **protector**: it reduces or cancels activation.  
- Inhibit is never punitive; it is a stabilizer.  
- `w_inhibit` defines how strongly an edge suppresses propagation.  
- Inhibit is balanced by excite (drivers) and resonate (bias).

## Runtime

- Inhibit edges subtract or mute activity.  
- High `w_inhibit` (>0.5) = hard stop, full brake.  
- Moderate (0.2–0.4) = soft dampening.  
- Low (<0.2) = gentle check.  

Inhibit is not semantic irrelevance — it is deliberate **suppression of flow**.

## Purpose

- To model guardrails, safety, conservation of energy.  
- To let glyphs **cool or contain** surges created by excite.  
- To be complemented by resonance, which biases but does not stop flow.  
- Without inhibit, loops spiral uncontrolled; with too much inhibit, the graph stagnates.
