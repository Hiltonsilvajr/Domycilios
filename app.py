from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
import uuid
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar o aplicativo
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'chave-secreta-padrao')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', os.environ.get('DATABASE_URI', 'sqlite:///cilios.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'img', 'portfolio')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Verificar se a pasta de upload existe, se não, criar
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Função para verificar extensões de arquivo permitidas
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Inicializar o banco de dados
db = SQLAlchemy(app)

# Configurar o gerenciador de login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Definir modelos
class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha_hash = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(20), default='cliente')  # cliente ou admin
    telefone = db.Column(db.String(20))
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    agendamentos = db.relationship('Agendamento', backref='cliente', lazy=True)

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)
    
    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

class Servico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    duracao = db.Column(db.Integer, nullable=False)  # duração em minutos
    preco = db.Column(db.Float, nullable=False)
    agendamentos = db.relationship('Agendamento', backref='servico', lazy=True)
    imagens = db.relationship('Imagem', backref='servico', lazy=True)

class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    servico_id = db.Column(db.Integer, db.ForeignKey('servico.id'), nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='agendado')  # agendado, concluído, cancelado
    observacoes = db.Column(db.Text)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

class Imagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_arquivo = db.Column(db.String(255), nullable=False)
    caminho = db.Column(db.String(255), nullable=False)
    titulo = db.Column(db.String(100))
    descricao = db.Column(db.Text)
    servico_id = db.Column(db.Integer, db.ForeignKey('servico.id'))
    data_upload = db.Column(db.DateTime, default=datetime.utcnow)
    destaque = db.Column(db.Boolean, default=False)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Adicionar variáveis globais para os templates
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# Rotas
@app.route('/')
def index():
    # Buscar imagens em destaque para exibir na página inicial
    imagens_destaque = Imagem.query.filter_by(destaque=True).limit(6).all()
    return render_template('index.html', imagens_destaque=imagens_destaque)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and usuario.verificar_senha(senha):
            login_user(usuario)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        
        flash('Email ou senha inválidos.', 'danger')
    
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        telefone = request.form.get('telefone')
        
        # Verificar se o email já existe
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            flash('Este email já está cadastrado.', 'danger')
            return render_template('cadastro.html')
        
        novo_usuario = Usuario(nome=nome, email=email, telefone=telefone)
        novo_usuario.set_senha(senha)
        
        db.session.add(novo_usuario)
        db.session.commit()
        
        flash('Cadastro realizado com sucesso! Faça login para continuar.', 'success')
        return redirect(url_for('login'))
    
    return render_template('cadastro.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Para clientes, mostrar seus agendamentos
    if current_user.tipo == 'cliente':
        agendamentos = Agendamento.query.filter_by(cliente_id=current_user.id).order_by(Agendamento.data_hora).all()
        return render_template('dashboard_cliente.html', agendamentos=agendamentos)
    
    # Para administradores, mostrar todos os agendamentos
    agendamentos = Agendamento.query.order_by(Agendamento.data_hora).all()
    return render_template('dashboard_admin.html', agendamentos=agendamentos)

@app.route('/agendar', methods=['GET', 'POST'])
@login_required
def agendar():
    if request.method == 'POST':
        servico_id = request.form.get('servico')
        data = request.form.get('data')
        hora = request.form.get('hora')
        observacoes = request.form.get('observacoes')
        
        # Converter data e hora para datetime
        data_hora_str = f"{data} {hora}"
        data_hora = datetime.strptime(data_hora_str, '%Y-%m-%d %H:%M')
        
        # Verificar se o horário está disponível
        agendamento_existente = Agendamento.query.filter_by(data_hora=data_hora, status='agendado').first()
        if agendamento_existente:
            flash('Este horário já está agendado. Por favor, escolha outro.', 'danger')
            servicos = Servico.query.all()
            return render_template('agendar.html', servicos=servicos)
        
        novo_agendamento = Agendamento(
            cliente_id=current_user.id,
            servico_id=servico_id,
            data_hora=data_hora,
            observacoes=observacoes
        )
        
        db.session.add(novo_agendamento)
        db.session.commit()
        
        flash('Agendamento realizado com sucesso!', 'success')
        return redirect(url_for('dashboard'))
    
    servicos = Servico.query.all()
    return render_template('agendar.html', servicos=servicos)

@app.route('/agendamento/<int:id>/cancelar', methods=['POST'])
@login_required
def cancelar_agendamento(id):
    agendamento = Agendamento.query.get_or_404(id)
    
    # Verificar se o usuário é o dono do agendamento ou um administrador
    if agendamento.cliente_id != current_user.id and current_user.tipo != 'admin':
        flash('Você não tem permissão para cancelar este agendamento.', 'danger')
        return redirect(url_for('dashboard'))
    
    agendamento.status = 'cancelado'
    db.session.commit()
    
    flash('Agendamento cancelado com sucesso!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/agendamento/<int:id>/concluir', methods=['POST'])
@login_required
def concluir_agendamento(id):
    if current_user.tipo != 'admin':
        flash('Apenas administradores podem marcar agendamentos como concluídos.', 'danger')
        return redirect(url_for('dashboard'))
    
    agendamento = Agendamento.query.get_or_404(id)
    agendamento.status = 'concluido'
    db.session.commit()
    
    flash('Agendamento marcado como concluído!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/admin/servicos', methods=['GET', 'POST'])
@login_required
def admin_servicos():
    if current_user.tipo != 'admin':
        flash('Acesso negado.', 'danger')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        acao = request.form.get('acao')
        
        if acao == 'novo':
            nome = request.form.get('nome')
            descricao = request.form.get('descricao')
            duracao = request.form.get('duracao')
            preco = request.form.get('preco')
            
            novo_servico = Servico(
                nome=nome,
                descricao=descricao,
                duracao=duracao,
                preco=preco
            )
            
            db.session.add(novo_servico)
            db.session.commit()
            
            flash('Serviço adicionado com sucesso!', 'success')
        
        elif acao == 'editar':
            servico_id = request.form.get('id')
            servico = Servico.query.get_or_404(servico_id)
            
            servico.nome = request.form.get('nome')
            servico.descricao = request.form.get('descricao')
            servico.duracao = request.form.get('duracao')
            servico.preco = request.form.get('preco')
            
            db.session.commit()
            
            flash('Serviço atualizado com sucesso!', 'success')
        
        elif acao == 'excluir':
            servico_id = request.form.get('id')
            servico = Servico.query.get_or_404(servico_id)
            
            # Verificar se há agendamentos para este serviço
            if servico.agendamentos:
                flash('Não é possível excluir este serviço pois existem agendamentos associados a ele.', 'danger')
            else:
                db.session.delete(servico)
                db.session.commit()
                flash('Serviço excluído com sucesso!', 'success')
        
        return redirect(url_for('admin_servicos'))
    
    servicos = Servico.query.all()
    return render_template('admin_servicos.html', servicos=servicos)

@app.route('/admin/clientes')
@login_required
def admin_clientes():
    if current_user.tipo != 'admin':
        flash('Acesso negado.', 'danger')
        return redirect(url_for('dashboard'))
    
    clientes = Usuario.query.filter_by(tipo='cliente').all()
    return render_template('admin_clientes.html', clientes=clientes)

@app.route('/api/horarios_disponiveis', methods=['GET'])
def horarios_disponiveis():
    data = request.args.get('data')
    
    if not data:
        return jsonify({'error': 'Data não fornecida'}), 400
    
    # Converter a data para datetime
    data_inicio = datetime.strptime(data, '%Y-%m-%d')
    data_fim = data_inicio + timedelta(days=1)
    
    # Buscar agendamentos para esta data
    agendamentos = Agendamento.query.filter(
        Agendamento.data_hora >= data_inicio,
        Agendamento.data_hora < data_fim,
        Agendamento.status == 'agendado'
    ).all()
    
    # Horários de funcionamento (9h às 18h, de hora em hora)
    horarios_possiveis = [f"{h:02d}:00" for h in range(9, 19)]
    
    # Remover horários já agendados
    horarios_ocupados = [agendamento.data_hora.strftime('%H:%M') for agendamento in agendamentos]
    horarios_disponiveis = [h for h in horarios_possiveis if h not in horarios_ocupados]
    
    return jsonify({'horarios': horarios_disponiveis})

@app.route('/portfolio')
def portfolio():
    servicos = Servico.query.all()
    imagens_destaque = Imagem.query.filter_by(destaque=True).all()
    
    # Agrupar imagens por serviço
    servicos_com_imagens = []
    for servico in servicos:
        if servico.imagens:
            servicos_com_imagens.append(servico)
    
    return render_template('portfolio.html', servicos_com_imagens=servicos_com_imagens, imagens_destaque=imagens_destaque)

@app.route('/precos')
def precos():
    return render_template('precos.html')

@app.route('/admin/imagens', methods=['GET', 'POST'])
@login_required
def admin_imagens():
    if current_user.tipo != 'admin':
        flash('Acesso negado.', 'danger')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        acao = request.form.get('acao')
        
        if acao == 'upload':
            # Verificar se o arquivo foi enviado
            if 'imagem' not in request.files:
                flash('Nenhum arquivo enviado.', 'danger')
                return redirect(request.url)
            
            arquivo = request.files['imagem']
            
            # Se o usuário não selecionar um arquivo
            if arquivo.filename == '':
                flash('Nenhum arquivo selecionado.', 'danger')
                return redirect(request.url)
            
            if arquivo and allowed_file(arquivo.filename):
                # Gerar um nome de arquivo seguro e único
                nome_arquivo = secure_filename(arquivo.filename)
                nome_base, extensao = os.path.splitext(nome_arquivo)
                nome_unico = f"{nome_base}_{uuid.uuid4().hex[:8]}{extensao}"
                
                # Salvar o arquivo
                caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], nome_unico)
                arquivo.save(caminho_arquivo)
                
                # Criar registro no banco de dados
                nova_imagem = Imagem(
                    nome_arquivo=nome_unico,
                    caminho=os.path.join('img', 'portfolio', nome_unico),
                    titulo=request.form.get('titulo'),
                    descricao=request.form.get('descricao'),
                    servico_id=request.form.get('servico_id'),
                    destaque=True if request.form.get('destaque') else False
                )
                
                db.session.add(nova_imagem)
                db.session.commit()
                
                flash('Imagem enviada com sucesso!', 'success')
            else:
                flash('Tipo de arquivo não permitido.', 'danger')
        
        elif acao == 'excluir':
            imagem_id = request.form.get('id')
            imagem = Imagem.query.get_or_404(imagem_id)
            
            # Excluir o arquivo físico
            try:
                caminho_completo = os.path.join('static', imagem.caminho)
                if os.path.exists(caminho_completo):
                    os.remove(caminho_completo)
            except Exception as e:
                flash(f'Erro ao excluir arquivo: {str(e)}', 'warning')
            
            # Excluir o registro do banco de dados
            db.session.delete(imagem)
            db.session.commit()
            
            flash('Imagem excluída com sucesso!', 'success')
        
        elif acao == 'atualizar':
            imagem_id = request.form.get('id')
            imagem = Imagem.query.get_or_404(imagem_id)
            
            imagem.titulo = request.form.get('titulo')
            imagem.descricao = request.form.get('descricao')
            imagem.servico_id = request.form.get('servico_id')
            imagem.destaque = True if request.form.get('destaque') else False
            
            db.session.commit()
            
            flash('Informações da imagem atualizadas com sucesso!', 'success')
        
        return redirect(url_for('admin_imagens'))
    
    imagens = Imagem.query.all()
    servicos = Servico.query.all()
    return render_template('admin_imagens.html', imagens=imagens, servicos=servicos)

# Criar o primeiro usuário administrador se não existir
def criar_admin():
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        criar_admin()
    app.run(debug=True) 