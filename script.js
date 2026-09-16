/* OrbGSS — minimal vanilla JS: navigation, Solutions dropdown, EN/TR language switch, image-failure handling. */

/* ------------------------------------------------------------------ */
/* Translations. Keys map to data-i18n* attributes in index.html.      */
/* data-i18n        -> textContent                                     */
/* data-i18n-html   -> innerHTML (static, trusted strings with <br />) */
/* data-i18n-alt / -aria-label / -content / -href -> that attribute     */
/* ------------------------------------------------------------------ */
const MAIL_EN = 'mailto:contact@orbgss.com?subject=OrbGSS%20Partnership%20Inquiry';
const MAIL_TR = 'mailto:contact@orbgss.com?subject=OrbGSS%20%C4%B0%C5%9F%20Birli%C4%9Fi%20Talebi';
const MAIL_PILOT_EN = 'mailto:contact@orbgss.com?subject=OrbGSS%20Pilot%20Inquiry';
const MAIL_PILOT_TR = 'mailto:contact@orbgss.com?subject=OrbGSS%20Pilot%20Talebi';
const MAIL_TECH_EN = 'mailto:contact@orbgss.com?subject=OrbGSS%20Technical%20Inquiry';
const MAIL_TECH_TR = 'mailto:contact@orbgss.com?subject=OrbGSS%20Teknik%20G%C3%B6r%C3%BC%C5%9Fme%20Talebi';

