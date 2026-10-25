/* OrbGSS — minimal vanilla JS: navigation, Solutions dropdown, image-failure handling, hero. */

/* ------------------------------------------------------------------ */
/* Translations. Keys map to data-i18n* attributes on the public pages. */
/* data-i18n        -> textContent                                     */
/* data-i18n-html   -> innerHTML (static, trusted strings with <br />) */
/* data-i18n-alt / -aria-label / -content / -href -> that attribute     */
/*                                                                      */
/* MER-241: this dictionary is the single source for BOTH languages, but */
/* it is applied at build time, not in the browser. scripts/            */
/* build_tr_pages.py reads it and writes the static Turkish pages under */
/* /tr/; the English pages carry their own text. The browser never      */
/* swaps text, so every page is complete in its own language with no    */
/* JavaScript. At runtime only the menu-toggle label below is read.     */
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
    'evidence.switchLabel': 'Evidence layer',
    'scene.kind.naturalColor': 'Natural-color composite',
    'scene.aoi.place': 'Kızıldere, Denizli, Türkiye',
    'scene.aoi.coords': '37.9794° N, 28.7907° E',
    'label.priority': 'Remote-Sensing Relative Priority — Experimental Baseline',
    'alt.terrain.home': 'Colour elevation map of the Kızıldere area of interest, with low ground in dark green and high ridges in pale stone and white',
    'alt.thm01': 'Diverging thermal anomaly map of the Kızıldere area of interest, with cooler ground in blue and warmer ground in red',
    'alt.alt01': 'Map of the surface alteration signal across the Kızıldere area of interest, running from deep blue where the signal is weakest to yellow where it is strongest',
    'alt.priority': 'Relative priority map of the Kızıldere area of interest, ranking ground from 0 to 100 within the area',
    'act.context.title': 'A real area, before any analysis.',
    'act.context.copy': 'Kızıldere sits in the Büyük Menderes graben in Denizli, Türkiye, as Landsat 8 photographed it.',
    'act.context.meta': 'Landsat 8 OLI · 2025-05-05 · 30 m · natural colour',
    'act.evidence.title': 'Three layers over the same ground.',
    'act.evidence.terrain.role': 'Context',
    'act.evidence.thermal.role': 'Evidence',
    'act.evidence.alteration.role': 'Evidence',
    'act.evidence.gapLabel': 'Data gap',
    'act.evidence.deeper': 'See every layer',
    'act.priority.title': 'Where to look first.',
    'act.priority.copy': 'One ranking across the area of interest, so a team can order the ground instead of guessing at it.',
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
    'company.copy': 'OrbGSS is a geospatial-intelligence platform. It exists to make exploration and land decisions evidence-based, traceable and easier to prioritize.',
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
    'footer.attribution': 'Landsat data courtesy of the U.S. Geological Survey. Contains modified Copernicus Sentinel data (2025).',
    'footer.copyright': '© 2026 OrbGSS. All rights reserved.',

    /* WEB-003 — deep public routes */
    'mail.pilot': MAIL_PILOT_EN,
    'mail.technical': MAIL_TECH_EN,

    /* WEB-005B R11 — the accepted final homepage design. */
    'act.evidence.shown': 'Shown',
    'act.evidence.terrain.index': '01',
    'act.evidence.terrain.tab': 'Terrain',
    'act.evidence.terrain.meta': 'From NASADEM elevation data',
    'act.evidence.thermal.index': '02',
    'act.evidence.thermal.tab': 'Thermal',
    'act.evidence.thermal.meta': 'From Landsat thermal bands',
    'act.evidence.alteration.index': '03',
    'act.evidence.alteration.tab': 'Alteration',
    'act.evidence.alteration.meta': 'From Sentinel-2 reflectance',
    'act.priority.def.why.term': 'Why it matters',
    'act.priority.def.why.copy': 'It turns a 36 × 36 km area into an ordered shortlist before anyone travels to it.',
    'act.priority.def.for.term': 'What it is for',
    'act.priority.def.for.copy': 'Deciding where to investigate next, with the evidence and its provenance attached.',
    'inspect.kicker': 'Inspection aid',
    'inspect.title': 'Hold a layer against the photograph.',
    'inspect.copy': 'Wipe between the natural-colour view of the area of interest and one derived layer over the same ground.',
    'inspect.against': 'Natural colour against',
    'inspect.pairsLabel': 'Layer to compare',
    'inspect.pair.thermal': 'Thermal',
    'inspect.pair.alteration': 'Alteration',
    'inspect.pair.priority': 'Priority score',
    'inspect.rangeLabel': 'Reveal the selected layer over the natural-colour view',
    'inspect.tag.layer': 'Derived layer',
    'inspect.tag.photo': 'Natural colour',
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

    'solutions.copy': 'Each domain states where it actually stands, and nothing in development is presented as a finished product.',

    'solutions.listLabel': 'Solution domains',
    /* WEB-005B R13 — the accepted homepage domain taxonomy. Separate from the app.* application
       ledger, which /solutions/ publishes with its own wording. */
    'domain.geothermal.title': 'Geothermal',
    'domain.mining.title': 'Mining',
    'domain.marine.title': 'Marine',
    'nav.home': 'Home',
    'nav.about': 'About',
    'nav.partner': 'Partner with us',
    'footer.sources': 'Data sources and attributions',
    'alt.locator': 'Map of Türkiye with the 36 km Kızıldere pilot area marked in Denizli',
    'scene.kind.locator': 'Locator map — Natural Earth',
    'alt.stage': 'Natural-colour Landsat 8 strip across the Büyük Menderes graben around Kızıldere, with irrigated fields on the valley floor and dry ridges on either side',
    'alt.aoi': 'Natural-colour Landsat 8 view of the 36 km Kızıldere analysis area: forested ridges, a cultivated valley floor and a road along the graben',
    'alt.terrain': 'Natural-colour Landsat 8 view of eroded red-brown hills and a river valley east of the Kızıldere analysis area',
    'alt.valley': 'Natural-colour Landsat 8 view of the cultivated floor of the Büyük Menderes graben, with a road crossing it, in the south-west of the Kızıldere context view',
    'scene.terrain.place': 'East of the Kızıldere pilot area, Türkiye',
    'scene.terrain.coords': '38.0936° N, 29.2483° E',
    'scene.valley.place': 'South-west of the Kızıldere pilot area, Türkiye',
    'scene.valley.coords': '37.8744° N, 28.5695° E',
    'notFound.meta.title': 'Page not found — OrbGSS',
    'notFound.title': 'This page is outside the area of interest.',
    'notFound.home': 'Return to OrbGSS',

    // === atlas:geothermal === MER-276 owns this region: the Geothermal page strings (geothermalPage.*).
    'geothermalPage.meta.title': 'Geothermal — Kızıldere pilot — OrbGSS',
    'geothermalPage.meta.description': 'The Kızıldere geothermal pilot in Denizli, Türkiye: where it is, every published layer, and what is still missing.',
    'geothermalPage.meta.ogDescription': 'Kızıldere: the first published OrbGSS pilot.',
    'geothermalPage.title.lead': 'Kızıldere:',
    'geothermalPage.title.tail': 'the first published pilot.',
    'geothermalPage.intro': 'Everything published for the pilot, in one place: where it is, which layers it holds, and what is still missing.',
    'geothermalPage.index.record': 'The pilot record',
    'geothermalPage.index.atlas': 'The layer atlas',
    'geothermalPage.index.result': 'The result',
    'geothermalPage.index.missing': 'What is missing',
    'geothermalPage.glance.title': 'One area, one grid',
    'geothermalPage.fact.place': 'Place',
    'geothermalPage.fact.placeValue': 'Büyük Menderes graben, Denizli, Türkiye',
    'geothermalPage.fact.centre': 'Centre',
    'geothermalPage.fact.area': 'Area',
    'geothermalPage.fact.areaValue': '36 × 36 km',
    'geothermalPage.fact.grid': 'Grid',
    'geothermalPage.fact.gridValue': '30 m, EPSG:32635, 1,200 × 1,200 cells',
    'geothermalPage.fact.layers': 'Layers',
    'geothermalPage.fact.layersValue': '2 context, 3 evidence, 1 priority surface',
    'geothermalPage.fact.score': 'Score',
    'geothermalPage.fact.scoreValue': 'Remote-Sensing Relative Priority — Experimental Baseline, 0–100 within the area',
    'geothermalPage.fact.gap': 'Not available',
    'geothermalPage.where.label': 'Where',
    'geothermalPage.where.copy': 'Kızıldere lies in the Büyük Menderes graben, Denizli, Türkiye. It is the one area OrbGSS has published end to end.',
    'geothermalPage.layers.title': 'Every layer',
    'geothermalPage.layers.copy': 'Two context layers orient the reader and three evidence layers carry the signal.',
    'geothermalPage.layers.link': 'Open the layers on the homepage',
    'geothermalPage.plate.abbr': 'Pl.',
    'geothermalPage.layer.natural': 'Natural colour',
    'geothermalPage.layer.structure': 'Structure and geology',
    'geothermalPage.layer.iron': 'Second alteration signal (iron)',
    'geothermalPage.layer.pending': 'Accepted, not shown yet',
    'geothermalPage.from.natural': 'Landsat 8 OLI, 2025-05-05',
    'geothermalPage.from.elevation': 'NASADEM',
    'geothermalPage.from.thermal': 'Landsat thermal bands',
    'geothermalPage.from.sentinel': 'Sentinel-2',
    'geothermalPage.from.none': 'Not available',
    'geothermalPage.role.context': 'Context',
    'geothermalPage.role.evidence': 'Evidence',
    'geothermalPage.role.support': 'Support',
    'geothermalPage.pending.asset': 'Asset to be supplied',
    'geothermalPage.gap.frame': 'No public-safe fault or lithology layer',
    'geothermalPage.outputs.title': 'One ranking',
    'geothermalPage.outputs.copy': 'The evidence layers are combined into one experimental score, 0 to 100, that ranks ground inside this area only. A higher value says look here first.',
    'geothermalPage.outputs.link': 'See the result on the homepage',
    'geothermalPage.scale.low': 'Look here later',
    'geothermalPage.scale.high': 'Look here first',
    'geothermalPage.scale.bar': 'Scale bar: 10 kilometres',
    'geothermalPage.relief.kicker': 'The result over relief',
    'geothermalPage.relief.title': 'Priority over relief',
    'geothermalPage.relief.copy': 'The priority surface read over NASADEM relief, so ranked ground can be seen against the valleys and ridges it sits on.',
    'geothermalPage.relief.state': 'Figure to be supplied',
    'geothermalPage.relief.slot': 'Priority over shaded NASADEM relief',
    'geothermalPage.missing.title': 'The gaps are part of the record.',
    'geothermalPage.next': 'Discuss a pilot',
    // === /atlas:geothermal ===

    // === atlas:solutions-about === MER-277 owns this region: the Solutions and About page strings (solutionsPage.*, aboutPage.*).
    'solutionsPage.meta.title': 'Solutions — OrbGSS',
    'solutionsPage.meta.description': 'Geothermal is active with a published pilot in Kızıldere, Türkiye. Mining and marine are expansion directions.',
    'solutionsPage.meta.ogDescription': 'Geothermal active, mining and marine next.',
    'solutionsPage.kicker': 'Solutions',
    'solutionsPage.title.lead': 'Where OrbGSS works today,',
    'solutionsPage.title.tail': 'and where next.',
    'solutionsPage.intro': 'Geothermal is active, with a published pilot. Mining and marine are expansion directions: nothing is published for them yet.',
    'solutionsPage.ground.geothermal': 'Geothermal exploration ground',
    'solutionsPage.ground.mining': 'Mineral exploration targets',
    'solutionsPage.ground.marine': 'Coastal and marine ground',
    'solutionsPage.published.geothermal': 'The Kızıldere pilot',
    'solutionsPage.published.none': 'Nothing published yet',
    'solutionsPage.band.pilot': 'See the Kızıldere pilot',
    'solutionsPage.band.kicker': 'Now',
    'solutionsPage.expansion.kicker': 'Next',
    'solutionsPage.thumb.priority': 'Thumbnail of the Kızıldere relative priority map',
    'solutionsPage.thumb.none': 'None yet',
    'aboutPage.meta.title': 'About — OrbGSS',
    'aboutPage.meta.description': 'OrbGSS — Orbital Geo-Spatial Solutions: what it is for, how it publishes and where its data comes from.',
    'aboutPage.meta.ogDescription': 'OrbGSS — Orbital Geo-Spatial Solutions: what it is for, how it publishes and where its data comes from.',
    'aboutPage.kicker': 'About',
    'aboutPage.title.name': 'OrbGSS —',
    'aboutPage.title.full': 'Orbital Geo-Spatial Solutions',
    'aboutPage.principles.kicker': 'Principles',
    'aboutPage.principles.title': 'How OrbGSS publishes',
    'aboutPage.principle.evidence': 'Priorities come from mapped layers, not an unexplained model output.',
    'aboutPage.principle.provenance': 'Every published visual maps back to a source and a recorded export.',
    'aboutPage.principle.gaps': 'A missing layer is published as missing, never invented.',
    'aboutPage.principle.aoi': 'One declared area, projection and grid before any interpretation.',
    'aboutPage.principle.narrowing': 'Large areas are ordered from orbit before field time is committed.',
    'aboutPage.principle.decision': 'Helps decide where to investigate; field investigation remains necessary.',
    'aboutPage.see.evidence': 'The three layers',
    'aboutPage.see.sources': 'Data sources',
    'aboutPage.see.gap': 'Structure and geology',
    'aboutPage.see.glance': 'The pilot area',
    'aboutPage.see.priority': 'Where to look first',
    'solutionsPage.ledger.label': 'Domains at a glance',
    'solutionsPage.feature.copy': 'The first application, with a published pilot in Kızıldere, Türkiye.',
    'solutionsPage.expansion.title': 'Expansion directions',
    'aboutPage.problem.title': 'Too much ground, too little time.',
    'aboutPage.problem.copy': 'Exploration and land decisions begin with more ground than anyone can walk. The hard question comes before any fieldwork: where to look first.',
    'aboutPage.position.title': 'Evidence that narrows the search.',
    'aboutPage.position.statement': 'Remote sensing can order the ground.',
    'aboutPage.position.statement.tail': 'Only the field can confirm it.',
    'aboutPage.layers.link': 'Every layer',
    'aboutPage.thumb.natural': 'Thumbnail: natural colour',
    'aboutPage.thumb.terrain': 'Thumbnail: elevation',
    'aboutPage.thumb.thermal': 'Thumbnail: thermal anomaly',
    'aboutPage.thumb.alteration': 'Thumbnail: alteration signal',
    'aboutPage.thumb.priority': 'Thumbnail: relative priority',
    'aboutPage.position.copy': 'OrbGSS publishes the evidence layers and their gaps beside every ranking, so a team can judge the result instead of trusting it.',
    'aboutPage.trust.title': 'Where the data comes from',
    'aboutPage.trust.copy': 'Every map traces back to open public data. Credits, citations and licence notices are kept together on one page.',
    // === /atlas:solutions-about ===

    // === atlas:partner-sources === MER-278 owns this region: the Partner and Sources page strings (partnerPage.*, sourcesPage.*).
    'partnerPage.meta.title': 'Partner with us — OrbGSS',
    'partnerPage.meta.description': 'Reach OrbGSS for pilot, partnership and technical conversations. contact@orbgss.com.',
    'partnerPage.meta.ogDescription': 'For pilot, partnership and technical conversations.',
    'partnerPage.title.a': 'Let’s talk about',
    'partnerPage.title.b': 'where to look next.',
    'partnerPage.intro': 'OrbGSS is available for pilot, partnership and technical conversations. Reach out directly by email — there is no form to fill in.',
    'partnerPage.conversations.title': 'Which conversation',
    'partnerPage.write': 'Write',
    'partnerPage.pilot.title': 'Pilot',
    'partnerPage.pilot.for': 'For prospective customers',
    'partnerPage.pilot.copy': 'A geothermal pilot, or a first application in a new area.',
    'partnerPage.partnership.title': 'Partnership',
    'partnerPage.partnership.for': 'For industry partners',
    'partnerPage.partnership.copy': 'A partnership or collaboration with OrbGSS.',
    'partnerPage.technical.title': 'Technical',
    'partnerPage.technical.for': 'For technical collaborators',
    'partnerPage.technical.copy': 'The evidence, its limits, or how a pilot would be scoped.',
    'sourcesPage.meta.title': 'Data sources and attributions — OrbGSS',
    'sourcesPage.meta.description': 'Where OrbGSS data comes from, how each image is credited, which papers to cite and the licence notices that travel with the work.',
    'sourcesPage.meta.ogDescription': 'Data sources, credits, references and licence notices.',
    'sourcesPage.kicker': 'Sources',
    'sourcesPage.title.a': 'Sources, credits',
    'sourcesPage.title.b': 'and licences.',
    'sourcesPage.intro': 'Four kinds of information, kept apart: the data behind the maps, the credit for each image, the papers to cite, and the licence notices that travel with the work.',
    'sourcesPage.index.data': 'Source data',
    'sourcesPage.index.images': 'Image credits',
    'sourcesPage.index.references': 'References',
    'sourcesPage.index.licences': 'Licences and notices',
    'sourcesPage.label.use': 'Used for',
    'sourcesPage.label.credit': 'Credit line',
    'sourcesPage.label.page': 'Official page',
    'sourcesPage.label.source': 'Source',
    'sourcesPage.label.terms': 'Terms',
    'sourcesPage.data.copy': 'Every public dataset behind the maps, with the credit line each one asks for.',
    'sourcesPage.name.landsat': 'Landsat',
    'sourcesPage.name.nasadem': 'NASADEM',
    'sourcesPage.name.sentinel': 'Copernicus Sentinel-2',
    'sourcesPage.name.nasaeo': 'NASA Earth Observatory',
    'sourcesPage.name.naturalearth': 'Natural Earth',
    'sourcesPage.name.scm': 'Scientific colour maps',
    'sourcesPage.landsat.name': 'Landsat 8 and 9',
    'sourcesPage.landsat.by': 'U.S. Geological Survey',
    'sourcesPage.landsat.use': 'Natural-colour photographs and thermal evidence.',
    'sourcesPage.landsat.credit': 'Landsat data courtesy of the U.S. Geological Survey.',
    'sourcesPage.landsat.page': 'Landsat Collection 2 Level-2 Science Products',
    'sourcesPage.nasadem.name': 'NASADEM',
    'sourcesPage.nasadem.by': 'NASA JPL, distributed by the NASA Land Processes DAAC',
    'sourcesPage.nasadem.use': 'Elevation and relief.',
    'sourcesPage.nasadem.credit': 'NASADEM elevation, NASA JPL (2020), via NASA Earthdata.',
    'sourcesPage.nasadem.page': 'doi:10.5067/MEaSUREs/NASADEM/NASADEM_HGT.001',
    'sourcesPage.sentinel.name': 'Copernicus Sentinel-2',
    'sourcesPage.sentinel.by': 'European Union, Copernicus programme (ESA)',
    'sourcesPage.sentinel.use': 'Alteration evidence, and ground detail in the rendered hero.',
    'sourcesPage.sentinel.credit': 'Contains modified Copernicus Sentinel data (2025).',
    'sourcesPage.sentinel.page': 'Copernicus Data Space Ecosystem',
    'sourcesPage.nasaeo.name': 'NASA Earth Observatory imagery',
    'sourcesPage.nasaeo.by': 'NASA Goddard Space Flight Center',
    'sourcesPage.nasaeo.use': 'Earth texture and city lights of the rendered hero.',
    'sourcesPage.nasaeo.credit': 'NASA Earth Observatory. Blue Marble: Next Generation, produced by Reto Stöckli, NASA Goddard Space Flight Center; Earth at Night 2012, Suomi NPP VIIRS.',
    'sourcesPage.nasaeo.page': 'Blue Marble: Next Generation',
    'sourcesPage.naturalearth.name': 'Natural Earth',
    'sourcesPage.naturalearth.by': 'Natural Earth contributors',
    'sourcesPage.naturalearth.use': 'The Kızıldere locator map.',
    'sourcesPage.naturalearth.credit': 'Made with Natural Earth.',
    'sourcesPage.naturalearth.page': 'naturalearthdata.com',
    'sourcesPage.scm.name': 'Scientific colour maps',
    'sourcesPage.scm.by': 'Fabio Crameri',
    'sourcesPage.scm.use': 'The colour scales of the cartographic maps.',
    'sourcesPage.scm.credit': 'Colour scales: Scientific colour maps v8.0 by Fabio Crameri (MIT licence).',
    'sourcesPage.scm.page': 'doi:10.5281/zenodo.1243862',
    'sourcesPage.images.copy': 'Each image, what it shows and which source it comes from.',
    'sourcesPage.img.hero': 'Homepage hero',
    'sourcesPage.img.hero.alt': 'Thumbnail of the rendered orbital sequence that opens the homepage',
    'sourcesPage.img.kizildere': 'Kızıldere, natural colour',
    'sourcesPage.img.kizildere.meta': 'Landsat 8 OLI · 5 May 2025 · LC08_L2SP_179034_20250505_02_T1 · 30 m',
    'sourcesPage.img.kizildere.alt': 'Thumbnail of the natural-colour Landsat view of the Kızıldere area',
    'sourcesPage.img.yellowstone.meta': 'Landsat 8 OLI · 9 June 2013 · LC08_L2SP_038029_20130609_02_T1',
    'sourcesPage.img.yellowstone.alt': 'Thumbnail of the Yellowstone photograph',
    'sourcesPage.img.chuquicamata.meta': 'Landsat 9 OLI-2 · 4 January 2024 · LC09_L2SP_001075_20240104_02_T1',
    'sourcesPage.img.chuquicamata.alt': 'Thumbnail of the Chuquicamata photograph',
    'sourcesPage.img.ili.meta': 'Landsat 8 OLI · 7 March 2020 · LC08_L2SP_152029_20200307_02_T1 and LC08_L2SP_152028_20200307_02_T1',
    'sourcesPage.img.ili.alt': 'Thumbnail of the Ili River Delta photograph',
    'sourcesPage.img.locator': 'Kızıldere locator map',
    'sourcesPage.img.locator.meta': 'Natural Earth 1:50m, version 5.1.2',
    'sourcesPage.img.locator.alt': 'Thumbnail of the Kızıldere locator map',
    'sourcesPage.img.maps': 'Evidence and priority maps',
    'sourcesPage.img.maps.meta': 'OrbGSS cartographic exports of the Kızıldere pilot area, built from NASADEM elevation, Landsat thermal bands and Sentinel-2 reflectance.',
    'sourcesPage.references.copy': 'Cite these when you use the colour scales or the elevation data.',
    'sourcesPage.ref.crameri2020': 'Crameri, F., Shephard, G. E. and Heron, P. J. (2020). The misuse of colour in science communication. Nature Communications, 11, 5444.',
    'sourcesPage.doi.crameri2020': 'doi:10.1038/s41467-020-19160-7',
    'sourcesPage.ref.scm': 'Crameri, F. (2023). Scientific colour maps, version 8.0. Zenodo.',
    'sourcesPage.doi.scm': 'doi:10.5281/zenodo.8035877',
    'sourcesPage.ref.nasadem': 'NASA JPL (2020). NASADEM Merged DEM Global 1 arc second V001. NASA EOSDIS Land Processes DAAC.',
    'sourcesPage.doi.nasadem': 'doi:10.5067/MEaSUREs/NASADEM/NASADEM_HGT.001',
    'sourcesPage.licences.copy': 'Terms for each source, and the full licence texts.',
    'sourcesPage.terms.landsat': 'Public domain. The U.S. Geological Survey asks for acknowledgement.',
    'sourcesPage.terms.landsat.link': 'USGS Landsat data policy',
    'sourcesPage.terms.nasadem': 'OrbGSS publishes renderings, never the data itself. Credit as above.',
    'sourcesPage.terms.sentinel': 'Free, full and open access. The credit line above is required.',
    'sourcesPage.terms.sentinel.link': 'Legal notice on Copernicus Sentinel data',
    'sourcesPage.terms.nasaeo': 'Public domain, as a U.S. government work.',
    'sourcesPage.terms.nasaeo.link': 'NASA media usage guidelines',
    'sourcesPage.terms.naturalearth': 'Public domain.',
    'sourcesPage.terms.naturalearth.link': 'Natural Earth terms of use',
    'sourcesPage.terms.scm': 'MIT licence. The notice on this page must accompany the colour scales.',
    'sourcesPage.name.fonts': 'OrbGSS Sans and Mono',
    'sourcesPage.terms.fonts': 'SIL Open Font License 1.1. Adapted from IBM Plex.',
    'sourcesPage.terms.fonts.link': 'IBM Plex',
    'sourcesPage.fonts.title': 'OrbGSS typefaces — SIL Open Font License 1.1',
    'sourcesPage.fonts.note': 'Adapted from IBM Plex, renamed because IBM reserves "Plex". Notices stay in English.',
    'sourcesPage.fonts.sans': 'IBM Plex Sans: Copyright 2018 IBM Corp. All rights reserved.',
    'sourcesPage.fonts.mono': 'IBM Plex Mono: Copyright 2017 IBM Corp. All rights reserved.',
    'sourcesPage.fonts.reserved': 'Copyright © 2017 IBM Corp. with Reserved Font Name "Plex"',
    'sourcesPage.fonts.licence': 'This Font Software is licensed under the SIL Open Font License, Version 1.1.',
    'sourcesPage.fonts.trademark': 'IBM Plex(R) is a trademark of IBM Corp, registered in many jurisdictions worldwide.',
    'sourcesPage.fonts.full': 'Full licence text',
    'sourcesPage.mit.title': 'Scientific colour maps v8.0 — MIT licence',
    'sourcesPage.mit.note': 'The licence text is kept in its original English; it is the binding text.',
    'sourcesPage.mit.name': 'MIT License',
    'sourcesPage.mit.copyright': 'Copyright (c) Fabio Crameri',
    'sourcesPage.mit.permission': 'Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:',
    'sourcesPage.mit.condition': 'The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.',
    'sourcesPage.mit.warranty': 'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.',
    // === /atlas:partner-sources ===
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
    'evidence.switchLabel': 'Kanıt katmanı',
    'scene.kind.naturalColor': 'Doğal renkli kompozit',
    'scene.aoi.place': 'Kızıldere, Denizli, Türkiye',
    'scene.aoi.coords': '37.9794° K, 28.7907° D',
    'label.priority': 'Uzaktan Algılama Göreli Önceliği — Deneysel Temel',
    'alt.terrain.home': 'Kızıldere ilgi alanının renkli yükselti haritası; alçak zemin koyu yeşil, yüksek sırtlar açık taş rengi ve beyaz',
    'alt.thm01': 'Kızıldere ilgi alanının ıraksak termal anomali haritası; daha serin zemin mavi, daha sıcak zemin kırmızı',
    'alt.alt01': 'Kızıldere ilgi alanı boyunca yüzey alterasyon sinyalinin haritası; sinyalin en zayıf olduğu yerde koyu mavi, en güçlü olduğu yerde sarı',
    'alt.priority': 'Kızıldere ilgi alanının göreli öncelik haritası; zemini alan içinde 0 ile 100 arasında sıralar',
    'act.context.title': 'Herhangi bir analizden önce, gerçek bir alan.',
    'act.context.copy': 'Kızıldere, Denizli, Türkiye’deki Büyük Menderes grabeninde yer alır; Landsat 8’in görüntülediği hâliyle.',
    'act.context.meta': 'Landsat 8 OLI · 2025-05-05 · 30 m · doğal renk',
    'act.evidence.title': 'Aynı zemin üzerinde üç katman.',
    'act.evidence.terrain.role': 'Bağlam',
    'act.evidence.thermal.role': 'Kanıt',
    'act.evidence.alteration.role': 'Kanıt',
    'act.evidence.gapLabel': 'Veri boşluğu',
    'act.evidence.deeper': 'Tüm katmanları görün',
    'act.priority.title': 'Önce nereye bakmalı.',
    'act.priority.copy': 'İlgi alanı genelinde tek bir sıralama; böylece bir ekip araziyi tahmin etmek yerine sıralayabilir.',
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
    'company.copy': 'OrbGSS bir coğrafi zekâ platformudur. Arama ve arazi kararlarını kanıta dayalı, izlenebilir ve önceliklendirilmesi kolay hâle getirmek için vardır.',
    'contact.cta': 'İş Birliği Kurun',
    'scene.yellowstone.place': 'Yellowstone Ulusal Parkı, ABD',
    'scene.yellowstone.coords': '44.4604° K, 110.8282° B',
    // Pre-uppercased: Turkish locale casing would otherwise render the Spanish name as "CHUQUİCAMATA".
    'scene.chuquicamata.place': 'Chuquicamata, Antofagasta, Şili',
    'scene.chuquicamata.coords': '22.3150° G, 68.9010° B',
    'scene.ili.place': 'İli Nehri Deltası ve Balkaş Gölü, Kazakistan',
    'scene.ili.coords': '45.0600° K, 74.5200° D',
    'alt.yellowstone': 'Yellowstone Ulusal Parkı çevresindeki jeotermal arazinin uydu görüntüsü',
    'alt.chuquicamata': 'Kuzey Şili Chuquicamata madencilik bölgesinin uydu görüntüsü',
    'alt.ili': 'Kazakistan İli Nehri Deltası ve Balkaş Gölü uydu görüntüsü',
    'footer.attribution': 'Landsat verileri ABD Jeoloji Araştırmaları Kurumu (USGS) kaynaklıdır. Değiştirilmiş Copernicus Sentinel verileri (2025) içerir.',
    'footer.copyright': '© 2026 OrbGSS. Tüm hakları saklıdır.',

    /* WEB-003 — deep public routes */
    'mail.pilot': MAIL_PILOT_TR,
    'mail.technical': MAIL_TECH_TR,

    /* WEB-005B R11 — the accepted final homepage design. */
    'act.evidence.shown': 'Gösteriliyor',
    'act.evidence.terrain.index': '01',
    'act.evidence.terrain.tab': 'Arazi',
    'act.evidence.terrain.meta': 'NASADEM yükselti verisinden',
    'act.evidence.thermal.index': '02',
    'act.evidence.thermal.tab': 'Termal',
    'act.evidence.thermal.meta': 'Landsat termal bantlarından',
    'act.evidence.alteration.index': '03',
    'act.evidence.alteration.tab': 'Alterasyon',
    'act.evidence.alteration.meta': 'Sentinel-2 yansıtımından',
    'act.priority.def.why.term': 'Neden önemli',
    'act.priority.def.why.copy': "36 × 36 km'lik bir alanı, kimse oraya gitmeden önce sıralı bir kısa listeye dönüştürür.",
    'act.priority.def.for.term': 'Ne için',
    'act.priority.def.for.copy': 'Kanıtı ve kökeni ekli hâlde, sırada nerenin inceleneceğine karar vermek.',
    'inspect.kicker': 'İnceleme aracı',
    'inspect.title': 'Bir katmanı fotoğrafın karşısına koyun.',
    'inspect.copy': 'İlgi alanının doğal renkli görünümü ile aynı zemin üzerindeki bir türetilmiş katman arasında gezinin.',
    'inspect.against': 'Doğal rengin karşısında',
    'inspect.pairsLabel': 'Karşılaştırılacak katman',
    'inspect.pair.thermal': 'Termal',
    'inspect.pair.alteration': 'Alterasyon',
    'inspect.pair.priority': 'Öncelik skoru',
    'inspect.rangeLabel': 'Seçili katmanı doğal renkli görünümün üzerinde açın',
    'inspect.tag.layer': 'Türetilmiş katman',
    'inspect.tag.photo': 'Doğal renk',
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

    'solutions.copy': 'Her alan bulunduğu noktayı açıkça belirtir; geliştirme aşamasındaki hiçbir şey tamamlanmış ürün olarak sunulmaz.',

    'solutions.listLabel': 'Çözüm alanları',
    /* WEB-005B R13 — the accepted homepage domain taxonomy. Separate from the app.* application
       ledger, which /solutions/ publishes with its own wording. */
    'domain.geothermal.title': 'Jeotermal',
    'domain.mining.title': 'Madencilik',
    'domain.marine.title': 'Denizel',
    'nav.home': 'Ana Sayfa',
    'nav.about': 'Hakkımızda',
    'nav.partner': 'İş Birliği',
    'footer.sources': 'Veri kaynakları ve atıflar',
    'alt.locator': "Denizli'de 36 km'lik Kızıldere pilot alanının işaretlendiği Türkiye haritası",
    'scene.kind.locator': 'Konum haritası — Natural Earth',
    'alt.stage': 'Kızıldere çevresindeki Büyük Menderes grabeni boyunca doğal renkli Landsat 8 şeridi; vadi tabanında sulu tarım alanları, iki yanda kuru sırtlar',
    'alt.aoi': 'Kızıldere’deki 36 km’lik analiz alanının doğal renkli Landsat 8 görünümü: ormanlık sırtlar, işlenen bir vadi tabanı ve graben boyunca uzanan bir yol',
    'alt.terrain': 'Kızıldere analiz alanının doğusunda aşınmış kırmızımsı kahverengi tepelerin ve bir nehir vadisinin doğal renkli Landsat 8 görünümü',
    'alt.valley': 'Kızıldere bağlam görünümünün güneybatısında, Büyük Menderes grabeninin işlenen tabanının ve onu kesen bir yolun doğal renkli Landsat 8 görünümü',
    'scene.terrain.place': 'Kızıldere pilot alanının doğusu, Türkiye',
    'scene.terrain.coords': '38.0936° K, 29.2483° D',
    'scene.valley.place': 'Kızıldere pilot alanının güneybatısı, Türkiye',
    'scene.valley.coords': '37.8744° K, 28.5695° D',
    'notFound.meta.title': 'Sayfa bulunamadı — OrbGSS',
    'notFound.title': 'Bu sayfa ilgi alanının dışında.',
    'notFound.home': "OrbGSS'e dönün",

    // === atlas:geothermal === MER-276 owns this region: the Geothermal page strings (geothermalPage.*).
    // MER-276: the Turkish strings that are new in the Atlas design are pending the CTO's language review (listed in docs/WEB_ATLAS_GEOTHERMAL_AUTHORITY.md).
    'geothermalPage.meta.title': 'Jeotermal — Kızıldere pilotu — OrbGSS',
    'geothermalPage.meta.description': "Denizli, Türkiye'deki Kızıldere jeotermal pilotu: nerede olduğu, yayımlanan her katman ve neyin hâlâ eksik olduğu.",
    'geothermalPage.meta.ogDescription': 'Kızıldere: yayımlanan ilk OrbGSS pilotu.',
    'geothermalPage.title.lead': 'Kızıldere:',
    'geothermalPage.title.tail': 'yayımlanan ilk pilot.',
    'geothermalPage.intro': 'Pilot için yayımlanan her şey tek yerde: nerede olduğu, hangi katmanları içerdiği ve neyin hâlâ eksik olduğu.',
    'geothermalPage.index.record': 'Pilot kaydı',
    'geothermalPage.index.atlas': 'Katman atlası',
    'geothermalPage.index.result': 'Sonuç',
    'geothermalPage.index.missing': 'Eksik olanlar',
    'geothermalPage.glance.title': 'Tek alan, tek ızgara',
    'geothermalPage.fact.place': 'Yer',
    'geothermalPage.fact.placeValue': 'Büyük Menderes grabeni, Denizli, Türkiye',
    'geothermalPage.fact.centre': 'Merkez',
    'geothermalPage.fact.area': 'Alan',
    'geothermalPage.fact.areaValue': '36 × 36 km',
    'geothermalPage.fact.grid': 'Izgara',
    'geothermalPage.fact.gridValue': '30 m, EPSG:32635, 1.200 × 1.200 hücre',
    'geothermalPage.fact.layers': 'Katmanlar',
    'geothermalPage.fact.layersValue': '2 bağlam, 3 kanıt, 1 öncelik yüzeyi',
    'geothermalPage.fact.score': 'Skor',
    'geothermalPage.fact.scoreValue': 'Uzaktan Algılama Göreli Önceliği — Deneysel Temel, alan içinde 0–100',
    'geothermalPage.fact.gap': 'Mevcut değil',
    'geothermalPage.where.label': 'Konum',
    'geothermalPage.where.copy': 'Kızıldere, Türkiye’nin Denizli ilinde, Büyük Menderes grabenindedir. OrbGSS’in baştan sona yayımladığı tek alandır.',
    'geothermalPage.layers.title': 'Her katman',
    'geothermalPage.layers.copy': 'İki bağlam katmanı okuru yönlendirir, üç kanıt katmanı sinyali taşır.',
    'geothermalPage.layers.link': 'Katmanları ana sayfada açın',
    'geothermalPage.plate.abbr': 'Lev.',
    'geothermalPage.layer.natural': 'Doğal renk',
    'geothermalPage.layer.structure': 'Yapı ve jeoloji',
    'geothermalPage.layer.iron': 'İkinci alterasyon işareti (demir)',
    'geothermalPage.layer.pending': 'Kabul edildi, henüz gösterilmiyor',
    'geothermalPage.from.natural': 'Landsat 8 OLI, 2025-05-05',
    'geothermalPage.from.elevation': 'NASADEM',
    'geothermalPage.from.thermal': 'Landsat termal bantları',
    'geothermalPage.from.sentinel': 'Sentinel-2',
    'geothermalPage.from.none': 'Mevcut değil',
    'geothermalPage.role.context': 'Bağlam',
    'geothermalPage.role.evidence': 'Kanıt',
    'geothermalPage.role.support': 'Destek',
    'geothermalPage.pending.asset': 'Görsel henüz teslim edilmedi',
    'geothermalPage.gap.frame': 'Kamuya açık kullanıma uygun fay veya litoloji katmanı yok',
    'geothermalPage.outputs.title': 'Tek sıralama',
    'geothermalPage.outputs.copy': 'Kanıt katmanları, yalnızca bu alanın içindeki zemini sıralayan, 0 ile 100 arası tek bir deneysel skorda birleştirilir. Yüksek değer “önce buraya bakın” der.',
    'geothermalPage.outputs.link': 'Sonucu ana sayfada görün',
    'geothermalPage.scale.low': 'Sonra bakın',
    'geothermalPage.scale.high': 'Önce bakın',
    'geothermalPage.scale.bar': 'Ölçek çubuğu: 10 kilometre',
    'geothermalPage.relief.kicker': 'Rölyef üzerinde sonuç',
    'geothermalPage.relief.title': 'Rölyef üzerinde öncelik',
    'geothermalPage.relief.copy': 'Öncelik yüzeyi NASADEM rölyefi üzerinde okunur; böylece sıralanan zemin, üzerinde durduğu vadi ve sırtlarla birlikte görülebilir.',
    'geothermalPage.relief.state': 'Şekil henüz teslim edilmedi',
    'geothermalPage.relief.slot': 'Gölgelendirilmiş NASADEM rölyefi üzerinde öncelik',
    'geothermalPage.missing.title': 'Boşluklar kaydın parçasıdır.',
    'geothermalPage.next': 'Pilot görüşün',
    // === /atlas:geothermal ===

    // === atlas:solutions-about === MER-277 owns this region: the Solutions and About page strings (solutionsPage.*, aboutPage.*).
    'solutionsPage.meta.title': 'Çözümler — OrbGSS',
    'solutionsPage.meta.description': "Jeotermal aktif ve Kızıldere, Türkiye'de yayımlanmış bir pilotu var. Madencilik ve denizel genişleme yönleridir.",
    'solutionsPage.meta.ogDescription': 'Jeotermal aktif; sırada madencilik ve denizel var.',
    'solutionsPage.kicker': 'Çözümler',
    'solutionsPage.title.lead': 'OrbGSS bugün nerede çalışıyor,',
    'solutionsPage.title.tail': 'sırada ne var.',
    'solutionsPage.intro': 'Jeotermal aktif ve yayımlanmış bir pilotu var. Madencilik ve denizel genişleme yönleri: bunlar için henüz yayımlanmış bir şey yok.',
    'solutionsPage.ground.geothermal': 'Jeotermal arama zemini',
    'solutionsPage.ground.mining': 'Maden arama hedefleri',
    'solutionsPage.ground.marine': 'Kıyı ve deniz zemini',
    'solutionsPage.published.geothermal': 'Kızıldere pilotu',
    'solutionsPage.published.none': 'Henüz yayımlanmış bir şey yok',
    'solutionsPage.band.pilot': 'Kızıldere pilotunu görün',
    'solutionsPage.band.kicker': 'Şimdi',
    'solutionsPage.expansion.kicker': 'Sırada',
    'solutionsPage.thumb.priority': 'Kızıldere göreli öncelik haritasının küçük görseli',
    'solutionsPage.thumb.none': 'Henüz yok',
    'aboutPage.meta.title': 'Hakkımızda — OrbGSS',
    'aboutPage.meta.description': 'OrbGSS — Orbital Geo-Spatial Solutions: ne için var olduğu, nasıl yayımladığı ve verilerinin nereden geldiği.',
    'aboutPage.meta.ogDescription': 'OrbGSS — Orbital Geo-Spatial Solutions: ne için var olduğu, nasıl yayımladığı ve verilerinin nereden geldiği.',
    'aboutPage.kicker': 'Hakkımızda',
    'aboutPage.title.name': 'OrbGSS —',
    'aboutPage.title.full': 'Orbital Geo-Spatial Solutions',
    'aboutPage.principles.kicker': 'İlkeler',
    'aboutPage.principles.title': 'OrbGSS nasıl yayımlar',
    'aboutPage.principle.evidence': 'Öncelikler açıklanmamış bir model çıktısından değil, haritalanmış katmanlardan gelir.',
    'aboutPage.principle.provenance': 'Yayımlanan her görsel bir kaynağa ve kayıtlı bir dışa aktarıma bağlanır.',
    'aboutPage.principle.gaps': 'Eksik bir katman eksik olarak yayımlanır, asla uydurulmaz.',
    'aboutPage.principle.aoi': 'Her yorumdan önce tek bir tanımlı alan, projeksiyon ve ızgara.',
    'aboutPage.principle.narrowing': 'Saha zamanı ayrılmadan önce geniş alanlar yörüngeden sıralanır.',
    'aboutPage.principle.decision': 'Nerede araştırma yapılacağına karar vermeye yardımcı olur; saha araştırması yine gereklidir.',
    'aboutPage.see.evidence': 'Üç katman',
    'aboutPage.see.sources': 'Veri kaynakları',
    'aboutPage.see.gap': 'Yapı ve jeoloji',
    'aboutPage.see.glance': 'Pilot alanı',
    'aboutPage.see.priority': 'Önce nereye bakılmalı',
    'solutionsPage.ledger.label': 'Alanlara genel bakış',
    'solutionsPage.feature.copy': 'İlk uygulama; Türkiye’nin Kızıldere bölgesinde yayımlanmış bir pilotla.',
    'solutionsPage.expansion.title': 'Genişleme yönleri',
    'aboutPage.problem.title': 'Çok geniş zemin, çok az zaman.',
    'aboutPage.problem.copy': 'Arama ve arazi kararları, kimsenin yürüyerek kat edemeyeceği kadar geniş bir zeminle başlar. Zor soru, her saha çalışmasından önce gelir: önce nereye bakılmalı.',
    'aboutPage.position.title': 'Aramayı daraltan kanıt.',
    'aboutPage.position.statement': 'Uzaktan algılama zemini sıralayabilir.',
    'aboutPage.position.statement.tail': 'Bunu doğrulayabilecek olan yalnızca sahadır.',
    'aboutPage.layers.link': 'Her katman',
    'aboutPage.thumb.natural': 'Küçük görsel: doğal renk',
    'aboutPage.thumb.terrain': 'Küçük görsel: yükselti',
    'aboutPage.thumb.thermal': 'Küçük görsel: termal anomali',
    'aboutPage.thumb.alteration': 'Küçük görsel: alterasyon işareti',
    'aboutPage.thumb.priority': 'Küçük görsel: göreli öncelik',
    'aboutPage.position.copy': 'OrbGSS her sıralamanın yanında kanıt katmanlarını ve boşluklarını yayımlar; böylece ekip sonuca güvenmek yerine onu değerlendirebilir.',
    'aboutPage.trust.title': 'Veriler nereden geliyor',
    'aboutPage.trust.copy': 'Her harita açık kamu verisine dayanır. Atıflar, kaynakçalar ve lisans bildirimleri tek sayfada toplanır.',
    // === /atlas:solutions-about ===

    // === atlas:partner-sources === MER-278 owns this region: the Partner and Sources page strings (partnerPage.*, sourcesPage.*).
    'partnerPage.meta.title': 'İş Birliği — OrbGSS',
    'partnerPage.meta.description': "Pilot, iş birliği ve teknik görüşmeler için OrbGSS'e ulaşın. contact@orbgss.com.",
    'partnerPage.meta.ogDescription': 'Pilot, iş birliği ve teknik görüşmeler için.',
    'partnerPage.title.a': 'Sırada nereye bakacağımızı',
    'partnerPage.title.b': 'konuşalım.',
    'partnerPage.intro': 'OrbGSS; pilot, iş birliği ve teknik görüşmeler için ulaşılabilir durumdadır. Doğrudan e-posta ile yazın — doldurulacak bir form yok.',
    'partnerPage.conversations.title': 'Hangi görüşme',
    'partnerPage.write': 'Yazın',
    'partnerPage.pilot.title': 'Pilot',
    'partnerPage.pilot.for': 'Olası müşteriler için',
    'partnerPage.pilot.copy': 'Bir jeotermal pilot ya da yeni bir alanda ilk uygulama.',
    'partnerPage.partnership.title': 'İş birliği',
    'partnerPage.partnership.for': 'Sektör ortakları için',
    'partnerPage.partnership.copy': 'OrbGSS ile bir iş birliği ya da ortaklık.',
    'partnerPage.technical.title': 'Teknik',
    'partnerPage.technical.for': 'Teknik paydaşlar için',
    'partnerPage.technical.copy': 'Kanıt, sınırları ya da bir pilotun nasıl kapsamlandırılacağı.',
    'sourcesPage.meta.title': 'Veri kaynakları ve atıflar — OrbGSS',
    'sourcesPage.meta.description': 'OrbGSS verilerinin nereden geldiği, her görselin nasıl anıldığı, hangi yayınlara atıf yapılacağı ve çalışmayla birlikte taşınan lisans bildirimleri.',
    'sourcesPage.meta.ogDescription': 'Veri kaynakları, atıflar, kaynakça ve lisans bildirimleri.',
    'sourcesPage.kicker': 'Kaynaklar',
    'sourcesPage.title.a': 'Kaynaklar, atıflar',
    'sourcesPage.title.b': 've lisanslar.',
    'sourcesPage.intro': 'Dört tür bilgi birbirinden ayrı tutulur: haritaların ardındaki veriler, her görselin atfı, anılacak yayınlar ve çalışmayla birlikte taşınan lisans bildirimleri.',
    'sourcesPage.index.data': 'Kaynak veriler',
    'sourcesPage.index.images': 'Görsel atıfları',
    'sourcesPage.index.references': 'Kaynakça',
    'sourcesPage.index.licences': 'Lisanslar ve bildirimler',
    'sourcesPage.label.use': 'Kullanıldığı yer',
    'sourcesPage.label.credit': 'Atıf cümlesi (özgün)',
    'sourcesPage.label.page': 'Resmî sayfa',
    'sourcesPage.label.source': 'Kaynak',
    'sourcesPage.label.terms': 'Koşullar',
    'sourcesPage.data.copy': 'Haritaların ardındaki her kamu veri seti ve her birinin istediği atıf cümlesi.',
    'sourcesPage.name.landsat': 'Landsat',
    'sourcesPage.name.nasadem': 'NASADEM',
    'sourcesPage.name.sentinel': 'Copernicus Sentinel-2',
    'sourcesPage.name.nasaeo': 'NASA Earth Observatory',
    'sourcesPage.name.naturalearth': 'Natural Earth',
    'sourcesPage.name.scm': 'Scientific colour maps',
    'sourcesPage.landsat.name': 'Landsat 8 ve 9',
    'sourcesPage.landsat.by': 'ABD Jeoloji Araştırmaları Kurumu (USGS)',
    'sourcesPage.landsat.use': 'Doğal renkli fotoğraflar ve termal kanıt.',
    'sourcesPage.landsat.credit': 'Landsat data courtesy of the U.S. Geological Survey.',
    'sourcesPage.landsat.page': 'Landsat Collection 2 Level-2 Science Products',
    'sourcesPage.nasadem.name': 'NASADEM',
    'sourcesPage.nasadem.by': 'NASA JPL; NASA Land Processes DAAC tarafından dağıtılır',
    'sourcesPage.nasadem.use': 'Yükselti ve rölyef.',
    'sourcesPage.nasadem.credit': 'NASADEM elevation, NASA JPL (2020), via NASA Earthdata.',
    'sourcesPage.nasadem.page': 'doi:10.5067/MEaSUREs/NASADEM/NASADEM_HGT.001',
    'sourcesPage.sentinel.name': 'Copernicus Sentinel-2',
    'sourcesPage.sentinel.by': 'Avrupa Birliği, Copernicus programı (ESA)',
    'sourcesPage.sentinel.use': 'Alterasyon kanıtı ve görselleştirilmiş açılış görselindeki zemin detayı.',
    'sourcesPage.sentinel.credit': 'Contains modified Copernicus Sentinel data (2025).',
    'sourcesPage.sentinel.page': 'Copernicus Data Space Ecosystem',
    'sourcesPage.nasaeo.name': 'NASA Earth Observatory görüntüleri',
    'sourcesPage.nasaeo.by': 'NASA Goddard Uzay Uçuş Merkezi',
    'sourcesPage.nasaeo.use': 'Görselleştirilmiş açılış görselinin Dünya dokusu ve şehir ışıkları.',
    'sourcesPage.nasaeo.credit': 'NASA Earth Observatory. Blue Marble: Next Generation, produced by Reto Stöckli, NASA Goddard Space Flight Center; Earth at Night 2012, Suomi NPP VIIRS.',
    'sourcesPage.nasaeo.page': 'Blue Marble: Next Generation',
    'sourcesPage.naturalearth.name': 'Natural Earth',
    'sourcesPage.naturalearth.by': 'Natural Earth katkı sağlayanlar',
    'sourcesPage.naturalearth.use': 'Kızıldere konum haritası.',
    'sourcesPage.naturalearth.credit': 'Made with Natural Earth.',
    'sourcesPage.naturalearth.page': 'naturalearthdata.com',
    'sourcesPage.scm.name': 'Scientific colour maps',
    'sourcesPage.scm.by': 'Fabio Crameri',
    'sourcesPage.scm.use': 'Kartografik haritaların renk skalaları.',
    'sourcesPage.scm.credit': 'Colour scales: Scientific colour maps v8.0 by Fabio Crameri (MIT licence).',
    'sourcesPage.scm.page': 'doi:10.5281/zenodo.1243862',
    'sourcesPage.images.copy': 'Her görsel, neyi gösterdiği ve hangi kaynaktan geldiği.',
    'sourcesPage.img.hero': 'Ana sayfa açılış görseli',
    'sourcesPage.img.hero.alt': 'Ana sayfayı açan görselleştirilmiş yörünge sekansının küçük görseli',
    'sourcesPage.img.kizildere': 'Kızıldere, doğal renk',
    'sourcesPage.img.kizildere.meta': 'Landsat 8 OLI · 5 Mayıs 2025 · LC08_L2SP_179034_20250505_02_T1 · 30 m',
    'sourcesPage.img.kizildere.alt': 'Kızıldere bölgesinin doğal renkli Landsat görünümünün küçük görseli',
    'sourcesPage.img.yellowstone.meta': 'Landsat 8 OLI · 9 Haziran 2013 · LC08_L2SP_038029_20130609_02_T1',
    'sourcesPage.img.yellowstone.alt': 'Yellowstone fotoğrafının küçük görseli',
    'sourcesPage.img.chuquicamata.meta': 'Landsat 9 OLI-2 · 4 Ocak 2024 · LC09_L2SP_001075_20240104_02_T1',
    'sourcesPage.img.chuquicamata.alt': 'Chuquicamata fotoğrafının küçük görseli',
    'sourcesPage.img.ili.meta': 'Landsat 8 OLI · 7 Mart 2020 · LC08_L2SP_152029_20200307_02_T1 ve LC08_L2SP_152028_20200307_02_T1',
    'sourcesPage.img.ili.alt': 'İli Nehri Deltası fotoğrafının küçük görseli',
    'sourcesPage.img.locator': 'Kızıldere konum haritası',
    'sourcesPage.img.locator.meta': 'Natural Earth 1:50m, sürüm 5.1.2',
    'sourcesPage.img.locator.alt': 'Kızıldere konum haritasının küçük görseli',
    'sourcesPage.img.maps': 'Kanıt ve öncelik haritaları',
    'sourcesPage.img.maps.meta': 'Kızıldere pilot alanının, NASADEM yükseltisinden, Landsat termal bantlarından ve Sentinel-2 yansımasından üretilen OrbGSS kartografik dışa aktarımları.',
    'sourcesPage.references.copy': 'Renk skalalarını ya da yükselti verisini kullanırken bunlara atıf yapın.',
    'sourcesPage.ref.crameri2020': 'Crameri, F., Shephard, G. E. and Heron, P. J. (2020). The misuse of colour in science communication. Nature Communications, 11, 5444.',
    'sourcesPage.doi.crameri2020': 'doi:10.1038/s41467-020-19160-7',
    'sourcesPage.ref.scm': 'Crameri, F. (2023). Scientific colour maps, version 8.0. Zenodo.',
    'sourcesPage.doi.scm': 'doi:10.5281/zenodo.8035877',
    'sourcesPage.ref.nasadem': 'NASA JPL (2020). NASADEM Merged DEM Global 1 arc second V001. NASA EOSDIS Land Processes DAAC.',
    'sourcesPage.doi.nasadem': 'doi:10.5067/MEaSUREs/NASADEM/NASADEM_HGT.001',
    'sourcesPage.licences.copy': 'Her kaynağın koşulları ve lisans metinlerinin tamamı.',
    'sourcesPage.terms.landsat': 'Kamu malı. ABD Jeoloji Araştırmaları Kurumu atıf yapılmasını ister.',
    'sourcesPage.terms.landsat.link': 'USGS Landsat veri politikası',
    'sourcesPage.terms.nasadem': 'OrbGSS verinin kendisini değil, görselleştirmelerini yayımlar. Atıf yukarıdaki gibidir.',
    'sourcesPage.terms.sentinel': 'Ücretsiz, tam ve açık erişim. Yukarıdaki atıf cümlesi zorunludur.',
    'sourcesPage.terms.sentinel.link': 'Copernicus Sentinel verilerine ilişkin yasal bildirim',
    'sourcesPage.terms.nasaeo': 'ABD hükümeti çalışması olarak kamu malı.',
    'sourcesPage.terms.nasaeo.link': 'NASA medya kullanım yönergeleri',
    'sourcesPage.terms.naturalearth': 'Kamu malı.',
    'sourcesPage.terms.naturalearth.link': 'Natural Earth kullanım koşulları',
    'sourcesPage.terms.scm': 'MIT lisansı. Bu sayfadaki bildirim renk skalalarına eşlik etmelidir.',
    'sourcesPage.name.fonts': 'OrbGSS Sans ve Mono',
    'sourcesPage.terms.fonts': 'SIL Open Font License 1.1. IBM Plex temel alınmıştır.',
    'sourcesPage.terms.fonts.link': 'IBM Plex',
    'sourcesPage.fonts.title': 'OrbGSS yazı tipleri — SIL Open Font License 1.1',
    'sourcesPage.fonts.note': 'IBM Plex temel alınarak uyarlandı; IBM "Plex" adını ayırdığı için yeniden adlandırıldı. Bildirimler İngilizce kalır.',
    'sourcesPage.fonts.sans': 'IBM Plex Sans: Copyright 2018 IBM Corp. All rights reserved.',
    'sourcesPage.fonts.mono': 'IBM Plex Mono: Copyright 2017 IBM Corp. All rights reserved.',
    'sourcesPage.fonts.reserved': 'Copyright © 2017 IBM Corp. with Reserved Font Name "Plex"',
    'sourcesPage.fonts.licence': 'This Font Software is licensed under the SIL Open Font License, Version 1.1.',
    'sourcesPage.fonts.trademark': 'IBM Plex(R) is a trademark of IBM Corp, registered in many jurisdictions worldwide.',
    'sourcesPage.fonts.full': 'Lisans metninin tamamı',
    'sourcesPage.mit.title': 'Scientific colour maps v8.0 — MIT lisansı',
    'sourcesPage.mit.note': 'Lisans metni özgün diliyle, İngilizce olarak verilmiştir; bağlayıcı olan bu metindir.',
    'sourcesPage.mit.name': 'MIT License',
    'sourcesPage.mit.copyright': 'Copyright (c) Fabio Crameri',
    'sourcesPage.mit.permission': 'Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:',
    'sourcesPage.mit.condition': 'The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.',
    'sourcesPage.mit.warranty': 'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.',
    // === /atlas:partner-sources ===
  }
};


