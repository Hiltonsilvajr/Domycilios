# Guia de Implantação do Domycilios

Este guia fornece instruções para hospedar a aplicação Domycilios na internet, tornando-a acessível globalmente.

## 1. Registrar um Domínio

Primeiro, você precisa registrar um nome de domínio (ex: domycilios.com):

- **Opções de registradores**:
  - [Registro.br](https://registro.br/) (para domínios .br)
  - [GoDaddy](https://www.godaddy.com/)
  - [Namecheap](https://www.namecheap.com/)
  - [Hostinger](https://www.hostinger.com.br/)

- **Custo aproximado**: R$40-R$100 por ano, dependendo da extensão (.com, .com.br, etc.)

## 2. Escolher um Serviço de Hospedagem

### Opção 1: Hospedagem Compartilhada (mais simples)
- **Provedores**: Hostgator, Locaweb, Hostinger
- **Vantagens**: Fácil de configurar, baixo custo
- **Desvantagens**: Menos flexível, pode ter limitações para aplicações Python/Flask

### Opção 2: VPS (Servidor Virtual Privado) (mais flexível)
- **Provedores**: DigitalOcean, Linode, AWS Lightsail, Contabo
- **Vantagens**: Controle total, mais recursos, melhor desempenho
- **Desvantagens**: Requer mais conhecimento técnico para configurar

### Opção 3: PaaS (Plataforma como Serviço) (mais fácil para aplicações Flask)
- **Provedores**: Heroku, Render, PythonAnywhere, Railway, Fly.io
- **Vantagens**: Fácil implantação, gerenciamento simplificado
- **Desvantagens**: Pode ser mais caro para aplicações com tráfego maior

## 3. Preparação para Implantação

### Gerar uma Chave Secreta Segura
Antes de implantar, gere uma chave secreta forte para proteger sua aplicação:

```bash
# Execute o script de geração de chave
python generate_secret_key.py
```

Copie a chave gerada e use-a nas configurações de ambiente da sua hospedagem.

### Arquivos de Configuração
Os seguintes arquivos já estão preparados para implantação:
- `Procfile`: Define como servidores como Heroku devem executar a aplicação
- `requirements.txt`: Lista as dependências do projeto
- `runtime.txt`: Especifica a versão do Python
- `wsgi.py`: Ponto de entrada para servidores WSGI como Gunicorn
- `.env.example`: Modelo para configuração de variáveis de ambiente

## 4. Implantação no Heroku (Opção Recomendada para Iniciantes)

O Heroku é uma plataforma que facilita a implantação de aplicações web. Siga estes passos:

### Passos para Implantação
1. **Crie uma conta no Heroku**: [Heroku Sign Up](https://signup.heroku.com/)

2. **Instale o Heroku CLI**:
   - Windows: Baixe o instalador em [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
   - Mac: `brew install heroku/brew/heroku`
   - Linux: `sudo snap install heroku --classic`

3. **Faça login no Heroku**:
   ```bash
   heroku login
   ```

4. **Crie um aplicativo Heroku**:
   ```bash
   heroku create domycilios
   ```

5. **Configure as variáveis de ambiente**:
   ```bash
   # Use a chave gerada pelo script generate_secret_key.py
   heroku config:set SECRET_KEY=sua_chave_secreta_aqui
   heroku config:set FLASK_ENV=production
   ```

6. **Implante a aplicação**:
   ```bash
   git add .
   git commit -m "Preparação para implantação"
   git push heroku main
   ```

7. **Configure o banco de dados** (opcional, para PostgreSQL):
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```
   
   Nota: Se usar PostgreSQL, você precisará atualizar o código para usar o SQLAlchemy com PostgreSQL.

8. **Abra a aplicação**:
   ```bash
   heroku open
   ```

### Conectando seu Domínio ao Heroku
1. No painel do Heroku, vá para Settings > Domains
2. Adicione seu domínio personalizado
3. Siga as instruções para configurar os registros DNS no seu registrador de domínio

## 5. Configuração do Servidor (para VPS)

Se você escolher um VPS, precisará configurar o servidor:

### Instalar Dependências
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx
```

### Configurar o Ambiente Virtual
```bash
cd /var/www/domycilios
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### Configurar Gunicorn
O arquivo `wsgi.py` já está criado na raiz do projeto.

Teste o Gunicorn:
```bash
gunicorn --bind 0.0.0.0:5000 wsgi:app
```

### Configurar Nginx
Crie um arquivo de configuração em `/etc/nginx/sites-available/domycilios`:
```
server {
    listen 80;
    server_name domycilios.com www.domycilios.com;

    location /static {
        alias /var/www/domycilios/static;
    }

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Ative a configuração:
```bash
sudo ln -s /etc/nginx/sites-available/domycilios /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### Configurar SSL (HTTPS)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d domycilios.com -d www.domycilios.com
```

## 6. Configuração para Produção

### Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto (não inclua no controle de versão):
```
FLASK_ENV=production
SECRET_KEY=sua_chave_secreta_muito_segura
DATABASE_URL=sqlite:///site.db
DEBUG=False
```

### Configurar Serviço Systemd
Crie um arquivo `/etc/systemd/system/domycilios.service`:
```
[Unit]
Description=Domycilios Gunicorn Daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/domycilios
Environment="PATH=/var/www/domycilios/venv/bin"
EnvironmentFile=/var/www/domycilios/.env
ExecStart=/var/www/domycilios/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 wsgi:app

[Install]
WantedBy=multi-user.target
```

Inicie o serviço:
```bash
sudo systemctl start domycilios
sudo systemctl enable domycilios
```

## 7. Configuração de DNS

Após registrar seu domínio, você precisará configurar os registros DNS para apontar para o seu servidor:

1. Acesse o painel de controle do seu registrador de domínio
2. Localize a seção de gerenciamento de DNS
3. Adicione um registro A apontando para o endereço IP do seu servidor:
   - Tipo: A
   - Nome: @ (ou domycilios)
   - Valor: [Endereço IP do seu servidor]
   - TTL: 3600 (ou o padrão)

4. Adicione outro registro A para o subdomínio www:
   - Tipo: A
   - Nome: www
   - Valor: [Mesmo endereço IP]
   - TTL: 3600 (ou o padrão)

## 8. Opção Simplificada: Render ou Railway

### Render
1. Crie uma conta em [Render](https://render.com/)
2. Conecte seu repositório GitHub
3. Crie um novo Web Service
4. Selecione o repositório e configure:
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn wsgi:app`
5. Configure variáveis de ambiente
6. Implante o serviço

### Railway
1. Crie uma conta em [Railway](https://railway.app/)
2. Inicie um novo projeto a partir do GitHub
3. Selecione seu repositório
4. Configure variáveis de ambiente
5. Railway detectará automaticamente sua aplicação Flask

## 9. Manutenção e Monitoramento

- **Backups**: Configure backups regulares do banco de dados
  ```bash
  # Exemplo para SQLite
  cp site.db site.db.backup-$(date +%Y%m%d)
  ```

- **Monitoramento**:
  - [UptimeRobot](https://uptimerobot.com/) (gratuito)
  - [Sentry](https://sentry.io/) (para rastreamento de erros)
  - [New Relic](https://newrelic.com/) (monitoramento avançado)

- **Atualizações**:
  - Mantenha o sistema operacional atualizado
  - Atualize regularmente as dependências Python
  ```bash
  pip install --upgrade -r requirements.txt
  ```

## 10. Segurança

- **Firewall**: Configure um firewall para proteger seu servidor
  ```bash
  sudo ufw allow 80/tcp
  sudo ufw allow 443/tcp
  sudo ufw allow 22/tcp
  sudo ufw enable
  ```

- **Atualizações de Segurança**: Mantenha seu sistema atualizado
  ```bash
  sudo apt update && sudo apt upgrade -y
  ```

- **Proteção contra Ataques**: Configure proteção contra ataques comuns
  ```bash
  # Instalar fail2ban para proteção contra ataques de força bruta
  sudo apt install fail2ban
  sudo systemctl enable fail2ban
  sudo systemctl start fail2ban
  ```

## Recursos Adicionais

- [Documentação do Flask sobre Implantação](https://flask.palletsprojects.com/en/2.3.x/deploying/)
- [Documentação do Heroku para Python](https://devcenter.heroku.com/categories/python-support)
- [Tutorial de Implantação do DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-20-04)
- [Guia de Implantação do Render](https://render.com/docs/deploy-flask)
- [Guia de Implantação do Railway](https://docs.railway.app/guides/flask) 