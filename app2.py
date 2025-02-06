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

# -------------------------------
# Parte 1: Analisi dei Dati Finanziari
# -------------------------------
# Simuliamo dati finanziari
np.random.seed(42)
mesi = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
costi = np.random.randint(80000, 120000, size=12)
costi[5] = 200000  # Generiamo un'anomalia a Giugno
ricavi = costi + np.random.randint(10000, 30000, size=12)

df = pd.DataFrame({"Mese": mesi, "Costi": costi, "Ricavi": ricavi})

# Assegniamo casualmente le categorie di spesa
categorie = ["Infrastrutture", "Consulenze", "Software", "Servizi Operativi", "Manutenzione"]
df["Categoria"] = np.random.choice(categorie, size=12)

# Raggruppamento costi per categoria
df_categorie = df.groupby("Categoria")["Costi"].sum().reset_index()

# Modulo Audit: Identificazione anomalie (calcolando lo Z-score)
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

def salva_grafico_previsione_turnover():
    buf = BytesIO()
    fig, ax = plt.subplots(figsize=(5, 3))
    
    
    # Disegniamo il turnover storico
    ax.plot(df_turnover["Mese"], df_turnover["Turnover"], label="Turnover Storico", marker="o")
    
    # Disegniamo la previsione
    ax.plot(["Gen 2026", "Feb 2026", "Mar 2026"], previsione_turnover, 
            label="Previsione Turnover", marker="x", linestyle="dashed")
    
    # Linea della soglia critica
    ax.axhline(y=soglia_turnover, color='r', linestyle='--', label=f"Soglia {soglia_turnover}%")
    
    ax.legend()
    plt.xticks(rotation=45, ha="right")
    plt.subplots_adjust(bottom=0.2)
    plt.title("Previsione Turnover")

    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return buf


# Funzione per generare il report PDF relativo ai dati finanziari
def genera_pdf():
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Titolo e KPI principali
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 50, "Report Audit - Analisi Costi & KPI")
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

    # Inserimento dei grafici
    y_position -= 200
    for grafico in [salva_grafico_andamento(), salva_grafico_categorie(), salva_grafico_previsione()]:
        img = ImageReader(grafico)
        c.drawImage(img, 100, y_position, width=400, height=200)
        y_position -= 180

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# Streamlit UI - Sezione Dati Finanziari
st.title("📊 Dashboard Monitoraggio Costi & KPI")
col1, col2 = st.columns(2)
col1.metric("📉 Costi Totali", f"€{df['Costi'].sum():,}")
col2.metric("💰 Ricavi Totali", f"€{df['Ricavi'].sum():,}")

# Visualizzazione anomalie
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

# Ruotiamo le etichette dell'asse X
plt.xticks(rotation=45, ha="right")

# Aggiungiamo spaziatura per evitare la sovrapposizione
plt.subplots_adjust(bottom=0.2)

plt.title("Previsione Costi Futuri")
st.pyplot(fig)

st.subheader("📄 Esportazione Report Audit")
pdf_buffer = genera_pdf()
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

# Simulazione dati per il turnover (percentuale di dipendenti che lasciano l'azienda ogni mese)
turnover = np.random.randint(5, 21, size=12)  # valori compresi tra il 5% e il 20%
df_turnover = pd.DataFrame({"Mese": mesi, "Turnover": turnover})

# Definiamo una soglia per il turnover (ad esempio il 15%)
soglia_turnover = 15

# Modello di regressione per la previsione del turnover
X_turn = np.arange(1, 13).reshape(-1, 1)
y_turn = df_turnover["Turnover"].values
modello_turnover = LinearRegression().fit(X_turn, y_turn)
mesi_futuri_turn = np.array([[13], [14], [15]])
previsione_turnover = modello_turnover.predict(mesi_futuri_turn)
df_turnover_pred = pd.DataFrame({
    "Mese": ["Gen 2026", "Feb 2026", "Mar 2026"],
    "Turnover Previsto": previsione_turnover.astype(int)
})

# Visualizzazione grafica del turnover storico
st.subheader("📈 Andamento Turnover Storico")
fig, ax = plt.subplots(figsize=(6, 3))
ax.plot(df_turnover["Mese"], df_turnover["Turnover"], label="Turnover Storico", marker="o")
ax.axhline(y=soglia_turnover, color='r', linestyle='--', label=f"Soglia {soglia_turnover}%")
ax.legend()

plt.title("Turnover Mensile")
st.pyplot(fig)

