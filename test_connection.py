import requests
import time
import sys

def test_connection():
    print("Testando conexão com o servidor...")
    try:
        response = requests.get("http://127.0.0.1:5000", timeout=5)
        if response.status_code == 200:
            print("Conexão bem-sucedida! O servidor está respondendo.")
            print(f"Status code: {response.status_code}")
            return True
        else:
            print(f"Servidor respondeu com status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("Erro de conexão: Não foi possível conectar ao servidor.")
        print("Possíveis causas:")
        print("1. O servidor não está rodando")
        print("2. A porta está bloqueada por um firewall")
        print("3. O endereço IP ou porta estão incorretos")
        return False
    except requests.exceptions.Timeout:
        print("Timeout: O servidor demorou muito para responder.")
        return False
    except Exception as e:
        print(f"Erro desconhecido: {str(e)}")
        return False

if __name__ == "__main__":
    test_connection() 