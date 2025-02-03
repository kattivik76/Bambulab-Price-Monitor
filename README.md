# Bambulab Price Monitor

## Descrizione

**Bambulab Price Monitor** è uno script Python progettato per monitorare i cambiamenti di prezzo di un prodotto sul sito ufficiale BambuLab, come il BambuLab X1 Carbon. Questo programma esegue periodicamente il controllo del prezzo del prodotto e invia notifiche tramite Telegram e il sistema operativo (Windows, Linux, macOS). Include anche un sistema di log per registrare le modifiche nel tempo e una barra di progresso per visualizzare il tempo rimanente prima del prossimo controllo.

## Funzionalità

- **Monitoraggio Prezzo**: Monitora il prezzo di un prodotto su un sito web.
- **Notifiche**: Invia notifiche via Telegram e sul sistema operativo (Windows, Linux, macOS) quando il prezzo cambia.
- **Log**: Registra le modifiche del prezzo in un file di log per tenere traccia della cronologia delle variazioni.
- **Barra di Progresso**: Visualizza una barra di progresso che indica il tempo rimanente prima del prossimo controllo del prezzo.
- **Modalità Debug**: Visualizza dettagli aggiuntivi sulle operazioni del programma (attivabile tramite riga di comando).
- **Controllo Automatico delle Dipendenze**: Installa automaticamente le librerie necessarie (BeautifulSoup, tqdm, plyer, httpx).

## Installazione

### Requisiti

- Python 3.7+ deve essere installato sul tuo sistema.
- Una connessione Internet per scaricare le librerie e accedere al sito web di BambuLab.
- Un bot Telegram configurato per inviare notifiche.

### Passaggi di installazione

1. **Clona il repository**:

   Clona questo repository sul tuo computer con il comando:

   ```bash
   git clone https://github.com/tuo-username/Bambulab-Price-Monitor.git
   cd Bambulab-Price-Monitor

2. **Installa le dipendenze**:

   Le librerie necessarie per il corretto funzionamento del programma sono elencate nel file requirements.txt. Puoi installarle usando il seguente comando:

  ```bash
  pip install -r requirements.txt
  ```

   Questo comando installerà le seguenti librerie:
  - beautifulsoup4: Per fare il parsing e l'estrazione dei dati dalla pagina web.
  - httpx: Per fare richieste HTTP asincrone al sito di BambuLab.
  - plyer: Per inviare notifiche sui sistemi operativi.
  - tqdm: Per visualizzare una barra di progresso.

3. **Configura Telegram**:

  Per inviare notifiche su Telegram, è necessario creare un bot su Telegram tramite il servizio BotFather e ottenere il token del bot. Inoltre, dovrai ottenere l'ID della chat (che può essere un gruppo o un canale).
  Una volta ottenuti questi dati, dovrai sostituire le seguenti variabili nel codice di monitor.py con il token e l'ID della chat:
  
  ```python
  TELEGRAM_BOT_TOKEN = "il_tuo_token_telegram"
  TELEGRAM_CHAT_ID = "il_tuo_chat_id"
  ```

## Uso
### Avviare il monitoraggio
Per avviare il monitoraggio del prezzo, esegui il programma con il comando:

  ```python
  python monitor.py --debug
  ```

- L'opzione --debug è facoltativa e attiva la modalità di debug. In questa modalità, il programma mostrerà informazioni dettagliate durante l'esecuzione, come le risposte del server e altre informazioni utili per il debug.

### Personalizzare l'intervallo di monitoraggio
L'intervallo di tempo tra un controllo e l'altro può essere personalizzato modificando il parametro interval nel codice.
Ad esempio, per impostare un intervallo di 30 minuti (1800 secondi), modifica la riga del codice come segue:
  
  ```python
  asyncio.run(monitor_price(product_url, interval=1800))  # Intervallo di 30 minuti (1800 secondi)
  ```

### Visualizzare la barra di progresso
Se la modalità debug è attivata, verrà mostrata una barra di progresso che indica quanto tempo manca al prossimo controllo del prezzo. La barra di progresso si aggiorna ogni 1% dell'intervallo di tempo impostato.

### Struttura del Progetto
La struttura del progetto è la seguente:

  ```bash
    Bambulab-Price-Monitor/
    │
    ├── monitor.py             # Script principale per il monitoraggio del prezzo
    ├── requirements.txt       # Elenco delle librerie necessarie
    ├── price_log.txt          # File di log per registrare le modifiche del prezzo
    ├── bambulab_icon.ico      # Icona per le notifiche (Windows)
    └── README.md              # Questo file
  ```

- **monitor.py**: Contiene il codice principale per monitorare il prezzo del prodotto e inviare notifiche.
- **requirements.txt**: Contiene le librerie necessarie per il funzionamento del programma.
- **price_log.txt**: Un file di log che memorizza tutte le modifiche del prezzo.
- **bambulab_icon.ico**: Un'icona per le notifiche su Windows (opzionale).
- **README.md**: Questo file, che descrive il progetto e come utilizzarlo.

### Licenza
Questo programma è distribuito sotto la **Licenza Pubblica Generica GNU (GPL v3)**. Puoi redistribuirlo e modificarlo liberamente, seguendo i termini della licenza GPL v3. Per maggiori dettagli, visita il link ufficiale della licenza GPL v3.

Autore: Alessandro Migliorini