const I18N = {
  en: {
    'meta.title': 'OrbGSS — Geospatial Intelligence',
    'meta.description': 'OrbGSS turns Earth observation and geoscience data into evidence-backed spatial priorities that help teams decide where to investigate next.',
    'meta.ogDescription': 'Know where to look next. Earth data, evidence, priority.',
    'a11y.skip': 'Skip to content',
    'nav.brand': 'OrbGSS home',
    'nav.primary': 'Primary navigation',
    'nav.footer': 'Footer navigation',
    'nav.open': 'Open navigation',
    'nav.close': 'Close navigation',
    'nav.language': 'Language',
    'nav.platform': 'Platform',
    'nav.solutions': 'Solutions',
    'nav.pilot': 'Pilot',
    'nav.company': 'Company',
    'nav.contact': 'Contact',
    'nav.geothermal': 'Geothermal Exploration',
    'nav.mineral': 'Mineral Exploration',
    'nav.environment': 'Environmental & Land Intelligence',
    'mail.partner': MAIL_EN,
    'hero.eyebrow': 'Earth data. Evidence. Priority.',
    'hero.title': 'Know where to look next.',
    'hero.copy': 'OrbGSS turns Earth observation and geoscience data into evidence-backed spatial priorities that help teams decide where to investigate next.',
    'hero.cta': 'See the pilot area',
    'hero.secondary': 'Partner With Us',
    'story.observe.title': 'Observe',
    'story.observe.statement': 'Every OrbGSS analysis starts from one area of interest. The Kızıldere pilot AOI is a 36 × 36 km frame on a fixed 30 m grid, and every layer that follows is registered to exactly this ground.',
    'story.observe.note': 'Source and AOI context only — not validation evidence.',
    'story.observe.meta': 'AOI · EPSG:32635 · 30 m · 36 × 36 km',
    'story.terrain.title': 'Terrain',
    'story.terrain.statement': 'Elevation gives the area its physical shape. NASADEM terrain is carried as display context, so every later signal can be read against real relief.',
    'story.terrain.note': 'Context and display only. Terrain is not a scored predictor and carries no universal geothermal-favourability direction.',
    'story.terrain.meta': 'Context · NASADEM elevation · metres',
    'story.evidence.title': 'Evidence',
    'story.evidence.statement': 'Three accepted remote-sensing layers describe the same ground: one Landsat thermal anomaly and two Sentinel-2 spectral alteration proxies. Switch between them to see what each one contributes.',
    'story.evidence.note': 'Evidence layers only — candidate and unvalidated. THM-01 is thermal evidence, not geothermal probability, reserve or resource, discovery or drilling-success evidence. ALT-01 and ALT-02 are broad spectral alteration proxies, never mineral or kaolinite identification, and not proof of hydrothermal alteration.',
    'story.evidence.meta': 'Evidence · THM-01 / ALT-01 / ALT-02',
    'evidence.switchLabel': 'Evidence layer',
    'story.structure.title': 'Structure',
    'story.structure.statement': 'Structural and geological context would sharpen interpretation here. For this baseline OrbGSS has no public-safe fault or lithology layer, so the page shows the gap rather than filling it.',
    'story.structure.note': 'Structure and geology are optional support and score-invariant. Their absence does not change the remote-sensing priority baseline.',
    'story.structure.meta': 'Optional support · Not published',
    'structure.gapMark': 'Data gap',
    'structure.gapCopy': 'No fault or lithology layer is published for this area. Nothing is drawn here on purpose: an invented structural line would look like evidence and would not be.',
    'structure.gapMeta': 'Structural context — optional support / data gap',
    'story.priority.title': 'Priority',
    'story.priority.statement': 'The thermal and alteration evidence is integrated into one within-AOI ranking surface, 0 to 100, so a team can order where to look first.',
    'story.priority.note': 'AOI-relative experimental screening only. Not probability, reserve or resource estimation, discovery likelihood, drilling-success likelihood, Full Prospectivity, or a score calibrated across areas.',
    'story.priority.meta': 'Score · mvp_remote_sensing_priority_v1',
    'story.geothermal.title': 'Geothermal',
    'story.geothermal.statement': 'Kızıldere is the first geothermal application of that baseline: the priority surface over NASADEM relief, in an active pilot area in Denizli, Türkiye.',
    'story.geothermal.note': 'First-application proof, not field validation, discovery, reserve or resource, drilling-target or drilling-success proof.',
    'story.geothermal.meta': 'First application · Kızıldere pilot',
    'scene.kind.naturalColor': 'Natural-color composite',
    'scene.aoi.place': 'Kızıldere, Denizli, Türkiye',
    'scene.aoi.coords': '37.9794° N, 28.7907° E',
    'label.observe': 'Kızıldere AOI — accepted MVP project context',
    'label.terrain': 'Elevation — NASADEM context',
    'label.thm01': 'THM-01 Thermal Anomaly',
    'label.alt01': 'ALT-01 Alteration Proxy — clay/hydroxyl',
    'label.alt02': 'ALT-02 Alteration Proxy — ferric/iron',
    'label.priority': 'Remote-Sensing Relative Priority — Experimental Baseline',
    'label.geothermal': 'Kızıldere — first geothermal application of the experimental remote-sensing baseline',
    'alt.observe': 'Greyscale elevation map of the 36 by 36 kilometre Kızıldere project area of interest, showing ridges and valleys across the pilot grid',
    'alt.terrain': 'Colour elevation map of the Kızıldere area of interest, with low ground in dark blue and high ridges in pale yellow',
    'alt.thm01': 'Diverging thermal anomaly map of the Kızıldere area of interest, with cooler ground in blue and warmer ground in red',
    'alt.alt01': 'Sequential map of the clay and hydroxyl spectral alteration proxy across the Kızıldere area of interest',
    'alt.alt02': 'Sequential map of the ferric iron spectral alteration proxy across the Kızıldere area of interest',
    'alt.priority': 'Relative priority map of the Kızıldere area of interest, ranking ground from 0 to 100 within the area',
    'alt.geothermal': 'Relative priority surface over shaded NASADEM relief across the Kızıldere geothermal pilot area',
    'hero.handoff.kicker': '04 · Result',
    'hero.handoff.cta': 'See how it was derived',
    'act.context.kicker': '02 · The place',
    'act.context.title': 'A real area, before any analysis.',
    'act.context.copy': 'Kızıldere sits in the Büyük Menderes graben in Denizli, Türkiye. This is the area as Landsat 8 photographed it — the ground the whole pilot is registered to, before a single layer is derived from it.',
    'act.context.note': 'Earth-observation context only. This is a natural-colour photographic composite of the area, not analytical evidence, not a scored input, and not the acquisition date of any THM or ALT evidence layer.',
    'act.context.meta': 'Landsat 8 OLI · 2025-05-05 · 30 m · natural colour',
    'act.evidence.kicker': '03 · The evidence',
    'act.evidence.title': 'Three layers over the same ground.',
    'act.evidence.copy': 'Relief for context, one Landsat thermal anomaly and one Sentinel-2 alteration proxy as evidence. Same area of interest, same 30 m grid, same story stage — which is what makes them comparable at all.',
    'act.evidence.listLabel': 'Evidence layers',
    'act.evidence.terrain.role': 'Context',
    'act.evidence.thermal.role': 'Evidence',
    'act.evidence.thermal.note': 'Evidence layer only. Do not describe it as geothermal probability, reserve, discovery, or drilling-success evidence.',
    'act.evidence.alteration.role': 'Evidence',
    'act.evidence.alteration.note': 'Broad Sentinel-2 spectral alteration proxy; not mineral/kaolinite identification and not proof of hydrothermal alteration.',
    'act.evidence.gapLabel': 'Data gap',
    'act.evidence.gap': 'Structural and geological evidence would sharpen interpretation here. OrbGSS has no public-safe fault or lithology layer for this baseline, so the gap is stated rather than filled — it is optional support and does not change the priority result.',
    'act.evidence.deeper': 'How the layers are built',
    'act.priority.kicker': '04 · The result',
    'act.priority.title': 'Where to look first.',
    'act.priority.copy': 'The thermal and alteration evidence is combined into one ranking surface across the area of interest, 0 to 100, so a team can order the ground instead of guessing at it. High values mean “look here before there” — inside this area, for this baseline.',
    'act.priority.note': 'AOI-relative experimental screening only. Not probability, reserve/resource estimation, discovery likelihood, drilling-success likelihood, Full Prospectivity, or a calibrated cross-AOI score.',
    'act.priority.meta': 'mvp_remote_sensing_priority_v1 · EPSG:32635 · 30 m · 36 × 36 km',
    'act.priority.deeper': 'Read the pilot method',
    'scene.hero.place': 'Kızıldere — Büyük Menderes graben, Denizli, Türkiye',
    'scene.hero.coords': '37.9794° N, 28.7907° E',
    'scene.hero.kind': 'Rendered orbital sequence — not sensor imagery',
    'scene.context.place': 'Kızıldere — Büyük Menderes graben, Denizli, Türkiye',
    'scene.context.coords': '37.9794° N, 28.7907° E',
    'scene.context.kind': 'Natural-color composite',
    'scene.priority.place': 'Kızıldere — Büyük Menderes graben, Denizli, Türkiye',
    'scene.priority.coords': '37.9794° N, 28.7907° E',
    'alt.hero': 'Rendered view from orbit of the eastern Mediterranean and western Türkiye, with a bright square acquisition frame locked over the Kızıldere pilot region',
    'alt.context': 'Natural-colour Landsat 8 view of the Büyük Menderes graben around Kızıldere, showing the valley floor, irrigated fields and the ridges on either side',
    'alt.priorityLegend': 'Colour scale for the relative priority map, running from 0 at the dark end to 100 at the pale end',
    'pilot.kicker': 'Pilot',
    'pilot.title': 'Geothermal first.',
    'pilot.copy': 'Geothermal exploration is where OrbGSS is applied first. Mineral exploration and environmental & land intelligence follow the same evidence-to-priority workflow and are expansion directions, not finished products.',
    'pilot.listLabel': 'Applications',
    'app.geothermal.title': 'Geothermal Exploration',
    'app.geothermal.status': 'Active · First application',
    'app.geothermal.copy': 'Evidence-backed prioritization of geothermal exploration areas.',
    'app.mineral.title': 'Mineral Exploration',
    'app.mineral.status': 'Expansion direction',
    'app.mineral.copy': 'The same workflow extended to mineral exploration targets.',
    'app.environment.title': 'Environmental & Land Intelligence',
    'app.environment.status': 'Expansion direction',
    'app.environment.copy': 'Land and environmental change read as spatial evidence.',
    'company.kicker': 'Company',
    'company.title': 'OrbGSS — Orbital Geo-Spatial Solutions',
    'company.copy': 'OrbGSS is a geospatial-intelligence platform built by VirgaSoft. It exists to make exploration and land decisions evidence-based, traceable and easier to prioritize.',
    'trust.kicker': 'How we work',
    'trust.provenance.title': 'Traceable provenance',
    'trust.provenance.copy': 'Every output can be followed back to its source data.',
    'trust.gaps.title': 'Explicit data gaps',
    'trust.gaps.copy': 'Missing or weak inputs are shown, not hidden.',
    'trust.evidence.title': 'Evidence-based outputs',
    'trust.evidence.copy': 'Priorities are derived from mapped evidence, with the reasoning attached.',
    'trust.decision.title': 'Decision support, not replacement',
    'trust.decision.copy': 'OrbGSS helps decide where to investigate. Field investigation remains necessary.',
    'contact.title': 'Contact',
    'contact.copy': 'For pilot, partnership and technical conversations.',
    'contact.cta': 'Partner With Us',
    'scene.crater.place': 'Crater Lake, Oregon, USA',
    'scene.crater.coords': '42.9443° N, 122.1353° W',
    'scene.yellowstone.place': 'Yellowstone National Park, USA',
    'scene.yellowstone.coords': '44.4604° N, 110.8282° W',
    'scene.chuquicamata.place': 'Chuquicamata, Antofagasta, Chile',
    'scene.chuquicamata.coords': '22.3150° S, 68.9010° W',
    'scene.ili.place': 'Ili River Delta & Lake Balkhash, Kazakhstan',
    'scene.ili.coords': '45.0600° N, 74.5200° E',
    'alt.crater': 'Satellite view of Crater Lake and the surrounding landscape in Oregon, United States',
    'alt.yellowstone': 'Satellite view of the geothermal landscape around Yellowstone National Park',
    'alt.chuquicamata': 'Satellite view of the Chuquicamata mining district in northern Chile',
    'alt.ili': 'Satellite view of the Ili River Delta and Lake Balkhash in Kazakhstan',
    'footer.builtBy': 'Built by VirgaSoft',
    'footer.attribution': 'Landsat data courtesy of the U.S. Geological Survey. The hero is an OrbGSS natural-color composite of Landsat Collection 2 surface reflectance. The story panels are OrbGSS cartographic exports of the Kızıldere pilot area, derived from NASADEM elevation, Landsat thermal and Sentinel-2 alteration evidence, with Scientific colour maps v8.0 by Fabio Crameri. Full provenance is documented in the production package.',
    'footer.copyright': '© 2026 OrbGSS. All rights reserved.',

    /* WEB-003 — deep public routes */
    'mail.pilot': MAIL_PILOT_EN,
    'mail.technical': MAIL_TECH_EN,

    'platformPage.meta.title': 'Platform — OrbGSS',
    'platformPage.meta.description': 'How OrbGSS turns an area of interest into a traceable, evidence-backed spatial priority — and where field investigation still takes over.',
    'platformPage.meta.ogDescription': 'From area of interest to spatial priority, with every step traceable.',
    'platformPage.kicker': 'Platform',
    'platformPage.title': 'How OrbGSS builds a spatial priority.',
    'platformPage.intro': 'OrbGSS takes an area of interest, brings the available inputs into one spatial frame, and turns them into a within-area priority a team can act on — with the reasoning attached at every step.',
    'platformPage.stepsTitle': 'The workflow',
    'platformPage.step1.title': 'Area of interest',
    'platformPage.step1.copy': 'Every analysis starts by fixing a boundary: a defined area on a known grid and coordinate system, so every layer that follows is registered to exactly the same ground.',
    'platformPage.step2.title': 'Source & context',
    'platformPage.step2.copy': 'Inputs are brought in from their original sources and kept traceable back to where they came from. Context layers such as terrain describe the ground; on their own, they are not evidence.',
    'platformPage.step3.title': 'Evidence',
    'platformPage.step3.copy': 'Domain-relevant signals are mapped as spatial evidence across the same area, so different indicators can be compared and read against one another on common ground.',
    'platformPage.step4.title': 'Explicit data gaps',
    'platformPage.step4.copy': 'Not every input is available everywhere. Where OrbGSS has no public-safe layer for something, the platform shows the gap rather than filling it with an inferred substitute.',
    'platformPage.step5.title': 'Integrated spatial priority',
    'platformPage.step5.copy': 'Available evidence is combined into one within-area ranking, so a team can see, in relative terms, where the ground is more or less interesting before anyone sets foot on site.',
    'platformPage.step6.title': 'Investigation decision support',
    'platformPage.step6.copy': 'The priority view is a starting point for planning field work, not a replacement for it. It helps a team decide where to look first; confirming what is actually there still requires investigation on the ground.',
    'platformPage.gaps.note': 'Every output can be traced back to the inputs and steps that produced it, and gaps in the underlying evidence are shown rather than hidden. This is decision support: it prioritizes where to look, and it does not replace field investigation.',
    'platformPage.cta.pilot': 'See the Kızıldere Pilot',
    'platformPage.cta.solutions': 'Explore Solutions',

    'solutionsPage.meta.title': 'Solutions — OrbGSS',
    'solutionsPage.meta.description': "Geothermal exploration is OrbGSS's active first application. Mineral exploration and environmental & land intelligence are expansion directions built on the same evidence-to-priority pattern.",
    'solutionsPage.meta.ogDescription': 'One evidence-to-priority pattern. Geothermal active first; mineral and environmental intelligence next.',
    'solutionsPage.kicker': 'Solutions',
    'solutionsPage.title': 'One workflow, applied where evidence matters.',
    'solutionsPage.intro': 'OrbGSS applies the same evidence-to-priority pattern across domains. Geothermal exploration is where it runs today; mineral exploration and environmental & land intelligence are the directions it is built to extend into.',
    'solutionsPage.listTitle': 'Applications',
    'solutionsPage.geothermal.body1': "OrbGSS's evidence-to-priority workflow is applied today to geothermal exploration, using remote-sensing evidence to rank an area of interest by relative priority.",
    'solutionsPage.geothermal.body2': 'The Kızıldere pilot in Denizli, Türkiye is the concrete first-application proof, evidence and data gaps included.',
    'solutionsPage.mineral.body1': 'Mineral exploration follows the same underlying pattern — area of interest, evidence, explicit gaps, integrated priority — applied to the evidence families relevant to mineral targeting.',
    'solutionsPage.mineral.body2': 'This is a direction the platform is built to extend into, not a deployed or validated product today.',
    'solutionsPage.environment.body1': 'Environmental and land-use change can be read as spatial evidence the same way exploration evidence is: mapped, compared and prioritized across an area of interest.',
    'solutionsPage.environment.body2': 'As with mineral exploration, this is an expansion direction, not a finished or deployed application.',
    'solutionsPage.footnote': 'Every OrbGSS application is decision support: it helps a team prioritize where to look. Field investigation remains necessary.',
    'solutionsPage.cta.platform': 'See How the Platform Works',
    'solutionsPage.cta.pilot': 'See the Kızıldere Pilot',

    'pilotPage.meta.title': 'Pilot — Kızıldere — OrbGSS',
    'pilotPage.meta.description': "Kızıldere is OrbGSS's first geothermal application: a 36 × 36 km pilot area in Denizli, Türkiye, showing how AOI context, remote-sensing evidence and an experimental relative-priority baseline fit together — and what is still an open data gap.",
    'pilotPage.meta.ogDescription': "The Kızıldere pilot: OrbGSS's first geothermal application, evidence and gaps shown in full.",
    'pilotPage.kicker': 'Pilot',
    'pilotPage.title': 'Kızıldere: the first OrbGSS application.',
    'pilotPage.intro': 'Kızıldere is a 36 × 36 km pilot area in Denizli, Türkiye, on a fixed 30 m grid (EPSG:32635). It is where the evidence-to-priority workflow has been applied for the first time, and where its evidence and its gaps can both be shown concretely.',
    'pilotPage.row1.title': 'AOI & project context',
    'pilotPage.row1.copy': 'Every layer in this pilot is registered to the same 36 × 36 km frame, so what follows can be compared directly, layer to layer, on identical ground.',
    'pilotPage.row2.title': 'Terrain',
    'pilotPage.row2.copy': 'NASADEM elevation is carried as context and display only. It gives the pilot area its physical shape; it is not a scored predictor and carries no universal geothermal-favourability direction.',
    'pilotPage.row3.title': 'Evidence',
    'pilotPage.row3.copy': 'One Landsat thermal anomaly layer (THM-01) and two Sentinel-2 spectral alteration proxies (ALT-01, ALT-02) form the accepted remote-sensing evidence core. They are candidate, unvalidated evidence — not mineral identification, and not proof of hydrothermal alteration.',
    'pilotPage.row4.title': 'Structure & geology',
    'pilotPage.row4.copy': 'No public-safe fault or lithology layer is authorized for this pilot yet. That is shown as an explicit gap rather than filled in, and the gap does not change the priority baseline: structure and geology are optional support and score-invariant.',
    'pilotPage.row5.title': 'Priority',
    'pilotPage.row5.copy': 'The thermal and alteration evidence is integrated into mvp_remote_sensing_priority_v1: one within-AOI ranking surface, 0 to 100. It is AOI-relative experimental screening, not a probability, a reserve or resource estimate, or a score calibrated across areas.',
    'pilotPage.closing.title': 'First application',
    'pilotPage.closing.copy': 'Kızıldere is the first geothermal application of that baseline: the priority surface read over NASADEM relief, in an active pilot area in Denizli, Türkiye.',
    'pilotPage.cta.contact': 'Talk to Us About the Pilot',
    'pilotPage.cta.home': 'See the Full Story on the Homepage',
    'pilotPage.nextStepsLabel': 'Next steps',

    'companyPage.meta.title': 'Company — OrbGSS',
    'companyPage.meta.description': 'OrbGSS — Orbital Geo-Spatial Solutions — is a geospatial-intelligence platform built by VirgaSoft, built on traceable provenance, explicit data gaps and evidence-based outputs.',
    'companyPage.meta.ogDescription': 'OrbGSS — Orbital Geo-Spatial Solutions, built by VirgaSoft.',
    'companyPage.principlesTitle': 'How we work',
    'companyPage.expansionTitle': 'Where OrbGSS is headed',
    'companyPage.expansion': 'OrbGSS is built as a general geospatial-intelligence platform. Geothermal exploration is its first proving ground today; the same evidence-to-priority pattern is designed to extend into mineral exploration and environmental & land intelligence as those directions mature.',
    'companyPage.cta.solutions': 'See Solutions',
    'companyPage.cta.contact': 'Get in Touch',

    'contactPage.meta.title': 'Contact — OrbGSS',
    'contactPage.meta.description': 'Reach OrbGSS for pilot, partnership and technical conversations. contact@orbgss.com.',
    'contactPage.meta.ogDescription': 'For pilot, partnership and technical conversations.',
    'contactPage.title': "Let's talk about where to look next.",
    'contactPage.intro': 'OrbGSS is available for pilot, partnership and technical conversations. Reach out directly by email — there is no form to fill in.',
    'contactPage.optionsLabel': 'Contact options',
    'contactPage.pilot.title': 'Pilot conversations',
    'contactPage.pilot.copy': 'Discuss a geothermal pilot, or what a first application in a new area could look like.',
    'contactPage.pilot.cta': 'Start a Pilot Conversation',
    'contactPage.partner.title': 'Partnership',
    'contactPage.partner.copy': 'Explore a partnership or collaboration with OrbGSS.',
    'contactPage.technical.title': 'Technical conversations',
    'contactPage.technical.copy': 'Talk through the evidence, the methodology boundaries, or how a pilot would be scoped.',
    'contactPage.technical.cta': 'Start a Technical Conversation',
    'contactPage.direct.label': 'Direct'
  },
  tr: {
    'meta.title': 'OrbGSS — Coğrafi Zekâ',
    'meta.description': 'OrbGSS, yer gözlem ve yer bilimi verilerini kanıta dayalı mekânsal önceliklere dönüştürerek ekiplerin sırada nerenin inceleneceğine karar vermesine yardımcı olur.',
    'meta.ogDescription': 'Sırada nereye bakacağınızı bilin. Dünya verisi, kanıt, öncelik.',
    'a11y.skip': 'İçeriğe geç',
    'nav.brand': 'OrbGSS ana sayfa',
    'nav.primary': 'Ana gezinme',
    'nav.footer': 'Alt bilgi gezinmesi',
    'nav.open': 'Menüyü aç',
    'nav.close': 'Menüyü kapat',
    'nav.language': 'Dil',
    'nav.platform': 'Platform',
    'nav.solutions': 'Çözümler',
    'nav.pilot': 'Pilot',
    'nav.company': 'Şirket',
    'nav.contact': 'İletişim',
    'nav.geothermal': 'Jeotermal Arama',
    'nav.mineral': 'Maden Arama',
    'nav.environment': 'Çevre ve Arazi Zekâsı',
    'mail.partner': MAIL_TR,
    'hero.eyebrow': 'Dünya verisi. Kanıt. Öncelik.',
    'hero.title': 'Sırada nereye bakacağınızı bilin.',
    'hero.copy': 'OrbGSS, yer gözlem ve yer bilimi verilerini kanıta dayalı mekânsal önceliklere dönüştürür; ekiplerin sırada nerenin inceleneceğine karar vermesine yardımcı olur.',
    'hero.cta': 'Pilot alanı görün',
    'hero.secondary': 'İş Birliği Kurun',
    'story.observe.title': 'Gözlem',
    'story.observe.statement': 'Her OrbGSS analizi tek bir ilgi alanından başlar. Kızıldere pilot alanı, sabit 30 m ızgara üzerinde 36 × 36 km’lik bir çerçevedir; sonrasında gelen her katman tam olarak bu zemine oturur.',
    'story.observe.note': 'Yalnızca kaynak ve alan bağlamı — doğrulama kanıtı değildir.',
    'story.observe.meta': 'İlgi alanı · EPSG:32635 · 30 m · 36 × 36 km',
    'story.terrain.title': 'Topoğrafya',
    'story.terrain.statement': 'Yükselti, alana fiziksel biçimini verir. NASADEM topoğrafyası, sonraki her sinyalin gerçek rölyefe göre okunabilmesi için görüntüleme bağlamı olarak taşınır.',
    'story.terrain.note': 'Yalnızca bağlam ve görüntüleme amaçlıdır. Topoğrafya skorlanan bir öngörücü değildir ve evrensel bir jeotermal uygunluk yönü taşımaz.',
    'story.terrain.meta': 'Bağlam · NASADEM yükselti · metre',
    'story.evidence.title': 'Kanıt',
    'story.evidence.statement': 'Kabul edilmiş üç uzaktan algılama katmanı aynı zemini tarif eder: bir Landsat termal anomalisi ve iki Sentinel-2 spektral alterasyon vekili. Her birinin katkısını görmek için katmanlar arasında geçiş yapın.',
    'story.evidence.note': 'Yalnızca kanıt katmanları — aday ve doğrulanmamış. THM-01 termal kanıttır; jeotermal olasılık, rezerv veya kaynak, keşif ya da sondaj başarısı kanıtı değildir. ALT-01 ve ALT-02 geniş bantlı spektral alterasyon vekilleridir; mineral veya kaolinit tanımlaması değildir ve hidrotermal alterasyon kanıtı sayılmaz.',
    'story.evidence.meta': 'Kanıt · THM-01 / ALT-01 / ALT-02',
    'evidence.switchLabel': 'Kanıt katmanı',
    'story.structure.title': 'Yapı',
    'story.structure.statement': 'Yapısal ve jeolojik bağlam burada yorumu keskinleştirirdi. Bu temel sürüm için OrbGSS’in kamuya açık kullanıma uygun fay veya litoloji katmanı yoktur; bu nedenle sayfa boşluğu doldurmak yerine boşluğu gösterir.',
    'story.structure.note': 'Yapı ve jeoloji isteğe bağlı destektir ve skoru değiştirmez. Bunların yokluğu uzaktan algılama önceliklendirme temelini etkilemez.',
    'story.structure.meta': 'İsteğe bağlı destek · Yayımlanmadı',
    'structure.gapMark': 'Veri boşluğu',
    'structure.gapCopy': 'Bu alan için yayımlanmış bir fay veya litoloji katmanı yok. Buraya bilinçli olarak hiçbir şey çizilmedi: uydurulmuş bir yapısal çizgi kanıt gibi görünür ama kanıt olmazdı.',
    'structure.gapMeta': 'Yapısal bağlam — isteğe bağlı destek / veri boşluğu',
    'story.priority.title': 'Öncelik',
    'story.priority.statement': 'Termal ve alterasyon kanıtı, ekiplerin önce nereye bakacağını sıralayabilmesi için 0–100 aralığında tek bir alan içi sıralama yüzeyinde birleştirilir.',
    'story.priority.note': 'Yalnızca alan içi deneysel ön eleme. Olasılık, rezerv veya kaynak tahmini, keşif olasılığı, sondaj başarısı olasılığı, Tam Prospektivite ya da alanlar arası kalibre edilmiş bir skor değildir.',
    'story.priority.meta': 'Skor · mvp_remote_sensing_priority_v1',
    'story.geothermal.title': 'Jeotermal',
    'story.geothermal.statement': 'Kızıldere, bu temelin ilk jeotermal uygulamasıdır: Denizli, Türkiye’deki aktif pilot alanda NASADEM rölyefi üzerine serilmiş öncelik yüzeyi.',
    'story.geothermal.note': 'İlk uygulama kanıtıdır; saha doğrulaması, keşif, rezerv veya kaynak, sondaj hedefi ya da sondaj başarısı kanıtı değildir.',
    'story.geothermal.meta': 'İlk uygulama · Kızıldere pilotu',
    'scene.kind.naturalColor': 'Doğal renkli kompozit',
    'scene.aoi.place': 'Kızıldere, Denizli, Türkiye',
    'scene.aoi.coords': '37.9794° K, 28.7907° D',
    'label.observe': 'Kızıldere ilgi alanı — kabul edilmiş MVP proje bağlamı',
    'label.terrain': 'Yükselti — NASADEM bağlamı',
    'label.thm01': 'THM-01 Termal Anomali',
    'label.alt01': 'ALT-01 Alterasyon Vekili — kil/hidroksil',
    'label.alt02': 'ALT-02 Alterasyon Vekili — ferrik/demir',
    'label.priority': 'Uzaktan Algılama Göreli Önceliği — Deneysel Temel',
    'label.geothermal': 'Kızıldere — deneysel uzaktan algılama temelinin ilk jeotermal uygulaması',
    'alt.observe': 'Kızıldere proje alanının 36 çarpı 36 kilometrelik gri tonlamalı yükselti haritası; pilot ızgara boyunca sırtları ve vadileri gösterir',
    'alt.terrain': 'Kızıldere ilgi alanının renkli yükselti haritası; alçak zemin koyu mavi, yüksek sırtlar soluk sarı',
    'alt.thm01': 'Kızıldere ilgi alanının ıraksak termal anomali haritası; daha serin zemin mavi, daha sıcak zemin kırmızı',
    'alt.alt01': 'Kızıldere ilgi alanı boyunca kil ve hidroksil spektral alterasyon vekilinin sıralı haritası',
    'alt.alt02': 'Kızıldere ilgi alanı boyunca ferrik demir spektral alterasyon vekilinin sıralı haritası',
    'alt.priority': 'Kızıldere ilgi alanının göreli öncelik haritası; zemini alan içinde 0 ile 100 arasında sıralar',
    'alt.geothermal': 'Kızıldere jeotermal pilot alanında gölgelendirilmiş NASADEM rölyefi üzerindeki göreli öncelik yüzeyi',
    'hero.handoff.kicker': '04 · Sonuç',
    'hero.handoff.cta': 'Nasıl türetildiğini görün',
    'act.context.kicker': '02 · Alan',
    'act.context.title': 'Herhangi bir analizden önce, gerçek bir alan.',
    'act.context.copy': 'Kızıldere, Denizli, Türkiye’deki Büyük Menderes grabeninde yer alır. Bu, alanın Landsat 8 tarafından görüntülenmiş hâlidir — tek bir katman türetilmeden önce, pilot çalışmanın tamamının üzerine oturduğu zemin.',
    'act.context.note': 'Yalnızca Yer gözlem bağlamı. Bu, alanın doğal renkli fotografik bileşimidir; analitik kanıt değildir, skorlanan bir girdi değildir ve herhangi bir THM ya da ALT kanıt katmanının görüntüleme tarihi değildir.',
    'act.context.meta': 'Landsat 8 OLI · 2025-05-05 · 30 m · doğal renk',
    'act.evidence.kicker': '03 · Kanıt',
    'act.evidence.title': 'Aynı zemin üzerinde üç katman.',
    'act.evidence.copy': 'Bağlam için rölyef, kanıt olarak bir Landsat termal anomalisi ve bir Sentinel-2 alterasyon vekili. Aynı ilgi alanı, aynı 30 m ızgara, aynı anlatı aşaması — bunları karşılaştırılabilir kılan da budur.',
    'act.evidence.listLabel': 'Kanıt katmanları',
    'act.evidence.terrain.role': 'Bağlam',
    'act.evidence.thermal.role': 'Kanıt',
    'act.evidence.thermal.note': 'Yalnızca kanıt katmanı. Jeotermal olasılık, rezerv, keşif ya da sondaj başarısı kanıtı olarak tanımlanmamalıdır.',
    'act.evidence.alteration.role': 'Kanıt',
    'act.evidence.alteration.note': 'Geniş bantlı Sentinel-2 spektral alterasyon vekili; mineral/kaolinit tanımlaması değildir ve hidrotermal alterasyon kanıtı değildir.',
    'act.evidence.gapLabel': 'Veri boşluğu',
    'act.evidence.gap': 'Yapısal ve jeolojik kanıt burada yorumu keskinleştirirdi. OrbGSS bu temel sürüm için kamuya açık kullanıma uygun bir fay veya litoloji katmanına sahip değildir; bu nedenle boşluk doldurulmak yerine açıkça belirtilir — isteğe bağlı destektir ve öncelik sonucunu değiştirmez.',
    'act.evidence.deeper': 'Katmanlar nasıl üretiliyor',
    'act.priority.kicker': '04 · Sonuç',
    'act.priority.title': 'Önce nereye bakmalı.',
    'act.priority.copy': 'Termal ve alterasyon kanıtı, ilgi alanı genelinde 0–100 aralığında tek bir sıralama yüzeyinde birleştirilir; böylece bir ekip zemini tahmin etmek yerine sıralayabilir. Yüksek değerler, bu alan içinde ve bu temel sürüm için “önce şuraya bak” anlamına gelir.',
    'act.priority.note': 'Yalnızca alan içi deneysel ön eleme. Olasılık, rezerv veya kaynak tahmini, keşif olasılığı, sondaj başarısı olasılığı, Tam Prospektivite ya da alanlar arası kalibre edilmiş bir skor değildir.',
    'act.priority.meta': 'mvp_remote_sensing_priority_v1 · EPSG:32635 · 30 m · 36 × 36 km',
    'act.priority.deeper': 'Pilot yöntemini okuyun',
    'scene.hero.place': 'Kızıldere — Büyük Menderes grabeni, Denizli, Türkiye',
    'scene.hero.coords': '37.9794° K, 28.7907° D',
    'scene.hero.kind': 'Görselleştirilmiş yörünge sekansı — sensör görüntüsü değildir',
    'scene.context.place': 'Kızıldere — Büyük Menderes grabeni, Denizli, Türkiye',
    'scene.context.coords': '37.9794° K, 28.7907° D',
    'scene.context.kind': 'Doğal renkli bileşim',
    'scene.priority.place': 'Kızıldere — Büyük Menderes grabeni, Denizli, Türkiye',
    'scene.priority.coords': '37.9794° K, 28.7907° D',
    'alt.hero': 'Doğu Akdeniz ve batı Türkiye’nin yörüngeden görselleştirilmiş görünümü; Kızıldere pilot bölgesinin üzerine kilitlenmiş parlak kare bir veri alım çerçevesi ile',
    'alt.context': 'Kızıldere çevresindeki Büyük Menderes grabeninin doğal renkli Landsat 8 görünümü; vadi tabanı, sulanan tarlalar ve iki yandaki sırtlar görülüyor',
    'alt.priorityLegend': 'Göreli öncelik haritasının renk ölçeği; koyu uçta 0 değerinden açık uçta 100 değerine uzanır',
    'pilot.kicker': 'Pilot',
    'pilot.title': 'Önce jeotermal.',
    'pilot.copy': 'OrbGSS ilk olarak jeotermal aramada uygulanıyor. Maden arama ile çevre ve arazi zekâsı aynı kanıttan önceliğe iş akışını izler; bunlar tamamlanmış ürünler değil, genişleme yönleridir.',
    'pilot.listLabel': 'Uygulama alanları',
    'app.geothermal.title': 'Jeotermal Arama',
    'app.geothermal.status': 'Aktif · İlk uygulama',
    'app.geothermal.copy': 'Jeotermal arama alanlarının kanıta dayalı önceliklendirilmesi.',
    'app.mineral.title': 'Maden Arama',
    'app.mineral.status': 'Genişleme yönü',
    'app.mineral.copy': 'Aynı iş akışının maden arama hedeflerine genişletilmesi.',
    'app.environment.title': 'Çevre ve Arazi Zekâsı',
    'app.environment.status': 'Genişleme yönü',
    'app.environment.copy': 'Arazi ve çevre değişiminin mekânsal kanıt olarak okunması.',
    'company.kicker': 'Şirket',
    'company.title': 'OrbGSS — Orbital Geo-Spatial Solutions',
    'company.copy': 'OrbGSS, VirgaSoft tarafından geliştirilen bir coğrafi zekâ platformudur. Arama ve arazi kararlarını kanıta dayalı, izlenebilir ve önceliklendirilmesi kolay hâle getirmek için vardır.',
    'trust.kicker': 'Nasıl çalışıyoruz',
    'trust.provenance.title': 'İzlenebilir kaynak',
    'trust.provenance.copy': 'Her çıktı, kaynak verisine kadar takip edilebilir.',
    'trust.gaps.title': 'Açık veri boşlukları',
    'trust.gaps.copy': 'Eksik veya zayıf girdiler gizlenmez, gösterilir.',
    'trust.evidence.title': 'Kanıta dayalı çıktılar',
    'trust.evidence.copy': 'Öncelikler, haritalanmış kanıtlardan gerekçesiyle birlikte türetilir.',
    'trust.decision.title': 'Karar desteği, ikame değil',
    'trust.decision.copy': 'OrbGSS nerenin inceleneceğine karar vermeye yardımcı olur. Saha incelemesi gerekli olmaya devam eder.',
    'contact.title': 'İletişim',
    'contact.copy': 'Pilot, iş birliği ve teknik görüşmeler için.',
    'contact.cta': 'İş Birliği Kurun',
    'scene.crater.place': 'Crater Lake, Oregon, ABD',
    'scene.crater.coords': '42.9443° K, 122.1353° B',
    'scene.yellowstone.place': 'Yellowstone Ulusal Parkı, ABD',
    'scene.yellowstone.coords': '44.4604° K, 110.8282° B',
    // Pre-uppercased: Turkish locale casing would otherwise render the Spanish name as "CHUQUİCAMATA".
    'scene.chuquicamata.place': 'CHUQUICAMATA, ANTOFAGASTA, ŞİLİ',
    'scene.chuquicamata.coords': '22.3150° G, 68.9010° B',
    'scene.ili.place': 'İli Nehri Deltası ve Balkaş Gölü, Kazakistan',
    'scene.ili.coords': '45.0600° K, 74.5200° D',
    'alt.crater': 'Oregon (ABD) Crater Lake ve çevresindeki arazinin uydu görüntüsü',
    'alt.yellowstone': 'Yellowstone Ulusal Parkı çevresindeki jeotermal arazinin uydu görüntüsü',
    'alt.chuquicamata': 'Kuzey Şili Chuquicamata madencilik bölgesinin uydu görüntüsü',
    'alt.ili': 'Kazakistan İli Nehri Deltası ve Balkaş Gölü uydu görüntüsü',
    'footer.builtBy': 'VirgaSoft tarafından geliştirildi',
    'footer.attribution': 'Landsat verileri ABD Jeoloji Araştırmaları Kurumu (USGS) kaynaklıdır. Açılış görseli, Landsat Collection 2 yüzey yansıtması ürünlerinden OrbGSS tarafından üretilen doğal renkli bir kompozittir. Bölüm görselleri ise NASADEM yükselti, Landsat termal ve Sentinel-2 alterasyon kanıtlarından türetilen, Kızıldere pilot alanına ait OrbGSS kartografik dışa aktarımlarıdır; renk skalaları Fabio Crameri, Scientific colour maps v8.0. Kaynak bilgileri üretim paketinde belgelenmiştir.',
    'footer.copyright': '© 2026 OrbGSS. Tüm hakları saklıdır.',

    /* WEB-003 — deep public routes */
    'mail.pilot': MAIL_PILOT_TR,
    'mail.technical': MAIL_TECH_TR,

    'platformPage.meta.title': 'Platform — OrbGSS',
    'platformPage.meta.description': "OrbGSS'in bir ilgi alanını izlenebilir, kanıta dayalı bir mekânsal önceliğe nasıl dönüştürdüğü — ve sahadaki incelemenin hâlâ nerede devraldığı.",
    'platformPage.meta.ogDescription': 'İlgi alanından mekânsal önceliğe, her adımı izlenebilir şekilde.',
    'platformPage.kicker': 'Platform',
    'platformPage.title': 'OrbGSS bir mekânsal önceliği nasıl kurar?',
    'platformPage.intro': 'OrbGSS bir ilgi alanını ele alır, mevcut girdileri tek bir mekânsal çerçevede birleştirir ve bunları bir ekibin üzerine hareket edebileceği, alan içi bir önceliğe dönüştürür — her adımda gerekçesi de birlikte taşınarak.',
    'platformPage.stepsTitle': 'İş akışı',
    'platformPage.step1.title': 'İlgi alanı',
    'platformPage.step1.copy': 'Her analiz bir sınır belirleyerek başlar: bilinen bir ızgara ve koordinat sistemi üzerinde tanımlı bir alan. Böylece sonrasında gelen her katman tam olarak aynı zemine oturur.',
    'platformPage.step2.title': 'Kaynak ve bağlam',
    'platformPage.step2.copy': 'Girdiler özgün kaynaklarından alınır ve nereden geldiği izlenebilir biçimde tutulur. Topoğrafya gibi bağlam katmanları zemini tarif eder; tek başlarına kanıt değildirler.',
    'platformPage.step3.title': 'Kanıt',
    'platformPage.step3.copy': 'Alanla ilgili sinyaller aynı bölge üzerinde mekânsal kanıt olarak haritalanır; böylece farklı göstergeler ortak bir zeminde karşılaştırılabilir ve birlikte okunabilir.',
    'platformPage.step4.title': 'Açık veri boşlukları',
    'platformPage.step4.copy': "Her girdi her yerde bulunmaz. OrbGSS'in kamuya açık kullanıma uygun bir katmanı olmadığında, platform boşluğu tahmini bir yerine koyma ile doldurmak yerine olduğu gibi gösterir.",
    'platformPage.step5.title': 'Bütünleşik mekânsal öncelik',
    'platformPage.step5.copy': 'Mevcut kanıtlar tek bir alan içi sıralamada birleştirilir; böylece bir ekip, sahaya adım atmadan önce zeminin göreli olarak nerede daha çok ya da daha az ilgi çekici olduğunu görebilir.',
    'platformPage.step6.title': 'Saha inceleme kararına destek',
    'platformPage.step6.copy': 'Öncelik görünümü, saha çalışmasını planlamak için bir başlangıç noktasıdır, onun yerine geçmez. Ekibin önce nereye bakacağına karar vermesine yardımcı olur; orada gerçekte ne olduğunu doğrulamak yine sahada inceleme gerektirir.',
    'platformPage.gaps.note': 'Her çıktı, onu üreten girdilere ve adımlara kadar geriye izlenebilir; alttaki kanıttaki boşluklar gizlenmez, gösterilir. Bu bir karar desteğidir: nereye bakılacağını önceliklendirir, sahadaki incelemenin yerini almaz.',
    'platformPage.cta.pilot': 'Kızıldere Pilotunu İnceleyin',
    'platformPage.cta.solutions': 'Çözümleri Keşfedin',

    'solutionsPage.meta.title': 'Çözümler — OrbGSS',
    'solutionsPage.meta.description': 'Jeotermal arama, OrbGSS’in aktif ilk uygulamasıdır. Maden arama ile çevre ve arazi zekâsı, aynı kanıttan önceliğe deseni üzerine kurulan genişleme yönleridir.',
    'solutionsPage.meta.ogDescription': 'Tek bir kanıttan önceliğe deseni. Önce aktif jeotermal; ardından maden ve çevre zekâsı.',
    'solutionsPage.kicker': 'Çözümler',
    'solutionsPage.title': 'Tek iş akışı, kanıtın önemli olduğu her yerde.',
    'solutionsPage.intro': "OrbGSS aynı kanıttan önceliğe desenini farklı alanlarda uygular. Bugün çalıştığı yer jeotermal aramadır; maden arama ile çevre ve arazi zekâsı, genişleyeceği yönlerdir.",
    'solutionsPage.listTitle': 'Uygulama alanları',
    'solutionsPage.geothermal.body1': "OrbGSS'in kanıttan önceliğe iş akışı, bugün jeotermal aramaya uygulanıyor; bir ilgi alanını göreli önceliğine göre sıralamak için uzaktan algılama kanıtını kullanıyor.",
    'solutionsPage.geothermal.body2': "Denizli, Türkiye'deki Kızıldere pilotu, kanıtı ve veri boşluklarıyla birlikte somut ilk uygulama kanıtıdır.",
    'solutionsPage.mineral.body1': 'Maden arama da aynı temel deseni izler — ilgi alanı, kanıt, açık boşluklar, bütünleşik öncelik — maden hedeflemesiyle ilgili kanıt ailelerine uygulanmış hâliyle.',
    'solutionsPage.mineral.body2': 'Bu, platformun genişlemek üzere kurgulandığı bir yöndür; bugün devreye alınmış ya da doğrulanmış bir ürün değildir.',
    'solutionsPage.environment.body1': 'Çevresel ve arazi kullanımı değişimi de, arama kanıtı gibi mekânsal kanıt olarak okunabilir: bir ilgi alanı boyunca haritalanır, karşılaştırılır ve önceliklendirilir.',
    'solutionsPage.environment.body2': 'Maden aramada olduğu gibi, bu da bir genişleme yönüdür; tamamlanmış ya da devreye alınmış bir uygulama değildir.',
    'solutionsPage.footnote': 'Her OrbGSS uygulaması bir karar desteğidir: ekibin nereye bakacağını önceliklendirmesine yardımcı olur. Sahada inceleme gerekli olmaya devam eder.',
    'solutionsPage.cta.platform': 'Platformun Nasıl Çalıştığını Görün',
    'solutionsPage.cta.pilot': 'Kızıldere Pilotunu İnceleyin',

    'pilotPage.meta.title': 'Pilot — Kızıldere — OrbGSS',
    'pilotPage.meta.description': "Kızıldere, OrbGSS'in ilk jeotermal uygulamasıdır: Denizli, Türkiye'de 36 × 36 km'lik bir pilot alan. İlgi alanı bağlamının, uzaktan algılama kanıtının ve deneysel göreli öncelik temelinin nasıl bir araya geldiğini — ve hâlâ açık olan veri boşluğunu gösterir.",
    'pilotPage.meta.ogDescription': "Kızıldere pilotu: OrbGSS'in ilk jeotermal uygulaması, kanıtı ve boşluklarıyla birlikte.",
    'pilotPage.kicker': 'Pilot',
    'pilotPage.title': 'Kızıldere: ilk OrbGSS uygulaması.',
    'pilotPage.intro': "Kızıldere, Denizli, Türkiye'de sabit 30 m'lik bir ızgara üzerinde (EPSG:32635) 36 × 36 km'lik bir pilot alandır. Kanıttan önceliğe iş akışının ilk kez uygulandığı ve hem kanıtının hem de boşluklarının somut biçimde gösterilebildiği yerdir.",
    'pilotPage.row1.title': 'İlgi alanı ve proje bağlamı',
    'pilotPage.row1.copy': 'Bu pilottaki her katman aynı 36 × 36 km çerçeveye kayıtlıdır; böylece sonrasında gelenler, katman katman, birebir aynı zemin üzerinde karşılaştırılabilir.',
    'pilotPage.row2.title': 'Topoğrafya',
    'pilotPage.row2.copy': 'NASADEM yükseltisi yalnızca bağlam ve görüntüleme amacıyla taşınır. Pilot alana fiziksel biçimini verir; skorlanan bir öngörücü değildir ve evrensel bir jeotermal uygunluk yönü taşımaz.',
    'pilotPage.row3.title': 'Kanıt',
    'pilotPage.row3.copy': 'Bir Landsat termal anomali katmanı (THM-01) ile iki Sentinel-2 spektral alterasyon vekili (ALT-01, ALT-02), kabul edilmiş uzaktan algılama kanıt çekirdeğini oluşturur. Bunlar aday ve doğrulanmamış kanıtlardır — mineral tanımlaması değildir ve hidrotermal alterasyon kanıtı sayılmaz.',
    'pilotPage.row4.title': 'Yapı ve jeoloji',
    'pilotPage.row4.copy': 'Bu pilot için henüz kamuya açık kullanıma uygun bir fay veya litoloji katmanı yetkilendirilmemiştir. Bu, doldurulmak yerine açık bir boşluk olarak gösterilir ve öncelik temelini değiştirmez: yapı ve jeoloji isteğe bağlı destektir, skoru etkilemez.',
    'pilotPage.row5.title': 'Öncelik',
    'pilotPage.row5.copy': 'Termal ve alterasyon kanıtı, mvp_remote_sensing_priority_v1 içinde birleştirilir: 0 ile 100 arasında tek bir alan içi sıralama yüzeyi. Bu, alan içi deneysel bir ön elemedir; olasılık, rezerv veya kaynak tahmini ya da alanlar arası kalibre edilmiş bir skor değildir.',
    'pilotPage.closing.title': 'İlk uygulama',
    'pilotPage.closing.copy': "Kızıldere, bu temelin ilk jeotermal uygulamasıdır: Denizli, Türkiye'deki aktif pilot alanda, NASADEM rölyefi üzerinden okunan öncelik yüzeyi.",
    'pilotPage.cta.contact': 'Pilot Hakkında Bizimle Görüşün',
    'pilotPage.cta.home': 'Ana Sayfada Hikâyenin Tamamını Görün',
    'pilotPage.nextStepsLabel': 'Sonraki adımlar',

    'companyPage.meta.title': 'Şirket — OrbGSS',
    'companyPage.meta.description': 'OrbGSS — Orbital Geo-Spatial Solutions — VirgaSoft tarafından geliştirilen; izlenebilir kaynak, açık veri boşlukları ve kanıta dayalı çıktılar üzerine kurulu bir coğrafi zekâ platformudur.',
    'companyPage.meta.ogDescription': 'OrbGSS — Orbital Geo-Spatial Solutions, VirgaSoft tarafından geliştirildi.',
    'companyPage.principlesTitle': 'Nasıl çalışıyoruz',
    'companyPage.expansionTitle': 'OrbGSS nereye gidiyor',
    'companyPage.expansion': 'OrbGSS genel bir coğrafi zekâ platformu olarak kurgulanmıştır. Jeotermal arama bugün ilk deneme alanıdır; aynı kanıttan önceliğe deseni, bu yönler olgunlaştıkça maden arama ile çevre ve arazi zekâsına genişlemek üzere tasarlanmıştır.',
    'companyPage.cta.solutions': 'Çözümleri Görün',
    'companyPage.cta.contact': 'Bize Ulaşın',

    'contactPage.meta.title': 'İletişim — OrbGSS',
    'contactPage.meta.description': "Pilot, iş birliği ve teknik görüşmeler için OrbGSS'e ulaşın. contact@orbgss.com.",
    'contactPage.meta.ogDescription': 'Pilot, iş birliği ve teknik görüşmeler için.',
    'contactPage.title': 'Sırada nereye bakacağımızı konuşalım.',
    'contactPage.intro': 'OrbGSS; pilot, iş birliği ve teknik görüşmeler için ulaşılabilir durumdadır. Doğrudan e-posta ile yazın — doldurulacak bir form yok.',
    'contactPage.optionsLabel': 'İletişim seçenekleri',
    'contactPage.pilot.title': 'Pilot görüşmeleri',
    'contactPage.pilot.copy': 'Bir jeotermal pilotu, ya da yeni bir alanda ilk uygulamanın nasıl görünebileceğini konuşalım.',
    'contactPage.pilot.cta': 'Pilot Görüşmesi Başlatın',
    'contactPage.partner.title': 'İş birliği',
    'contactPage.partner.copy': 'OrbGSS ile bir iş birliği ya da ortaklık imkânını değerlendirin.',
    'contactPage.technical.title': 'Teknik görüşmeler',
    'contactPage.technical.copy': 'Kanıtı, yöntem sınırlarını ya da bir pilotun nasıl kapsamlandırılacağını konuşalım.',
    'contactPage.technical.cta': 'Teknik Görüşme Başlatın',
    'contactPage.direct.label': 'Doğrudan'
  }
};


