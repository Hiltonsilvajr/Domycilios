#!/usr/bin/env python
"""
Script para gerar uma chave secreta aleatória para uso em produção.
Execute este script para gerar uma chave secreta forte para sua aplicação Flask.
"""

import os
import secrets
import base64

def generate_secret_key(length=32):
    """Gera uma chave secreta aleatória com o comprimento especificado."""
    return secrets.token_hex(length)

def generate_base64_key(length=32):
    """Gera uma chave secreta aleatória codificada em base64."""
    return base64.b64encode(os.urandom(length)).decode('utf-8')

if __name__ == "__main__":
    print("\nGerando chaves secretas para uso em produção...\n")
    
    hex_key = generate_secret_key()
    base64_key = generate_base64_key()
    
    print(f"Chave Hexadecimal (64 caracteres):")
    print(f"{hex_key}\n")
    
    print(f"Chave Base64 (43 caracteres):")
    print(f"{base64_key}\n")
    
    print("Instruções:")
    print("1. Copie uma das chaves acima")
    print("2. Adicione ao seu arquivo .env em produção:")
    print("   SECRET_KEY=sua_chave_aqui")
    print("3. Ou defina como variável de ambiente no seu servidor:")
    print("   export SECRET_KEY=sua_chave_aqui\n")
    
    print("IMPORTANTE: Mantenha esta chave em segredo!")
    print("Nunca compartilhe ou cometa esta chave em repositórios públicos.\n") 