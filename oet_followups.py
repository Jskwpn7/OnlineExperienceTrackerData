"""Add Tier 1-3 follow-up questions (per in-scope harm) to estimates_long.csv.
Harm becomes the 'metric' selector; response categories become 'item'.
Waves 4-9 only (these follow-ups don't exist in the W1-2 files)."""
import pandas as pd, numpy as np, pyreadstat, re
from oet_checks import short, assert_waves_mapped, assert_unique

SAV="raw/data-sav-merged-waves-4-9.sav"
HARMS={"26":"Scams","24":"Deepfakes","11":"Misinformation","19":"Impersonation"}
MONTH2WAVE={"2023-07":4,"2024-01":5,"2024-05":6,"2024-06":6,"2025-01":7,"2025-06":8,"2025-07":8,"2026-01":9}
AGE_DUMMIES=["D2_2","D2_3","D2_4","D2_5","D2_6","D2_7","D2_8"]
GENDER={1:"Male",2:"Female",3:"Non-binary",4:"Other term",5:"Prefer not to say"}
AGE={ "D2_2":"18-24","D2_3":"25-34","D2_4":"35-44","D2_5":"45-54","D2_6":"55-64","D2_7":"65-74","D2_8":"75+"}
REGION={1:"Scotland",2:"North East",3:"North West",4:"Yorkshire & Humber",5:"West Midlands",6:"East Midlands",7:"Wales",8:"East of England",9:"London",10:"South East",11:"South West",12:"Northern Ireland"}
SEG={1:"AB",2:"AB",3:"C1C2",4:"C1C2",5:"DE",6:"DE"}
SMALL=50

# multi-select option labels (from questionnaire)
Q15={1:"Reported/flagged/marked junk",2:"Reposted to highlight it was wrong",3:"Contacted community to warn",4:"Complained to website/app/sender",5:"Informed the police",6:"Informed Ofcom",7:"Informed a support service",8:"Contacted account/user responsible",9:"Closed account/left service",10:"Unfollowed/blocked/muted/deleted",11:"Told a friend or family member",12:"Use the platform less",13:"Stopped using the platform",14:"Stopped commenting/liking/posting",15:"Stopped what I was doing/closed app",16:"Scrolled past it",17:"Started but didn't finish reporting",18:"Something else (ISP/other regulator)",19:"Changed content settings",20:"Changed privacy settings",21:"Flagged content not interested in",22:"Other",23:"Didn't take any action"}
Q16={1:"Didn't consider it harmful",2:"Didn't like it but not bad enough",3:"Didn't see the need",4:"Didn't know what to do/who to tell",5:"Didn't want to get into trouble",6:"Wanted to leave immediately",7:"Thought someone else would report",8:"Asked someone else to report",9:"Didn't think it would help",10:"Wasn't directly impacted",11:"Couldn't be bothered",12:"Thought the site would remove it",13:"Scared of retaliation",14:"Didn't have time",15:"People can say what they want",16:"Other"}
Q17={1:"Nothing yet",2:"Content was removed",3:"Got a written response",4:"Asked for further information",5:"Something else",6:"Don't know"}
MULTI={"Q15":("Actions taken (Q15)",Q15),"Q16":("Reasons for no action (Q16)",Q16),"Q17":("Reporting outcome (Q17)",Q17)}
# single-pick follow-ups: var pattern Qn_<harm>; title
SINGLE={"Q12":"Frequency seen (Q12)","Q21":"Where encountered (Q21)","Q30":"GenAI tool involved (Q30)","Q18":"Reporting satisfaction (Q18)"}

def load():
    cols=["starttime","weight","D1_C8","D3","profile_socialgrade_cie"]+AGE_DUMMIES+["Q9","Q32a1","Q32a"]
    for h in HARMS:
        for b in SINGLE: cols.append(f"{b}_{h}")
        for b in MULTI:
            cols+= [f"{b}_{h}_{i}" for i in MULTI[b][1]]
    cols=[c for c in dict.fromkeys(cols)]
    df,meta=pyreadstat.read_sav(SAV,usecols=cols)
    st=pd.to_datetime(df["starttime"],errors="coerce")
    df["wave"]=st.dt.to_period("M").astype(str).map(MONTH2WAVE)
    assert_waves_mapped(df,"oet_followups")
    df["Gender"]=df["D1_C8"].map(GENDER); df["Region"]=df["D3"].map(REGION); df["SEG"]=df["profile_socialgrade_cie"].map(SEG)
    age=pd.Series(index=df.index,dtype="object")
    for c,l in AGE.items(): age=age.mask(df[c]==1,l)
    df["Age"]=age
    df["is18plus"]=df[AGE_DUMMIES].fillna(0).sum(axis=1)>0
    return df,meta

