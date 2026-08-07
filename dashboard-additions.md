# What else the data offers — candidate additions to the explorer

> **STATUS: BUILT.** Tiers 1–3 below have been added to the explorer (waves 4–9), with the harm theme as the metric selector and response categories as items. Low-base series are included (as requested, to track going forward) and flagged with ⚠. The explorer now has 13 question blocks / ~11,260 estimates. See the summary at the bottom.


The tracker has a large set of **follow-up questions** asked of people who experienced a harm. Each repeats the harm list, so there's a scams / deepfakes / impersonation / misinformation slice of every one. Below is what's available and worth adding, ranked by how robust the base sizes are.

**One structural caveat that drives everything:** most follow-ups (frequency, platform, actions, reasons) are asked about a *single harm sampled per respondent*, not every harm they experienced. So per-harm bases are far smaller than the headline "experienced" numbers — e.g. in Wave 9 the scams follow-up base is ~514, deepfakes ~320, misinformation ~911, impersonation ~51. They're reliable at **Total level**, shaky for subgroup splits, and impersonation is often too thin to report.

## Tier 1 — strong bases, add now

These have large bases and add real analytical value:

- **Q9 — "most recent" harm** (base ~4,800; all who hit any harm). Share of people whose *most recently encountered* harm was each in-scope type. W9: misinformation 18.7%, scams 10.4%, deepfakes 6.6%, impersonation 1.1%. A good "salience" measure to sit alongside raw prevalence, and trendable across waves.
- **Q32a1 — type of misinformation** (base ~3,100). Mirrors the Q32 scam-type breakdown we already added. W9: **political/electoral 40.4%**, conflict 12.6%, discrimination 11.4%, health 7.2%. Highly policy-relevant and a strong base.
- **Q32a — source of misinformation** (who it came from: public figure, official body, someone known, etc.) — same solid base as the misinformation module.

## Tier 2 — Total-level only, add with base caveats

Genuinely interesting, but report at Total (and at most gender) with the small-base flag, not fine subgroups:

- **Q21 — where the harm was encountered** (site/service type). W9 scams: **email 50.7%**, social media 19.4%, messenger 5.8%, search 4.0%. Deepfakes/misinformation would skew very differently (more social/video) — a strong story about *channel*.
- **Q12 — frequency** (once → 10+ times in 4 weeks). W9 scams: 2–3 times 35.7%, once 21.4%, **10+ times 17.4%** — i.e. a chunk see scams very frequently. A repeat-exposure measure per harm.
- **Q15 — actions taken** when they saw it (reported, blocked, ignored, told someone…). Multi-select; shows whether people act on scams/deepfakes.
- **Q16 — reasons for taking no action** (didn't know how, didn't think it'd help, etc.). Barriers to reporting.

## Tier 3 — topical but thin / situational

Available, but bases are small or the question only applies to a sub-channel:

- **Q30 — which generative-AI tool** the harm came from (ChatGPT, Gemini, Snapchat My AI…). Very on-topic for deepfakes/misinformation, but only asked of the small group who encountered it via a genAI tool — tiny base. Worth watching as it grows.
- **Q22–Q29 — specific platform** within a channel (which social app, which messenger, which search engine…). Granular, but bases fragment quickly.
- **Q17/Q18 — reporting outcome & satisfaction** with the complaints process. Small base (only those who reported).

## Tier 4 — whole-sample attitudes (not harm-specific, but in-theme)

- **Q46 — confidence in the Online Safety Act** keeping people safe (full sample; trendable). Policy-relevant context for the scams/harms story.
- **Q34 — had your own content wrongly taken down** (full sample).

## Suggested next step

Add **Tier 1 now** (misinformation type + source, and the "most recent harm" measure) since they're robust and high-value, and add **Tier 2 as Total-level series** with the existing small-base flagging. That roughly doubles what the team can explore — adding the *what type, where, how often, and what people did about it* dimensions on top of the current concern/experience/scam-detail views — without overstating thin numbers.

Tell me which tiers you want and I'll fold them into `estimates_long.csv` and the explorer (the explorer auto-detects new questions, so it's mostly pipeline work).

## What was built (all tiers, waves 4–9)

In the explorer, pick one of the new **Question** blocks, then use the **Metric** dropdown to choose the harm (Scams / Deepfakes / Misinformation / Impersonation), and the **Item** dropdown for the response category:

- **Most recent harm (Q9)** — share whose most-recent harm was each in-scope type. Full subgroups (good base).
- **Misinformation: type (Q32a1)** and **source (Q32a)** — strong base (~2,600+).
- **Frequency seen (Q12)** — once → 10+ times, per harm.
- **Where encountered (Q21)** — channel (email, social, search, messenger…), per harm.
- **Actions taken (Q15)** — 23 actions (reported, blocked, told someone…), per harm.
- **Reasons for no action (Q16)** — 16 reasons, per harm.
- **Reporting outcome (Q17)** and **Reporting satisfaction (Q18)** — small base, flagged.
- **GenAI tool involved (Q30)** — which AI tool the harm came from; very small base now, flagged, useful to watch as it grows.

**Base caveat:** the per-harm follow-ups (everything except Q9 and the misinformation modules) are asked about a single sampled harm per person, so Total-level only and often small — they're shown with ⚠ flags and should be read as indicative, especially impersonation (frequently <50) and Q30. These are included deliberately so the team can track them going forward.

All new figures were spot-checked against direct weighted calculations (e.g. scams encountered via email 50.7%, misinformation that is political/electoral 40.4%, most-recent-harm shares) and match.

## Second batch added (Q14, Q22–Q29, attitudes)

Now also in the explorer — **26 question blocks, ~26,400 estimates** total:

- **Impact: how bothered (Q14b)** — share who were "really bothered/found it offensive", per harm. A genuine harm-severity measure (e.g. deepfakes "really bothered" runs ~25%→17% across waves). Reasonable base.
- **Who it was directed at (Q14c)** — at me / someone close / someone I don't know, per harm.
- **Specific platform used (Q22–Q29)** — which video app / search engine / social app / livestream / messenger / gaming platform / Q&A site / file-sharing service the harm was experienced on, per harm. Breakdown bars are capped to the top 15 in the explorer; full lists remain in the data/table.
- **Online Safety Act: knowledge (Q45)** and **confidence (Q46)** — full sample, full subgroups, trendable. Policy context.
- **Own content taken down (Q34)** — full sample.

**Heavy base caveat on the platform specifics (Q22–Q29 and Q30).** These are a subset of a subset (experienced *this* harm, *and* on *this* channel type, *and* on *this* specific app), so most cells are tiny — several max out in single digits (file-sharing, gaming, Q&A, search, genAI tool). They're included purely so the team can **watch them build over future waves**; today they're indicative at best and almost all carry the ⚠ small-base flag. The more usable ones are social app (Q24), messenger (Q26) and video app (Q22). Q32b is already fully covered by the Scams detail (Q32) block; its `_rc` (email-excluded) recodes were left out to avoid double-counting.
