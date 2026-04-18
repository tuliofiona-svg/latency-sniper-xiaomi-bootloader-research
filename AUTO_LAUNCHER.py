import time
import datetime
import subprocess
import sys

# --- CONFIGURAÇÃO ---
# Horário que o script FINAL.py deve começar a rodar (Calibragem + Hardware)
LAUNCH_TIME = "12:59:00" 

def start_launcher():
    print(f"--- AUTO-LAUNCHER ATIVADO (TÚLIO) ---")
    print(f"Aguardando o relógio bater {LAUNCH_TIME} para iniciar o Sniper...")

    target_time = LAUNCH_TIME.split(':')
    h, m, s = int(target_time[0]), int(target_time[1]), int(target_time[2])

    while True:
        now = datetime.datetime.now()
        
        # Verifica se chegamos no segundo exato
        if now.hour == h and now.minute == m and now.second == s:
            print(f"\n[{now.strftime('%H:%M:%S.%f')}] >>> EXECUTANDO FINAL.PY!")
            # Chama o seu script principal
            subprocess.Popen([sys.executable, "FINAL.py"])
            break
        
        # Mostra contagem regressiva simples
        remaining = (datetime.datetime.combine(now.date(), datetime.time(h, m, s)) - now).total_seconds()
        if remaining > 0:
            print(f"Faltam {remaining:.1f}s para o Launcher disparar...", end='\r')
        
        time.sleep(0.1) # Loop leve para não consumir CPU antes da hora

    print("\n[OK] Sniper entregue ao sistema. Boa sorte!")

if __name__ == "__main__":
    start_launcher()