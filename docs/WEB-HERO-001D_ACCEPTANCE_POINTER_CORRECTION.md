# WEB-HERO-001D acceptance pointer — provenance correction

**Raised by:** WEB-005 / MER-93 during precondition verification
**Class:** evidence / provenance defect
**Scope:** pointer only. **No accepted Product or Science semantics change, and nothing about what
was accepted changes.**

## The defect

`tasks/WEB-005_CINEMATIC_HERO.md` §2 cites the terminal Product acceptance for WEB-HERO-001D as:

```
e95fdcac7cac82e597d40dab4cdc96ce1a6b319e:tasks/WEB-HERO-001D_TERMINAL_PRODUCT_ACCEPTANCE.md
```

That path does not exist at that commit. `git cat-file` resolves the commit, but the tree at
`e95fdca` contains no `tasks/WEB-HERO-001D_TERMINAL_PRODUCT_ACCEPTANCE.md`.

## What is actually true

The acceptance record was published **one commit later** on the same branch:

| | |
| --- | --- |
| Branch | `feat/web-hero-001-predata-scene` |
| Accepted implementation HEAD | `93e17f6293aeb8bdc882dfd28221ed786b772df1` |
| Accepted REVIEW_READY / evidence HEAD | `e95fdcac7cac82e597d40dab4cdc96ce1a6b319e` |
| **Acceptance record actually lives at** | **`573f4f10cbe397e8f3bdf6611deea5cd2660dcae:tasks/WEB-HERO-001D_TERMINAL_PRODUCT_ACCEPTANCE.md`** |

`573f4f1` is a documentation-only commit. Verified with `git show --stat`:

```
573f4f1 docs(web-hero-001d): publish terminal Product acceptance
 tasks/WEB-HERO-001D_TERMINAL_PRODUCT_ACCEPTANCE.md | 38 ++++++++++++++++++++++
 1 file changed, 38 insertions(+)
```

It adds that one file and changes nothing else, so the accepted *implementation content* at
`e95fdca` is byte-for-byte unaffected by it. The acceptance record itself names `e95fdca` as the
accepted evidence HEAD, which is consistent with the task authority.

## Why this is not a `WAITING_DOMAIN_DECISION`

The task places "evidence and publication defects" inside implementation/E&D, and reserves a stop
for conflicting *authorities*. There is no conflict here: both documents agree on what was accepted
and at which HEAD. Only the path in one citation is wrong, by one commit.

## What WEB-005 did

1. **Consumed exactly what the task instructed.** The hero production workspace was taken from
   `e95fdcac7cac82e597d40dab4cdc96ce1a6b319e` with
   `git checkout e95fdcac7cac82e597d40dab4cdc96ce1a6b319e -- hero/`, and provenance is retained to
   that commit throughout — in `hero/config/lane.json`, in the production scene's own description,
   in `hero/evidence/production_media.json`, in `index.html`, and in the review evidence.
2. **Cited the acceptance record where it exists**, at `573f4f1`, wherever the acceptance decision
   itself is referenced.
3. **Recorded both pointers machine-readably** in `hero/config/lane.json`
   (`consumed_hero_evidence_head`, `consumed_hero_implementation_head`,
   `consumed_hero_acceptance_record`), so a later phase resolves them without re-deriving this.
4. **Did not edit the published task authority.** Correcting the citation inside
   `tasks/WEB-005_CINEMATIC_HERO.md` is a Product edit to a Product-owned document, not an
   implementation change, so the defect is published here instead.

## Recommended Product action (not blocking)

Amend the citation in `tasks/WEB-005_CINEMATIC_HERO.md` §2 from `e95fdca` to `573f4f1` for the
acceptance-record path only. The accepted implementation HEAD and accepted evidence HEAD in that
section are correct and must stay as they are.
