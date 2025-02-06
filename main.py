# main.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import zscore
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

# Importiamo le funzioni dal file helper.py
from helper import (
    salva_grafico_andamento,
    salva_grafico_categorie,
    salva_grafico_previsione,
    genera_pdf,
    salva_grafico_turnover,
    genera_pdf_capitale_umano,
    salva_grafico_commesse,
    salva_grafico_previsione_turnover
)

# -------------------------------
# Parte 1: Analisi dei Dati Finanziari
# -------------------------------
np.random.seed(42)
mesi = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
costi = np.random.randint(80000, 120000, size=12)
costi[5] = 200000  # Generiamo un'anomalia a Giugno
ricavi = costi + np.random.randint(10000, 30000, size=12)

df = pd.DataFrame({"Mese": mesi, "Costi": costi, "Ricavi": ricavi})
categorie = ["Infrastrutture", "Consulenze", "Software", "Servizi Operativi", "Manutenzione"]
df["Categoria"] = np.random.choice(categorie, size=12)
df_categorie = df.groupby("Categoria")["Costi"].sum().reset_index()

# Calcolo Z-Score per individuare anomalie
df["Z-Score Costi"] = zscore(df["Costi"])
soglia_anomalia = 2
anomalie = df[df["Z-Score Costi"].abs() > soglia_anomalia]

# Analisi Predittiva sui Costi
X = np.arange(1, 13).reshape(-1, 1)
y = df["Costi"].values
modello = LinearRegression().fit(X, y)
mesi_futuri = np.array([[13], [14], [15]])
previsione = modello.predict(mesi_futuri)
df_pred = pd.DataFrame({
    "Mese": ["Gen 2026", "Feb 2026", "Mar 2026"],
    "Costi Previsti": previsione.astype(int)
})

st.title("📊 Dashboard Monitoraggio Costi & KPI")
col1, col2 = st.columns(2)
col1.metric("📉 Costi Totali", f"€{df['Costi'].sum():,}")
col2.metric("💰 Ricavi Totali", f"€{df['Ricavi'].sum():,}")

st.subheader("🚨 Anomalie nei Costi")
if not anomalie.empty:
    for _, row in anomalie.iterrows():
        st.error(f"❌ {row['Mese']}: €{row['Costi']:,} (Z-Score: {row['Z-Score Costi']:.2f})")
else:
    st.success("✅ Nessuna anomalia rilevata.")

st.subheader("📈 Andamento Costi e Ricavi")
fig, ax = plt.subplots(figsize=(6, 3))
ax.plot(df["Mese"], df["Costi"], label="Costi", marker="o", linestyle="-")
ax.plot(df["Mese"], df["Ricavi"], label="Ricavi", marker="s", linestyle="--")
ax.legend()
st.pyplot(fig)

st.subheader("📊 Ripartizione Costi per Categoria")
fig, ax = plt.subplots(figsize=(6, 3))
ax.pie(df_categorie["Costi"], labels=df_categorie["Categoria"], autopct='%1.1f%%', startangle=140)
st.pyplot(fig)

st.subheader("📈 Previsione Costi Futuri")
fig, ax = plt.subplots(figsize=(6, 3))
ax.plot(df["Mese"], df["Costi"], label="Costi Storici", marker="o")
ax.plot(["Gen 2026", "Feb 2026", "Mar 2026"], previsione, label="Previsione Costi", marker="x", linestyle="dashed")
ax.legend()
plt.xticks(rotation=45, ha="right")
plt.subplots_adjust(bottom=0.2)
plt.title("Previsione Costi Futuri")
st.pyplot(fig)

st.subheader("📄 Esportazione Report Audit")
pdf_buffer = genera_pdf(df, df_categorie, anomalie, previsione)
st.download_button(
    label="📥 Scarica Report in PDF",
    data=pdf_buffer,
    file_name="report_audit.pdf",
    mime="application/pdf",
)

# -------------------------------
# Parte 2: Analisi Turnover Dipendenti & Capitale Umano
# -------------------------------
st.title("👥 Analisi Turnover Dipendenti & Capitale Umano")
turnover = np.random.randint(5, 21, size=12)
df_turnover = pd.DataFrame({"Mese": mesi, "Turnover": turnover})
soglia_turnover = 15

