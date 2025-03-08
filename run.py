from app import app
import os

if __name__ == '__main__':
    # Verificar se estamos em ambiente de produção ou desenvolvimento
    if os.environ.get('FLASK_ENV') == 'production':
        # Configurações para produção
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
    else:
        # Configurações para desenvolvimento
        app.run(debug=True, host='0.0.0.0', port=5000) 