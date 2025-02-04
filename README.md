# 📊 Dashboard Monitoraggio Costi & KPI

## Descrizione
Questa dashboard interattiva, sviluppata con **Streamlit**, permette di:
- Monitorare **costi e ricavi mensili**.
- Identificare **anomalie nei costi** usando lo **Z-Score**.
- Effettuare una **previsione dei costi futuri** con **Regressione Lineare**.
- Generare un **report PDF** con dati e grafici.
Ecco solo la parte aggiornata della descrizione:

## Analisi del Turnover dei Dipendenti
- Simulazione di dati sul **turnover mensile**.
- **Modello di Machine Learning** (Regressione Lineare) per prevedere il turnover dei prossimi mesi.
- **Segnalazione di soglie critiche**: avvisi quando il turnover supera il 15%.
- **Visualizzazione grafica** dell'andamento storico e delle previsioni future.
- **Esportazione di un report PDF sul Capitale Umano**, includendo il grafico delle previsioni.

## 🔧 Tecnologie Utilizzate
- **Python** (Librerie: `streamlit`, `pandas`, `numpy`, `matplotlib`, `scipy`, `sklearn`)
- **Machine Learning**: Regressione Lineare (`sklearn.linear_model.LinearRegression`)
- **Report PDF**: `reportlab`

## 🚀 Installazione
1. Clonare la repo:
   ```sh
   git clone https://github.com/mat1312/DEMO_INFRATEL.git
   cd DEMO_INFRATEL
   ```
2. Installare le dipendenze:
   ```sh
   pip install -r requirements.txt
   ```
3. Avviare l'applicazione:
   ```sh
   streamlit run app.py
   ```

## 📌 Funzionalità
✅ **Monitoraggio costi e ricavi** con visualizzazioni interattive.<br>
🚨 **Rilevamento anomalie** nei costi tramite Z-Score.<br>
📈 **Previsione costi futuri** basata su regressione lineare.<br>
📄 **Esportazione report PDF** con dati e grafici.<br>
📊 **Monitoraggio Turnover** con visualizzazione grafica.<br>
