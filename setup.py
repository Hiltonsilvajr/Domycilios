from setuptools import setup, find_packages

setup(
    name="cilios_app",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask==2.3.3",
        "Flask-SQLAlchemy==3.1.1",
        "Flask-Login==0.6.2",
        "Werkzeug==2.3.7",
        "python-dotenv==1.0.0",
        "SQLAlchemy==2.0.20",
        "email-validator==2.0.0",
    ],
    author="Desenvolvedor",
    author_email="dev@exemplo.com",
    description="Sistema de Agendamento de Manutenção de Cílios",
    keywords="cílios, agendamento, beleza",
    url="https://github.com/seu-usuario/cilios-app",
    project_urls={
        "Bug Tracker": "https://github.com/seu-usuario/cilios-app/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
) 