def wshare(d,var,val):
    s=d[[var,"weight"]].dropna(subset=[var]); base=len(s)
    if base==0: return np.nan,0,0
    w=s["weight"].astype(float); eff=int(round(w.sum()**2/(w**2).sum())) if (w**2).sum()>0 else 0
    return round(100*(s[var].eq(val)*w).sum()/w.sum(),1),base,eff

def row(**k): return k

def build(df,meta):
    vvl=meta.variable_value_labels; rows=[]
    def emit(wave,basis,question,metric,item,var,pct,base,eff):
        rows.append(row(wave=int(wave),basis=basis,question=question,metric=metric,item=item,variable=var,
            subgroup="ALL",subgroup_value="All asked",weighted_pct=pct,unweighted_base=base,eff_base=eff,small_base=base<SMALL))
    for basis,d0 in [("as_published",df),("age18plus",df[df.is18plus])]:
        for wave,d in d0.groupby("wave"):
            # Q9 most recent harm (with subgroups)
            for code,theme in HARMS.items():
                # Q9 values are floats; harm code as int
                pct,base,eff=wshare(d,"Q9",float(code))
                rows.append(row(wave=int(wave),basis=basis,question="Most recent harm (Q9)",metric="most_recent",
                    item=theme,variable="Q9",subgroup="ALL",subgroup_value="All who hit any harm",
                    weighted_pct=pct,unweighted_base=base,eff_base=eff,small_base=base<SMALL))
                for sgname,sgcol in [("Gender","Gender"),("Age","Age"),("Region","Region"),("SEG","SEG")]:
                    for v,g in d.groupby(sgcol):
                        if pd.isna(v):continue
                        p,b,beff=wshare(g,"Q9",float(code))
                        rows.append(row(wave=int(wave),basis=basis,question="Most recent harm (Q9)",metric="most_recent",
                            item=theme,variable="Q9",subgroup=sgname,subgroup_value=v,weighted_pct=p,unweighted_base=b,eff_base=beff,small_base=b<SMALL))
            # Misinformation type & source (single var, misinfo only)
            for var,q in [("Q32a1","Misinformation: type (Q32a1)"),("Q32a","Misinformation: source (Q32a)")]:
                for code,lab in vvl.get(var,{}).items():
                    p,b,beff=wshare(d,var,code); emit(wave,basis,q,"Misinformation",short(lab),var,p,b,beff)
            # single-pick per-harm: Q12,Q21,Q30,Q18
            for b_,title in SINGLE.items():
                for code,theme in HARMS.items():
                    var=f"{b_}_{code}"
                    if var not in d.columns: continue
                    for cval,lab in vvl.get(var,{}).items():
                        p,bs,bse=wshare(d,var,cval); emit(wave,basis,title,theme,short(lab),var,p,bs,bse)
            # multi-select per-harm: Q15,Q16,Q17
            for b_,(title,optmap) in MULTI.items():
                for code,theme in HARMS.items():
                    for oi,olab in optmap.items():
                        var=f"{b_}_{code}_{oi}"
                        if var not in d.columns: continue
                        p,bs,bse=wshare(d,var,1.0); emit(wave,basis,title,theme,olab,var,p,bs,bse)
    return pd.DataFrame(rows)

if __name__=="__main__":
    df,meta=load(); print("loaded",len(df),flush=True)
    fu=build(df,meta); print("follow-up rows:",len(fu),flush=True)
    base=pd.read_csv("estimates_long.csv")
    base=base[~base.question.isin(fu.question.unique())]  # idempotent
    out=pd.concat([base,fu],ignore_index=True)
    assert_unique(fu,"oet_followups")
    out.to_csv("estimates_long.csv",index=False)
    print("total rows:",len(out),"| questions:",len(out.question.unique()),flush=True)
