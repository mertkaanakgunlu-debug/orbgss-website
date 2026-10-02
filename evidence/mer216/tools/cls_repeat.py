import sys,time,json
sys.path.insert(0, __file__.rsplit("\\",1)[0])
from mer216_harness import Chrome, serve
import audit_phase4 as ap
res={}
for tag,root in (("baseline",sys.argv[1]),("after",sys.argv[2])):
    srv=serve(root); chrome=Chrome(); vals=[]
    try:
        for _ in range(6):
            page=ap.open_page(chrome,srv,3840,2160,1.0,False,reduced=True)
            page.navigate(srv.base+"/"); page.js(ap.SCROLL,timeout=90); time.sleep(0.5)
            vals.append(page.js(ap.PAGE_CHECK)["cls"]); page.close()
    finally:
        chrome.close(); srv.close()
    res[tag]=vals
print(json.dumps(res))
json.dump(res,open(sys.argv[3],"w"))
