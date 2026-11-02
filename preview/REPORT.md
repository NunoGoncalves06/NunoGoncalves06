# Profile preview and verification report

Branch `design/quiet-signal` (Quiet Signal restyle on top of `profile-refresh`). Nothing is pushed or edited on GitHub. Site column: `portfolio/src/data.ts`, `App.tsx` and the live bundle (https://nunogoncalves06.github.io, `assets/index-BKs1rZvI.js`), where every data.ts string used below was found by exact match.

## 1. Fact comparison: site vs GitHub

| Fact | Site | GitHub | Status |
|---|---|---|---|
| Name | Nuno Gonçalves (h1, App.tsx) | Header SVG title and alt text | equal |
| Hero title | Offensive security | Header SVG title | equal |
| Hero line | Informatics Engineering student at ISEP, Porto. Looking for a curricular internship from February to June 2027. | Same sentence in the opening paragraph (the header no longer repeats it) | equal |
| Highlight 1 | CCNA certified / Cisco, August 2026 | CCNA certified, Cisco, August 2026 | equal |
| Highlight 2 | 8th of 300+ teams / upCTF 2026, my first CTF | 8th of 300+ teams, upCTF 2026, my first CTF | equal |
| Highlight 3 | Junior top 10 / National bootcamp, National Cybersecurity Centre, 2026 | Junior top 10, National bootcamp, National Cybersecurity Centre, 2026 | equal |
| Badge CCNA | Credly badge: CCNA, Cisco, Aug 2026, links to the Credly record | Shield 'CCNA certified', links to the same Credly record | equal |
| Badge IELTS | Training list: IELTS Academic, English at C1 | Shield 'IELTS Academic English C1' | equal |
| Badge CEH | 'Certified Ethical Hacker v13', training completed at ISEP Academy | Shield 'CEH v13 training completed' | differs (abbreviated name; never says certified, so rule-safe) |
| Badge AWS | 'AWS Cloud Practitioner', training completed at ISEP Academy | Shield 'AWS Cloud Practitioner training completed' | equal |
| Other Credly badges | Endpoint Security, Enterprise Networking Security and Automation, Switching Routing and Wireless Essentials, Introduction to Networks | Not on the profile | differs (four site badges absent on GitHub) |
| Project: Three-site enterprise network | The CCNA 3 final project ... It got the maximum score. Stack chips: Cisco IOS, OSPF, IPsec, ACLs, Ansible | Same summary; line 'Cisco IOS, OSPF, IPsec VPN, ACLs, NAT, port security and Ansible. The repository is private.' | differs (stack line adds VPN, NAT, port security from the site detail text, plus the private note) |
| Project: AISafe | A flight control management prototype ... security clearances. | Same summary, plus a paragraph 'Worked on every part of the project with my team ... The repository is private, so there is no link.' | differs (extra paragraph not on the site) |
| Project: IoT sensor node | An ESP32-C6 board with a distance sensor ... with my group. | Same | equal |
| Project: SpotCast | An Android app for Mobile Application Development at Aarhus University ... API clients. | Same, linked to the repo | equal |
| Project: Wakecast | An alarm that reads you a morning briefing ... no tracking. | Same, linked to the repo | equal |
| Projects: All Aboard, Sueca (More) | One-sentence summaries | Same wording, as bullets under 'More' | equal |
| Project: Alchemist's Arsenal | Not on the site (absent from data.ts and the live bundle) | Bullet 'Alchemist's Arsenal. Unity game in C#, built on my own.' with repo link | differs (project present only on GitHub) |
| Project order | Network, SpotCast, Wakecast, AISafe, All Aboard, Sueca, IoT | Network, AISafe, IoT, SpotCast, Wakecast, then More | differs (ACCEPTED: project order) |
| Skills: Security | Kali Linux, Nmap, Wireshark, Burp Suite, Hydra, Ghidra | Same | equal |
| Skills: Networks | Cisco IOS, VLANs and STP, OSPF, NAT and ACLs, IPsec VPN, Ansible | Same | equal |
| Skills: Code | Java, C, Python, Kotlin, C++, C# | Same | equal |
| Skills: Platforms | Linux, Docker, Git and GitLab, Android, AWS fundamentals | Same | equal |
| Contact: email | nunogoncalves070906@gmail.com | Same, mailto link | equal |
| Contact: LinkedIn | Label www.linkedin.com/in/nunogonçalves070906 | Same label; href percent-encoded, as a browser encodes the site link | equal |
| Contact: Credly | credly.com/users/nuno-goncalves.ad1fc5dd | Same | equal |
| Contact: GitHub | github.com/NunoGoncalves06 link | Not listed (the profile is on GitHub) | differs (site-only link) |
| Contact: CV | Download CV (PDF) | Not listed | differs (site-only item) |
| Site link | https://nunogoncalves06.github.io | Same, in the intro and in Contact | equal |
| About section | CHAØS, NEI-ISEP, teaching, scouts and volunteering | Not on the profile | differs (site-only section) |
| Repo description: SpotCast | Site summary: 'An Android app ... Go, Maybe or Skip ... with unit tests ...' | 'Android app in Kotlin: save outdoor spots and get a Go, Maybe or Skip for each activity from the forecast.' | differs (shortened for the one-line field) |
| Repo description: Wakecast | Site summary: 'An alarm that reads you a morning briefing ... no account and no tracking.' | 'Android alarm that reads a morning briefing when you dismiss it: weather, calendar, to-dos, news. No account.' | differs (shortened; drops 'no tracking') |
| Repo description: site repo | Hero: Offensive security; Informatics Engineering student at ISEP | 'Personal website of Nuno Gonçalves, offensive security student at ISEP' | differs (paraphrase, no site equivalent) |
| Repo description: alchemists-arsenal | Not on the site | 'Unity game in C#, built on my own.' | differs (same source as the README bullet) |
| Repo homepage | Site URL | Site URL on 4 repos (SpotCast, Wakecast, site repo, profile repo) | equal |

Only the project order is an accepted difference. Every other row marked differs is a decision for Nuno: approve it as deliberate or have the profile aligned with the site. The biggest ones: Alchemist's Arsenal appears only on GitHub, AISafe has an extra paragraph, the Three-site stack line is longer, and four Credly badges, the GitHub and CV links and the About section are site-only.

## 2. Link check

`curl -s -o /dev/null -w "%{http_code}" -L --max-time 30 <url>` on every URL in README.md, repo-changes.json and repo-readmes/*.md. mailto links are not curled. No link points to a private repo.

| Code | URL | Result |
|---|---|---|
| 200 | https://github.com/NunoGoncalves06/SpotCast | ok |
| 200 | https://github.com/NunoGoncalves06/Wakecast | ok |
| 200 | https://github.com/NunoGoncalves06/alchemists-arsenal | ok |
| 200 | https://nunogoncalves06.github.io | ok |
| 200 | https://www.credly.com/badges/8c053a69-a852-435b-9cd2-595bfd291f4f | ok |
| 200 | https://www.credly.com/users/nuno-goncalves.ad1fc5dd | ok |
| 999 | https://www.linkedin.com/in/nunogon%C3%A7alves070906 | bot-blocked, manual check (LinkedIn answers 999 to bots) |
| 200 | 29 shields.io badge URLs (4 certification, 25 skill, style=flat). Skill badges are one quiet chip each: `badge/-<item>-2b2b31?style=flat&logo=<slug>&logoColor=<brand hex or white>` with a logo, `badge/<item>-2b2b31?style=flat` without | all ok (curl --max-time 60); all 13 logo badges return an SVG with an embedded image, the 12 without a logo have none |

## 3. Tests and checker

`python -m pytest -q`: 46 passed. `python check_readme.py README.md ../portfolio/src/data.ts` printed nothing and exited 0.

## 4. Exact change list

### 4.1 `apply_repo_changes.py --dry-run` (verbatim, nothing applied)

```
gh repo edit NunoGoncalves06/SpotCast --description "Android app in Kotlin: save outdoor spots and get a Go, Maybe or Skip for each activity from the forecast." --homepage https://nunogoncalves06.github.io --add-topic android --add-topic kotlin --add-topic jetpack-compose --add-topic firebase --add-topic ktor --add-topic openstreetmap
gh repo edit NunoGoncalves06/Wakecast --description "Android alarm that reads a morning briefing when you dismiss it: weather, calendar, to-dos, news. No account." --homepage https://nunogoncalves06.github.io
gh repo edit NunoGoncalves06/NunoGoncalves06.github.io --description "Personal website of Nuno Gonçalves, offensive security student at ISEP" --homepage https://nunogoncalves06.github.io --add-topic portfolio --add-topic react --add-topic tailwindcss --add-topic offensive-security
gh repo edit NunoGoncalves06/alchemists-arsenal --description "Unity game in C#, built on my own." --add-topic unity --add-topic csharp --add-topic game
gh repo edit NunoGoncalves06/NunoGoncalves06 --homepage https://nunogoncalves06.github.io
```

### 4.2 Profile repo files to push (`git diff --stat cf080cb..HEAD`, `preview/` excluded)

```
```

The push also deletes `.github/workflows/metrics.yml`, `metrics.terminal.svg`, `assets/header.svg` and `assets/make_header.py` (replaced by the two headers, four section icons, `make_header.py` and `make_icons.py`). Preview HTML is not part of the push.

### 4.3 README splices in other repos (files in `repo-readmes/`)

- NunoGoncalves06.github.io: replaces the WHOLE README (the unmodified Vite template, from "# React + TypeScript + Vite" to the last heading).
- SpotCast: replaces from the "# SpotCast" title through the two intro paragraphs, stopping before the `<p align="center">` demo GIF block (just before "## Try it"). The new text also adds a package-name line and a portfolio link line.
- Wakecast: replaces from the "# Wakecast" title through the two intro paragraphs, stopping before the `<p align="center">` screenshot block (just before "## What you hear"). The new text adds a portfolio link line.

### 4.4 Pinned repos Nuno sets by hand

SpotCast, Wakecast, NunoGoncalves06.github.io.

## 5. Screenshots

Files from `preview/shoot.py` (headless Edge, `<details>` forced open in the preview HTML only): `preview/shots/light-1440.png`, `dark-1440.png`, `light-375.png`, `dark-375.png`. Edge headless will not lay out narrower than about 492 px, so each page sits in an iframe of the exact width.

| Shot | scrollWidth | innerWidth | Result |
|---|---|---|---|
| light 1440 | 1440 | 1440 | OK |
| light 375 | 375 | 375 | OK |
| dark 1440 | 1440 | 1440 | OK |
| dark 375 | 375 | 375 | OK |

All four were read by eye. Nothing is cut at 375 px. The smallest text on the phone is the header name at 28 SVG units scaled by 345/800, about 12.1 px; body text is 16 px. Skill badges are 20 px shields with about 11 px text, a known shields.io limit. Critique: `preview/CRITIQUE-quiet-signal.md`. The controller should still confirm in the browser pane.