const DEFAULT_LANG = 'en';
const LANG_KEY = 'orbgss.lang';
const ATTR_MAP = [
  ['data-i18n-alt', 'alt'],
  ['data-i18n-aria-label', 'aria-label'],
  ['data-i18n-content', 'content'],
  ['data-i18n-href', 'href']
];

let currentLang = DEFAULT_LANG;
const t = (key) => (I18N[currentLang] && I18N[currentLang][key]) || I18N[DEFAULT_LANG][key] || '';

function readStoredLang() {
  try {
    const stored = window.localStorage.getItem(LANG_KEY);
    return stored && I18N[stored] ? stored : DEFAULT_LANG;
  } catch (error) {
    return DEFAULT_LANG;
  }
}

function applyLanguage(lang) {
  if (!I18N[lang]) return;
  currentLang = lang;
  document.documentElement.lang = lang;

  document.querySelectorAll('[data-i18n]').forEach((el) => {
    el.textContent = t(el.getAttribute('data-i18n'));
  });
  document.querySelectorAll('[data-i18n-html]').forEach((el) => {
    el.innerHTML = t(el.getAttribute('data-i18n-html'));
  });
  ATTR_MAP.forEach(([dataAttr, target]) => {
    document.querySelectorAll(`[${dataAttr}]`).forEach((el) => {
      el.setAttribute(target, t(el.getAttribute(dataAttr)));
    });
  });

  // The menu toggle label depends on both language and open state.
  syncMenuToggleLabel();

  document.querySelectorAll('.lang-btn').forEach((button) => {
    button.setAttribute('aria-pressed', String(button.dataset.lang === lang));
  });

  try {
    window.localStorage.setItem(LANG_KEY, lang);
  } catch (error) {
    /* storage unavailable: language still applies for this page view */
  }
}

