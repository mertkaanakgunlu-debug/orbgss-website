/* OrbGSS — minimal vanilla JS: navigation, Solutions dropdown, EN/TR language switch, image-failure handling. */

/* ------------------------------------------------------------------ */
/* Translations. Keys map to data-i18n* attributes on the public pages. */
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
    'nav.solutions': 'Solutions',
    'nav.geothermal': 'Geothermal',
    'nav.mining': 'Mining',
    'nav.marine': 'Marine',
    'mail.partner': MAIL_EN,
    'hero.eyebrow': 'Earth data. Evidence. Priority.',
    'hero.title': 'Know where to look next.',
    'hero.copy': 'OrbGSS turns Earth observation and geoscience data into evidence-backed spatial priorities that help teams decide where to investigate next.',
    'hero.cta': 'See the pilot area',
    'hero.secondary': 'Partner With Us',
    'story.observe.note': 'Source and AOI context only — not validation evidence.',
    'story.terrain.note': 'Context and display only. Terrain is not a scored predictor and carries no universal geothermal-favourability direction.',
    'story.evidence.note': 'Evidence layers only — candidate and unvalidated. THM-01 is thermal evidence, not geothermal probability, reserve or resource, discovery or drilling-success evidence. ALT-01 and ALT-02 are broad spectral alteration proxies, never mineral or kaolinite identification, and not proof of hydrothermal alteration.',
    'evidence.switchLabel': 'Evidence layer',
    'story.priority.note': 'AOI-relative experimental screening only. Not probability, reserve or resource estimation, discovery likelihood, drilling-success likelihood, Full Prospectivity, or a score calibrated across areas.',
    'story.geothermal.note': 'First-application proof, not field validation, discovery, reserve or resource, drilling-target or drilling-success proof.',
    'scene.kind.naturalColor': 'Natural-color composite',
    'scene.aoi.place': 'Kızıldere, Denizli, Türkiye',
    'scene.aoi.coords': '37.9794° N, 28.7907° E',
    'label.priority': 'Remote-Sensing Relative Priority — Experimental Baseline',
    'alt.terrain.home': 'Colour elevation map of the Kızıldere area of interest, with low ground in dark green and high ridges in pale stone and white',
    'alt.thm01': 'Diverging thermal anomaly map of the Kızıldere area of interest, with cooler ground in blue and warmer ground in red',
    'alt.alt01': 'Map of the surface alteration signal across the Kızıldere area of interest, running from deep blue where the signal is weakest to yellow where it is strongest',
    'alt.priority': 'Relative priority map of the Kızıldere area of interest, ranking ground from 0 to 100 within the area',
    'act.context.title': 'A real area, before any analysis.',
    'act.context.copy': 'Kızıldere sits in the Büyük Menderes graben in Denizli, Türkiye. This is the area as Landsat 8 photographed it — the ground the whole pilot is registered to, before a single layer is derived from it.',
    'act.context.note': 'Earth-observation context only. This is a natural-colour photographic composite of the area, not analytical evidence, not a scored input, and not the acquisition date of any evidence layer.',
    'act.context.meta': 'Landsat 8 OLI · 2025-05-05 · 30 m · natural colour',
    'act.evidence.title': 'Three layers over the same ground.',
    'act.evidence.copy': 'The frame never moves. Same ground, same grid, same projection — only the evidence inside it changes, which is what makes the layers comparable at all.',
    'act.evidence.terrain.role': 'Context',
    'act.evidence.thermal.role': 'Evidence',
    'act.evidence.thermal.note': 'Evidence layer only. Do not describe it as geothermal probability, reserve, discovery, or drilling-success evidence.',
    'act.evidence.alteration.role': 'Evidence',
    'act.evidence.alteration.note': 'Broad Sentinel-2 spectral alteration proxy; not mineral identification and not proof of hydrothermal alteration.',
    'act.evidence.gapLabel': 'Data gap',
    'act.evidence.gap': 'Structural and geological evidence would sharpen interpretation here. OrbGSS has no public-safe fault or lithology layer for this baseline, so the gap is stated rather than filled — it is optional support and does not change the priority result.',
    'act.evidence.deeper': 'See every layer',
    'act.priority.title': 'Where to look first.',
    'act.priority.copy': 'The thermal and alteration evidence is combined into one ranking surface across the area of interest, 0 to 100, so a team can order the ground instead of guessing at it. High values mean “look here before there” — inside this area, for this baseline.',
    'act.priority.note': 'AOI-relative experimental screening only. Not probability, reserve/resource estimation, discovery likelihood, drilling-success likelihood, Full Prospectivity, or a calibrated cross-AOI score.',
    'act.priority.meta': 'mvp_remote_sensing_priority_v1 · EPSG:32635 · 30 m · 36 × 36 km',
    'act.priority.deeper': 'See the Kızıldere pilot',
    'scene.hero.place': 'Kızıldere — Büyük Menderes graben, Denizli, Türkiye',
    'scene.hero.coords': '37.9794° N, 28.7907° E',
    'scene.hero.kind': 'Rendered orbital sequence — not sensor imagery',
    'scene.context.place': 'Kızıldere — Büyük Menderes graben, Denizli, Türkiye',
    'scene.context.coords': '37.9794° N, 28.7907° E',
    'scene.context.kind': 'Natural-color composite',
    'scene.priority.place': 'Kızıldere — Büyük Menderes graben, Denizli, Türkiye',
    'scene.priority.coords': '37.9794° N, 28.7907° E',
    'alt.hero': 'Rendered view from orbit: Earth over the eastern Mediterranean, closing on the Kızıldere area in western Türkiye with a thin cyan outline around the 36 km analysis area',
    'alt.heroPriority': 'Rendered terrain relief of the Kızıldere analysis area with the Remote-Sensing Relative Priority — Experimental Baseline surface draped over it; terrain shows through where there is no analytical support',
    'alt.context': 'Natural-colour Landsat 8 view of the Büyük Menderes graben around Kızıldere, showing the valley floor, irrigated fields and the ridges on either side',
    'alt.priorityLegend': 'Colour scale for the relative priority map, running from 0 at the dark end to 100 at the pale end',
    'app.geothermal.title': 'Geothermal',
    'app.geothermal.status': 'Active · First application',
    'app.mining.title': 'Mining',
    'app.mining.status': 'Expansion direction',
    'app.marine.title': 'Marine',
    'app.marine.status': 'Expansion direction',
    'company.title': 'OrbGSS — Orbital Geo-Spatial Solutions',
    'company.copy': 'OrbGSS is a geospatial-intelligence platform built by VirgaSoft. It exists to make exploration and land decisions evidence-based, traceable and easier to prioritize.',
    'contact.cta': 'Partner With Us',
    'scene.yellowstone.place': 'Yellowstone National Park, USA',
    'scene.yellowstone.coords': '44.4604° N, 110.8282° W',
    'scene.chuquicamata.place': 'Chuquicamata, Antofagasta, Chile',
    'scene.chuquicamata.coords': '22.3150° S, 68.9010° W',
    'scene.ili.place': 'Ili River Delta & Lake Balkhash, Kazakhstan',
    'scene.ili.coords': '45.0600° N, 74.5200° E',
    'alt.yellowstone': 'Satellite view of the geothermal landscape around Yellowstone National Park',
    'alt.chuquicamata': 'Satellite view of the Chuquicamata mining district in northern Chile',
    'alt.ili': 'Satellite view of the Ili River Delta and Lake Balkhash in Kazakhstan',
    'footer.builtBy': 'Built by VirgaSoft',
    'footer.attribution': 'Landsat data courtesy of the U.S. Geological Survey. The hero is a rendered orbital sequence whose Earth texture is NASA Blue Marble with ground detail from modified Copernicus Sentinel-2 data (2025). The story panels are OrbGSS cartographic exports of the Kızıldere pilot area, derived from NASADEM elevation, Landsat thermal and Sentinel-2 alteration evidence, with Scientific colour maps v8.0 by Fabio Crameri.',
    'footer.copyright': '© 2026 OrbGSS. All rights reserved.',

    /* WEB-003 — deep public routes */
    'mail.pilot': MAIL_PILOT_EN,
    'mail.technical': MAIL_TECH_EN,


    'solutionsPage.meta.title': 'Solutions — OrbGSS',
    'solutionsPage.meta.description': 'Geothermal is active with a published pilot in Kızıldere, Türkiye. Mining and marine are expansion directions.',
    'solutionsPage.meta.ogDescription': 'Geothermal active, mining and marine next.',
    'solutionsPage.kicker': 'Solutions',
    'solutionsPage.title': 'Where OrbGSS works today, and where next.',
    'solutionsPage.intro': 'Geothermal is active, with a published pilot. Mining and marine are expansion directions: nothing is published for them yet.',



    /* WEB-005B R11 — the accepted final homepage design. */
    'act.evidence.shown': 'Shown',
    'act.evidence.terrain.index': '01',
    'act.evidence.terrain.tab': 'Terrain',
    'act.evidence.terrain.body': 'The shape of the ground — the valley floor, the ridges that bound it, and what the evidence layers sit on.',
    'act.evidence.terrain.meta': 'From NASADEM elevation data',
    'act.evidence.thermal.index': '02',
    'act.evidence.thermal.tab': 'Thermal',
    'act.evidence.thermal.body': 'Where the surface runs warmer or cooler than the rest of the area.',
    'act.evidence.thermal.meta': 'From Landsat thermal bands',
    'act.evidence.alteration.index': '03',
    'act.evidence.alteration.tab': 'Alteration',
    'act.evidence.alteration.body': 'Where the surface reflects light the way chemically altered rock tends to.',
    'act.evidence.alteration.meta': 'From Sentinel-2 reflectance',
    'act.evidence.shared.frame': 'One frame · 36 × 36 km · 30 m grid · EPSG:32635',
    'act.priority.def.is.term': 'What it is',
    'act.priority.def.is.copy': 'A within-area ranking of ground from 0 to 100, derived from the mapped evidence layers above.',
    'act.priority.def.why.term': 'Why it matters',
    'act.priority.def.why.copy': 'It turns a 36 × 36 km area into an ordered shortlist before anyone travels to it.',
    'act.priority.def.for.term': 'What it is for',
    'act.priority.def.for.copy': 'Deciding where to investigate next, with the evidence and its provenance attached.',
    'act.priority.def.not.term': 'What it is not',
    'inspect.kicker': 'Inspection aid',
    'inspect.title': 'Hold a layer against the photograph.',
    'inspect.copy': 'Wipe between the natural-colour view of the area of interest and one derived layer over the same ground. It is a way to look, not a published figure — and both sides are exactly the files published above.',
    'inspect.against': 'Natural colour against',
    'inspect.pairsLabel': 'Layer to compare',
    'inspect.pair.thermal': 'Thermal',
    'inspect.pair.alteration': 'Alteration',
    'inspect.pair.priority': 'Priority score',
    'inspect.rangeLabel': 'Reveal the selected layer over the natural-colour view',
    'inspect.tag.layer': 'Derived layer',
    'inspect.tag.photo': 'Natural colour',
    'inspect.note': 'A visual inspection aid, not a published report figure. Both sides are the files published above, on the same 36 × 36 km frame and the same 30 m grid; the wipe changes nothing about either. The published figures are the ones above.',
    'alt.inspectBase': 'Natural-colour Landsat view of the Kızıldere area of interest, the base of the comparison',
    'alt.inspectThermal': 'Thermal anomaly map of the same area of interest, revealed over the natural-colour view',
    'alt.inspectAlteration': 'Alteration proxy map of the same area of interest, revealed over the natural-colour view',
    'alt.inspectPriority': 'Relative priority map of the same area of interest, revealed over the natural-colour view',
    'domains.illustrativeLabel': 'Illustrative',
    'domains.illustrative': 'The three photographs above are public-domain Landsat scenes of other places, chosen to show the kind of ground each domain reads. They are not OrbGSS analytical outputs, not results, and not the Kızıldere pilot area.',
    'proof.evidence.title': 'Evidence-backed screening',
    'proof.provenance.title': 'Traceable provenance',
    'proof.gaps.title': 'Explicit data gaps',
    'proof.aoi.title': 'AOI-first analysis',
    'proof.narrowing.title': 'Remote narrowing',
    'proof.decision.title': 'Decision support',
    'proof.foot': 'No accuracy, performance, deployment, customer or scale figures are published for this baseline.',
    /* WEB-005B R14 — simplified evidence language and the Solutions section. */
    'act.evidence.terrain.name': 'Elevation',

    'act.evidence.thermal.name': 'Thermal anomaly',

    'act.evidence.alteration.name': 'Alteration signal',


    'solutions.title': 'One workflow, applied where the evidence supports it.',

    'solutions.copy': 'The same evidence-to-priority workflow, read against different ground. Each domain states where it actually stands, and nothing in development is presented as a finished product.',

    'solutions.listLabel': 'Solution domains',
    /* WEB-005B R13 — the accepted homepage domain taxonomy. Separate from the app.* application
       ledger, which /solutions/ publishes with its own wording. */
    'domain.geothermal.title': 'Geothermal',
    'domain.mining.title': 'Mining',
    'domain.marine.title': 'Marine',
    'nav.home': 'Home',
    'nav.about': 'About',
    'nav.partner': 'Partner with us',
    'footer.sources': 'Every source is listed on the About page.',
    'solutionsPage.glance.title': 'At a glance',
    'solutionsPage.col.domain': 'Domain',
    'solutionsPage.col.status': 'Status',
    'solutionsPage.col.ground': 'Ground it reads',
    'solutionsPage.col.published': 'Published today',
    'solutionsPage.ground.geothermal': 'Geothermal exploration ground',
    'solutionsPage.ground.mining': 'Mineral exploration targets',
    'solutionsPage.ground.marine': 'Coastal and marine ground',
    'solutionsPage.published.geothermal': 'The Kızıldere pilot',
    'solutionsPage.published.none': 'Nothing yet',
    'solutionsPage.band.pilot': 'See the Kızıldere pilot',
    'geothermalPage.meta.title': 'Geothermal — Kızıldere pilot — OrbGSS',
    'geothermalPage.meta.description': 'The Kızıldere geothermal pilot in Denizli, Türkiye: where it is, every published layer and its limits, and what is still missing.',
    'geothermalPage.meta.ogDescription': 'Kızıldere: the first published OrbGSS pilot.',
    'geothermalPage.title': 'Kızıldere: the first published pilot.',
    'geothermalPage.intro': 'Everything published for the pilot, in one place: where it is, which layers it holds, what each layer is not, and what is still missing.',
    'alt.locator': 'Map of Türkiye with the 36 km Kızıldere pilot area marked in Denizli',
    'scene.kind.locator': 'Locator map — Natural Earth',
    'geothermalPage.glance.title': 'The pilot at a glance',
    'geothermalPage.fact.area': 'Area',
    'geothermalPage.fact.areaValue': '36 × 36 km',
    'geothermalPage.fact.place': 'Place',
    'geothermalPage.fact.placeValue': 'Büyük Menderes graben, Denizli, Türkiye',
    'geothermalPage.fact.centre': 'Centre',
    'geothermalPage.fact.grid': 'Grid',
    'geothermalPage.fact.gridValue': '30 m, EPSG:32635, 1,200 × 1,200 cells',
    'geothermalPage.fact.layers': 'Layers',
    'geothermalPage.fact.layersValue': '2 context, 3 evidence, 1 priority surface',
    'geothermalPage.fact.score': 'Score',
    'geothermalPage.fact.scoreValue': 'Remote-Sensing Relative Priority — Experimental Baseline, 0–100 within the area',
    'geothermalPage.fact.missing': 'Not available',
    'geothermalPage.fact.missingValue': 'Structure and geology',
    'geothermalPage.layers.title': 'Every layer, and what it is not',
    'geothermalPage.col.layer': 'Layer',
    'geothermalPage.col.from': 'From',
    'geothermalPage.col.role': 'Role',
    'geothermalPage.col.not': 'What it is not',
    'geothermalPage.layer.natural': 'Natural colour',
    'geothermalPage.layer.iron': 'Second alteration signal (iron)',
    'geothermalPage.layer.priority': 'Priority',
    'geothermalPage.layer.pending': 'Accepted, not shown yet',
    'geothermalPage.from.natural': 'Landsat 8 OLI, 2025-05-05',
    'geothermalPage.from.elevation': 'NASADEM',
    'geothermalPage.from.thermal': 'Landsat thermal bands',
    'geothermalPage.from.sentinel': 'Sentinel-2',
    'geothermalPage.from.priority': 'The evidence layers',
    'geothermalPage.role.context': 'Context',
    'geothermalPage.role.evidence': 'Evidence',
    'geothermalPage.role.score': 'Score',
    'geothermalPage.outputs.title': 'What the pilot produced',
    'geothermalPage.col.output': 'Output',
    'geothermalPage.col.what': 'What it is',
    'geothermalPage.output.area': 'Area definition',
    'geothermalPage.output.areaValue': 'One boundary, grid and projection for every layer',
    'geothermalPage.output.context': 'Context layers',
    'geothermalPage.output.contextValue': 'Natural colour and elevation, for orientation only',
    'geothermalPage.output.evidence': 'Evidence layers',
    'geothermalPage.output.evidenceValue': 'Mapped remote-sensing signals, each with its limits',
    'geothermalPage.output.gap': 'Data-gap statement',
    'geothermalPage.output.gapValue': 'What is missing, stated instead of filled',
    'geothermalPage.output.priority': 'Priority surface',
    'geothermalPage.output.priorityValue': 'One within-area ranking, 0 to 100',
    'geothermalPage.output.provenance': 'Provenance record',
    'geothermalPage.output.provenanceValue': 'The source and export behind every visual',
    'geothermalPage.gap.title': 'Not available: structure and geology',
    'geothermalPage.gap.frame': 'No public-safe fault or lithology layer',
    'geothermalPage.gap.copy': 'No public-safe fault or lithology layer is authorized for this pilot. The gap is shown, not filled, and it does not change the priority: structure and geology are optional support and score-invariant.',
    'geothermalPage.next': 'Discuss a pilot',
    'aboutPage.meta.title': 'About — OrbGSS',
    'aboutPage.meta.description': 'OrbGSS — Orbital Geo-Spatial Solutions, built by VirgaSoft: the principles it publishes by and every data source it uses.',
    'aboutPage.meta.ogDescription': 'OrbGSS — Orbital Geo-Spatial Solutions, built by VirgaSoft.',
    'aboutPage.kicker': 'About',
    'aboutPage.principles.title': 'How OrbGSS publishes',
    'aboutPage.col.principle': 'Principle',
    'aboutPage.col.means': 'What it means',
    'aboutPage.col.see': 'See it',
    'aboutPage.principle.evidence': 'Priorities come from mapped layers, not an unexplained model output.',
    'aboutPage.principle.provenance': 'Every published visual maps back to a source and a recorded export.',
    'aboutPage.principle.gaps': 'A missing layer is published as missing, never invented.',
    'aboutPage.principle.aoi': 'One declared area, projection and grid before any interpretation.',
    'aboutPage.principle.narrowing': 'Large areas are ordered from orbit before field time is committed.',
    'aboutPage.principle.decision': 'Helps decide where to investigate; field investigation remains necessary.',
    'aboutPage.see.evidence': 'The three layers',
    'aboutPage.see.sources': 'Data sources',
    'aboutPage.see.gap': 'Structure and geology',
    'aboutPage.see.glance': 'The pilot at a glance',
    'aboutPage.see.priority': 'Where to look first',
    'aboutPage.sources.title': 'Data and imagery sources',
    'aboutPage.col.source': 'Source',
    'aboutPage.col.used': 'Used for',
    'aboutPage.col.credit': 'Credit',
    'aboutPage.source.landsat': 'Landsat 8 (USGS)',
    'aboutPage.source.landsatUse': 'Natural colour, thermal evidence, domain photographs',
    'aboutPage.source.landsatCredit': 'Landsat data courtesy of the U.S. Geological Survey',
    'aboutPage.source.nasadem': 'NASADEM (NASA)',
    'aboutPage.source.nasademUse': 'Elevation and relief',
    'aboutPage.source.nasademCredit': 'NASADEM elevation, via NASA Earthdata',
    'aboutPage.source.sentinel': 'Copernicus Sentinel-2',
    'aboutPage.source.sentinelUse': 'Alteration evidence; hero ground detail',
    'aboutPage.source.sentinelCredit': 'Contains modified Copernicus Sentinel data (2025)',
    'aboutPage.source.bluemarble': 'NASA Blue Marble',
    'aboutPage.source.bluemarbleUse': 'The rendered hero’s Earth texture',
    'aboutPage.source.bluemarbleCredit': 'NASA Earth Observatory; public domain',
    'aboutPage.source.crameri': 'Scientific colour maps v8.0',
    'aboutPage.source.crameriUse': 'Map palettes',
    'aboutPage.source.crameriCredit': 'Fabio Crameri; MIT licence',
    'aboutPage.source.naturalearth': 'Natural Earth',
    'aboutPage.source.naturalearthUse': 'The Kızıldere locator map',
    'aboutPage.source.naturalearthCredit': 'Made with Natural Earth; public domain',
    'partnerPage.meta.title': 'Partner with us — OrbGSS',
    'partnerPage.meta.description': 'Reach OrbGSS for pilot, partnership and technical conversations. contact@orbgss.com.',
    'partnerPage.meta.ogDescription': 'For pilot, partnership and technical conversations.',
    'partnerPage.title': "Let's talk about where to look next.",
    'partnerPage.intro': 'OrbGSS is available for pilot, partnership and technical conversations. Reach out directly by email — there is no form to fill in.',
    'partnerPage.direct.label': 'Direct',
    'partnerPage.conversations.title': 'Which conversation',
    'partnerPage.col.conversation': 'Conversation',
    'partnerPage.col.covers': 'What it covers',
    'partnerPage.col.write': 'Write',
    'partnerPage.write': 'Write',
    'partnerPage.pilot.title': 'Pilot',
    'partnerPage.pilot.copy': 'A geothermal pilot, or a first application in a new area.',
    'partnerPage.partnership.title': 'Partnership',
    'partnerPage.partnership.copy': 'A partnership or collaboration with OrbGSS.',
    'partnerPage.technical.title': 'Technical',
    'partnerPage.technical.copy': 'The evidence, its limits, or how a pilot would be scoped.',
    'notFound.meta.title': 'Page not found — OrbGSS',
    'notFound.title': 'This page is outside the area of interest.',
    'notFound.home': 'Return to OrbGSS',
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
    'nav.solutions': 'Çözümler',
    'nav.geothermal': 'Jeotermal',
    'nav.mining': 'Madencilik',
    'nav.marine': 'Denizel',
    'mail.partner': MAIL_TR,
    'hero.eyebrow': 'Dünya verisi. Kanıt. Öncelik.',
    'hero.title': 'Sırada nereye bakacağınızı bilin.',
    'hero.copy': 'OrbGSS, yer gözlem ve yer bilimi verilerini kanıta dayalı mekânsal önceliklere dönüştürür; ekiplerin sırada nerenin inceleneceğine karar vermesine yardımcı olur.',
    'hero.cta': 'Pilot alanı görün',
    'hero.secondary': 'İş Birliği Kurun',
    'story.observe.note': 'Yalnızca kaynak ve alan bağlamı — doğrulama kanıtı değildir.',
    'story.terrain.note': 'Yalnızca bağlam ve görüntüleme amaçlıdır. Topoğrafya skorlanan bir öngörücü değildir ve evrensel bir jeotermal uygunluk yönü taşımaz.',
    'story.evidence.note': 'Yalnızca kanıt katmanları — aday ve doğrulanmamış. THM-01 termal kanıttır; jeotermal olasılık, rezerv veya kaynak, keşif ya da sondaj başarısı kanıtı değildir. ALT-01 ve ALT-02 geniş bantlı spektral alterasyon vekilleridir; mineral veya kaolinit tanımlaması değildir ve hidrotermal alterasyon kanıtı sayılmaz.',
    'evidence.switchLabel': 'Kanıt katmanı',
    'story.priority.note': 'Yalnızca alan içi deneysel ön eleme. Olasılık, rezerv veya kaynak tahmini, keşif olasılığı, sondaj başarısı olasılığı, Tam Prospektivite ya da alanlar arası kalibre edilmiş bir skor değildir.',
    'story.geothermal.note': 'İlk uygulama kanıtıdır; saha doğrulaması, keşif, rezerv veya kaynak, sondaj hedefi ya da sondaj başarısı kanıtı değildir.',
    'scene.kind.naturalColor': 'Doğal renkli kompozit',
    'scene.aoi.place': 'Kızıldere, Denizli, Türkiye',
    'scene.aoi.coords': '37.9794° K, 28.7907° D',
    'label.priority': 'Uzaktan Algılama Göreli Önceliği — Deneysel Temel',
    'alt.terrain.home': 'Kızıldere ilgi alanının renkli yükselti haritası; alçak zemin koyu yeşil, yüksek sırtlar açık taş rengi ve beyaz',
    'alt.thm01': 'Kızıldere ilgi alanının ıraksak termal anomali haritası; daha serin zemin mavi, daha sıcak zemin kırmızı',
    'alt.alt01': 'Kızıldere ilgi alanı boyunca yüzey alterasyon sinyalinin haritası; sinyalin en zayıf olduğu yerde koyu mavi, en güçlü olduğu yerde sarı',
    'alt.priority': 'Kızıldere ilgi alanının göreli öncelik haritası; zemini alan içinde 0 ile 100 arasında sıralar',
    'act.context.title': 'Herhangi bir analizden önce, gerçek bir alan.',
    'act.context.copy': 'Kızıldere, Denizli, Türkiye’deki Büyük Menderes grabeninde yer alır. Bu, alanın Landsat 8 tarafından görüntülenmiş hâlidir — tek bir katman türetilmeden önce, pilot çalışmanın tamamının üzerine oturduğu zemin.',
    'act.context.note': 'Yalnızca Yer gözlem bağlamı. Bu, alanın doğal renkli fotografik bileşimidir; analitik kanıt değildir, skorlanan bir girdi değildir ve herhangi bir kanıt katmanının görüntüleme tarihi değildir.',
    'act.context.meta': 'Landsat 8 OLI · 2025-05-05 · 30 m · doğal renk',
    'act.evidence.title': 'Aynı zemin üzerinde üç katman.',
    'act.evidence.copy': 'Çerçeve hiç değişmiyor. Aynı zemin, aynı ızgara, aynı projeksiyon — yalnızca içindeki kanıt değişiyor; katmanları karşılaştırılabilir kılan da bu.',
    'act.evidence.terrain.role': 'Bağlam',
    'act.evidence.thermal.role': 'Kanıt',
    'act.evidence.thermal.note': 'Yalnızca kanıt katmanı. Jeotermal olasılık, rezerv, keşif ya da sondaj başarısı kanıtı olarak tanımlanmamalıdır.',
    'act.evidence.alteration.role': 'Kanıt',
    'act.evidence.alteration.note': 'Geniş bantlı Sentinel-2 spektral alterasyon vekili; mineral tanımlaması değildir ve hidrotermal alterasyon kanıtı değildir.',
    'act.evidence.gapLabel': 'Veri boşluğu',
    'act.evidence.gap': 'Yapısal ve jeolojik kanıt burada yorumu keskinleştirirdi. OrbGSS bu temel sürüm için kamuya açık kullanıma uygun bir fay veya litoloji katmanına sahip değildir; bu nedenle boşluk doldurulmak yerine açıkça belirtilir — isteğe bağlı destektir ve öncelik sonucunu değiştirmez.',
    'act.evidence.deeper': 'Tüm katmanları görün',
    'act.priority.title': 'Önce nereye bakmalı.',
    'act.priority.copy': 'Termal ve alterasyon kanıtı, ilgi alanı genelinde 0–100 aralığında tek bir sıralama yüzeyinde birleştirilir; böylece bir ekip zemini tahmin etmek yerine sıralayabilir. Yüksek değerler, bu alan içinde ve bu temel sürüm için “önce şuraya bak” anlamına gelir.',
    'act.priority.note': 'Yalnızca alan içi deneysel ön eleme. Olasılık, rezerv veya kaynak tahmini, keşif olasılığı, sondaj başarısı olasılığı, Tam Prospektivite ya da alanlar arası kalibre edilmiş bir skor değildir.',
    'act.priority.meta': 'mvp_remote_sensing_priority_v1 · EPSG:32635 · 30 m · 36 × 36 km',
    'act.priority.deeper': 'Kızıldere pilotunu görün',
    'scene.hero.place': 'Kızıldere — Büyük Menderes grabeni, Denizli, Türkiye',
    'scene.hero.coords': '37.9794° K, 28.7907° D',
    'scene.hero.kind': 'Görselleştirilmiş yörünge sekansı — sensör görüntüsü değildir',
    'scene.context.place': 'Kızıldere — Büyük Menderes grabeni, Denizli, Türkiye',
    'scene.context.coords': '37.9794° K, 28.7907° D',
    'scene.context.kind': 'Doğal renkli bileşim',
    'scene.priority.place': 'Kızıldere — Büyük Menderes grabeni, Denizli, Türkiye',
    'scene.priority.coords': '37.9794° K, 28.7907° D',
    'alt.hero': 'Yörüngeden görselleştirilmiş görünüm: Doğu Akdeniz üzerinde Dünya, Batı Türkiye’deki Kızıldere bölgesine yaklaşır; 36 km’lik analiz alanının çevresinde ince camgöbeği bir çerçeve ile',
    'alt.heroPriority': 'Kızıldere analiz alanının görselleştirilmiş arazi kabartması; üzerine Uzaktan Algılama Göreli Önceliği — Deneysel Temel yüzeyi giydirilmiştir; analitik desteğin olmadığı yerlerde arazi görünür',
    'alt.context': 'Kızıldere çevresindeki Büyük Menderes grabeninin doğal renkli Landsat 8 görünümü; vadi tabanı, sulanan tarlalar ve iki yandaki sırtlar görülüyor',
    'alt.priorityLegend': 'Göreli öncelik haritasının renk ölçeği; koyu uçta 0 değerinden açık uçta 100 değerine uzanır',
    'app.geothermal.title': 'Jeotermal',
    'app.geothermal.status': 'Aktif · İlk uygulama',
    'app.mining.title': 'Madencilik',
    'app.mining.status': 'Genişleme yönü',
    'app.marine.title': 'Denizel',
    'app.marine.status': 'Genişleme yönü',
    'company.title': 'OrbGSS — Orbital Geo-Spatial Solutions',
    'company.copy': 'OrbGSS, VirgaSoft tarafından geliştirilen bir coğrafi zekâ platformudur. Arama ve arazi kararlarını kanıta dayalı, izlenebilir ve önceliklendirilmesi kolay hâle getirmek için vardır.',
    'contact.cta': 'İş Birliği Kurun',
    'scene.yellowstone.place': 'Yellowstone Ulusal Parkı, ABD',
    'scene.yellowstone.coords': '44.4604° K, 110.8282° B',
    // Pre-uppercased: Turkish locale casing would otherwise render the Spanish name as "CHUQUİCAMATA".
    'scene.chuquicamata.place': 'CHUQUICAMATA, ANTOFAGASTA, ŞİLİ',
    'scene.chuquicamata.coords': '22.3150° G, 68.9010° B',
    'scene.ili.place': 'İli Nehri Deltası ve Balkaş Gölü, Kazakistan',
    'scene.ili.coords': '45.0600° K, 74.5200° D',
    'alt.yellowstone': 'Yellowstone Ulusal Parkı çevresindeki jeotermal arazinin uydu görüntüsü',
    'alt.chuquicamata': 'Kuzey Şili Chuquicamata madencilik bölgesinin uydu görüntüsü',
    'alt.ili': 'Kazakistan İli Nehri Deltası ve Balkaş Gölü uydu görüntüsü',
    'footer.builtBy': 'VirgaSoft tarafından geliştirildi',
    'footer.attribution': 'Landsat verileri ABD Jeoloji Araştırmaları Kurumu (USGS) kaynaklıdır. Açılış görseli, görselleştirilmiş bir yörünge sekansıdır; Dünya dokusu NASA Blue Marble’dır ve zemin detayı değiştirilmiş Copernicus Sentinel-2 verilerinden (2025) gelir. Bölüm görselleri ise NASADEM yükselti, Landsat termal ve Sentinel-2 alterasyon kanıtlarından türetilen, Kızıldere pilot alanına ait OrbGSS kartografik dışa aktarımlarıdır; renk skalaları Fabio Crameri, Scientific colour maps v8.0.',
    'footer.copyright': '© 2026 OrbGSS. Tüm hakları saklıdır.',

    /* WEB-003 — deep public routes */
    'mail.pilot': MAIL_PILOT_TR,
    'mail.technical': MAIL_TECH_TR,


    'solutionsPage.meta.title': 'Çözümler — OrbGSS',
    'solutionsPage.meta.description': "Jeotermal aktif ve Kızıldere, Türkiye'de yayımlanmış bir pilotu var. Madencilik ve denizel genişleme yönleridir.",
    'solutionsPage.meta.ogDescription': 'Jeotermal aktif; sırada madencilik ve denizel var.',
    'solutionsPage.kicker': 'Çözümler',
    'solutionsPage.title': 'OrbGSS bugün nerede çalışıyor, sırada ne var.',
    'solutionsPage.intro': 'Jeotermal aktif ve yayımlanmış bir pilotu var. Madencilik ve denizel genişleme yönleri: bunlar için henüz yayımlanmış bir şey yok.',



    /* WEB-005B R11 — the accepted final homepage design. */
    'act.evidence.shown': 'Gösteriliyor',
    'act.evidence.terrain.index': '01',
    'act.evidence.terrain.tab': 'Arazi',
    'act.evidence.terrain.body': 'Zeminin biçimi — vadi tabanı, onu sınırlayan sırtlar ve kanıt katmanlarının üzerine oturduğu yüzey.',
    'act.evidence.terrain.meta': 'NASADEM yükselti verisinden',
    'act.evidence.thermal.index': '02',
    'act.evidence.thermal.tab': 'Termal',
    'act.evidence.thermal.body': 'Yüzeyin, alanın geri kalanına göre daha sıcak ya da daha soğuk olduğu yerler.',
    'act.evidence.thermal.meta': 'Landsat termal bantlarından',
    'act.evidence.alteration.index': '03',
    'act.evidence.alteration.tab': 'Alterasyon',
    'act.evidence.alteration.body': 'Yüzeyin, kimyasal olarak değişime uğramış kayaçların yansıttığı biçimde ışık yansıttığı yerler.',
    'act.evidence.alteration.meta': 'Sentinel-2 yansıtımından',
    'act.evidence.shared.frame': 'Tek çerçeve · 36 × 36 km · 30 m ızgara · EPSG:32635',
    'act.priority.def.is.term': 'Ne olduğu',
    'act.priority.def.is.copy': 'Yukarıdaki haritalanmış kanıt katmanlarından türetilen, alan içi 0-100 zemin sıralaması.',
    'act.priority.def.why.term': 'Neden önemli',
    'act.priority.def.why.copy': "36 × 36 km'lik bir alanı, kimse oraya gitmeden önce sıralı bir kısa listeye dönüştürür.",
    'act.priority.def.for.term': 'Ne için',
    'act.priority.def.for.copy': 'Kanıtı ve kökeni ekli hâlde, sırada nerenin inceleneceğine karar vermek.',
    'act.priority.def.not.term': 'Ne olmadığı',
    'inspect.kicker': 'İnceleme aracı',
    'inspect.title': 'Bir katmanı fotoğrafın karşısına koyun.',
    'inspect.copy': 'İlgi alanının doğal renkli görünümü ile aynı zemin üzerindeki bir türetilmiş katman arasında gezinin. Bu bir bakma yöntemidir, yayımlanmış bir şekil değildir — ve iki taraf da tam olarak yukarıda yayımlanan dosyalardır.',
    'inspect.against': 'Doğal rengin karşısında',
    'inspect.pairsLabel': 'Karşılaştırılacak katman',
    'inspect.pair.thermal': 'Termal',
    'inspect.pair.alteration': 'Alterasyon',
    'inspect.pair.priority': 'Öncelik skoru',
    'inspect.rangeLabel': 'Seçili katmanı doğal renkli görünümün üzerinde açın',
    'inspect.tag.layer': 'Türetilmiş katman',
    'inspect.tag.photo': 'Doğal renk',
    'inspect.note': 'Görsel bir inceleme aracıdır, yayımlanmış bir rapor şekli değildir. Her iki taraf da yukarıda yayımlanan dosyalardır; aynı 36 × 36 km çerçeve ve aynı 30 m ızgara üzerindedir ve bu geçiş hiçbirini değiştirmez. Yayımlanmış şekiller yukarıdakilerdir.',
    'alt.inspectBase': 'Kızıldere ilgi alanının doğal renkli Landsat görünümü; karşılaştırmanın temeli',
    'alt.inspectThermal': 'Aynı ilgi alanının termal anomali haritası, doğal renkli görünümün üzerinde açılmış',
    'alt.inspectAlteration': 'Aynı ilgi alanının alterasyon vekili haritası, doğal renkli görünümün üzerinde açılmış',
    'alt.inspectPriority': 'Aynı ilgi alanının göreli öncelik haritası, doğal renkli görünümün üzerinde açılmış',
    'domains.illustrativeLabel': 'Örnekleme',
    'domains.illustrative': 'Yukarıdaki üç fotoğraf, her alanın okuduğu zemin türünü göstermek için seçilmiş, başka yerlere ait kamuya açık Landsat sahneleridir. OrbGSS analitik çıktısı değildir, sonuç değildir ve Kızıldere pilot alanı değildir.',
    'proof.evidence.title': 'Kanıta dayalı ön eleme',
    'proof.provenance.title': 'İzlenebilir kaynak',
    'proof.gaps.title': 'Açık veri boşlukları',
    'proof.aoi.title': 'Önce ilgi alanı analizi',
    'proof.narrowing.title': 'Uzaktan daraltma',
    'proof.decision.title': 'Karar desteği',
    'proof.foot': 'Bu temel sürüm için doğruluk, performans, devreye alma, müşteri veya ölçek rakamı yayımlanmaz.',
    /* WEB-005B R14 — simplified evidence language and the Solutions section. */
    'act.evidence.terrain.name': 'Yükselti',

    'act.evidence.thermal.name': 'Termal anomali',

    'act.evidence.alteration.name': 'Alterasyon işareti',


    'solutions.title': 'Tek bir iş akışı, kanıtın desteklediği her yerde uygulanır.',

    'solutions.copy': 'Aynı kanıttan önceliğe iş akışı, farklı zeminler üzerinde okunur. Her alan bulunduğu noktayı açıkça belirtir; geliştirme aşamasındaki hiçbir şey tamamlanmış ürün olarak sunulmaz.',

    'solutions.listLabel': 'Çözüm alanları',
    /* WEB-005B R13 — the accepted homepage domain taxonomy. Separate from the app.* application
       ledger, which /solutions/ publishes with its own wording. */
    'domain.geothermal.title': 'Jeotermal',
    'domain.mining.title': 'Madencilik',
    'domain.marine.title': 'Denizel',
    'nav.home': 'Ana Sayfa',
    'nav.about': 'Hakkımızda',
    'nav.partner': 'İş Birliği',
    'footer.sources': 'Tüm kaynaklar Hakkımızda sayfasında listelenir.',
    'solutionsPage.glance.title': 'Bir bakışta',
    'solutionsPage.col.domain': 'Alan',
    'solutionsPage.col.status': 'Durum',
    'solutionsPage.col.ground': 'Okuduğu zemin',
    'solutionsPage.col.published': 'Bugün yayımlanan',
    'solutionsPage.ground.geothermal': 'Jeotermal arama zemini',
    'solutionsPage.ground.mining': 'Maden arama hedefleri',
    'solutionsPage.ground.marine': 'Kıyı ve deniz zemini',
    'solutionsPage.published.geothermal': 'Kızıldere pilotu',
    'solutionsPage.published.none': 'Henüz yok',
    'solutionsPage.band.pilot': 'Kızıldere pilotunu görün',
    'geothermalPage.meta.title': 'Jeotermal — Kızıldere pilotu — OrbGSS',
    'geothermalPage.meta.description': "Denizli, Türkiye'deki Kızıldere jeotermal pilotu: nerede olduğu, yayımlanan her katman ve sınırları, ve neyin hâlâ eksik olduğu.",
    'geothermalPage.meta.ogDescription': 'Kızıldere: yayımlanan ilk OrbGSS pilotu.',
    'geothermalPage.title': 'Kızıldere: yayımlanan ilk pilot.',
    'geothermalPage.intro': 'Pilot için yayımlanan her şey tek yerde: nerede olduğu, hangi katmanları içerdiği, her katmanın ne olmadığı ve neyin hâlâ eksik olduğu.',
    'alt.locator': "Denizli'de 36 km'lik Kızıldere pilot alanının işaretlendiği Türkiye haritası",
    'scene.kind.locator': 'Konum haritası — Natural Earth',
    'geothermalPage.glance.title': 'Bir bakışta pilot',
    'geothermalPage.fact.area': 'Alan',
    'geothermalPage.fact.areaValue': '36 × 36 km',
    'geothermalPage.fact.place': 'Yer',
    'geothermalPage.fact.placeValue': 'Büyük Menderes grabeni, Denizli, Türkiye',
    'geothermalPage.fact.centre': 'Merkez',
    'geothermalPage.fact.grid': 'Izgara',
    'geothermalPage.fact.gridValue': '30 m, EPSG:32635, 1.200 × 1.200 hücre',
    'geothermalPage.fact.layers': 'Katmanlar',
    'geothermalPage.fact.layersValue': '2 bağlam, 3 kanıt, 1 öncelik yüzeyi',
    'geothermalPage.fact.score': 'Skor',
    'geothermalPage.fact.scoreValue': 'Uzaktan Algılama Göreli Önceliği — Deneysel Temel, alan içinde 0–100',
    'geothermalPage.fact.missing': 'Mevcut değil',
    'geothermalPage.fact.missingValue': 'Yapı ve jeoloji',
    'geothermalPage.layers.title': 'Her katman ve ne olmadığı',
    'geothermalPage.col.layer': 'Katman',
    'geothermalPage.col.from': 'Kaynak',
    'geothermalPage.col.role': 'Rol',
    'geothermalPage.col.not': 'Ne olmadığı',
    'geothermalPage.layer.natural': 'Doğal renk',
    'geothermalPage.layer.iron': 'İkinci alterasyon işareti (demir)',
    'geothermalPage.layer.priority': 'Öncelik',
    'geothermalPage.layer.pending': 'Kabul edildi, henüz gösterilmiyor',
    'geothermalPage.from.natural': 'Landsat 8 OLI, 2025-05-05',
    'geothermalPage.from.elevation': 'NASADEM',
    'geothermalPage.from.thermal': 'Landsat termal bantları',
    'geothermalPage.from.sentinel': 'Sentinel-2',
    'geothermalPage.from.priority': 'Kanıt katmanları',
    'geothermalPage.role.context': 'Bağlam',
    'geothermalPage.role.evidence': 'Kanıt',
    'geothermalPage.role.score': 'Skor',
    'geothermalPage.outputs.title': 'Pilotun ürettikleri',
    'geothermalPage.col.output': 'Çıktı',
    'geothermalPage.col.what': 'Nedir',
    'geothermalPage.output.area': 'Alan tanımı',
    'geothermalPage.output.areaValue': 'Her katman için tek sınır, ızgara ve projeksiyon',
    'geothermalPage.output.context': 'Bağlam katmanları',
    'geothermalPage.output.contextValue': 'Doğal renk ve yükselti, yalnızca yön bulmak için',
    'geothermalPage.output.evidence': 'Kanıt katmanları',
    'geothermalPage.output.evidenceValue': 'Haritalanmış uzaktan algılama işaretleri, her biri kendi sınırlarıyla',
    'geothermalPage.output.gap': 'Veri boşluğu beyanı',
    'geothermalPage.output.gapValue': 'Eksik olan, doldurulmak yerine belirtilir',
    'geothermalPage.output.priority': 'Öncelik yüzeyi',
    'geothermalPage.output.priorityValue': 'Alan içinde tek bir sıralama, 0 ile 100 arası',
    'geothermalPage.output.provenance': 'Köken kaydı',
    'geothermalPage.output.provenanceValue': 'Her görselin ardındaki kaynak ve dışa aktarım',
    'geothermalPage.gap.title': 'Mevcut değil: yapı ve jeoloji',
    'geothermalPage.gap.frame': 'Kamuya açık kullanıma uygun fay veya litoloji katmanı yok',
    'geothermalPage.gap.copy': 'Bu pilot için kamuya açık kullanıma uygun bir fay veya litoloji katmanı yetkilendirilmemiştir. Boşluk doldurulmaz, gösterilir ve önceliği değiştirmez: yapı ve jeoloji isteğe bağlı destektir, skoru etkilemez.',
    'geothermalPage.next': 'Pilot görüşün',
    'aboutPage.meta.title': 'Hakkımızda — OrbGSS',
    'aboutPage.meta.description': 'OrbGSS — Orbital Geo-Spatial Solutions, VirgaSoft tarafından geliştirildi: yayın ilkeleri ve kullandığı tüm veri kaynakları.',
    'aboutPage.meta.ogDescription': 'OrbGSS — Orbital Geo-Spatial Solutions, VirgaSoft tarafından geliştirildi.',
    'aboutPage.kicker': 'Hakkımızda',
    'aboutPage.principles.title': 'OrbGSS nasıl yayımlar',
    'aboutPage.col.principle': 'İlke',
    'aboutPage.col.means': 'Anlamı',
    'aboutPage.col.see': 'Görün',
    'aboutPage.principle.evidence': 'Öncelikler açıklanmamış bir model çıktısından değil, haritalanmış katmanlardan gelir.',
    'aboutPage.principle.provenance': 'Yayımlanan her görsel bir kaynağa ve kayıtlı bir dışa aktarıma bağlanır.',
    'aboutPage.principle.gaps': 'Eksik bir katman eksik olarak yayımlanır, asla uydurulmaz.',
    'aboutPage.principle.aoi': 'Her yorumdan önce tek bir tanımlı alan, projeksiyon ve ızgara.',
    'aboutPage.principle.narrowing': 'Saha zamanı ayrılmadan önce geniş alanlar yörüngeden sıralanır.',
    'aboutPage.principle.decision': 'Nerede araştırma yapılacağına karar vermeye yardımcı olur; saha araştırması yine gereklidir.',
    'aboutPage.see.evidence': 'Üç katman',
    'aboutPage.see.sources': 'Veri kaynakları',
    'aboutPage.see.gap': 'Yapı ve jeoloji',
    'aboutPage.see.glance': 'Bir bakışta pilot',
    'aboutPage.see.priority': 'Önce nereye bakılmalı',
    'aboutPage.sources.title': 'Veri ve görüntü kaynakları',
    'aboutPage.col.source': 'Kaynak',
    'aboutPage.col.used': 'Kullanıldığı yer',
    'aboutPage.col.credit': 'Atıf',
    'aboutPage.source.landsat': 'Landsat 8 (USGS)',
    'aboutPage.source.landsatUse': 'Doğal renk, termal kanıt, alan fotoğrafları',
    'aboutPage.source.landsatCredit': 'Landsat verileri ABD Jeoloji Araştırmaları Kurumu (USGS) kaynaklıdır',
    'aboutPage.source.nasadem': 'NASADEM (NASA)',
    'aboutPage.source.nasademUse': 'Yükselti ve rölyef',
    'aboutPage.source.nasademCredit': 'NASADEM yükselti verisi, NASA Earthdata aracılığıyla',
    'aboutPage.source.sentinel': 'Copernicus Sentinel-2',
    'aboutPage.source.sentinelUse': 'Alterasyon kanıtı; açılış görselinin zemin detayı',
    'aboutPage.source.sentinelCredit': 'Contains modified Copernicus Sentinel data (2025)',
    'aboutPage.source.bluemarble': 'NASA Blue Marble',
    'aboutPage.source.bluemarbleUse': 'Açılış görselinin Dünya dokusu',
    'aboutPage.source.bluemarbleCredit': 'NASA Earth Observatory; kamu malı',
    'aboutPage.source.crameri': 'Scientific colour maps v8.0',
    'aboutPage.source.crameriUse': 'Harita paletleri',
    'aboutPage.source.crameriCredit': 'Fabio Crameri; MIT lisansı',
    'aboutPage.source.naturalearth': 'Natural Earth',
    'aboutPage.source.naturalearthUse': 'Kızıldere konum haritası',
    'aboutPage.source.naturalearthCredit': 'Made with Natural Earth; kamu malı',
    'partnerPage.meta.title': 'İş Birliği — OrbGSS',
    'partnerPage.meta.description': "Pilot, iş birliği ve teknik görüşmeler için OrbGSS'e ulaşın. contact@orbgss.com.",
    'partnerPage.meta.ogDescription': 'Pilot, iş birliği ve teknik görüşmeler için.',
    'partnerPage.title': 'Sırada nereye bakacağımızı konuşalım.',
    'partnerPage.intro': 'OrbGSS; pilot, iş birliği ve teknik görüşmeler için ulaşılabilir durumdadır. Doğrudan e-posta ile yazın — doldurulacak bir form yok.',
    'partnerPage.direct.label': 'Doğrudan',
    'partnerPage.conversations.title': 'Hangi görüşme',
    'partnerPage.col.conversation': 'Görüşme',
    'partnerPage.col.covers': 'Kapsamı',
    'partnerPage.col.write': 'Yazın',
    'partnerPage.write': 'Yazın',
    'partnerPage.pilot.title': 'Pilot',
    'partnerPage.pilot.copy': 'Bir jeotermal pilot ya da yeni bir alanda ilk uygulama.',
    'partnerPage.partnership.title': 'İş birliği',
    'partnerPage.partnership.copy': 'OrbGSS ile bir iş birliği ya da ortaklık.',
    'partnerPage.technical.title': 'Teknik',
    'partnerPage.technical.copy': 'Kanıt, sınırları ya da bir pilotun nasıl kapsamlandırılacağı.',
    'notFound.meta.title': 'Sayfa bulunamadı — OrbGSS',
    'notFound.title': 'Bu sayfa ilgi alanının dışında.',
    'notFound.home': "OrbGSS'e dönün",
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
document.querySelectorAll('.panel-image, .story-panel > img, .evidence-plate img, .domain-card > img, .domain-band > img, .locator-figure > img, .inspect-frame img').forEach((image) => {
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
/* The sequence ends on a stable hold on the 36 km analysis AOI and     */
/* carries no analytical pixel. What follows is composited here: the    */
/* DEM relief rises out of the ground (rendered lossless states,        */
/* interpolated on the scene's own clock) into four lossless full-frame */
/* drape states that share the poster's fit rule, cross-faded in the    */
/* accepted order and ending on the priority surface alone — or the     */
/* priority surface at once, on the held base, in every static state,   */
/* so a visitor who never sees the motion still sees the answer. The    */
/* startup poster is the OPENING frame; the held base is a separate     */
/* still. No legend, card or label: Acts 3 and 4 carry those.           */
/* ------------------------------------------------------------------ */
(function cinematicHero() {
  const hero = document.querySelector('.hero[data-hero-slot="cinematic"]');
  if (!hero) return;

  const video = hero.querySelector('.hero-video');
  const drape = hero.querySelector('[data-hero-drape]');
  const heldBase = hero.querySelector('[data-hero-held]');

  /* Frame 268 of 276 at 24 fps: the approach settles at 266 and the video holds still to its last
     frame, which is also the poster. The drape sequence starts inside that stillness, so the end of
     the motion and the first state read as one continuous resolve. */
  const HOLD_SECONDS = 268 / 24;
  /* The accepted evidence order: context, thermal, alteration, then the priority result. Four
     states 750 ms apart with a 450 ms cross-fade: 2.7 s in all, inside the approved 2.4-3.2 s. */
  const LAYER_ORDER = ['terrain', 'thm01', 'alt01', 'priority'];
  const LAYER_STEP_MS = 750;
  const LAYER_FADE_MS = 450;
  /* The relief rise (docs/web-005-polish-authority@0e87675). The scene raises the DEM from the held
     frame (276) to the Terrain state (292): 16 frames, 0.667 s, eased by the scene's own keys. The
     page has the scene's frames in between as lossless states and plays them on that same clock.
     Terrain then dwells exactly as long as it used to before THM-01 arrives (step minus fade), so
     Terrain -> THM-01 -> ALT-01 -> priority is unchanged. */
  const HELD_FRAME = 276;
  const TERRAIN_FRAME = 292;
  const SCENE_FPS = 24;
  const TERRAIN_DWELL_MS = LAYER_STEP_MS - LAYER_FADE_MS;

  /* ---- audited geometry of the held frame -> page coordinates ---------------------------- */
  /* Fractions of the 1920 x 1080 frame with y measured from the bottom, exactly as
     hero/evidence/shot_audit_production.json reports them (handoff_anchor: the true analysis AOI's
     centre and its four projected corners nw, ne, se, sw); the cover-fit below reproduces what
     object-fit: cover / object-position: center 46% does to that frame at any hero size. The drape
     states need none of this -- they are full-frame and share the media's fit rule -- it exists so
     the copy column can yield to the payoff. */
  let anchor = null;
  try { anchor = JSON.parse(hero.getAttribute('data-hero-anchor') || 'null'); } catch (e) { anchor = null; }
  if (anchor && !(Array.isArray(anchor.corners) && anchor.corners.length === 4)) anchor = null;
  const desktopLayout = window.matchMedia('(min-width: 981px)');

  function frameGeometry() {
    const W = hero.clientWidth;
    const H = hero.clientHeight;
    const fw = anchor.frame[0];
    const fh = anchor.frame[1];
    const s = Math.max(W / fw, H / fh);
    const rw = fw * s;
    const rh = fh * s;
    const ox = (W - rw) * 0.5;
    const oy = (H - rh) * anchor.position;
    const xs = anchor.corners.map((c) => ox + c[0] * rw);
    const ys = anchor.corners.map((c) => oy + (1 - c[1]) * rh);
    return {
      W, H,
      left: Math.min.apply(null, xs), right: Math.max.apply(null, xs),
      top: Math.min.apply(null, ys), bottom: Math.max.apply(null, ys),
    };
  }

  /* The footprint's position is fixed by the render, so on narrower desktops the headline column has
     to yield to it rather than run underneath. Applied from first layout, not at the reveal, so the
     copy never reflows mid-visit. */
  const heroContent = hero.querySelector('.hero-content');
  function constrainCopy() {
    if (!heroContent) return;
    if (!anchor || !desktopLayout.matches) { heroContent.style.maxWidth = ''; return; }
    /* max-width covers the padding box; the right padding is empty space and may sit under the payoff. */
    const padRight = parseFloat(getComputedStyle(heroContent).paddingRight) || 0;
    heroContent.style.maxWidth = Math.max(420, Math.round(frameGeometry().left - 24 + padRight)) + 'px';
  }
  constrainCopy();

  function layerImage(name) {
    return drape ? drape.querySelector('.hero-drape-layer[data-layer="' + name + '"]') : null;
  }

  /* A transitional state is data-src until the motion actually plays: a static visitor only ever
     fetches the priority state. */
  function promote(img) {
    if (!img) return;
    if (img.dataset.src) { img.src = img.dataset.src; img.removeAttribute('data-src'); }
    img.loading = 'eager';
    if (typeof img.decode === 'function') img.decode().catch(() => {});
  }

  function riseImages() {
    if (!drape) return [];
    return Array.prototype.slice.call(drape.querySelectorAll('.hero-drape-rise[data-rise-frame]'))
      .sort((a, b) => Number(a.dataset.riseFrame) - Number(b.dataset.riseFrame));
  }

  /* Warm the states while the sequence plays so they are decoded by the time the hold arrives. The
     rise states are motion-path only: nothing else ever calls this before the payoff. */
  function warmLayers() {
    if (!drape || !desktopLayout.matches) return;
    riseImages().forEach(promote);
    LAYER_ORDER.forEach((name) => promote(layerImage(name)));
  }

  /* The held base covers the startup poster before any static payoff: the drape states register
     with the held frame only, never with the opening Earth. If it cannot load, no payoff is shown. */
  function showHeldBase(then) {
    if (!heldBase) { then(); return; }
    if (heldBase.dataset.src) {
      heldBase.sizes = '100vw';
      if (heldBase.dataset.srcset) heldBase.srcset = heldBase.dataset.srcset;
      heldBase.src = heldBase.dataset.src;
      heldBase.removeAttribute('data-src');
      heldBase.removeAttribute('data-srcset');
    }
    const ready = () => { heldBase.classList.add('is-on'); then(); };
    if (heldBase.complete && heldBase.naturalWidth > 0) { ready(); return; }
    heldBase.addEventListener('load', ready, { once: true });
    heldBase.addEventListener('error', () => { hero.dataset.heroHeld = 'failed'; }, { once: true });
  }

  /* ---- the relief rise ------------------------------------------------------------------- */
  /* Keyframes: nothing (held frame) -> each rendered rise state -> the Terrain state. At scene
     frame f the two neighbouring keyframes are shown at opacities (1 - p) and p; with plus-lighter
     in an isolated group that is an exact linear interpolation of two partly transparent images.
     Without plus-lighter the nearest state is shown whole (a flipbook), never a dipping cross-fade. */
  const exactBlend = !!(window.CSS && CSS.supports && CSS.supports('mix-blend-mode', 'plus-lighter'));
  let riseRaf = 0;
  function riseReady() {
    const imgs = riseImages().concat([layerImage('terrain')]);
    return imgs.length > 1 && imgs.every((img) => img && img.complete && img.naturalWidth > 0);
  }
  function clearRise() {
    if (riseRaf) window.cancelAnimationFrame(riseRaf);
    riseRaf = 0;
    riseImages().forEach((img) => { img.style.opacity = ''; });
    const terrain = layerImage('terrain');
    if (terrain) terrain.style.opacity = '';
    if (drape) drape.classList.remove('is-rising');
  }
  function playRise(done) {
    const terrain = layerImage('terrain');
    const keys = [{ frame: HELD_FRAME, img: null }]
      .concat(riseImages().map((img) => ({ frame: Number(img.dataset.riseFrame), img })))
      .concat([{ frame: TERRAIN_FRAME, img: terrain }]);
    const span = TERRAIN_FRAME - HELD_FRAME;
    const total = span / SCENE_FPS * 1000;
    const t0 = performance.now();
    drape.classList.add('is-rising');
    hero.dataset.heroLayer = 'rise';
    function paint(now) {
      const progress = Math.min(1, Math.max(0, (now - t0) / total));
      const frame = HELD_FRAME + progress * span;
      let i = 0;
      while (i < keys.length - 2 && frame >= keys[i + 1].frame) i += 1;
      const from = keys[i];
      const to = keys[i + 1];
      let p = (frame - from.frame) / (to.frame - from.frame);
      if (!exactBlend) p = p < 0.5 ? 0 : 1;
      keys.forEach((key) => {
        if (!key.img) return;
        key.img.style.opacity = key === from ? String(1 - p) : key === to ? String(p) : '0';
      });
      if (progress < 1) { riseRaf = window.requestAnimationFrame(paint); return; }
      riseRaf = 0;
      terrain.classList.add('is-on');
      clearRise();
      hero.dataset.heroLayer = 'terrain';
      done();
    }
    riseRaf = window.requestAnimationFrame(paint);
  }

  /* Show exactly `id`. The incoming state fades in over the outgoing one, which is dropped once it
     is fully covered, so the sequence ends on the priority surface alone. */
  let sequenceTimers = [];
  function setLayer(id, instant) {
    LAYER_ORDER.forEach((name) => {
      const img = layerImage(name);
      if (!img) return;
      if (name === id) { promote(img); img.classList.add('is-on'); return; }
      if (instant) img.classList.remove('is-on');
      else sequenceTimers.push(window.setTimeout(() => img.classList.remove('is-on'), LAYER_FADE_MS + 60));
    });
    hero.dataset.heroLayer = id;
  }

  let revealed = false;
  function revealPayoff(instant) {
    if (revealed || !drape) return;
    /* Desktop layout only (see styles.css). If the viewport becomes one later, the listener below
       comes back here. */
    if (!desktopLayout.matches) return;
    revealed = true;
    drape.hidden = false;
    hero.setAttribute('data-hero-payoff', 'on');
    if (instant || reduceMotion.matches) {
      /* Review hook: in a static state, #hero-layer=<id> settles on that state instead of the
         result, so each step of the sequence can be captured deterministically. */
      const pick = /^#hero-layer=(terrain|thm01|alt01|priority|rise-f\d+)$/.exec(window.location.hash || '');
      if (pick && pick[1].indexOf('rise-f') === 0) {
        const still = riseImages().find((img) => img.dataset.riseFrame === pick[1].slice(6));
        if (still) { promote(still); still.style.opacity = '1'; hero.dataset.heroLayer = pick[1]; return; }
      }
      setLayer(pick && pick[1].indexOf('rise-f') !== 0 ? pick[1] : 'priority', true);
      return;
    }
    warmLayers();
    /* Two frames: one for the elements to exist, one for the transitions to have a start value. */
    requestAnimationFrame(() => requestAnimationFrame(() => {
      if (riseReady()) {
        /* The relief rises into Terrain; the rest of the order follows on its accepted cadence. */
        playRise(() => {
          LAYER_ORDER.slice(1).forEach((name, i) => {
            sequenceTimers.push(window.setTimeout(() => setLayer(name), TERRAIN_DWELL_MS + i * LAYER_STEP_MS));
          });
        });
        return;
      }
      /* Rise states not decoded in time: the accepted cross-fade from the held frame, as before. */
      LAYER_ORDER.forEach((name, i) => {
        sequenceTimers.push(window.setTimeout(() => setLayer(name), i * LAYER_STEP_MS));
      });
    }));
  }

  let layoutTimer = null;
  window.addEventListener('resize', () => {
    window.clearTimeout(layoutTimer);
    layoutTimer = window.setTimeout(constrainCopy, 120);
  });
  /* The copy constraint depends on the hero's own box, which can change without a window resize
     (82vh moves with browser chrome). Observe the box itself. */
  if (typeof ResizeObserver === 'function') {
    let pending = false;
    new ResizeObserver(() => {
      if (pending) return;
      pending = true;
      requestAnimationFrame(() => { pending = false; constrainCopy(); });
    }).observe(hero);
  }
  window.addEventListener('load', constrainCopy, { once: true });
  /* A window widened into the desktop layout after the hero has settled still gets the payoff. */
  const onLayoutChange = () => {
    const state = hero.getAttribute('data-hero-state');
    if (!desktopLayout.matches) return;
    if (state === 'static') showHeldBase(() => revealPayoff(true));
    else if (state === 'held') revealPayoff(true);
  };
  if (typeof desktopLayout.addEventListener === 'function') desktopLayout.addEventListener('change', onLayoutChange);

  function settleStatic(reason) {
    hero.setAttribute('data-hero-state', 'static');
    if (hero.dataset.heroReason !== reason) hero.dataset.heroReason = reason;
    /* A video that was playing is stopped, not swapped: the held still takes over (MER-216). */
    if (video && !video.paused && typeof video.pause === 'function') video.pause();
    /* Static means the video is not what the visitor is looking at, so the startup poster is: cover
       it with the held base first, then the payoff. */
    showHeldBase(() => revealPayoff(true));
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

  /* ---- delivery tiers (MER-216) ------------------------------------------------------------ */
  /* The sequence is published as a small ladder of encodes of the SAME frames (hero/evidence/
     responsive_media.json), each in WebM and MP4. One tier and one codec are chosen here, once,
     before a byte of video is requested, from signals that exist before playback: the device pixels
     the 16:9 frame must cover, the network's own downlink hint, and what the decoder says it can play
     smoothly. Nothing is ever swapped mid-play, and the largest encode is not forced on anyone. The
     bare data-hero-webm / data-hero-mp4 pair is the middle tier and stays the fallback when the
     ladder is absent or unreadable. */
  function readTiers() {
    let list = null;
    try { list = JSON.parse(video.getAttribute('data-hero-tiers') || 'null'); } catch (e) { list = null; }
    if (Array.isArray(list)) {
      list = list.filter((t) => t && t.w > 0 && (t.webm || t.mp4)).sort((a, b) => a.w - b.w);
    }
    if (Array.isArray(list) && list.length) return list;
    return [{
      id: 'default', w: 1920,
      webm: video.getAttribute('data-hero-webm'), mp4: video.getAttribute('data-hero-mp4'),
      kbps: { webm: 2200, mp4: 3300 },
      codecs: { webm: 'vp09.00.40.08', mp4: 'avc1.640028' },
    }];
  }
  const tiers = readTiers();

  /* Device pixels the frame has to cover: the hero is a cover-fit of a 16:9 frame, so the binding
     axis is whichever of the width or the (height x 16/9) is larger. A tier may undershoot by 8%
     (a 1366 px laptop is served the 1280 encode) but is never asked to stand in for a wider screen. */
  function demandPx() {
    const dpr = window.devicePixelRatio || 1;
    return Math.max(hero.clientWidth, hero.clientHeight * 16 / 9) * dpr;
  }
  function firstTierIndex() {
    const need = demandPx() * 0.92;
    for (let i = 0; i < tiers.length; i += 1) if (tiers[i].w >= need) return i;
    return tiers.length - 1;
  }
  /* Codec order: WebM (VP9) where the browser is confident, MP4 (H.264) otherwise. */
  function codecOrder() {
    const order = [];
    const vp9 = video.canPlayType('video/webm; codecs="vp9"');
    const avc = video.canPlayType('video/mp4; codecs="avc1.4d4028"') || video.canPlayType('video/mp4');
    if (vp9 === 'probably') order.push('webm');
    if (avc) order.push('mp4');
    if (vp9 && vp9 !== 'probably') order.push('webm');
    return order.filter((c, i) => order.indexOf(c) === i);
  }
  function codecString(tier, codec) {
    const c = tier.codecs && tier.codecs[codec];
    if (c) return (codec === 'webm' ? 'video/webm; codecs="' : 'video/mp4; codecs="') + c + '"';
    return codec === 'webm' ? 'video/webm; codecs="vp09.00.40.08"' : 'video/mp4; codecs="avc1.640028"';
  }
  function tierBps(tier, codec) {
    const k = tier.kbps && (tier.kbps[codec] || tier.kbps.webm || tier.kbps.mp4);
    return (k || 2500) * 1000;
  }
  /* Downlink is a hint in Mbit/s (Chrome caps it at 10 and reports a conservative default until it has
     measured something; other engines omit it). It only ever moves a visitor DOWN the ladder: a tier
     needs 1.5x its own average bitrate (the encodes are VBR with peaks up to 1.6x), measured to be the
     margin below which a 1.6 Mbit/s link stalls the smallest tier mid-play, and a visitor who cannot
     sustain even that is better served by the still. Unknown downlink: no cap. */
  function networkOk(tier, codec) {
    const down = typeof connection.downlink === 'number' && connection.downlink > 0 ? connection.downlink * 1e6 : 0;
    return !down || tierBps(tier, codec) * 1.5 <= down;
  }
  /* The decoder's verdict on one (tier, codec) candidate, true or false, never a guess:
       - no mediaCapabilities, or no answer inside the shared 1.2 s budget: unknown, so the candidate
         stands on canPlayType and the network gate alone (the hero must not wait on a silent API);
       - an answer that says unsupported or not smooth, or a query that REJECTS (the configuration
         could not be evaluated): the candidate is not safe. */
  function decoderAccepts(candidate, deadline) {
    const mc = navigator.mediaCapabilities;
    if (!mc || typeof mc.decodingInfo !== 'function') return Promise.resolve(true);
    const budget = deadline - Date.now();
    if (budget <= 0) return Promise.resolve(true);
    const { tier, codec } = candidate;
    let query;
    try {
      query = mc.decodingInfo({
        type: 'file',
        video: {
          contentType: codecString(tier, codec), width: tier.w, height: Math.round(tier.w * 9 / 16),
          bitrate: tierBps(tier, codec), framerate: SCENE_FPS,
        },
      });
    } catch (e) { return Promise.resolve(false); }
    const verdict = Promise.resolve(query).then((info) => !!(info && info.supported && info.smooth !== false), () => false);
    return Promise.race([verdict, new Promise((resolve) => window.setTimeout(() => resolve(true), budget))]);
  }
  /* One delivery, chosen before any video byte. Every candidate that can be returned has passed BOTH
     gates, the network margin and the decoder verdict, in this order of preference: the preferred codec
     from the demanded tier down the ladder (the existing downshift policy), then each alternate codec
     the same way. No candidate left means no delivery, and the caller falls back to the held still. */
  let refusal = 'no-playable-encode';
  function pickDelivery() {
    const order = codecOrder();
    if (!order.length) return null;
    const candidates = [];
    order.forEach((codec) => {
      for (let index = firstTierIndex(); index >= 0; index -= 1) {
        if (tiers[index][codec]) candidates.push({ tier: tiers[index], codec });
      }
    });
    const deadline = Date.now() + 1200;
    refusal = 'no-playable-encode';
    const next = (k) => {
      if (k >= candidates.length) return Promise.resolve(null);
      const candidate = candidates[k];
      if (!networkOk(candidate.tier, candidate.codec)) {
        if (refusal !== 'decoder-refused') refusal = 'slow-network';
        return next(k + 1);
      }
      return decoderAccepts(candidate, deadline).then((ok) => {
        if (ok) {
          return {
            tier: candidate.tier, codec: candidate.codec, src: candidate.tier[candidate.codec],
            type: candidate.codec === 'webm' ? 'video/webm' : 'video/mp4',
          };
        }
        refusal = 'decoder-refused';
        return next(k + 1);
      });
    };
    return next(0);
  }

  let started = false;
  function start(choice) {
    if (started) return;
    started = true;
    hero.dataset.heroTier = choice.tier.id;
    hero.dataset.heroCodec = choice.codec;

    video.addEventListener('timeupdate', function onTime() {
      if (video.currentTime >= HOLD_SECONDS) {
        video.removeEventListener('timeupdate', onTime);
        revealPayoff();
      }
    });
    /* The last rendered frame is the held frame, so ending on it is a settle, not a stop. */
    video.addEventListener('ended', () => {
      hero.setAttribute('data-hero-state', 'held');
      revealPayoff();
    });
    /* The video is shown only once it has presented a real frame (requestVideoFrameCallback where it
       exists), so a decoder that reports "playing" and paints nothing can never put a black box over
       the poster. If it never presents one, the held still is the hero. */
    let shown = false;
    function show() {
      if (shown || hero.getAttribute('data-hero-state') === 'static') return;
      shown = true;
      if (!(video.videoWidth > 0)) { settleStatic('no-video-frame'); return; }
      hero.setAttribute('data-hero-state', 'playing');
      warmLayers();
      watchPlayback();
    }
    video.addEventListener('playing', () => {
      if (typeof video.requestVideoFrameCallback === 'function') {
        video.requestVideoFrameCallback(show);
        window.setTimeout(() => { if (!shown && !video.paused && video.readyState > 2) show(); }, 1500);
      } else show();
    }, { once: true });
    video.addEventListener('error', () => settleStatic('encode-error'), { once: true });

    /* Playback quality after it has started: a stall that lasts, or a decoder that drops a large share
       of the first seconds, ends in the held still instead of a frozen or stuttering hero. The video is
       paused and never swapped for another source. */
    let stallTimer = 0;
    function watchPlayback() {
      video.addEventListener('waiting', () => {
        if (video.ended || hero.getAttribute('data-hero-state') === 'static') return;
        window.clearTimeout(stallTimer);
        stallTimer = window.setTimeout(() => settleStatic('buffering'), 3000);
      });
      ['playing', 'timeupdate', 'ended'].forEach((name) => video.addEventListener(name, () => {
        if (name === 'timeupdate' && video.readyState < 3) return;
        window.clearTimeout(stallTimer);
      }));
      window.setTimeout(() => {
        if (hero.getAttribute('data-hero-state') !== 'playing' || typeof video.getVideoPlaybackQuality !== 'function') return;
        const q = video.getVideoPlaybackQuality();
        if (q.totalVideoFrames >= 48 && q.droppedVideoFrames / q.totalVideoFrames > 0.4) settleStatic('dropped-frames');
      }, 4500);
    }

    video.muted = true;
    video.loop = false;
    video.setAttribute('src', choice.src);
    video.load();

    const attempt = video.play();
    if (attempt && typeof attempt.catch === 'function') {
      /* Autoplay refused by policy is a normal outcome, not a failure: fall back to the held base
         and hand off straight away rather than leaving a blank frame or nagging the visitor. */
      attempt.catch((err) => settleStatic(err && err.name === 'NotAllowedError' ? 'autoplay-blocked' : 'encode-error'));
    }
  }

  /* Never compete with the poster: the poster is the LCP element. The delivery choice is made first
     and the encode is requested only after it. */
  function begin() {
    Promise.resolve(pickDelivery()).then((choice) => {
      if (choice) start(choice); else settleStatic(refusal);
    }, () => settleStatic('no-playable-encode'));
  }
  function startWhenIdle() {
    if (document.readyState === 'complete') begin();
    else window.addEventListener('load', begin, { once: true });
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
    sequenceTimers.forEach((id) => window.clearTimeout(id));
    sequenceTimers = [];
    clearRise();
    if (revealed) setLayer('priority', true);
    settleStatic('reduced-motion');
  };
  if (typeof reduceMotion.addEventListener === 'function') {
    reduceMotion.addEventListener('change', onMotionChange);
  }

  /* Belt and braces: however playback goes, the result must not stay hidden. */
  /* A stalled playback must not get the payoff laid over whatever frame it stopped on: the states
     register with the held frame only. settleStatic covers everything with the held base first. */
  window.setTimeout(() => {
    if (revealed) return;
    if (!video.paused && !video.ended && video.readyState > 2) return;
    settleStatic('stalled');
  }, 15000);
})();

/* ------------------------------------------------------------------ */
/* WEB-005B act entrances                                               */
/*                                                                      */
/* One quiet rise per post-hero visual, once, as it enters the view.    */
/* Only the wrapper's opacity and position move; the images inside are  */
/* never filtered, and at rest nothing is transformed. No observer, or   */
/* reduced motion, and the class is never added: everything is simply   */
/* there. Independent of the hero sequence above.                       */
/* ------------------------------------------------------------------ */
(function actEntrances() {
  const items = document.querySelectorAll('[data-reveal]');
  if (!items.length || !('IntersectionObserver' in window)) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  document.documentElement.classList.add('has-reveal');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-revealed');
      observer.unobserve(entry.target);
    });
  }, { rootMargin: '0px 0px -6% 0px', threshold: 0.06 });
  items.forEach((item) => observer.observe(item));
})();

