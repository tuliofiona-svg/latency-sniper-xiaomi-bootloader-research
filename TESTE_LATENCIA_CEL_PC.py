import subprocess
import time
import ctypes
import os

def set_high_priority():
    if os.name == 'nt':
        process = ctypes.windll.kernel32.GetCurrentProcess()
        ctypes.windll.kernel32.SetPriorityClass(process, 0x00008000)

def test_real_transit():
    set_high_priority()
    device_id = "Q87LKNZ9NRQ4V4VS"
    
    print(f"--- TESTE DE LATÊNCIA REAL (PC -> CABO -> XIAOMI) ---")
    input("\nPronto? Aperte [ENTER] para disparar o comando e medir...")

    # MARCO ZERO: O momento em que o processador do PC recebe a ordem
    start_time = time.perf_counter()

    # O COMANDO: Enviamos um 'echo' para o shell do Android.
    # O tempo termina quando o Android processa e devolve o texto para o PC.
    process = subprocess.run(
        f"adb -s {device_id} shell echo 1", 
        capture_output=True, 
        shell=True
    )

    # MARCO FINAL: O pacote voltou do celular
    end_time = time.perf_counter()

    total_time_ms = (end_time - start_time) * 1000

    print(f"\n[RESULTADO]")
    print(f"Tempo total de trânsito: {total_time_ms:.2f} ms")
    print(f"Estimativa de 'Dedo na Tela' (Unidirecional): {total_time_ms / 2:.2f} ms")
    print("-" * 45)
    print("Nota: O 'Dedo na Tela' é aproximadamente metade do tempo total,")
    print("pois o comando só precisa IR, não precisa voltar para ser executado.")

if __name__ == "__main__":
    # Garante que o ADB está acordado antes do teste
    subprocess.run("adb devices", capture_output=True)
    test_real_transit()