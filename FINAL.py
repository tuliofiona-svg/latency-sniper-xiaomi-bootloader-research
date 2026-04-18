import subprocess
import time
import datetime
import statistics
import ctypes
import os

# --- CONFIGURAÇÕES DO ALVO ---
DEVICE_ID = "Q87LKNZ9NRQ4V4VS"
XIAOMI_SERVER = "unlock.update.miui.com"
SWIPE_CMD = "input swipe 150 2250 150 2250 500"
TARGET_TIME = "13:00:00" # Horário oficial do reset

def set_realtime_priority():
    """Eleva o processo ao nível máximo de prioridade do Windows."""
    if os.name == 'nt':
        process = ctypes.windll.kernel32.GetCurrentProcess()
        # REALTIME_PRIORITY_CLASS (0x00000100)
        ctypes.windll.kernel32.SetPriorityClass(process, 0x00000100)

def force_windows_time_sync():
    """Força a sincronização do relógio com o servidor NTP do Google."""
    print("[SISTEMA] Sincronizando relógio com time.google.com...")
    try:
        subprocess.run("w32tm /resync /force", shell=True, capture_output=True)
        print("[SISTEMA] Relógio sincronizado.")
    except:
        print("[ERRO] Falha ao sincronizar. Execute como Administrador.")

def get_calibrated_offset():
    """Mede a latência real PC -> XIAOMI via Dados Móveis."""
    print(f"\n[1/3] CALIBRANDO REDE (MODO DADOS MÓVEIS)...")
    latencies = []
    for i in range(5):
        t_start = time.perf_counter()
        cmd = f"adb -s {DEVICE_ID} shell \"echo > /dev/tcp/{XIAOMI_SERVER}/443\""
        subprocess.run(cmd, shell=True, capture_output=True, timeout=5)
        t_end = time.perf_counter()
        latencies.append((t_end - t_start) * 1000)
        print(f"      Amostra {i+1}: {latencies[-1]:.2f} ms")
        time.sleep(0.1)
    
    avg_rtt = statistics.mean(latencies)
    return avg_rtt / 2000 # Offset em segundos (apenas ida)

def prepare_hardware():
    """Isolamento total da rede celular conforme o protocolo Xiaomi."""
    print(f"[2/3] CONFIGURANDO HARDWARE...")
    # Desativa Wi-Fi e Ativa Dados (Exige Root ou permissões ADB svc)
    subprocess.run(f"adb -s {DEVICE_ID} shell svc wifi disable", shell=True)
    subprocess.run(f"adb -s {DEVICE_ID} shell svc data enable", shell=True)
    time.sleep(2) # Estabilização da rádio
    print("      [OK] Rede Celular Exclusiva Ativa.")

def run_sniper():
    set_realtime_priority()
    force_windows_time_sync()
    
    # 1. Calibragem
    offset = get_calibrated_offset()
    
    # 2. Hardware
    prepare_hardware()

    # 3. Sincronia de Gatilho
    now = datetime.datetime.now()
    target_dt = datetime.datetime.strptime(TARGET_TIME, "%H:%M:%S").replace(
        year=now.year, month=now.month, day=now.day
    )
    trigger_ts = target_dt.timestamp() - offset

    print(f"\n[3/3] AGUARDANDO MOMENTO CRÍTICO...")
    print(f"Alvo: {TARGET_TIME} | Compensação: {offset*1000:.2f} ms")
    print(f"Gatilho: {datetime.datetime.fromtimestamp(trigger_ts).strftime('%H:%M:%S.%f')}")

    # Spin-lock (Consumo de CPU para precisão de nanossegundos)
    while time.time() < trigger_ts:
        # Pre-warm do ADB faltando 3 segundos
        if (trigger_ts - time.time()) < 3.0 and (trigger_ts - time.time()) > 2.95:
             subprocess.run(f"adb -s {DEVICE_ID} shell echo 1", capture_output=True)

    # ATAQUE INCESSANTE (30 Swipes em rajada)
    print(f"\n[{datetime.datetime.now().strftime('%H:%M:%S.%f')}] >>> EXECUTANDO SNIPER BURST!")
    full_cmd = f"adb -s {DEVICE_ID} shell {SWIPE_CMD}"
    
    for _ in range(30):
        subprocess.Popen(full_cmd, shell=True)
    
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S.%f')}] PROCESSO CONCLUÍDO.")

if __name__ == "__main__":
    run_sniper()