/* ------------------------------------------------------------------ */
/* WEB-005B R11 inspection aid                                          */
/*                                                                      */
/* The wipe is a progressive enhancement over a composition that        */
/* already reads: the three radios are the layer choice and CSS shows   */
/* the selected one, so with no JavaScript the frame rests at a static  */
/* 50/50 split and still says what it is. What JavaScript adds is the   */
/* drag: a range input covering the whole frame, so the touch target is */
/* the figure rather than a thin handle, and arrow keys move it for     */
/* free. The input is display:none until this runs — an input nothing   */
/* listens to is worse than no input at all.                            */
/*                                                                      */
/* Nothing here touches a pixel of either raster. The only thing that   */
/* moves is the --pos custom property the clip and the divider read.    */
/* ------------------------------------------------------------------ */
(function inspectionAid() {
  const frame = document.querySelector('.inspect-frame');
  const range = frame ? frame.querySelector('.inspect-range') : null;
  if (!frame || !range) return;

  let queued = false;
  function paint() {
    queued = false;
    frame.style.setProperty('--pos', `${range.value}%`);
  }
  function schedule() {
    if (queued) return;
    queued = true;
    window.requestAnimationFrame(paint);
  }

  range.addEventListener('input', schedule);
  range.addEventListener('change', schedule);
  frame.classList.add('is-live');
  paint();
})();