/* ------------------------------------------------------------------ */
/* Mobile navigation                                                    */
/* ------------------------------------------------------------------ */
const toggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('.main-nav');

function syncMenuToggleLabel() {
  if (!toggle || !nav) return;
  const open = nav.classList.contains('open');
  toggle.setAttribute('aria-expanded', String(open));
  toggle.setAttribute('aria-label', t(open ? 'nav.close' : 'nav.open'));
}

function closeNav({ focusToggle = false } = {}) {
  if (!nav || !nav.classList.contains('open')) return;
  nav.classList.remove('open');
  syncMenuToggleLabel();
  if (focusToggle && toggle) toggle.focus();
}

if (toggle && nav) {
  toggle.addEventListener('click', () => {
    nav.classList.toggle('open');
    syncMenuToggleLabel();
  });
  nav.querySelectorAll('a').forEach((link) => link.addEventListener('click', () => closeNav()));
}

/* ------------------------------------------------------------------ */
/* Solutions dropdown (disclosure pattern: button + list of links)      */
/* ------------------------------------------------------------------ */
const menuItem = document.querySelector('.has-menu');
const trigger = menuItem ? menuItem.querySelector('.nav-trigger') : null;
const submenuLinks = menuItem ? Array.from(menuItem.querySelectorAll('.submenu a')) : [];
const desktopHover = window.matchMedia('(min-width: 981px) and (hover: hover)');
const desktopLayout = window.matchMedia('(min-width: 981px)');
let openedByFocus = false;
let openedByHover = false;