# Visualizzazione grafica della previsione del turnover
st.subheader("📈 Previsione Turnover Futuro")
fig, ax = plt.subplots(figsize=(6, 3))
ax.plot(df_turnover["Mese"], df_turnover["Turnover"], label="Turnover Storico", marker="o")
ax.plot(["Gen 2026", "Feb 2026", "Mar 2026"], previsione_turnover, label="Previsione Turnover", marker="x", linestyle="dashed")
ax.axhline(y=soglia_turnover, color='r', linestyle='--', label=f"Soglia {soglia_turnover}%")
ax.legend()
# Ruotiamo le etichette dell'asse X per migliorare la leggibilità
plt.xticks(rotation=45, ha="right")

# Aggiungiamo spaziatura per evitare la sovrapposizione
plt.subplots_adjust(bottom=0.2)

plt.title("Previsione Turnover")
st.pyplot(fig)

# Avvisi se il turnover supera la soglia
if (df_turnover["Turnover"] > soglia_turnover).any():
    st.error(f"⚠️ Attenzione: Il turnover ha superato la soglia del {soglia_turnover}% in alcuni mesi!")
if (previsione_turnover > soglia_turnover).any():
    st.error(f"⚠️ Attenzione: La previsione indica che il turnover supererà la soglia del {soglia_turnover}% nei prossimi mesi!")

# Funzione per salvare il grafico del turnover (storico)
def salva_grafico_turnover():
    buf = BytesIO()
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(df_turnover["Mese"], df_turnover["Turnover"], label="Turnover Storico", marker="o")
    ax.axhline(y=soglia_turnover, color='r', linestyle='--', label=f"Soglia {soglia_turnover}%")
    ax.legend()
    plt.title("Andamento Turnover")
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return buf

# Funzione per generare il report PDF relativo al Capitale Umano
def genera_pdf_capitale_umano():
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Titolo e KPI del capitale umano
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 50, "Report Capitale Umano - Turnover Dipendenti")
    c.setFont("Helvetica", 12)
    turnover_medio = df_turnover["Turnover"].mean()
    c.drawString(100, height - 80, f"📊 Turnover Medio: {turnover_medio:.1f}%")
    c.drawString(100, height - 100, f"📈 Turnover Totale (somma): {df_turnover['Turnover'].sum()}%")

    if (df_turnover["Turnover"] > soglia_turnover).any():
        c.drawString(100, height - 120, f"⚠️ Attenzione: Il turnover ha superato la soglia di {soglia_turnover}% in alcuni mesi!")

    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, height - 160, "Previsione Turnover:")
    
    y_position = height - 180
    for _, row in df_turnover_pred.iterrows():
        c.drawString(100, y_position, f"{row['Mese']}: {row['Turnover Previsto']}%")
        y_position -= 20

    # Inseriamo il grafico della previsione del turnover
    buf_img_turnover = salva_grafico_previsione_turnover()
    img_turnover = ImageReader(buf_img_turnover)
    
    y_position -= 200
    c.drawImage(img_turnover, 100, y_position, width=400, height=200)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer


st.subheader("📄 Esportazione Report Capitale Umano")
pdf_buffer_capitale = genera_pdf_capitale_umano()
st.download_button(
    label="📥 Scarica Report Capitale Umano in PDF",
    data=pdf_buffer_capitale,
    file_name="report_capitale_umano.pdf",
    mime="application/pdf",
)

# Simulazione dati per il monitoraggio delle commesse
from sklearn.ensemble import RandomForestRegressor

# Simula un DataFrame per le commesse
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

st.title("📌 Monitoraggio Commesse e Collaudi")
st.dataframe(df_commesse)

# Grafico comparativo Budget vs Costi Attuali
fig, ax = plt.subplots(figsize=(6,3))
ax.bar(df_commesse['Progetto'], df_commesse['Budget'], label='Budget', alpha=0.6)
ax.bar(df_commesse['Progetto'], df_commesse['Costi Attuali'], label='Costi Attuali', alpha=0.6)
ax.set_ylabel("€")
ax.legend()
plt.title("Budget vs Costi Attuali")
st.pyplot(fig)

# Analisi predittiva (es. stima del superamento costi)
# Simulazione: se i costi attuali superano il 90% del budget, il progetto è a rischio.
df_commesse['A Rischio'] = df_commesse['Costi Attuali'] > 0.9 * df_commesse['Budget']
st.subheader("Progetti a Rischio")
st.write(df_commesse[df_commesse['A Rischio']])
