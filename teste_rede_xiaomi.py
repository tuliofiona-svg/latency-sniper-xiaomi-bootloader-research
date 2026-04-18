import socket
import time
import statistics

def test_xiaomi_network_latency():
    host = "unlock.update.miui.com"
    port = 443
    samples = 15
    latencies = []

    print(f"--- DIAGNÓSTICO DE REDE: PC -> SERVIDOR XIAOMI ---")
    print(f"Alvo: {host} (Porta {port})")
    print(f"Amostras: {samples}\n")

    for i in range(samples):
        try:
            # Criamos um socket para medir o tempo de conexão real
            start_time = time.perf_counter()
            
            # Tenta estabelecer a conexão TCP
            sock = socket.create_connection((host, port), timeout=5)
            
            end_time = time.perf_counter()
            
            latency_ms = (end_time - start_time) * 1000
            latencies.append(latency_ms)
            
            print(f"Amostra {i+1:02d}: {latency_ms:.2f} ms")
            
            sock.close()
            # Pequeno intervalo para não ser bloqueado por flood
            time.sleep(0.3)
            
        except Exception as e:
            print(f"Erro na amostra {i+1}: {e}")

    if latencies:
        avg_lat = statistics.mean(latencies)
        min_lat = min(latencies)
        jitter = max(latencies) - min_lat
        
        print("\n" + "="*30)
        print(f"Média de Rede:  {avg_lat:.2f} ms")
        print(f"Mínima (Best):  {min_lat:.2f} ms")
        print(f"Jitter Rede:    {jitter:.2f} ms")
        print("="*30)
        
        print("\n[CÁLCULO PARA O SNIPER]")
        print(f"Seu comando leva 40ms no cabo + {avg_lat:.2f}ms na rede.")
        print(f"Atraso total estimado: {40 + avg_lat:.2f} ms")
    else:
        print("Não foi possível conectar ao servidor. Verifique sua internet.")

if __name__ == "__main__":
    test_xiaomi_network_latency()