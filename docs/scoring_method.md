# SmartATS Scoring Method

## Formula

```text
Final score = semantic points
            + skill points
            + project points
            + experience points
            + education points
```

For each component:

```text
Points awarded = match percentage x component weight / 100
```

## Default weights

| Component | Weight |
|---|---:|
| Semantic similarity | 35 |
| Required skills | 35 |
| Related projects | 15 |
| Experience | 10 |
| Education | 5 |

The application stops scoring if the weights do not total 100.

## Semantic similarity

The job description and resume are divided into meaningful chunks. SBERT compares
each job requirement with all eligible resume chunks. The strongest resume chunk
is saved as evidence. Similarities below the configured useful-match threshold add
no semantic points.

## Required skills

```text
Skill percentage = detected required skills / total required skills x 100
```

Skill aliases are loaded from `data/skill_aliases.csv`. The system reports
"not detected" rather than claiming that a candidate does not possess a skill.

## Related projects

The project component combines:

- SBERT project relevance: 10 of the 15 internal project points
- Required technologies used in projects: 5 of the 15 internal project points

Up to the two strongest project evidence chunks are used.

## Experience

SmartATS checks explicit duration statements and employment date ranges. When a
candidate meets or exceeds the requirement, experience match is capped at 100%.
Uncertain or missing duration evidence is flagged for manual verification.

## Education

Education terminology comes from `data/education_terms.csv`. A detected higher
configured level can satisfy a lower required level. Field equivalence remains a
human-review decision.

## Match categories

| Overall score | Category |
|---:|---|
| 80-100 | Strong match |
| 65-79.99 | Good match |
| 50-64.99 | Partial match |
| Below 50 | Low match |

These labels describe resume-to-job alignment only. They are not hiring decisions.

## Example

```text
Semantic:  80% x 35 / 100 = 28.0
Skills:    60% x 35 / 100 = 21.0
Projects:  70% x 15 / 100 = 10.5
Experience:50% x 10 / 100 =  5.0
Education:100% x  5 / 100 =  5.0

Final score = 28 + 21 + 10.5 + 5 + 5 = 69.5
Category = Good match
```