function setSubmenu(open) {
  if (!menuItem || !trigger) return;
  menuItem.classList.toggle('open', open);
  trigger.setAttribute('aria-expanded', String(open));
}
const submenuOpen = () => Boolean(menuItem && menuItem.classList.contains('open'));

if (menuItem && trigger) {
  // Click / tap toggles (works everywhere, including mobile).
  trigger.addEventListener('click', () => {
    if (openedByFocus || openedByHover) {
      // Hover or focus already opened it during this interaction: a click confirms, not toggles.
      openedByFocus = false;
      openedByHover = false;
      return;
    }
    setSubmenu(!submenuOpen());
  });

  // Hover opens on pointer-capable desktop layouts only.
  menuItem.addEventListener('mouseenter', () => {
    if (desktopHover.matches && !submenuOpen()) {
      setSubmenu(true);
      openedByHover = true;
    }
  });
  menuItem.addEventListener('mouseleave', () => {
    if (desktopHover.matches) {
      setSubmenu(false);
      openedByHover = false;
    }
  });

  // Keyboard focus entering the group opens on desktop; leaving the group closes it.
  // Focus moving within the group (e.g. Escape returning focus to the trigger) must not reopen it.
  menuItem.addEventListener('focusin', (event) => {
    if (desktopLayout.matches && !submenuOpen() && !menuItem.contains(event.relatedTarget)) {
      setSubmenu(true);
      openedByFocus = true;
    }
  });
  menuItem.addEventListener('focusout', (event) => {
    if (!menuItem.contains(event.relatedTarget)) {
      setSubmenu(false);
      openedByFocus = false;
    }
  });
  trigger.addEventListener('blur', () => { openedByFocus = false; });

  // Arrow-key navigation inside the disclosure.
  menuItem.addEventListener('keydown', (event) => {
    const index = submenuLinks.indexOf(document.activeElement);
    if (event.key === 'ArrowDown') {
      event.preventDefault();
      if (!submenuOpen()) setSubmenu(true);
      const next = index === -1 ? 0 : Math.min(index + 1, submenuLinks.length - 1);
      submenuLinks[next].focus();
    } else if (event.key === 'ArrowUp') {
      event.preventDefault();
      if (index <= 0) trigger.focus();
      else submenuLinks[index - 1].focus();
    } else if (event.key === 'Home' && index !== -1) {
      event.preventDefault();
      submenuLinks[0].focus();
    } else if (event.key === 'End' && index !== -1) {
      event.preventDefault();
      submenuLinks[submenuLinks.length - 1].focus();
    }
  });

  // Choosing a solution closes the dropdown.
  submenuLinks.forEach((link) => link.addEventListener('click', () => setSubmenu(false)));

  // Click outside closes it.
  document.addEventListener('pointerdown', (event) => {
    if (submenuOpen() && !menuItem.contains(event.target)) setSubmenu(false);
  });
}

