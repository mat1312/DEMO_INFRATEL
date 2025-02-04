# 📊 Dashboard Monitoraggio Costi & KPI

## Descrizione
Questa dashboard interattiva, sviluppata con **Streamlit**, permette di:
- Monitorare **costi e ricavi mensili**.
- Identificare **anomalie nei costi** usando lo **Z-Score**.
- Effettuare una **previsione dei costi futuri** con **Regressione Lineare**.
- Generare un **report PDF** con dati e grafici.

## 🔧 Tecnologie Utilizzate
- **Python** (Librerie: `streamlit`, `pandas`, `numpy`, `matplotlib`, `scipy`, `sklearn`)
- **Machine Learning**: Regressione Lineare (`sklearn.linear_model.LinearRegression`)
- **Report PDF**: `reportlab`

## 🚀 Installazione
1. Clonare la repo:
   ```sh
   git clone https://github.com/tuo-username/DEMO_INFRATEL.git
   cd nome-repo
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
