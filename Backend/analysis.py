import pandas as pd

def gesamt_tore(df):
    return df['Tore'].sum()

def gesamt_7m(df):
    return df['7m_Treffer'].sum(), df['7m_Chancen'].sum()

def gesamt_zweitstrafe(df):
    return df[['2min_1','2min_2','2min_3']].apply(lambda x: x.ne('').sum()).sum()

def gesamt_disq(df):
    return df['Disqualifikation'].ne('').sum()

def tore_spieler(df, spieler_name):
    df_spieler = df[df['Name'] == spieler_name]
    return df_spieler['Tore'].sum()

def ranking_gesamttore(df):
    df_summary = df.groupby("Name")["Tore"].sum().reset_index()
    df_summary = df_summary.sort_values(by="Tore", ascending=False).reset_index(drop=True)
    df_summary['Rang'] = df_summary.index + 1
    return df_summary

def ranking_gesamt(df):
    df_summary = df.groupby("Name").agg({
        "Tore": "sum",
        "7m_Treffer": "sum",
        "7m_Chancen": "sum",
        "2min_1": lambda x: x.ne('').sum(),
        "2min_2": lambda x: x.ne('').sum(),
        "2min_3": lambda x: x.ne('').sum(),
        "Disqualifikation": lambda x: x.ne('').sum()
    }).reset_index()

    df_summary['2min_gesamt'] = df_summary[['2min_1','2min_2','2min_3']].sum(axis=1)
    df_summary = df_summary[['Name','Tore','7m_Treffer','7m_Chancen','2min_gesamt','Disqualifikation']]
    df_summary = df_summary.sort_values(by="Tore", ascending=False).reset_index(drop=True)
    df_summary['Rang'] = df_summary.index + 1
    return df_summary