const DEFAULT_LANG = 'en';
/* MER-241: the language is the page. <html lang> is "en" or "tr" in the static markup, and a
   visitor changes language by following the EN | TR links in the header (real pages, so it works
   without JavaScript and crawlers see each language at its own URL). Nothing is read from or
   written to storage, and nothing redirects by browser language. */
const currentLang = document.documentElement.lang === 'tr' ? 'tr' : DEFAULT_LANG;
const t = (key) => (I18N[currentLang] && I18N[currentLang][key]) || I18N[DEFAULT_LANG][key] || '';

/* The earlier client-side switch kept the choice in localStorage under this key. It is retired:
   the preference is never read (a stored "tr" would otherwise contradict the English URL and its
   canonical), and the leftover entry is removed so the site stores nothing in the browser. */
try {
  window.localStorage.removeItem('orbgss.lang');
} catch (error) {
  /* storage unavailable: nothing to remove */
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
/* Language: the page is already in its language (see above); only the   */
/* menu-toggle label, which depends on language and open state, is set.  */
/* ------------------------------------------------------------------ */
syncMenuToggleLabel();

/* ------------------------------------------------------------------ */
/* Graceful failure for self-hosted imagery: hide a scene that fails    */
/* to load so the dark panel background shows, never a broken glyph.    */
/* ------------------------------------------------------------------ */
document.querySelectorAll('.panel-image, .story-panel > img, .evidence-plate img, .domain-card > img, .domain-band > img, .locator-figure > img, .inspect-frame img, .stage-media, .panel-figure > img, .aoi-figure > img, .wide-figure > img, .split-figure > img, .plane img, .thumb').forEach((image) => {
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

/* Relative luminance at which the light caption (Agate mist, #E3E5E4) and the dark caption
   (Agate Graphite, #202629) contrast equally against their backdrop. Above it the dark tone wins,
   below it the light tone does. Derived from the WCAG contrast formula for those two exact colours
   (0.1885); it was 0.185 for the white and near-black captions the Atlas build used. */
const CAPTION_TONE_CROSSOVER = 0.1885;

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