/* ------------------------------------------------------------------ */
/* WEB-004: a viewport or orientation change must not leave stale       */
/* disclosure state. Crossing the 980px breakpoint with the mobile menu */
/* open used to keep .main-nav flagged open and leave the now-hidden    */
/* menu button reporting aria-expanded="true" with its "Close           */
/* navigation" label, and the Solutions submenu stayed visibly open on  */
/* the desktop bar with no pointer or focus inside it. Both are reset   */
/* on the breakpoint crossing, which is also what a phone rotation      */
/* into a wide landscape layout triggers.                              */
/* ------------------------------------------------------------------ */
function resetNavState() {
  closeNav();
  setSubmenu(false);
  openedByFocus = false;
  openedByHover = false;
}
if (typeof desktopLayout.addEventListener === 'function') {
  desktopLayout.addEventListener('change', resetNavState);
} else if (typeof desktopLayout.addListener === 'function') {
  desktopLayout.addListener(resetNavState);
}

/* ------------------------------------------------------------------ */
/* Escape: close dropdown first, then the mobile menu                   */
/* ------------------------------------------------------------------ */
document.addEventListener('keydown', (event) => {
  if (event.key !== 'Escape') return;
  if (submenuOpen()) {
    setSubmenu(false);
    if (menuItem.contains(document.activeElement)) trigger.focus();
    return;
  }
  closeNav({ focusToggle: true });
});

