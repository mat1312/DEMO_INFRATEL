# helper.py
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

def salva_grafico_andamento(df):
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

def salva_grafico_categorie(df_categorie):
    buf = BytesIO()
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.pie(df_categorie["Costi"], labels=df_categorie["Categoria"], autopct='%1.1f%%', startangle=140)
    plt.title("Ripartizione Costi per Categoria")
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return buf

def salva_grafico_previsione(df, previsione):
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

def salva_grafico_previsione_turnover(df_turnover, previsione_turnover, soglia_turnover):
    buf = BytesIO()
    fig, ax = plt.subplots(figsize=(5, 3))
    # Turnover storico
    ax.plot(df_turnover["Mese"], df_turnover["Turnover"], label="Turnover Storico", marker="o")
    # Previsione turnover
    ax.plot(["Gen 2026", "Feb 2026", "Mar 2026"], previsione_turnover, label="Previsione Turnover", marker="x", linestyle="dashed")
    # Soglia critica
    ax.axhline(y=soglia_turnover, color='r', linestyle='--', label=f"Soglia {soglia_turnover}%")
    ax.legend()
    plt.xticks(rotation=45, ha="right")
    plt.subplots_adjust(bottom=0.2)
    plt.title("Previsione Turnover")
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return buf

def genera_pdf(df, df_categorie, anomalie, previsione):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Titolo e KPI
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

    # Inserimento grafici
    y_position -= 200
    grafici = [
        salva_grafico_andamento(df),
        salva_grafico_categorie(df_categorie),
        salva_grafico_previsione(df, previsione)
    ]
    for grafico in grafici:
        img = ImageReader(grafico)
        c.drawImage(img, 100, y_position, width=400, height=200)
        y_position -= 180

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

def salva_grafico_turnover(df_turnover, soglia_turnover):
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

def genera_pdf_capitale_umano(df_turnover, df_turnover_pred, soglia_turnover, previsione_turnover):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

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

    buf_img_turnover = salva_grafico_previsione_turnover(df_turnover, previsione_turnover, soglia_turnover)
    img_turnover = ImageReader(buf_img_turnover)
    y_position -= 200
    c.drawImage(img_turnover, 100, y_position, width=400, height=200)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

def salva_grafico_commesse(df_commesse):
    buf = BytesIO()
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.bar(df_commesse['Progetto'], df_commesse['Budget'], label='Budget', alpha=0.6)
    ax.bar(df_commesse['Progetto'], df_commesse['Costi Attuali'], label='Costi Attuali', alpha=0.6)
    ax.set_ylabel("€")
    ax.legend()
    plt.title("Budget vs Costi Attuali")
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return buf
