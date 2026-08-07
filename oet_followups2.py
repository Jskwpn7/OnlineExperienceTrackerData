"""Add remaining follow-ups: impact (Q14b), who-directed-at (Q14c), specific
platform per channel (Q22-Q29), and whole-sample attitudes (Q45/Q46/Q34).
Harm = 'metric' for per-harm items; attitudes use metric='Total' with subgroups."""
import pandas as pd, numpy as np, pyreadstat, re
from oet_checks import short, assert_waves_mapped, assert_unique
SAV="raw/data-sav-merged-waves-4-9.sav"
HARMS={"26":"Scams","24":"Deepfakes","11":"Misinformation","19":"Impersonation"}
MONTH2WAVE={"2023-07":4,"2024-01":5,"2024-05":6,"2024-06":6,"2025-01":7,"2025-06":8,"2025-07":8,"2026-01":9}
AGE_DUMMIES=["D2_2","D2_3","D2_4","D2_5","D2_6","D2_7","D2_8"]
GENDER={1:"Male",2:"Female",3:"Non-binary",4:"Other term",5:"Prefer not to say"}
AGE={"D2_2":"18-24","D2_3":"25-34","D2_4":"35-44","D2_5":"45-54","D2_6":"55-64","D2_7":"65-74","D2_8":"75+"}
REGION={1:"Scotland",2:"North East",3:"North West",4:"Yorkshire & Humber",5:"West Midlands",6:"East Midlands",7:"Wales",8:"East of England",9:"London",10:"South East",11:"South West",12:"Northern Ireland"}
SEG={1:"AB",2:"AB",3:"C1C2",4:"C1C2",5:"DE",6:"DE"}
SMALL=50
SINGLE_PERHARM={"Q14b":"Impact: how bothered (Q14b)","Q22":"Video app used (Q22)","Q23":"Search engine used (Q23)",
 "Q24":"Social app used (Q24)","Q25":"Livestream app used (Q25)","Q26":"Messenger app used (Q26)",
 "Q27":"Gaming platform used (Q27)","Q28":"Q&A site used (Q28)","Q29":"File-sharing used (Q29)"}
Q14c={1:"Directed at me",2:"Directed at someone close to me",3:"Happened to someone I don't know",4:"Don't know"}
ATT={"Q45":"Online Safety Act: knowledge (Q45)","Q46_combined":"Online Safety Act: confidence (Q46)","Q34":"Own content taken down (Q34)"}
SUBS=[("ALL",None),("Gender","Gender"),("Age","Age"),("Region","Region"),("SEG","SEG")]

def load():
    cols=["starttime","weight","D1_C8","D3","profile_socialgrade_cie"]+AGE_DUMMIES+list(ATT)
    for h in HARMS:
        for b in SINGLE_PERHARM: cols.append(f"{b}_{h}")
        cols+=[f"Q14c_{h}_{i}" for i in Q14c]
    cols=[c for c in dict.fromkeys(cols)]
    df,meta=pyreadstat.read_sav(SAV,usecols=cols)
    st=pd.to_datetime(df["starttime"],errors="coerce"); df["wave"]=st.dt.to_period("M").astype(str).map(MONTH2WAVE)
    assert_waves_mapped(df,"oet_followups2")
    df["Gender"]=df["D1_C8"].map(GENDER); df["Region"]=df["D3"].map(REGION); df["SEG"]=df["profile_socialgrade_cie"].map(SEG)
    age=pd.Series(index=df.index,dtype="object")
    for c,l in AGE.items(): age=age.mask(df[c]==1,l)
    df["Age"]=age; df["is18plus"]=df[AGE_DUMMIES].fillna(0).sum(axis=1)>0
    return df,meta

def wshare(d,var,val):
    s=d[[var,"weight"]].dropna(subset=[var]); base=len(s)
    if base==0: return np.nan,0,0
    w=s["weight"].astype(float); eff=int(round(w.sum()**2/(w**2).sum())) if (w**2).sum()>0 else 0
    return round(100*(s[var].eq(val)*w).sum()/w.sum(),1),base,eff

def build(df,meta):
    vvl=meta.variable_value_labels; rows=[]
    def add(wave,basis,q,metric,item,var,sgname,sgval,pct,base,eff):
        rows.append(dict(wave=int(wave),basis=basis,question=q,metric=metric,item=item,variable=var,
            subgroup=sgname,subgroup_value=sgval,weighted_pct=pct,unweighted_base=base,eff_base=eff,small_base=base<SMALL))
    for basis,d0 in [("as_published",df),("age18plus",df[df.is18plus])]:
        for wave,d in d0.groupby("wave"):
            # single-pick per-harm (Q14b, Q22-Q29)
            for b_,title in SINGLE_PERHARM.items():
                for code,theme in HARMS.items():
                    var=f"{b_}_{code}"
                    if var not in d.columns: continue
                    for cval,lab in vvl.get(var,{}).items():
                        p,bs,bse=wshare(d,var,cval); add(wave,basis,title,theme,short(lab),var,"ALL","All asked",p,bs,bse)
            # Q14c multi-select per-harm
            for code,theme in HARMS.items():
                for oi,olab in Q14c.items():
                    var=f"Q14c_{code}_{oi}"
                    if var not in d.columns: continue
                    p,bs,bse=wshare(d,var,1.0); add(wave,basis,"Who it was directed at (Q14c)",theme,olab,var,"ALL","All asked",p,bs,bse)
            # whole-sample attitudes with subgroups
            for var,title in ATT.items():
                if var not in d.columns: continue
                for cval,lab in vvl.get(var,{}).items():
                    for sgname,sgcol in SUBS:
                        groups=[("All respondents",d)] if sgcol is None else [(v,g) for v,g in d.groupby(sgcol) if pd.notna(v)]
                        for sgval,g in groups:
                            p,bs,bse=wshare(g,var,cval); add(wave,basis,title,"Total",short(lab),var,sgname,sgval,p,bs,bse)
    return pd.DataFrame(rows)

if __name__=="__main__":
    df,meta=load(); print("loaded",len(df),flush=True)
    fu=build(df,meta); print("rows:",len(fu),flush=True)
    base=pd.read_csv("estimates_long.csv"); base=base[~base.question.isin(fu.question.unique())]
    out=pd.concat([base,fu],ignore_index=True)
    out=out[(out.unweighted_base.fillna(0)>0)&out.weighted_pct.notna()]
    assert_unique(out,"oet_followups2 (final table)")
    out.to_csv("estimates_long.csv",index=False)
    print("total rows:",len(out),"| questions:",out.question.nunique(),flush=True)
