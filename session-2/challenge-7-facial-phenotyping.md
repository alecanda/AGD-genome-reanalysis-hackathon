# Challenge 7 — Explore rare-disease facial phenotypes with GestaltMatcher

## Goal

Build an interactive dashboard or small exploration platform for a cohort of rare-disease facial images.

You will receive 125 patient images from five rare disorders, together with:

- the known syndrome label for each image
- GestaltMatcher facial embeddings
- GestaltMatcher prediction results
- additional image/patient metadata

The main goal is not simply to calculate prediction accuracy.

Instead, think of this as a **research exploration task**:

> How can we interactively explore a collection of patient images, their learned facial representations, and their diagnostic predictions?

For example, you could build a platform that allows a researcher to:

- visualize patients in a 2D embedding space
- see whether patients with the same syndrome cluster together
- color points by the known syndrome
- hover over or click a point to see the corresponding facial image
- inspect the GestaltMatcher prediction for an individual patient
- identify unusual patients or possible outliers
- explore patients that are close to each other in embedding space
- compare correctly and incorrectly predicted cases
- investigate where different syndromes overlap in the learned facial phenotype space

A useful prototype should make it easier to move between **cohort-level patterns** and **individual patient images**.

---

## Dataset

Download the dataset from [Sciebo](https://uni-bonn.sciebo.de/s/z9c26aWQBqxDb9Q).

The dataset is password-protected. Please request the password from the workshop organizers (Tzung-Chien Hsieh).

The dataset contains:

- 125 aligned facial images
- 5 rare disorders
- 25 images per disorder
- image and patient metadata
- one GestaltMatcher embedding per image
- one GestaltMatcher prediction JSON file per image

The extracted folder is approximately:

```text
demo_data/
├── demo_align/
│   ├── 1_aligned.jpg
│   ├── 2_aligned.jpg
│   └── ...
├── image_metadata_demo.tsv
├── demo_embeddings_v115.tsv
└── demo_output_v115/
    ├── 1_aligned.json
    ├── 2_aligned.json
    └── ...
```

The files can be connected using `image_id`.

For example:

```text
image_id = 1
```

corresponds to:

```text
image_metadata_demo.tsv
    → metadata for image 1

demo_embeddings_v115.tsv
    → facial embedding for image 1

demo_align/1_aligned.jpg
    → facial image

demo_output_v115/1_aligned.json
    → GestaltMatcher prediction
```

---

## Image metadata

`image_metadata_demo.tsv` contains one row per image.

Important fields include:

```text
image_id
patient_id
internal_syndrome_id
internal_syndrome_name
```

For this challenge, the most useful label is:

```text
internal_syndrome_name
```

This is the known syndrome diagnosis and can be used as the **class label** when exploring or visualizing the cohort.

For example, in an embedding plot you might use:

```text
x = t-SNE / UMAP dimension 1
y = t-SNE / UMAP dimension 2
color = internal_syndrome_name
```

This makes it possible to visually inspect whether patients with the same syndrome occupy similar regions of the embedding space.

The metadata file also contains additional fields such as gene information, phenotype features, age, gender, and ethnicity, which you may use if useful for your exploration.

---

## Facial images

The folder:

```text
demo_align/
```

contains the aligned facial images.

The naming convention is:

```text
<image_id>_aligned.jpg
```

For example:

```text
1_aligned.jpg
```

corresponds to:

```text
image_id = 1
```

A useful interactive visualization could allow the user to click or hover over a point and immediately see the corresponding facial image.

---

## Facial embeddings

`demo_embeddings_v115.tsv` contains one GestaltMatcher facial embedding per image.

It contains two columns:

```text
image_id
encoding
```

The `encoding` is a high-dimensional numerical representation of facial appearance learned by GestaltMatcher.

Conceptually:

```text
facial image
     ↓
GestaltMatcher
     ↓
facial embedding
     ↓
high-dimensional facial phenotype space
```

You can use these embeddings for:

- PCA
- t-SNE
- UMAP
- clustering
- nearest-neighbor search
- similarity analysis

One possible visualization is:

```text
                       ● patient
               ●
        ●                  ●

   ●        ●

color = internal_syndrome_name
hover/click = show patient image and prediction
```

The purpose is not necessarily to find perfectly separated clusters.

Instead, the visualization can help you explore:

- which syndromes form compact groups
- which syndromes overlap
- which patients appear unusual
- which patients are close to cases with another diagnosis
- whether prediction errors correspond to particular regions of the embedding space

---

## GestaltMatcher prediction results

`demo_output_v115/` contains one JSON prediction file per image.

For example:

```text
1_aligned.json
```

contains the prediction for:

```text
1_aligned.jpg
```

The JSON contains sections such as:

```text
suggested_genes_list
suggested_syndromes_list
suggested_patients_list
```

For syndrome-level exploration, the most relevant section is:

```text
suggested_syndromes_list
```

This is a ranked list of syndrome predictions.

A simplified result looks like:

```json
{
  "syndrome_name": "WILLIAMS-BEUREN SYNDROME; WBS",
  "omim_id": 194050,
  "distance": 0.548,
  "gestalt_score": 0.752,
  "image_id": "13834",
  "subject_id": "8750"
}
```

Useful fields include:

- `syndrome_name` — predicted syndrome
- `distance` — distance to the matched representation
- `gestalt_score` — facial similarity score
- `image_id` — matched reference image
- `subject_id` — matched reference patient

In general:

```text
lower distance        → greater similarity
higher gestalt_score  → greater similarity
```

The list order is the prediction ranking.

Therefore:

```python
data["suggested_syndromes_list"][0]
```

is the Top-1 prediction, while:

```python
data["suggested_syndromes_list"][:5]
```

contains the Top-5 predictions.

You can compare these predictions with `internal_syndrome_name` from the metadata.

---

## What could you build?

There is no required interface.

One possible idea is a research dashboard with several linked views:

```text
┌──────────────────────────────────────────────┐
│ Cohort summary                               │
│ 125 patients | 5 disorders                  │
├──────────────────────────────────────────────┤
│ Interactive embedding visualization         │
│                                              │
│     ● ●           ▲                          │
│  ●       ●              ■ ■                  │
│                                              │
│ color = syndrome                             │
│ hover = image + prediction                   │
├──────────────────────────────────────────────┤
│ Selected patient                             │
│ [image]                                      │
│ Known diagnosis: ...                         │
│ Top prediction: ...                          │
│ Gestalt Score: ...                           │
├──────────────────────────────────────────────┤
│ Patient browser / prediction overview        │
└──────────────────────────────────────────────┘
```

You could combine:

- interactive t-SNE or UMAP
- facial image previews
- known syndrome labels
- Top-1 / Top-5 predictions
- Gestalt Scores
- nearest neighbors
- filters by syndrome
- filters by correct/incorrect prediction
- patient-level detail views
- cohort-level performance summaries

You are encouraged to think about what would actually help a researcher explore this dataset.

---

## Some research questions you could explore

For example:

- Do patients with the same syndrome cluster together?
- Which disorders appear close to each other in embedding space?
- Are some patients clear outliers?
- Are incorrectly predicted patients located near another syndrome cluster?
- Which patients are nearest neighbors?
- Are patients with high Gestalt Scores located in denser regions?
- Which disorders are easier or harder to distinguish visually?
- Can the embedding visualization help explain certain prediction errors?

You do not need to answer all of these.

---

## Minimum goal

Create a working prototype that combines at least two different types of information.

For example:

- embeddings + syndrome labels
- images + embeddings
- images + predictions
- embeddings + predictions
- patient metadata + predictions

A simple but interactive research exploration tool is enough.

---

## Stretch ideas

If time allows, consider adding:

- image preview on hover
- linked plots
- nearest-neighbor exploration
- syndrome filtering
- outlier identification
- prediction-error filtering
- case-level detail views
- Top-1 / Top-5 summary
- confusion analysis
- downloadable filtered results

---

## What to present

At the end of the session, briefly show:

1. What you built
2. How users can explore the patient cohort
3. Which data sources you connected
4. One interesting pattern or case you discovered
5. What you would improve with more time

The goal is to create a small tool that helps turn model outputs into something that can be **explored, inspected, and interpreted at both the cohort and individual-patient level**.