# Challenge 6 — HPO annotation tool

HPO terms are the foundation of phenotype-driven diagnostics, yet assigning them is often still slow manual work.

Build an annotation tool with a graphical user interface that lets a user tag an input with HPO terms.

Possible inputs:
- hand radiographs
- free-text diagnosis descriptions
- clinical letters or case vignettes

Minimum concept:

    input (image or text)
             ↓
      HPO term search / suggestion
             ↓
      user confirms or corrects
             ↓
      stored annotation (input, HPO terms, annotator, timestamp)

Directions to consider:
- fast term lookup over the HPO ontology, including synonyms
- keyboard-driven annotation rather than click-heavy forms
- region-of-interest annotation on images
- showing parent/child terms so the annotator can pick the right level of detail
- export in a format a downstream model can consume

## Data

Download the HPO annotations yourself from https://hpo.jax.org/data/annotations (CC BY 4.0). `phenotype.hpoa` gives you, for each OMIM, ORPHANET or DECIPHER disease, the HPO terms curated for it, with frequency, onset and evidence code.

That file does not contain the ontology, so it has no HPO term labels, synonyms or parent/child links. Take `hp.json` or `hp.obo` from https://hpo.jax.org/data/ontology if you need term search or hierarchy.

A useful shortcut: if you know the disease behind an input, `phenotype.hpoa` gives you the terms expected for that disease. That is a strong suggestion list to put in front of the annotator before any model exists.

If annotating works well, the collected annotations become training data for a model that predicts HPO terms automatically, or makes good suggestions directly in the tool.

**Success:** someone can annotate a series of inputs faster and more consistently with your tool than by hand, and the exported annotations are usable as training data.

Use public or synthetic images and text only. No patient-identifiable material.
