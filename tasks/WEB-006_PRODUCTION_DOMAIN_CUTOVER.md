# WEB-006 — Production Release, Vercel Verification & Domain Cutover

**Linear:** MER-95
**State:** READY_FOR_CTO_APPROVAL — DO NOT START EXECUTION
**Owner:** Product & Software
**Repository:** `mertkaanakgunlu-debug/orbgss-website`
**Exact accepted release candidate:** `feat/web-005c-public-domain-taxonomy-parity@79cc2cb82a4542461cbbfc1d0c349cf02b861084`
**Current main:** `00af0f232a8d7d77f5ca61d758461ff7316ba151`
**Ancestry:** release candidate is a direct fast-forward descendant of current main (ahead 25 / behind 0)
**Target canonical hostname:** `https://orbgss.com`
**Registrar / DNS host:** Squarespace-managed DNS unless separate CTO authority changes it.

## 1. Outcome

Publish the exact accepted OrbGSS website release candidate through the existing authorized Vercel deployment path, verify it end-to-end, then—only after a separate deliberate CTO DNS approval—cut over `orbgss.com` and `www.orbgss.com` without disturbing mail or unrelated DNS services.

WEB-006 is release/deployment/cutover work only. It does not redesign or materially change the accepted website.

## 2. Immutable release identity

The only accepted website source for this launch is:

`79cc2cb82a4542461cbbfc1d0c349cf02b861084`

Do not:
- reconstruct the release from stale `main`;
- cherry-pick selected commits;
- squash/rebase/amend accepted commits;
- rebuild a semantically different tree;
- substitute the legacy upstream repository.

Any code/content/media defect discovered during launch returns to a bounded code branch/review; WEB-006 pauses.

## 3. Phase A — read-only release preflight

Before any production mutation:

1. verify the accepted branch and exact SHA are still present remotely;
2. run or confirm the accepted site/hero/WEB-005/WEB-005B/WEB-005C validator set against that exact tree;
3. resolve the live Vercel team/project identity from authoritative runtime state;
4. identify the current Vercel production-branch/deployment policy and existing domain associations;
5. identify whether exact-SHA preview deployment and later promotion are supported without rebuilding different bytes;
6. verify `contact@orbgss.com` ownership/deliverability for the existing CONTACT_RELEASE_GATE;
7. capture the complete current DNS before-state relevant to apex, `www`, MX, SPF, DKIM, DMARC, CAA/HTTPS, verification and unrelated records;
8. record rollback values before any DNS write.

### Vercel identity observation

The Vercel connector available to Product during planning currently exposes team
`team_ZBzlro6Nug9yaS7vTB5NHsuV` / `baranitu18-9783`, but returns **zero projects**.

Therefore:
- do not guess a project ID, team binding or deployment URL from historical chat names;
- resolve the actual Vercel project/team from the authorized local Vercel session, `.vercel/project.json` if present outside Git, Vercel CLI, or the Vercel dashboard;
- if the correct existing project cannot be resolved without new credentials/admin access, STOP and request CTO action.

This is an environment/authentication preflight issue, not authority to create a replacement Vercel project.

## 4. Release integration policy

Because the accepted release candidate is a pure fast-forward descendant of current `main`, no merge commit is needed.

Preferred release path:
1. deploy/verify the exact accepted candidate as a Vercel preview or equivalent immutable deployment;
2. prove deployment source identity equals `79cc2cb...`;
3. run the production-candidate smoke suite;
4. only at the deliberate production gate, use the live Vercel configuration to choose the minimal path that preserves exact source identity:
   - promote the already-verified exact deployment when supported; or
   - fast-forward `main` to the exact accepted release candidate if the project requires the production branch to be main.

Do not fast-forward `main` early if doing so would auto-deploy production before the human production gate.

No merge commit, squash or rebase is authorized.

## 5. Production-candidate smoke

Before DNS cutover, verify the deployed candidate over HTTPS:

