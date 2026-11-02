⚠️ DEGRADED: single-context (no sub-agent allowed for this task; impeccable critique.md read and its method applied by hand. Assessment B is replaced by the repo checker, the scrollWidth table and the badge URL curls, because a GitHub README is markdown with no CSS or JS and `impeccable detect` has nothing to scan.)

# Critique: Quiet Signal profile README (light and dark, 1440 and 375 px)

Target: `profile-work/README.md` rendered by `gh api markdown` with the thin header SVGs and four section icons. Screenshots in `preview/shots/`.

## Design specificity verdict

Authored. The thin header (grey name over a heavy condensed OFFENSIVE SECURITY, with a single red bar) and the red outline icons beside each section repeat the site's black and red identity with one accent and no cards, counters or trophies. It does not read as a template profile. The 28 px name stays near 12 px on a phone.

## Heuristic read (0-4, README as the interface; 7 and 10 n/a for a portfolio page)

| # | Heuristic | Score | Key issue |
|---|---|---|---|
| 1 | Visibility of status | 3 | Availability sits in the first line under the header |
| 2 | Match with real world | 3 | Plain language, "training completed" never says certified |
| 3 | User control | 3 | Links open normally; More projects collapses |
| 4 | Consistency | 3 | One accent red, icons all outline at 20 px |
| 5 | Error prevention | 3 | Private repos are named as private, not linked |
| 6 | Recognition over recall | 3 | Four labelled skill rows, five projects visible |
| 7 | Flexibility | n/a | Static portfolio page |
| 8 | Aesthetic and minimal | 3 | Badges are the only loud element |
| 9 | Error recovery | n/a | No errors to recover from |
| 10 | Help | n/a | Static portfolio page |
| **Total** | | **21/28** | **Good (75%)** |

## What is working

- The header is thin: about 150 units tall, so the intro line and the highlights are visible without scrolling at 1440 px.
- Section icons give the page rhythm and echo the header bar colour without adding weight.
- Skills as a two-column table of four labelled rows stays inside 375 px; badges wrap onto a second line and nothing is clipped.

## Priority issues

- **[P3] Skill badges are 20 px tall with about 11 px text.** Known limit of shields.io flat badges; not fixable here. The same words are not repeated as text, so the badge alt text is the accessible copy.
- **[P3] Dark theme: the black label half of the four certification badges merges with the `#0d1117` page**, so the left edge of each badge disappears. The text stays white on black and readable. Changing `labelColor` would change the light theme as well; left as is.
- **[P3] Skill row labels sit a few pixels lower than the first badge on desktop** (baseline alignment of an inline image against 16 px text). Cosmetic; left as is to keep the markup minimal.

No P0, P1 or P2 issues.

## Persona red flags

- **Casey (mobile, 375 px):** header name about 12 px, badges 11 px text; both readable but at the floor. Rows wrap without clipping and no horizontal scroll (375/375).
- **Sam (accessibility):** header has alt text; icons are decorative (`alt=""`, 20 px); every badge has descriptive alt text; text contrast checked by the header test (name) and GitHub link colours.
- **Jordan (recruiter skim):** reads name, role, availability, three highlights within the first screen at 1440 px.

## Minor observations

- Dark theme icon red (`#d4153b`) is dimmer than the badge red on `#0d1117` (3.6:1 icon contrast, above the 3:1 rule).
- Long LinkedIn label wraps at 375 px; link text is fixed by the wording rules.

## Questions to consider

- Would one wider-spaced row of skill names as text read better than 25 badges, if the badge size becomes a concern?

## Fixes made

Fix round 1 (controller ruling): all 25 skill badges are now one uniform 2b2b31 chip; only the logo carries colour (white for Wireshark, Python and C++, whose brand colours are under 3:1 on 2b2b31), badges without a logo are single-segment so there is no empty label stub, and row labels got `valign="middle"`. This removes the rainbow, so the P3 on heavy badges is now only the 11 px text limit.

Otherwise none needed for the critique. Two controller-ruled fixes were made first: header `<img>` alt is now "Nuno Gonçalves, offensive security." and the double blank line in Contact is gone.

Questions skipped: fewer than 3 priority issues rated above P3 (3 P3 notes, none blocking).
