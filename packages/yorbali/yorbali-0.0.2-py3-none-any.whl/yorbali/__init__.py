import pandas as pd
import numpy as np
import random
import datetime
# =======================================================================

def CreData(rec=100000, dys=1000, dst='01/01/2017', pof=1):
    """
    Create a dataframe with rec number of records, spread over dys mumber of
    days starting from date dst, including pof percent of offsetting records.
    Two records are offsetting if they have same values for "item" fields;
    and positive "amounts" record is followed by negative "amounts" record.
    """

    dfr1 = pd.DataFrame(data = {
           'TranDat': np.random.randint(1,dys,rec),
           'RefrOne': np.random.randint(1,10,rec),
           'RefrTwo': np.random.randint(1,100,rec),
           'RefrTri': np.random.randint(1,1000,rec),
           'RefrFor': np.random.randint(1,10000,rec),
           'RefrFiv': np.random.randint(1,100000,rec),
           'RefrSix': np.random.randint(1,1000000,rec),
           'ValuOne': np.random.randint(1,10000000,rec),
           'ValuTwo': np.random.randint(1,10000000,rec),
           'ValuTri': np.random.randint(1,10000000,rec) })
    
    rof = int(rec*pof/100)
    dfr2 = dfr1.iloc[np.random.randint(1,rec,rof),:]
    dfr2['TranDat'] = dfr2['TranDat'].apply(lambda x: random.randint(-5,35))
    dfr2['ValuOne'] = - dfr2['ValuOne']
    dfr2['ValuTwo'] = - dfr2['ValuTwo']
    dfr2['ValuTri'] = - dfr2['ValuTri']

    dfr3 = pd.concat([dfr1, dfr2], axis = 0, ignore_index=True)

    dfr3['TranDat'] = dfr3['TranDat'].apply(lambda x: datetime.datetime.strptime(dst,"%m/%d/%Y") + datetime.timedelta(days=x))
    dfr3['ValuOne'] = dfr3['ValuOne'].apply(lambda x: round(x/100,2))
    dfr3['ValuTwo'] = dfr3['ValuTwo'].apply(lambda x: round(x/100,2))
    dfr3['ValuTri'] = dfr3['ValuTri'].apply(lambda x: round(x/100,2))

    print("Rows: " + str(dfr3.shape[0]) + ", Columns: " + str(dfr3.shape[1]))
    return dfr3
# =======================================================================

def GetOffs(dfr, cre, cvl, cdt):
    """
    Identify offsetting records in dataframe dfr, with array cre of
    grouping fields, array cvl of amount fields, and date field cdt.
    """

    dfr1 = dfr.loc[:,cre+cvl+[cdt]]
    cab = ["Abs" + com for com in cvl]
    qry = "Qty == 2 & Dat < 1"
    for com in cvl:
        dfr1["Abs" + com] = dfr1.loc[:,com].apply(lambda x: abs(x))
        qry = qry + " & " + com + " == 0"

    dfr1["Qty"] = dfr1[cvl[0]]
    dfr1["Dat"] = dfr1[cdt].apply(lambda x: (x.year-2000)*10000+(x.month)*100+(x.day))
    dfr1["Dat"] = dfr1.apply(lambda x: -x.Dat if (x.Qty < 0) else x.Dat, axis=1)
    dfr1["Qty"] = 1

    dfr2 = dfr1.loc[:,cre+cab+cvl+["Qty","Dat"]].groupby(cre+cab).sum()
    dfr2.reset_index(inplace=True)
    dfr2 = dfr2.query(qry)
    dfr2 = dfr2.loc[:, cre+cab]
    dfr2["Off"] = "Offs"

    dfr3 = dfr.merge(dfr2, how="outer")
    dfr3["Off"] = dfr3["Off"].fillna("NonO")
    for com in cvl:
        dfr3["Abs" + com] = dfr3.loc[:,com].apply(lambda x: abs(x))

    print("Rows: " + str(dfr3.shape[0]) + ", Columns: " + str(dfr3.shape[1]))
    return dfr3
# =======================================================================

def GroupDf(dfr, cgp, cvl):
    """
    Run GroupBy on a datafarme dfr, for all possible combinations of fields
    specified in array cgp, and evaluate Sum for fields in array cvl.
    """

    chk = []
    for col in cgp+['z']:

        dfr1 = dfr.copy()
        for cof in chk:
            dfr1.loc[:,cof] = "_"
        dfr1 = dfr1.loc[:,cgp+cvl].groupby(cgp).sum()
        dfr1.reset_index(inplace=True)

        if chk == []:
            dfr2 = dfr1
        else:
            dfr2 = pd.concat([dfr1, dfr2], axis = 0, ignore_index=True)
        chk = chk + [col]

    print("Rows: " + str(dfr2.shape[0]) + ", Columns: " + str(dfr2.shape[1]))
    return dfr2
# =======================================================================

def HighCol(col, dct={"z":"white"}):
    """
    Use this as an argument in dataframe.style.apply,
    to highlight columns specified by keys of dictionary dct.
    """

    if col.name in dct.keys():
        return ["background-color: {}".format(dct[col.name])]*len(col)
    return [''] * len(col)
# =======================================================================

def FormDis(dfr, num=5):
    """
    Format and display num number of rows of dataframe dfr,
    with float-type values in 2 decimals and yellow color.
    """

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
    ros = r if ((r < 20) & (num == 5)) else num

    print("Rows: " + str(r) + ", Columns: " + str(c))
    return dfr.head(ros).style.format(ftn).apply(HighCol,dct=ftc)
# =======================================================================
