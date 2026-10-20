"""OET Phase 1+ — build in-scope catalogue + weighted estimates (waves 4+; files set in oet_sources.py),
incl. the Q32 scams-detail module. Run: python oet_build_estimates.py"""
import pandas as pd, numpy as np, pyreadstat
from oet_sources import read_merged, MONTH2WAVE
from oet_checks import assert_waves_mapped, assert_unique

ITEMS = {"11":"Misinformation / fake news","19":"Catfishing / impersonation",
         "24":"Deepfakes (fake/deceptive images & video)","26":"Scams, fraud, or phishing"}
AGE_DUMMIES = {"D2_2":"18-24","D2_3":"25-34","D2_4":"35-44","D2_5":"45-54",
               "D2_6":"55-64","D2_7":"65-74","D2_8":"75+"}
GENDER = {1:"Male",2:"Female",3:"Non-binary",4:"Other term",5:"Prefer not to say"}
REGION = {1:"Scotland",2:"North East",3:"North West",4:"Yorkshire & Humber",5:"West Midlands",
          6:"East Midlands",7:"Wales",8:"East of England",9:"London",10:"South East",
          11:"South West",12:"Northern Ireland"}
SEG = {1:"AB",2:"AB",3:"C1C2",4:"C1C2",5:"DE",6:"DE"}
SMALL_BASE = 50
FRAUD_TYPES = {"1":"Impersonation fraud","2":"Counterfeit goods scam","3":"Investment/pension scam",
   "4":"Computer software / ransomware","5":"Fake employment scam","6":"Romance/dating scam",
   "7":"Health/medical scam","8":"Identity fraud","9":"Psychic/clairvoyant scam",
   "10":"Holiday scam","11":"Money mule / laundering","12":"Purchase scam"}
METRICS = [("Concern (Q7)","Q7","very_concerned",(5,)),
           ("Concern (Q7)","Q7","any_concern",(1,2,3,4,5)),
           ("Experienced (Q8)","Q8","experienced",(1,))]
SUBGROUPS = [("ALL",None),("Gender","Gender"),("Age","Age"),("Region","Region"),("SEG","SEG")]

def load():
    q=[f"Q7_{s}" for s in ITEMS]+[f"Q8_{s}" for s in ITEMS]+["Q32b1"]+[f"Q32b2_{i}" for i in range(1,13)]
    cols=["starttime","weight","D1_C8","D3","profile_socialgrade_cie"]+list(AGE_DUMMIES)+q
    df,_=read_merged(cols)
    st=pd.to_datetime(df["starttime"],errors="coerce")
    df["wave"]=st.dt.to_period("M").astype(str).map(MONTH2WAVE)
    assert_waves_mapped(df,"oet_build_estimates")
    df["Gender"]=df["D1_C8"].map(GENDER); df["Region"]=df["D3"].map(REGION)
    df["SEG"]=df["profile_socialgrade_cie"].map(SEG)
    age=pd.Series(index=df.index,dtype="object")
    for c,lab in AGE_DUMMIES.items(): age=age.mask(df[c]==1,lab)
    df["Age"]=age
    df["is18plus"]=df[list(AGE_DUMMIES)].fillna(0).sum(axis=1)>0
    return df

def wpct(d,var,positive):
    s=d[[var,"weight"]].dropna(subset=[var]); base=len(s)
    if base==0: return np.nan,0,0
    w=s["weight"].astype(float); pos=s[var].isin(positive).astype(float)
    eff=int(round(w.sum()**2/(w**2).sum())) if (w**2).sum()>0 else 0
    return round(100*(pos*w).sum()/w.sum(),1),base,eff

