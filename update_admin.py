from app import app, db, Usuario
from werkzeug.security import generate_password_hash

def update_admin():
    with app.app_context():
        # Buscar o administrador existente
        admin = Usuario.query.filter_by(tipo='admin').first()
        
        if admin:
            # Atualizar informações
            admin.nome = 'Marcela'
            admin.email = 'marcela_2@hotmail.com'
            admin.set_senha('admin123')  # Redefinir a senha para garantir
            db.session.commit()
            print("Administrador atualizado com sucesso!")
        else:
            # Criar um novo administrador se não existir
            novo_admin = Usuario(
                nome='Marcela',
                email='marcela_2@hotmail.com',
                tipo='admin'
            )
            novo_admin.set_senha('admin123')
            db.session.add(novo_admin)
            db.session.commit()
            print("Novo administrador criado com sucesso!")

if __name__ == '__main__':
    update_admin() 