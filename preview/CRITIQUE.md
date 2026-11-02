⚠️ DEGRADED: single-context (no Skill tool in this run; impeccable's critique.md read and its method applied by hand. Assessment B is replaced by the repo checker and `gh repo view`, because a GitHub README is markdown with no CSS or JS and `impeccable detect` has nothing to scan.)

# Critique: live profile README (git show cf080cb:README.md) and public repos against the site

Target: the live profile README, the five public repos, and the published site (portfolio/src/data.ts, App.tsx) as the source of truth.

## Design specificity verdict

The live README was generic. Green badges, a skillicons grid and a Kali terminal metrics card could sit on any student's profile. Nothing tied it to the site's black and red identity, and it did not say what Nuno is looking for in the site's own words.

## Heuristic read (0-4, README as the interface)

| Heuristic | Score | Note |
|---|---|---|
| Visibility of status (what he wants, when) | 2 | Availability present but phrased differently from the site hero |
| Match with the real world | 2 | CTF categories named in the intro, against the wording rules |
| Consistency with the site | 1 | Colours, project set, project wording and highlights all differ |
| Recognition over recall | 2 | 13-row, 5-column table; the strongest project is buried in row 7 |
| Aesthetic and minimal design | 1 | Decorative metrics card, icon grid, commit counts |
| Error prevention (private repo exposure) | 3 | Private repos not linked, but their names and commit stats are published |

Cognitive load failures: a 13-row table with 5 columns forces scanning; more than 4 equal-weight choices at the top level (13 projects).

## Priority issues

1. The project table dilutes the best evidence. It lists 13 projects with commit counts, team sizes and private repos; the site curates 7 and leads with the network project.
2. The README contradicts the site. Different hero text, no highlights, green badge values, no Credly link, no link to the site.
3. Decorative stats. The metrics terminal card and the workflow that draws it add no information a recruiter needs.
4. Repo metadata does not support the README. Several public repos have no topics, no homepage, and descriptions that differ from the site.

## Discrepancy list

| # | Discrepancy | Resolved in |
|---|---|---|
| 1 | Intro says "this semester I'm on Erasmus" and names CTF categories; the site hero is "Informatics Engineering student at ISEP, Porto. Looking for a curricular internship from February to June 2027." | Task 2 |
| 2 | No link to the published site | Task 2 |
| 3 | No three highlights (CCNA, upCTF 8th of 300+, junior top 10) | Task 2 |
| 4 | Cert badges in an HTML table with green values (35d07f, 1f7a4d); site is black label and red (ff2a4f earned, 8a1a2e training); no Credly link; alt text was the label only | Task 2 |
| 5 | 13-row project table with commit counts, team sizes and private-repo projects (European stations, LAPR3, JPA demo); site shows 7 curated projects | Task 2 |
| 6 | Project wording differs from data.ts; the three-site network is mid-table and without NAT or port security | Task 2 |
| 7 | Alchemist's Arsenal described as "Unity game project", "3 of 6, team of 2" | Task 2 (README), Task 3 (repo description) |
| 8 | Metrics terminal card, metrics.yml workflow and lowlighter credit | Task 2 |
| 9 | Skills use skillicons.dev and name CTF categories; site has four groups: Security, Networks, Code, Platforms | Task 2 |
| 10 | Contact is two badges only; no Credly, no site | Task 2 |
| 11 | Old header.svg and assets/make_header.py superseded by header-dark.svg and header-light.svg | Task 2 |
| 12 | Profile repo homepageUrl is github.com/Nunex06, not the site | Task 3 |
| 13 | NunoGoncalves06.github.io: description "Nuno Gonçalves, offensive security", no homepage, no topics | Task 3 |
| 14 | SpotCast: no topics, no homepage; description differs from the site summary | Task 3 |
| 15 | Wakecast: no homepage; description is long and differs from the site summary | Task 3 |
| 16 | alchemists-arsenal: description "Alchemist's Arsenal — Unity game project" has an em dash; no topics | Task 3 |

## Persona red flags

Recruiter in 10 seconds: the old page led with an Erasmus note and CTF category names, and put the CCNA 3 network project in row 7. The new page leads with the site's hero line, three highlights and the network project.

## Run notes

Target slug and ignore list: not used (no `.impeccable/` store for this repo). Assessment independence: no, single context. CLI detector: not applicable to markdown. Browser overlay: not run; the GitHub-rendered preview belongs to a later task.