def build_estimates(df):
    rows=[]
    for basis,d in [("as_published",df),("age18plus",df[df.is18plus])]:
        for wave,dw in d.groupby("wave"):
            for qlabel,pref,metric,pos in METRICS:
                for suf,ilabel in ITEMS.items():
                    var=f"{pref}_{suf}"
                    if var not in dw.columns: continue
                    for sgname,sgcol in SUBGROUPS:
                        groups=[("All respondents",dw)] if sgcol is None else [(v,g) for v,g in dw.groupby(sgcol) if pd.notna(v)]
                        for sgval,g in groups:
                            pct,base,eff=wpct(g,var,pos)
                            rows.append(dict(wave=int(wave),basis=basis,question=qlabel,metric=metric,
                                item=ilabel,variable=var,subgroup=sgname,subgroup_value=sgval,
                                weighted_pct=pct,unweighted_base=base,eff_base=eff,small_base=base<SMALL_BASE))
    return pd.DataFrame(rows)

def build_q32(df):
    rows=[]
    for basis,d in [("as_published",df),("age18plus",df[df.is18plus])]:
        for wave,dw in d.groupby("wave"):
            if "Q32b1" in dw.columns:
                for sgname,sgcol in SUBGROUPS:
                    groups=[("All who experienced scams",dw)] if sgcol is None else [(v,g) for v,g in dw.groupby(sgcol) if pd.notna(v)]
                    for sgval,g in groups:
                        pct,base,eff=wpct(g,"Q32b1",(1,))
                        rows.append(dict(wave=int(wave),basis=basis,question="Scams detail (Q32)",
                            metric="lost_money",item="Lost money/assets to a scam",variable="Q32b1",
                            subgroup=sgname,subgroup_value=sgval,weighted_pct=pct,unweighted_base=base,eff_base=eff,small_base=base<SMALL_BASE))
            for suf,lab in FRAUD_TYPES.items():
                var=f"Q32b2_{suf}"
                if var not in dw.columns: continue
                pct,base,eff=wpct(dw,var,(1,))
                rows.append(dict(wave=int(wave),basis=basis,question="Scams detail (Q32)",
                    metric="scam_type_money_lost",item=lab,variable=var,subgroup="ALL",
                    subgroup_value="Of those who lost money to a scam",weighted_pct=pct,unweighted_base=base,eff_base=eff,small_base=base<SMALL_BASE))
    return pd.DataFrame(rows)

def build_catalogue(df):
    rows=[]
    def present(var):
        return ",".join(str(int(w)) for w in sorted(df.dropna(subset=[var])["wave"].dropna().unique()))
    specs=[("Q7","Concern (Q7)","Scale 1-5 top-box; base=all"),("Q8","Experienced (Q8)","Seen/experienced last 4 wks; base=all")]
    for suf,ilabel in ITEMS.items():
        for pref,qlabel,desc in specs:
            var=f"{pref}_{suf}"
            if var not in df.columns: continue
            waves=sorted(int(w) for w in df.dropna(subset=[var])["wave"].dropna().unique())
            rows.append(dict(item=ilabel,question=qlabel,variable=var,metric=desc,waves_present=",".join(map(str,waves))))
    rows.append(dict(item="Lost money/assets to a scam",question="Scams detail (Q32)",variable="Q32b1",
        metric="% Yes; base = those who experienced scams",waves_present=present("Q32b1")))
    for suf,lab in FRAUD_TYPES.items():
        rows.append(dict(item=lab,question="Scams detail (Q32)",variable=f"Q32b2_{suf}",
            metric="% of money-losers; SMALL base",waves_present=present(f"Q32b2_{suf}")))
    return pd.DataFrame(rows)

if __name__=="__main__":
    df=load(); print("loaded",len(df),flush=True)
    build_catalogue(df).to_csv("catalogue.csv",index=False)
    est=pd.concat([build_estimates(df),build_q32(df)],ignore_index=True)
    assert_unique(est,"oet_build_estimates")
    est.to_csv("estimates_long.csv",index=False)
    print("WROTE",len(est),"rows; questions:",est.question.unique().tolist(),flush=True)
