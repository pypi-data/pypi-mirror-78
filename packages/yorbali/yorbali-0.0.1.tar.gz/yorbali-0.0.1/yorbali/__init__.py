import pandas as pd

def GroupDf(dfr, cgp, cvl):
    chk = []
    for col in cgp+['z']:
        dfa = dfr.copy()
        for cof in chk:
            dfa.loc[:,cof] = "_"
        dfa = dfa.loc[:,cgp+cvl].groupby(cgp).sum()
        dfa.reset_index(inplace=True)
        if chk == []:
            dfs = dfa
        else:
            dfs = pd.concat([dfa, dfs],axis = 0, ignore_index=True)
        chk = chk + [col]
    r, c = dfs.shape
    print("Rows: " + str(r) + ", Columns: " + str(c))
    return dfs

def HighCol(col, cdt={"z":"white"}):
    if col.name in cdt.keys():
        return ["background-color: {}".format(cdt[col.name])]*len(col)
    return [''] * len(col)
    
def FormDis(dfr, lim=5):
    ftn = {"z":"{0:,.2f}"}
    ftc = {"z":"green"}
    for com in dfr.columns:
        try:
            one = dfr.loc[0,com]
            if float(one):
                if one != int(one):
                    ftn.update({com:"{0:,.2f}"})
                    ftc.update({com:"yellow"})
        except:
            dfr = dfr
    r, c = dfr.shape
    print("Rows: " + str(r) + ", Columns: " + str(c))
    ros = r if ((r < 20) & (lim == 5)) else lim
    return dfr.head(ros).style.format(ftn).apply(HighCol,cdt=ftc)