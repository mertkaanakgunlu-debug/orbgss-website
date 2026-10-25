"""Text-contrast audit of every route in a real browser (Heat Trace brand adoption).

    python evidence/heat_trace/measure_contrast.py [--base http://127.0.0.1:8766] [--out measurements/contrast_audit.json]

Serve the repository root first (python -m http.server). For every text node on a solid ground the script resolves the
effective background (alpha-composited down the ancestor chain, white at the bottom) and the effective text colour, and
checks WCAG contrast against 4.5:1 (3:1 for large text). Text over photographs, the hero, figures and the caption labels
is judged by the caption-tone rule instead and is skipped here. Local tooling; not deployed.
"""
import argparse, json, pathlib
from playwright.sync_api import sync_playwright
ap=argparse.ArgumentParser(); ap.add_argument("--base",default="http://127.0.0.1:8766"); ap.add_argument("--chrome",default="/opt/pw-browsers/chromium-1243/chrome-linux64/chrome")
ap.add_argument("--out",default=str(pathlib.Path(__file__).parent/"measurements"/"contrast_audit.json")); args=ap.parse_args()
BASE=args.base; CHROME=args.chrome; OUT=args.out
routes=["/index.html","/solutions/index.html","/solutions/geothermal/index.html","/about/index.html","/partner/index.html","/sources/index.html","/404.html",
"/tr/index.html","/tr/cozumler/index.html","/tr/cozumler/jeotermal/index.html","/tr/hakkimizda/index.html","/tr/is-birligi/index.html","/tr/kaynaklar/index.html"]
JS = r"""
() => {
  const SKIP = '.hero, #hero, .context, #context, .domain-card, .domain-band, .scene-label, .panel-figure, [data-label-tone], .page-hero.ground-orbit, figure, .evidence-stage, .inspect-stage, .skip-link, #priority-legend, .priority-legend';
  function parse(c){ const m=c.match(/rgba?\(([^)]+)\)/); if(!m) return null; const p=m[1].split(/[ ,\/]+/).filter(Boolean).map(Number); return {r:p[0],g:p[1],b:p[2],a:p.length>3?p[3]:1}; }
  function over(fg,bg){ const a=fg.a; return {r:fg.r*a+bg.r*(1-a),g:fg.g*a+bg.g*(1-a),b:fg.b*a+bg.b*(1-a),a:1}; }
  function lum(c){ const f=v=>{v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4)}; return 0.2126*f(c.r)+0.7152*f(c.g)+0.0722*f(c.b); }
  function bgOf(el){
    const stack=[]; let n=el;
    while(n && n.nodeType===1){ const cs=getComputedStyle(n); if(cs.backgroundImage!=='none') return null; const c=parse(cs.backgroundColor); if(c && c.a>0){ stack.push(c); if(c.a>=1) break; } n=n.parentElement; }
    let base={r:255,g:255,b:255,a:1}; if(!(stack.length && stack[stack.length-1].a>=1)) base={r:255,g:255,b:255,a:1};
    for(let i=stack.length-1;i>=0;i--) base=over(stack[i],base);
    return base;
  }
  const out=[]; let count=0;
  const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
  const seen=new Set();
  while(walker.nextNode()){
    const t=walker.currentNode; if(!t.nodeValue.trim()) continue;
    const el=t.parentElement; if(!el||seen.has(el)) continue; seen.add(el);
    if(el.closest(SKIP)) continue;
    const cs=getComputedStyle(el); if(cs.visibility==='hidden'||cs.display==='none'||parseFloat(cs.opacity)===0) continue;
    const r=el.getBoundingClientRect(); if(r.width===0||r.height===0) continue;
    if(el.closest('[aria-hidden="true"]')) continue;
    const bg=bgOf(el); if(!bg) continue;
    let fg=parse(cs.color); if(!fg) continue; fg=over(fg,bg);
    const L1=lum(fg),L2=lum(bg); const ratio=(Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05);
    const size=parseFloat(cs.fontSize), bold=parseInt(cs.fontWeight)>=700;
    const large=size>=24||(size>=18.66&&bold);
    const floor=large?3:4.5; count++;
    if(ratio<floor) out.push({text:t.nodeValue.trim().slice(0,40),cls:el.className&&el.className.toString().slice(0,40),tag:el.tagName,ratio:+ratio.toFixed(2),floor,color:cs.color});
  }
  return {count,out};
}
"""
res={}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=CHROME)
    for vw,vh in ((1440,900),(390,844)):
        ctx=b.new_context(viewport={"width":vw,"height":vh}); pg=ctx.new_page()
        for r in routes:
            pg.goto(BASE+r); pg.wait_for_timeout(500)
            d=pg.evaluate(JS)
            res[f"{vw}{r}"]=d
            print(vw,r,d["count"],"checked",len(d["out"]),"below floor")
            for o in d["out"][:8]: print("   ",o)
        ctx.close()
    b.close()
summary={"routes":len(routes),"viewports":[1440,390],"text_nodes_checked":sum(v["count"] for v in res.values()),"below_floor":sum(len(v["out"]) for v in res.values())}
pathlib.Path(OUT).write_text(json.dumps({"summary":summary,"per_route":{k:{"checked":v["count"],"below_floor":v["out"]} for k,v in res.items()}},indent=1)+"\n")
print(summary)
