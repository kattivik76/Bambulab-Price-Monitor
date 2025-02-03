"""
Monitoraggio del Prezzo del Prodotto BambuLab

Descrizione:
Questo programma permette di monitorare il prezzo di un prodotto sul sito BambuLab, come il BambuLab X1 Carbon. 
Ogni intervallo di tempo configurato, il programma esegue il controllo del prezzo e invia notifiche in caso di cambiamento.
Le notifiche possono essere inviate localmente tramite il sistema operativo (Windows, Linux, macOS) o su Telegram, utilizzando un bot Telegram configurato.

Funzionalità:
- Monitoraggio continuo del prezzo del prodotto tramite il suo URL.
- Invio di notifiche via sistema operativo (Windows, Linux, macOS) e Telegram.
- Log del prezzo in un file di log per tenere traccia delle modifiche nel tempo.
- Barra di progresso che indica l'avanzamento dell'intervallo fino al prossimo controllo del prezzo (0% - 100%).
- Intervallo di monitoraggio personalizzabile in minuti (default: 30 minuti).
- Modalità debug per visualizzare dettagli aggiuntivi sulle operazioni del programma.

Autore:
Alessandro Migliorini

Copyright:
Copyright (c) 2025 Alessandro Migliorini. Tutti i diritti riservati.

Licenza:
Questo programma è distribuito sotto la Licenza Pubblica Generica GNU (GPL v3). 
Puoi redistribuirlo e modificarlo sotto i termini della licenza GPL v3. 
Per maggiori dettagli, visita il link ufficiale:
https://www.gnu.org/licenses/gpl-3.0.html
"""

import time
import asyncio
import httpx
import argparse
import sys
import platform
import subprocess

# Controlla e installa automaticamente le librerie necessarie
REQUIRED_MODULES = ["bs4", "tqdm", "plyer", "httpx"]

# Installa i moduli mancanti
for module in REQUIRED_MODULES:
    try:
        __import__(module)
    except ImportError:
        print(f"[SETUP] Installazione di {module} in corso...")
        subprocess.run([sys.executable, "-m", "pip", "install", module], check=True)

# Importa i moduli necessari
from bs4 import BeautifulSoup
from tqdm import tqdm
from plyer import notification

# Configura Telegram (sostituire con i tuoi valori reali)
TELEGRAM_BOT_TOKEN = "il_tuo_token_telegram"
TELEGRAM_CHAT_ID = "il_tuo_chat_id"

# Parsing degli argomenti da riga di comando
parser = argparse.ArgumentParser(description="Monitoraggio del prezzo BambuLab.")
parser.add_argument("--debug", action="store_true", help="Attiva il debug mode per visualizzare informazioni dettagliate")
args = parser.parse_args()
DEBUG_MODE = args.debug

# Funzione di debug per stampare informazioni aggiuntive
def debug_print(message):
    """Stampa un messaggio di debug solo se DEBUG_MODE è attivo."""
    if DEBUG_MODE:
        print(message)

# Funzione per ottenere il sistema operativo in uso
def get_os():
    """Ritorna il sistema operativo attuale."""
    return platform.system()

