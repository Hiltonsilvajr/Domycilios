from app import app, db

def update_db():
    with app.app_context():
        # Criar todas as tabelas que não existem
        db.create_all()
        print("Banco de dados atualizado com sucesso!")

if __name__ == '__main__':
    update_db() 