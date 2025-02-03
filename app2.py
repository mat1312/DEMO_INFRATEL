import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import zscore
from sklearn.linear_model import LinearRegression
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# Simuliamo dati finanziari
np.random.seed(42)
mesi = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
costi = np.random.randint(80000, 120000, size=12)
costi[5] = 200000  # Generiamo un'anomalia a Giugno
ricavi = costi + np.random.randint(10000, 30000, size=12)

df = pd.DataFrame({"Mese": mesi, "Costi": costi, "Ricavi": ricavi})

# Assegnazione casuale delle categorie di spesa
categorie = ["Infrastrutture", "Consulenze", "Software", "Servizi Operativi", "Manutenzione"]
df["Categoria"] = np.random.choice(categorie, size=12)

# Raggruppamento costi per categoria
df_categorie = df.groupby("Categoria")["Costi"].sum().reset_index()

# Modulo Audit: Identificazione anomalie
df["Z-Score Costi"] = zscore(df["Costi"])
soglia_anomalia = 2
anomalie = df[df["Z-Score Costi"].abs() > soglia_anomalia]

# Visualizzazione anomalie
st.subheader("🚨 Anomalie nei Costi")
if not anomalie.empty:
    for _, row in anomalie.iterrows():
        st.error(f"❌ {row['Mese']}: €{row['Costi']:,} (Z-Score: {row['Z-Score Costi']:.2f})")
else:
    st.success("✅ Nessuna anomalia rilevata.")

# Analisi Predittiva
X = np.arange(1, 13).reshape(-1, 1)
y = df["Costi"].values
modello = LinearRegression().fit(X, y)
mesi_futuri = np.array([[13], [14], [15]])
previsione = modello.predict(mesi_futuri)
df_pred = pd.DataFrame({"Mese": ["Gen 2026", "Feb 2026", "Mar 2026"], "Costi Previsti": previsione.astype(int)})

# 📊 Funzioni per salvare i grafici
def salva_grafico_andamento():
    buf = BytesIO()
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(df["Mese"], df["Costi"], label="Costi", marker="o", linestyle="-")
    ax.plot(df["Mese"], df["Ricavi"], label="Ricavi", marker="s", linestyle="--")
    ax.legend()
    plt.title("Andamento Costi vs Ricavi")
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return buf

def salva_grafico_categorie():
    buf = BytesIO()
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.pie(df_categorie["Costi"], labels=df_categorie["Categoria"], autopct='%1.1f%%', startangle=140)
    plt.title("Ripartizione Costi per Categoria")
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return buf

def salva_grafico_previsione():
    buf = BytesIO()
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(df["Mese"], df["Costi"], label="Costi Storici", marker="o")
    ax.plot(["Gen 2026", "Feb 2026", "Mar 2026"], previsione, label="Previsione Costi", marker="x", linestyle="dashed")
    ax.legend()
    plt.title("Previsione Costi Futuri")
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return buf

# 📝 Funzione per generare PDF con tutti i grafici

def genera_pdf():
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Titolo
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 50, "Report Audit - Analisi Costi & KPI")

    # KPI principali
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 80, f"📉 Costi Totali: €{df['Costi'].sum():,}")
    c.drawString(100, height - 100, f"💰 Ricavi Totali: €{df['Ricavi'].sum():,}")

    # Sezione anomalie
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, height - 140, "🚨 Anomalie nei Costi:")
    c.setFont("Helvetica", 12)
    y_position = height - 160
    if not anomalie.empty:
        for _, row in anomalie.iterrows():
            c.drawString(100, y_position, f"❌ {row['Mese']}: €{row['Costi']:,} (Z-Score: {row['Z-Score Costi']:.2f})")
            y_position -= 20
    else:
        c.drawString(100, y_position, "✅ Nessuna anomalia rilevata.")

    # Grafici
    y_position -= 200
    for grafico in [salva_grafico_andamento(), salva_grafico_categorie(), salva_grafico_previsione()]:
        img = ImageReader(grafico)
        c.drawImage(img, 100, y_position, width=400, height=200)
        y_position -= 180

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer


# Streamlit UI
st.title("📊 Dashboard Monitoraggio Costi & KPI")

# KPI principali
col1, col2 = st.columns(2)
col1.metric("📉 Costi Totali", f"€{df['Costi'].sum():,}")
col2.metric("💰 Ricavi Totali", f"€{df['Ricavi'].sum():,}")

# Grafico Costi vs Ricavi
st.subheader("📈 Andamento Costi e Ricavi")
fig, ax = plt.subplots(figsize=(6, 3))
ax.plot(df["Mese"], df["Costi"], label="Costi", marker="o", linestyle="-")
ax.plot(df["Mese"], df["Ricavi"], label="Ricavi", marker="s", linestyle="--")
ax.legend()
st.pyplot(fig)

# Grafico Ripartizione Costi per Categoria
st.subheader("📊 Ripartizione Costi per Categoria")
fig, ax = plt.subplots(figsize=(6, 3))
ax.pie(df_categorie["Costi"], labels=df_categorie["Categoria"], autopct='%1.1f%%', startangle=140)
st.pyplot(fig)

# Grafico Previsione Costi
st.subheader("📈 Previsione Costi Futuri")
fig, ax = plt.subplots(figsize=(6, 3))
ax.plot(df["Mese"], df["Costi"], label="Costi Storici", marker="o")
ax.plot(["Gen 2026", "Feb 2026", "Mar 2026"], previsione, label="Previsione Costi", marker="x", linestyle="dashed")
ax.legend()
st.pyplot(fig)

# Bottone per scaricare il report PDF
st.subheader("📄 Esportazione Report")
pdf_buffer = genera_pdf()
st.download_button(
    label="📥 Scarica Report in PDF",
    data=pdf_buffer,
    file_name="report_audit.pdf",
    mime="application/pdf",
)