X_turn = np.arange(1, 13).reshape(-1, 1)
y_turn = df_turnover["Turnover"].values
modello_turnover = LinearRegression().fit(X_turn, y_turn)
mesi_futuri_turn = np.array([[13], [14], [15]])
previsione_turnover = modello_turnover.predict(mesi_futuri_turn)
df_turnover_pred = pd.DataFrame({
    "Mese": ["Gen 2026", "Feb 2026", "Mar 2026"],
    "Turnover Previsto": previsione_turnover.astype(int)
})

st.subheader("📈 Andamento Turnover Storico")
fig, ax = plt.subplots(figsize=(6, 3))
ax.plot(df_turnover["Mese"], df_turnover["Turnover"], label="Turnover Storico", marker="o")
ax.axhline(y=soglia_turnover, color='r', linestyle='--', label=f"Soglia {soglia_turnover}%")
ax.legend()
plt.title("Turnover Mensile")
st.pyplot(fig)

st.subheader("📈 Previsione Turnover Futuro")
fig, ax = plt.subplots(figsize=(6, 3))
ax.plot(df_turnover["Mese"], df_turnover["Turnover"], label="Turnover Storico", marker="o")
ax.plot(["Gen 2026", "Feb 2026", "Mar 2026"], previsione_turnover, label="Previsione Turnover", marker="x", linestyle="dashed")
ax.axhline(y=soglia_turnover, color='r', linestyle='--', label=f"Soglia {soglia_turnover}%")
ax.legend()
plt.xticks(rotation=45, ha="right")
plt.subplots_adjust(bottom=0.2)
plt.title("Previsione Turnover")
st.pyplot(fig)

if (df_turnover["Turnover"] > soglia_turnover).any():
    st.error(f"⚠️ Attenzione: Il turnover ha superato la soglia del {soglia_turnover}% in alcuni mesi!")
if (previsione_turnover > soglia_turnover).any():
    st.error(f"⚠️ Attenzione: La previsione indica che il turnover supererà la soglia del {soglia_turnover}% nei prossimi mesi!")

st.subheader("📄 Esportazione Report Capitale Umano")
pdf_buffer_capitale = genera_pdf_capitale_umano(df_turnover, df_turnover_pred, soglia_turnover, previsione_turnover)
st.download_button(
    label="📥 Scarica Report Capitale Umano in PDF",
    data=pdf_buffer_capitale,
    file_name="report_capitale_umano.pdf",
    mime="application/pdf",
)

# -------------------------------
# Parte 3: Monitoraggio Commesse e Collaudi
# -------------------------------
st.title("📌 Monitoraggio Commesse e Collaudi")
progetti = ['Progetto A', 'Progetto B', 'Progetto C', 'Progetto D']
budget = np.random.randint(200000, 500000, size=4)
costi_attuali = budget * np.random.uniform(0.5, 1.2, size=4)
avanzamento = np.random.randint(30, 100, size=4)
data_scadenza = pd.to_datetime(['2025-06-30', '2025-09-30', '2025-12-31', '2025-11-15'])
df_commesse = pd.DataFrame({
    'Progetto': progetti,
    'Budget': budget,
    'Costi Attuali': costi_attuali.astype(int),
    'Avanzamento (%)': avanzamento,
    'Data Scadenza': data_scadenza
})
st.dataframe(df_commesse)

fig, ax = plt.subplots(figsize=(6, 3))
ax.bar(df_commesse['Progetto'], df_commesse['Budget'], label='Budget', alpha=0.6)
ax.bar(df_commesse['Progetto'], df_commesse['Costi Attuali'], label='Costi Attuali', alpha=0.6)
ax.set_ylabel("€")
ax.legend()
plt.title("Budget vs Costi Attuali")
st.pyplot(fig)

df_commesse['A Rischio'] = df_commesse['Costi Attuali'] > 0.9 * df_commesse['Budget']
st.subheader("Progetti a Rischio")
st.write(df_commesse[df_commesse['A Rischio']])
