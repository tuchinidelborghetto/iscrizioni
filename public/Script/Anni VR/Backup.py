import os
import json
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

# Inizializzazione Firebase
CREDENTIALS_PATH = "serviceAccountKey.json"

if not firebase_admin._apps:
    cred = credentials.Certificate(CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def esporta_database():
    print("🔄 Connessione a Firebase e lettura di tutte le collezioni...")
    
    backup_data = {}
    
    # Recupera dinamicamente tutte le collezioni presenti nel database
    collezioni = db.collections()
    
    for coll in collezioni:
        nome_collezione = coll.id
        print(f"📥 Esportazione collezione: '{nome_collezione}'...")
        backup_data[nome_collezione] = {}
        
        docs = coll.stream()
        for doc in docs:
            backup_data[nome_collezione][doc.id] = doc.to_dict()

    # Genera un nome file con la data e l'ora corrente
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_output = f"backup_dbiscrizioni_{timestamp}.json"
    
    with open(file_output, "w", encoding="utf-8") as f:
        json.dump(backup_data, f, ensure_ascii=False, indent=4)
        
    print("\n--------------------------------------------------")
    print(f"✨ Backup completato con successo!")
    print(f"📁 File salvato come: {file_output}")
    print("--------------------------------------------------")

if __name__ == "__main__":
    esporta_database()