from app import app, db, Usuario, Servico, criar_admin
from werkzeug.security import generate_password_hash

def init_db():
    with app.app_context():
        # Criar tabelas
        db.create_all()
        
        # Criar usuário administrador
        admin = Usuario.query.filter_by(tipo='admin').first()
        if not admin:
            admin = Usuario(
                nome='Marcela',
                email='marcela_2@hotmail.com',
                tipo='admin'
            )
            admin.set_senha('admin123')
            db.session.add(admin)
            db.session.commit()
        
        # Verificar se já existem serviços
        servicos_existentes = Servico.query.count()
        if servicos_existentes == 0:
            # Criar usuário cliente de exemplo
            cliente = Usuario.query.filter_by(email='cliente@exemplo.com').first()
            if not cliente:
                cliente = Usuario(
                    nome='Cliente Exemplo',
                    email='cliente@exemplo.com',
                    senha_hash=generate_password_hash('cliente123'),
                    tipo='cliente',
                    telefone='(11) 88888-8888'
                )
                db.session.add(cliente)
            
            # Criar serviços iniciais
            servicos = [
                Servico(nome='Aplicação Clássica', descricao='Aplicação de cílios fio a fio', duracao=90, preco=150.00),
                Servico(nome='Aplicação Volume Russo', descricao='Aplicação de cílios com técnica volume russo', duracao=120, preco=200.00),
                Servico(nome='Manutenção Clássica', descricao='Manutenção de cílios fio a fio', duracao=60, preco=100.00),
                Servico(nome='Manutenção Volume Russo', descricao='Manutenção de cílios volume russo', duracao=90, preco=150.00),
                Servico(nome='Remoção de Cílios', descricao='Remoção completa de cílios', duracao=30, preco=50.00)
            ]
            
            for servico in servicos:
                db.session.add(servico)
            
            db.session.commit()
            print("Banco de dados inicializado com sucesso!")
        else:
            print("O banco de dados já foi inicializado anteriormente.")

if __name__ == '__main__':
    init_db() 