# Funzione per recuperare il prezzo del prodotto dalla pagina web
async def get_price(url, client):
    """Recupera il prezzo del prodotto dalla pagina web."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://eu.store.bambulab.com/it-it/products/x1-carbon",
        }
        # Esegue la richiesta HTTP per ottenere la pagina
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            price_container = soup.find("div", class_="ProductMeta__PriceList Heading")
            if price_container:
                price_element = price_container.find("span", class_="ProductMeta__Price Price Price--highlight Text--subdued u-h4")
                if price_element:
                    price_text = price_element.text.strip()
                    price_text = price_text.replace("€", "").replace(" EUR", "").strip()
                    if ',' not in price_text:
                        price_text += ".00"
                    return price_text
        else:
            debug_print(f"Errore nella risposta del server: {response.status_code}")
    except Exception as e:
        debug_print(f"Si è verificato un errore: {e}")
    return None

# Funzione per registrare le modifiche del prezzo nel file di log
async def log_price_change(price, price_changed=False):
    """Salva il nuovo prezzo nel file di log."""
    try:
        with open("price_log.txt", "a") as file:
            if price_changed:
                file.write(f"Nuovo prezzo: {price}€ - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            else:
                file.write(f"Controllo eseguito senza variazioni, prezzo attuale: {price}€ - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        debug_print(f"[LOG] Prezzo aggiornato: {price}€" if price_changed else f"[LOG] Controllo eseguito senza variazioni, prezzo attuale: {price}€")
    except Exception as e:
        debug_print(f"Errore durante la scrittura nel log: {e}")

# Funzione per inviare una notifica locale
async def send_notification(price):
    """Invia una notifica locale in base al sistema operativo."""
    os_name = get_os()
    message = f"Il nuovo prezzo è: {price}€"
    
    try:
        if os_name == "Windows":
            notification.notify(title="Bambulab Price Monitor", message=message, timeout=10, app_icon="bambulab_icon.ico")
        elif os_name == "Linux":
            subprocess.run(["notify-send", "Bambulab Price Monitor", message])
        elif os_name == "Darwin":  # macOS
            subprocess.run(["osascript", "-e", f'display notification "{message}" with title "Bambulab Price Monitor"'])
        else:
            debug_print("Notifiche non supportate su questo sistema.")
    except Exception as e:
        debug_print(f"Errore nella notifica locale: {e}")

# Funzione per inviare una notifica su Telegram
async def send_telegram_notification(price):
    """Invia una notifica su Telegram."""
    try:
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": f"📢 *Bambulab Price Monitor*\n\nIl nuovo prezzo è: *{price}€*",
            "parse_mode": "Markdown"
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(telegram_url, data=data)
            if response.status_code == 200:
                debug_print("Notifica Telegram inviata con successo!")
            else:
                debug_print(f"Errore nell'invio della notifica Telegram: {response.text}")
    except Exception as e:
        debug_print(f"Errore nella notifica Telegram: {e}")

# Funzione principale che monitora il prezzo a intervalli regolari
async def monitor_price(url, interval=1800):
    """Monitora il prezzo del prodotto a intervalli regolari."""
    last_price = None
    interval_minutes = interval // 60  # Converti l'intervallo in minuti
    async with httpx.AsyncClient() as client:
        while True:
            debug_print("[DEBUG] Inizio controllo prezzo...")
            price = await get_price(url, client)
            if price:
                debug_print(f"[DEBUG] Prezzo recuperato: {price}")
                if last_price is None or price != last_price:
                    # Se il prezzo è cambiato, aggiorna il log e invia le notifiche
                    await log_price_change(price, price_changed=True)
                    await send_notification(price)
                    await send_telegram_notification(price)
                    last_price = price
                else:
                    await log_price_change(price, price_changed=False)
            else:
                debug_print("Errore nel recupero del prezzo.")
            
            if DEBUG_MODE:
                debug_print("[DEBUG] Avvio barra di progresso...")
                # Barra di progresso sincronizzata con l'intervallo
                for i in tqdm(range(100), desc=f"Tempo rimanente: ({interval_minutes} min)", ncols=80, colour="green", bar_format="{l_bar}{bar}| {remaining}"):
                    # Calcola il tempo rimanente per ogni step della barra
                    remaining_time = interval - (i * interval / 100)
                    remaining_minutes = int(remaining_time // 60)
                    remaining_seconds = int(remaining_time % 60)
                    tqdm.write(f"{remaining_minutes:02}:{remaining_seconds:02} rimanenti", end="\r")
                    await asyncio.sleep(interval / 100)  # Aggiorna la barra ogni 1% dell'intervallo
            else:
                await asyncio.sleep(interval)  # Pausa prima del prossimo controllo

# Funzione di avvio del programma
if __name__ == "__main__":
    product_url = "https://eu.store.bambulab.com/it-it/products/x1-carbon?variant=53735784939868"
    asyncio.run(monitor_price(product_url, interval=1800))  # Intervallo di 30 minuti (1800 secondi)
