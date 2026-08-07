import pandas as pd, json, datetime

HARM_ITEM={"Scams, fraud, or phishing":"Scams & fraud","Deepfakes (fake/deceptive images & video)":"Deepfakes",
 "Misinformation / fake news":"Misinformation","Catfishing / impersonation":"Impersonation"}
THEME={"Scams":"Scams & fraud","Deepfakes":"Deepfakes","Misinformation":"Misinformation","Impersonation":"Impersonation"}
FOLLOWUP={"Frequency seen (Q12)":("How often seen","Severity & context"),
 "Where encountered (Q21)":("Where encountered (channel)","Where"),
 "Actions taken (Q15)":("Actions taken","Response"),
 "Reasons for no action (Q16)":("Reasons for no action","Response"),
 "Reporting outcome (Q17)":("Reporting outcome","Response"),
 "Reporting satisfaction (Q18)":("Reporting satisfaction","Response"),
 "GenAI tool involved (Q30)":("GenAI tool involved","Where"),
 "Impact: how bothered (Q14b)":("How bothered (impact)","Severity & context"),
 "Who it was directed at (Q14c)":("Who it targeted","Severity & context"),
 "Video app used (Q22)":("Specific platform: video","Where"),
 "Search engine used (Q23)":("Specific platform: search","Where"),
 "Social app used (Q24)":("Specific platform: social","Where"),
 "Livestream app used (Q25)":("Specific platform: livestream","Where"),
 "Messenger app used (Q26)":("Specific platform: messenger","Where"),
 "Gaming platform used (Q27)":("Specific platform: gaming","Where"),
 "Q&A site used (Q28)":("Specific platform: Q&A","Where"),
 "File-sharing used (Q29)":("Specific platform: file-sharing","Where")}
ATT={"Online Safety Act: knowledge (Q45)":("Online Safety Act: knowledge","Online Safety Act"),
 "Online Safety Act: confidence (Q46)":("Online Safety Act: confidence","Online Safety Act"),
 "Own content taken down (Q34)":("Own content taken down","Content moderation")}

def meta(q,metric,item):
    if q=="Concern (Q7)":
        return HARM_ITEM[item], ("Concern: very concerned" if metric=="very_concerned" else "Concern: any concern"),"Concern",False,True,""
    if q=="Experienced (Q8)": return HARM_ITEM[item],"Experienced","Prevalence",False,True,""
    if q=="Most recent harm (Q9)": return (HARM_ITEM.get(item) or THEME.get(item)),"Most recent harm","Prevalence",False,True,""
    if q=="Scams detail (Q32)":
        if metric=="lost_money": return "Scams & fraud","Money lost to a scam","Scams detail",False,False,""
        return "Scams & fraud","Type of scam (money lost)","Scams detail",True,False,item
    if q=="Misinformation: type (Q32a1)": return "Misinformation","Type of misinformation","Misinformation detail",True,False,item
    if q=="Misinformation: source (Q32a)": return "Misinformation","Source of misinformation","Misinformation detail",True,False,item
    if q in ATT:
        nm,st=ATT[q]; return "Attitudes",nm,st,True,False,item
    if q in FOLLOWUP and metric in THEME:
        nm,st=FOLLOWUP[q]; return THEME[metric],nm,st,True,True,item
    return None

e=pd.read_csv("estimates_long.csv").where(lambda d:d.notna(),None)
TOPICS=["Scams & fraud","Deepfakes","Misinformation","Impersonation","Attitudes"]
STAGE_ORDER=["Prevalence","Concern","Severity & context","Where","Response","Scams detail","Misinformation detail","Online Safety Act","Content moderation"]
measures={}  # name -> dict(stage,isCat,crossHarm)
responses=[]; subs=[]; sgvals=[]
rmap={}; gmap={}; vmap={}; mmap={}
def ridx(x):
    if x not in rmap: rmap[x]=len(responses); responses.append(x)
    return rmap[x]
def gidx(x):
    if x not in gmap: gmap[x]=len(subs); subs.append(x)
    return gmap[x]
def vidx(x):
    if x not in vmap: vmap[x]=len(sgvals); sgvals.append(x)
    return vmap[x]
def midx(name,stage,isCat,cross):
    if name not in mmap:
        mmap[name]=len(measures); measures[name]=dict(i=len(measures),n=name,stage=stage,isCat=isCat,cross=cross)
    return mmap[name]
B=["as_published","age18plus"]
rows=[]
for _,r in e.iterrows():
    m=meta(r["question"],r["metric"],r["item"])
    if not m: continue
    topic,measure,stage,isCat,cross,resp=m
    if r["weighted_pct"] is None: continue
    rows.append([int(r["wave"]),B.index(r["basis"]),TOPICS.index(topic),
        midx(measure,stage,isCat,cross),ridx(resp),gidx(r["subgroup"]),vidx(str(r["subgroup_value"])),
        round(float(r["weighted_pct"]),1),int(r["unweighted_base"]),1 if r["small_base"] else 0,int(r["eff_base"])])
# final gate: no two rows may share the same explorer key, or the UI silently shows the wrong figure
seen=set()
for x in rows:
    k=tuple(x[:7])  # wave,basis,topic,measure,response,subgroup,value
    if k in seen: raise SystemExit(f"build_explorer: duplicate explorer key {k} — label collision upstream?")
    seen.add(k)
M=[measures[n] for n in sorted(measures,key=lambda n:measures[n]["i"])]
for d in M: d.pop("i",None)
# polarity: 'bad' = a rise is adverse (red); everything else 'neu' (grey delta).
# Only unambiguous measures get a polarity — categorical follow-ups (actions taken,
# OSA knowledge, satisfaction, channel shares...) depend on which category is
# selected, so they stay neutral rather than mislead.
BAD={"Experienced","Concern: very concerned","Concern: any concern","Most recent harm","Money lost to a scam"}
for d in M: d["pol"]="bad" if d["n"] in BAD else "neu"
payload=dict(T=TOPICS,M=M,R=responses,G=subs,V=sgvals,B=B,STAGE=STAGE_ORDER,rows=rows)
DATA=json.dumps(payload,separators=(",",":"))
BUILD=datetime.date.today().isoformat()
print("topics",len(TOPICS),"measures",len(M),"rows",len(rows))

TEMPLATE=open("explorer_template.html").read()
open("OET_explorer.html","w").write(TEMPLATE.replace("/*__DATA__*/0",DATA).replace("__DATE__",BUILD))
print("wrote OET_explorer.html bytes:",len(TEMPLATE)+len(DATA))