- source/deployment provenance binds to exact accepted SHA;
- homepage hero playback, poster, reduced-motion and mobile fallback;
- real Kızıldere context;
- Terrain / Thermal / Alteration Evidence selector;
- Priority/Result presentation;
- Geothermal / Mining / Marine homepage card routing;
- legacy `#mineral` / `#environment` anchors;
- EN/TR behavior;
- routes:
  - `/`
  - `/platform/`
  - `/solutions/`
  - `/pilot/`
  - `/company/`
  - `/contact/`
- 404 behavior;
- no broken assets or console-blocking failures;
- WebM / MP4 / WebP / poster content types;
- intended long-lived cache headers for `/assets/*`;
- security headers declared in `vercel.json`;
- representative desktop/mobile visual smoke;
- canonical/metadata/robots/sitemap behavior appropriate for launch.

If deployment output differs visually or behaviorally from the accepted candidate, STOP; do not compensate through ad-hoc production edits.

## 6. Deliberate production + DNS human gate

No production promotion that makes the release publicly canonical, and no DNS write, occurs without explicit CTO approval after Phase A/pre-production smoke is presented.

The approval package must show:
- exact deployment URL/ID;
- exact source SHA;
- resolved Vercel project/team identity;
- production-branch/promotion behavior;
- current `orbgss.com` / `www` web records;
- exact Vercel-required new records;
- preserved mail/security/verification records;
- rollback values;
- CONTACT_RELEASE_GATE result.

## 7. DNS cutover contract

At the approved cutover:

- change only web-serving records required for apex and `www`;
- preserve MX, SPF, DKIM, DMARC, CAA/HTTPS, domain verification and unrelated records;
- keep Squarespace as registrar/DNS host unless separately authorized;
- target `https://orbgss.com` as canonical;
- configure `www` to permanently redirect to apex;
- do not change nameservers, DNSSEC, mail provider, billing/plan, credentials or unrelated records without separate CTO approval.

If Vercel requires a broader mutation than this contract permits, STOP.

## 8. Post-cutover acceptance

After propagation, verify:
- apex HTTPS valid;
- `www` redirects permanently to apex;
- all six routes load;
- assets/media load with correct MIME/cache behavior;
- EN/TR works;
- no certificate/mixed-content/console-blocking error;
- contact path works and mail gate remains intact;
- DNS records not in cutover scope remain unchanged;
- production deployment still resolves to the accepted release identity.

Capture post-state and rollback evidence.

## 9. Genuine STOP conditions

STOP and return for CTO/Product action if:
- correct Vercel project/team cannot be resolved;
- credentials/admin access is required;
- project creation, paid-plan change or billing action is required;
- exact accepted deployment source cannot be proven;
- current production behavior would require rewriting accepted code;
- CONTACT_RELEASE_GATE fails;
- DNS before-state or rollback values cannot be captured;
- requested DNS changes touch mail/unrelated records;
- nameserver/DNSSEC/provider migration is proposed;
- destructive/irreversible action is required;
- regression is found in the accepted website.

Routine Vercel/CLI/config discovery or reversible preview-deployment issues inside these boundaries are implementation details and do not require a new Product task.

## 10. Required evidence

Return a pre-cutover package before the CTO production/DNS gate with:
- release candidate SHA + tree identity;
- Vercel team/project/deployment IDs and URLs;
- proof of deployed source identity;
- validator + browser smoke results;
- production configuration/branch behavior;
- DNS before-state;
- exact proposed web-record delta;
- rollback plan;
- contact gate result;
- PASSED / FAILED / NOT RUN truthfully marked.

Only after explicit CTO production/DNS approval may the cutover proceed.

## 11. Terminal

WEB-006 is terminal only when:
- exact accepted release is production;
- apex + www behavior is correct;
- HTTPS/routes/assets/EN-TR pass;
- mail/unrelated DNS remain intact;
- post-state/rollback evidence is recorded.

Publication of this task does not start execution.