/* ------------------------------------------------------------------ */
/* Language switch                                                      */
/* ------------------------------------------------------------------ */
document.querySelectorAll('.lang-btn').forEach((button) => {
  button.addEventListener('click', () => applyLanguage(button.dataset.lang));
});
applyLanguage(readStoredLang());

/* ------------------------------------------------------------------ */
/* Graceful failure for self-hosted imagery: hide a scene that fails    */
/* to load so the dark panel background shows, never a broken glyph.    */
/* ------------------------------------------------------------------ */
document.querySelectorAll('.panel-image, .story-panel > img, .evidence-card img').forEach((image) => {
  image.addEventListener('error', () => {
    image.style.visibility = 'hidden';
  }, { once: true });
});

/* ------------------------------------------------------------------ */
/* WEB-004 measured caption tone                                        */
/*                                                                      */
/* WEB-002 chose each proof panel's caption tone by hand, from the      */
/* measured luminance of the region the caption sits over. That rule is */
/* right; applying it once is not. Story panels crop their raster with  */
/* object-fit: cover, so the pixels underneath the bottom-right caption */
/* change every time the viewport changes shape. Measured on the        */
/* accepted build, the light captions read 5.1:1 at 375px but only      */
/* 2.4-2.9:1 at 1440px, and ALT-01/ALT-02 invert outright between       */
/* 768px and 1440px — so no single authored value can be correct at     */
/* every width.                                                         */
/*                                                                      */
/* The fix applies WEB-002's own rule continuously: sample the rendered */
/* region, keep whichever of the two accepted tones contrasts better.   */
/* The raster is never touched, read back or re-rendered — only the     */
/* caption's own colour changes, and only between tones the design      */
/* already ships. Without JavaScript, or if the canvas cannot be read,  */
/* the authored WEB-002 tone stays exactly as it is.                    */
/* ------------------------------------------------------------------ */

/* Relative luminance at which the accepted light caption (#fbfdfe) and the accepted dark caption
   (#050d13) contrast equally against their backdrop. Above it the dark tone wins, below it the
   light tone does. Derived from the WCAG contrast formula for those two exact colours. */
const CAPTION_TONE_CROSSOVER = 0.185;

