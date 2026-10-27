import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Inizializzazione Firebase
CREDENTIALS_PATH = "serviceAccountKey.json"

if not firebase_admin._apps:
    cred = credentials.Certificate(CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def ripristina_database():
    nome_file = input("📂 Inserisci il nome esatto del file JSON di backup da importare (es. backup_dbiscrizioni_20260915.json): ").strip()
    
    if not os.path.exists(nome_file):
        print(f"\n❌ ERRORE: Il file '{nome_file}' non esiste nella cartella.")
        return

    conferma = input(f"⚠️ ATTENZIONE: Questa operazione scriverà i dati del file '{nome_file}' nel database Firebase. Continuare? (s/n): ").strip().lower()
    if conferma != 's':
        print("❌ Operazione annullata.")
        return

    print("\n🔄 Lettura del file di backup...")
    with open(nome_file, "r", encoding="utf-8") as f:
        backup_data = json.load(f)

    print("🚀 Inizio importazione su Firestore...")
    
    totale_documenti = 0
    for nome_collezione, documenti in backup_data.items():
        print(f"📂 Elaborazione collezione: '{nome_collezione}' ({len(documenti)} documenti)...")
        
        for doc_id, dati_doc in documenti.items():
            # Utilizza set() per mantenere lo stesso ID del documento originale
            db.collection(nome_collezione).document(doc_id).set(dati_doc)
            totale_documenti += 1

    print("\n--------------------------------------------------")
    print(f"✨ Ripristino completato con successo!")
    print(f"✔ Totale documenti scritti nel database: {totale_documenti}")
    print("--------------------------------------------------")

if __name__ == "__main__":
    ripristina_database()