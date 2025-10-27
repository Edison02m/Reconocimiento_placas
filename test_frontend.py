"""
Script simple para enviar una placa al backend
Uso: python test_frontend.py <PLACA>
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.supabase_client import enviar_deteccion_a_supabase

def main():

    placa = sys.argv[1].upper().strip()
    

    print(f"\nEnviando placa '{placa}'...")
    
    if enviar_deteccion_a_supabase(placa):
        print(f"Placa '{placa}' enviada correctamente")
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print(f"Error al enviar placa '{placa}'")

if __name__ == "__main__":
    main()
