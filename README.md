# Domycilios - Sistema de Agendamento

Sistema web para agendamento de serviços de extensão de cílios e design de sobrancelhas.

## Funcionalidades

- Página inicial com informações sobre os serviços
- Galeria de fotos de trabalhos realizados
- Página de preços com tabela de serviços
- Sistema de agendamento online
- Painel administrativo para gerenciamento de imagens
- Integração com Instagram

## Tecnologias Utilizadas

- **Backend**: Python com Flask
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Banco de Dados**: SQLite (desenvolvimento) / PostgreSQL (produção)
- **Autenticação**: Flask-Login
- **Upload de Imagens**: Werkzeug

## Instalação e Execução Local

### Pré-requisitos
- Python 3.9+
- pip (gerenciador de pacotes Python)

### Passos para Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/domycilios.git
   cd domycilios
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente:
   - Crie um arquivo `.env` na raiz do projeto com base no `.env.example`

5. Execute a aplicação:
   ```bash
   python run.py
   ```

6. Acesse a aplicação em:
   - http://localhost:5000

## Estrutura do Projeto

```
domycilios/
├── app.py              # Aplicação principal Flask
├── run.py              # Script para executar a aplicação
├── wsgi.py             # Ponto de entrada para servidores WSGI
├── requirements.txt    # Dependências do projeto
├── static/             # Arquivos estáticos (CSS, JS, imagens)
│   ├── css/
│   ├── js/
│   └── img/
├── templates/          # Templates HTML
│   ├── base.html       # Template base
│   ├── index.html      # Página inicial
│   ├── portfolio.html  # Galeria de fotos
│   ├── precos.html     # Tabela de preços
│   └── admin_imagens.html # Painel administrativo
└── DEPLOY.md           # Guia de implantação
```

## Implantação

Para instruções detalhadas sobre como implantar a aplicação em um servidor de produção, consulte o arquivo [DEPLOY.md](DEPLOY.md).

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para mais detalhes.

## Contato

Instagram: [@domycilios](https://www.instagram.com/domycilios) 