function backdropLuminance(label, image) {
  if (!image || !image.naturalWidth || !image.naturalHeight) return null;
  const labelBox = label.getBoundingClientRect();
  const imageBox = image.getBoundingClientRect();
  if (!labelBox.width || !labelBox.height || !imageBox.width || !imageBox.height) return null;

  // Undo object-fit: cover to find which part of the raster is actually under the caption.
  // object-position is read rather than assumed to be centred: the story panels all use the
  // default 50% 50%, but the hero crops at 68% on narrow viewports, and a panel that ever picks
  // its own crop would otherwise be measured against the wrong pixels without anything failing.
  const position = window.getComputedStyle(image).objectPosition.split(' ');
  const posX = (parseFloat(position[0]) || 0) / 100;
  const posY = (parseFloat(position[1]) || 0) / 100;
  const scale = Math.max(imageBox.width / image.naturalWidth, imageBox.height / image.naturalHeight);
  const originX = imageBox.left + (imageBox.width - image.naturalWidth * scale) * posX;
  const originY = imageBox.top + (imageBox.height - image.naturalHeight * scale) * posY;
  const sx = Math.max(0, (labelBox.left - originX) / scale);
  const sy = Math.max(0, (labelBox.top - originY) / scale);
  const sw = Math.min(image.naturalWidth - sx, labelBox.width / scale);
  const sh = Math.min(image.naturalHeight - sy, labelBox.height / scale);
  if (sw <= 1 || sh <= 1) return null;

  // Sample small: the caption only needs the average tone under it, not a faithful copy.
  const width = Math.max(1, Math.min(96, Math.round(sw)));
  const height = Math.max(1, Math.min(32, Math.round(sh)));
  const canvas = document.createElement('canvas');
  canvas.width = width;
  canvas.height = height;
  const context = canvas.getContext('2d', { willReadFrequently: true });
  if (!context) return null;

  let pixels;
  try {
    context.drawImage(image, sx, sy, sw, sh, 0, 0, width, height);
    pixels = context.getImageData(0, 0, width, height).data;
  } catch (error) {
    return null; /* cross-origin or otherwise unreadable: keep the authored tone */
  }

  const channel = (value) => {
    const v = value / 255;
    return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
  };
  let total = 0;
  for (let i = 0; i < pixels.length; i += 4) {
    total += 0.2126 * channel(pixels[i]) + 0.7152 * channel(pixels[i + 1]) + 0.0722 * channel(pixels[i + 2]);
  }
  return total / (pixels.length / 4);
}

function tunePanel(panel) {
  /* WEB-005: a panel whose caption sits over a protection gradient has an authored tone, not a
     measured one. Measuring would read the raster underneath and miss the gradient on top, which
     is how you end up choosing dark text for a deliberately darkened corner. Only panels whose
     caption sits directly on untreated imagery — the accepted /pilot/ proof panels — are tuned. */
  if (panel.hasAttribute('data-label-tone-locked')) return;
  const label = panel.querySelector('.scene-label');
  const image = panel.querySelector('img');
  if (!label || !image) return;
  const luminance = backdropLuminance(label, image);
  if (luminance === null) return;
  panel.setAttribute('data-label-tone', luminance > CAPTION_TONE_CROSSOVER ? 'dark' : 'light');
}

/* Only panels at or near the viewport are measured. Reading pixels back from seven full-size
   rasters in one go cost ~100ms of blocking time on a mid-range phone, for captions the reader
   could not see yet; spread across the scroll it costs nothing anyone can perceive. */
const captionPanels = Array.from(document.querySelectorAll('[data-label-tone]'));
const nearViewport = new Set();

function tuneNearbyPanels() {
  nearViewport.forEach(tunePanel);
}

let captionToneTimer = null;
function scheduleCaptionTones() {
  window.clearTimeout(captionToneTimer);
  captionToneTimer = window.setTimeout(tuneNearbyPanels, 150);
}

if (captionPanels.length && typeof IntersectionObserver === 'function') {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        nearViewport.add(entry.target);
        tunePanel(entry.target);
      } else {
        nearViewport.delete(entry.target);
      }
    });
  }, { rootMargin: '250px 0px' });
  captionPanels.forEach((panel) => {
    observer.observe(panel);
    // A lazy raster usually arrives after the panel is already in view, so the first useful
    // measurement is the one taken when it finishes decoding.
    const image = panel.querySelector('img');
    if (image && !image.complete) {
      image.addEventListener('load', () => { if (nearViewport.has(panel)) tunePanel(panel); }, { once: true });
    }
  });
  window.addEventListener('resize', scheduleCaptionTones);
} else {
  /* No IntersectionObserver: measure everything once, late, and on resize. */
  captionPanels.forEach((panel) => {
    nearViewport.add(panel);
    const image = panel.querySelector('img');
    if (image && !image.complete) image.addEventListener('load', scheduleCaptionTones, { once: true });
  });
  window.addEventListener('resize', scheduleCaptionTones);
  scheduleCaptionTones();
}

/* ------------------------------------------------------------------ */
/* WEB-005 cinematic hero                                              */
/*                                                                      */
/* The hero ships as a poster image with an empty <video> beside it.    */
/* Nothing about the video is declared in HTML except the two candidate */
/* URLs, because an <video> with <source> children starts fetching as   */
/* soon as it is parsed and that is a decision this file should own,    */
/* not the markup:                                                      */
/*                                                                      */
/*   - reduced motion, small screens, Save-Data and slow connections    */
/*     never attach a source at all, so they cost zero video bytes and  */
/*     get the poster as an intentional still hero rather than a        */
/*     degraded one;                                                    */
/*   - everyone else gets exactly ONE encode, chosen by canPlayType,    */
/*     so no browser is ever asked to download both;                    */
/*   - with JavaScript off, the poster is the hero.                     */
/*                                                                      */
/* The accepted sequence ends on a stable regional hold. What it hands  */
/* off to is the result element below it, which is revealed when the    */
/* hold is reached — or immediately, in every static state, so that a   */
/* visitor who never sees the motion still sees the answer.             */
/* ------------------------------------------------------------------ */
(function cinematicHero() {
  const hero = document.querySelector('.hero[data-hero-slot="cinematic"]');
  if (!hero) return;

  const video = hero.querySelector('.hero-video');
  const handoff = hero.querySelector('[data-hero-handoff]');

  /* Frame 200 of 276 at 24 fps: the first frame of the accepted regional-hold beat. */
  const HOLD_SECONDS = 200 / 24;

  function revealHandoff() {
    if (!handoff || !handoff.hidden) return;
    handoff.hidden = false;
    /* Two frames: one for the element to exist, one for the transition to have a start value. */
    requestAnimationFrame(() => requestAnimationFrame(() => handoff.classList.add('is-visible')));
  }

  function settleStatic(reason) {
    hero.setAttribute('data-hero-state', 'static');
    if (hero.dataset.heroReason !== reason) hero.dataset.heroReason = reason;
    revealHandoff();
  }

  const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection || {};
  const saveData = connection.saveData === true;
  const slowNetwork = typeof connection.effectiveType === 'string'
    && /^(slow-2g|2g|3g)$/.test(connection.effectiveType);
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  /* A phone-sized viewport is the reduced-data case in practice, and the hero reads as a still
     composition there anyway once the copy takes most of the frame. */
  const smallScreen = window.matchMedia('(max-width: 780px)');

  if (!video || typeof video.canPlayType !== 'function') return settleStatic('unsupported');
  if (reduceMotion.matches) return settleStatic('reduced-motion');
  if (smallScreen.matches) return settleStatic('small-screen');
  if (saveData) return settleStatic('save-data');
  if (slowNetwork) return settleStatic('slow-network');

  const candidates = [
    { src: video.getAttribute('data-hero-webm'), type: 'video/webm', probe: 'video/webm; codecs="vp9"' },
    { src: video.getAttribute('data-hero-mp4'), type: 'video/mp4', probe: 'video/mp4; codecs="avc1.4d4028"' },
    { src: video.getAttribute('data-hero-mp4'), type: 'video/mp4', probe: 'video/mp4' },
  ];
  const chosen = candidates.find((c) => c.src && video.canPlayType(c.probe) === 'probably')
    || candidates.find((c) => c.src && video.canPlayType(c.probe));
  if (!chosen) return settleStatic('no-playable-encode');

  let started = false;
  function start() {
    if (started) return;
    started = true;

    video.addEventListener('timeupdate', function onTime() {
      if (video.currentTime >= HOLD_SECONDS) {
        video.removeEventListener('timeupdate', onTime);
        revealHandoff();
      }
    });
    /* The last rendered frame is the poster frame, so ending on it is a settle, not a stop. */
    video.addEventListener('ended', () => {
      hero.setAttribute('data-hero-state', 'held');
      revealHandoff();
    });
    video.addEventListener('playing', () => {
      hero.setAttribute('data-hero-state', 'playing');
    }, { once: true });
    video.addEventListener('error', () => settleStatic('encode-error'), { once: true });

    video.muted = true;
    video.loop = false;
    video.setAttribute('src', chosen.src);
    video.load();

    const attempt = video.play();
    if (attempt && typeof attempt.catch === 'function') {
      /* Autoplay refused by policy is a normal outcome, not a failure: fall back to the poster
         and hand off straight away rather than leaving a blank frame or nagging the visitor. */
      attempt.catch(() => settleStatic('autoplay-blocked'));
    }
  }

  /* Never compete with the poster: the poster is the LCP element. */
  function startWhenIdle() {
    if (document.readyState === 'complete') start();
    else window.addEventListener('load', start, { once: true });
  }

  if (typeof IntersectionObserver === 'function') {
    const observer = new IntersectionObserver((entries, self) => {
      if (!entries.some((entry) => entry.isIntersecting)) return;
      self.disconnect();
      startWhenIdle();
    }, { rootMargin: '0px' });
    observer.observe(hero);
  } else {
    startWhenIdle();
  }

  /* A visitor who turns reduced motion on mid-visit gets the still hero from that point. */
  const onMotionChange = () => {
    if (!reduceMotion.matches) return;
    if (!video.paused) video.pause();
    settleStatic('reduced-motion');
  };
  if (typeof reduceMotion.addEventListener === 'function') {
    reduceMotion.addEventListener('change', onMotionChange);
  }

  /* Belt and braces: however playback goes, the result must not stay hidden. */
  window.setTimeout(revealHandoff, 15000);
})();
