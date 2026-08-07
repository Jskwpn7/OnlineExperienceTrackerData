"""Backfill OET waves 1 (2021) & 2 (2022) into the estimates table.
Crosswalk is by LABEL — codes differ from modern waves.
Produces rows in the same schema as oet_build_estimates and appends them."""
import pandas as pd, numpy as np, pyreadstat
from oet_checks import assert_unique

DIR="raw/waves 1 and 2/"
FILES={1:("online-experiences-tracker-wave-1.sav",2021),
       2:("online-experiences-tracker-wave-2.sav",2022)}
# item suffix maps (same in W1 & W2)
Q8={"q08_09":"Misinformation / fake news","q08_15":"Catfishing / impersonation",
    "q08_20":"Deepfakes (fake/deceptive images & video)","q08_22":"Scams, fraud, or phishing"}
Q7={"q07_09":"Misinformation / fake news","q07_16":"Catfishing / impersonation",
    "q07_21":"Deepfakes (fake/deceptive images & video)","q07_23":"Scams, fraud, or phishing"}  # W1 only
GENDER={1:"Male",2:"Female",3:"Non-binary",4:"Other term",6:"Prefer not to say"}
AGE={3:"18-24",4:"25-34",5:"35-44",6:"45-54",7:"55-64",8:"65-74",9:"75+",10:"75+"}  # <18 (1,2) -> None
REGION={1:"Scotland",2:"North East",3:"North West",4:"Yorkshire & Humber",5:"West Midlands",
        6:"East Midlands",7:"Wales",8:"East of England",9:"London",10:"South East",11:"South West",12:"Northern Ireland"}
SEG={1:"AB",2:"AB",3:"C1C2",4:"C1C2",5:"DE",6:"DE"}
SUBGROUPS=[("ALL",None),("Gender","Gender"),("Age","Age"),("Region","Region"),("SEG","SEG")]
SMALL_BASE=50

def wpct(d,var,positive):
    s=d[[var,"weight"]].dropna(subset=[var]); base=len(s)
    if base==0: return np.nan,0,0
    w=s["weight"].astype(float); pos=s[var].isin(positive).astype(float)
    eff=int(round(w.sum()**2/(w**2).sum())) if (w**2).sum()>0 else 0
    return round(100*(pos*w).sum()/w.sum(),1),base,eff

def metric_rows(df,wave,question,metric,varmap,positive,is18col):
    rows=[]
    for basis,d in [("as_published",df),("age18plus",df[df[is18col]])]:
        for var,ilabel in varmap.items():
            if var not in d.columns: continue
            for sgname,sgcol in SUBGROUPS:
                groups=[("All respondents" if metric!="lost_money" else "x",d)] if sgcol is None \
                       else [(v,g) for v,g in d.groupby(sgcol) if pd.notna(v)]
                for sgval,g in groups:
                    pct,base,eff=wpct(g,var,positive)
                    rows.append(dict(wave=wave,basis=basis,question=question,metric=metric,
                        item=ilabel,variable=var,subgroup=sgname,subgroup_value=sgval,
                        weighted_pct=pct,unweighted_base=base,eff_base=eff,small_base=base<SMALL_BASE))
    return rows

def build():
    allrows=[]
    for wv,(f,year) in FILES.items():
        df,_=pyreadstat.read_sav(DIR+f)
        df["Gender"]=df["d01"].map(GENDER); df["Age"]=df["d02"].map(AGE)
        df["Region"]=df["d03"].map(REGION); df["SEG"]=df["d04b"].map(SEG)
        df["is18plus"]=df["d02"].isin(list(AGE.keys()))
        # Q8 experienced (both waves)
        allrows+=metric_rows(df,wv,"Experienced (Q8)","experienced",Q8,(1,),"is18plus")
        # Q7 concern (wave 1 only)
        if any(c in df.columns for c in Q7):
            allrows+=metric_rows(df,wv,"Concern (Q7)","very_concerned",Q7,(5,),"is18plus")
            allrows+=metric_rows(df,wv,"Concern (Q7)","any_concern",Q7,(1,2,3,4,5),"is18plus")
    return pd.DataFrame(allrows)

if __name__=="__main__":
    w12=build()
    print("W1/W2 rows:",len(w12),flush=True)
    base=pd.read_csv("estimates_long.csv")
    base=base[~base.wave.isin([1,2])]  # idempotent
    out=pd.concat([base,w12],ignore_index=True).sort_values(["question","metric","item","basis","subgroup","wave"])
    assert_unique(out,"oet_backfill_w12 (after append)")
    out.to_csv("estimates_long.csv",index=False)
    print("total rows now:",len(out),"| waves:",sorted(out.wave.unique()),flush=True)
