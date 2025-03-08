from app import app
import webbrowser
import threading
import time

def open_browser():
    # Aguardar 2 segundos para o servidor iniciar
    time.sleep(2)
    # Abrir o navegador automaticamente
    webbrowser.open('http://127.0.0.1:8080')
    print("Navegador aberto. Se não abrir automaticamente, acesse: http://127.0.0.1:8080")

if __name__ == '__main__':
    # Iniciar thread para abrir o navegador
    threading.Thread(target=open_browser).start()
    
    # Iniciar o servidor em uma porta diferente (8080)
    print("Iniciando servidor na porta 8080...")
    app.run(debug=True, host='0.0.0.0', port=8080, threaded=True) 