import argparse
import getpass
import hashlib
import sys

import requests

API_URL = "https://api.pwnedpasswords.com/range/"
TIMEOUT = 10

CRITERIOS = [
    ("tem pelo menos 8 caracteres", lambda s: len(s) >= 8),
    ("tem letra minúscula", lambda s: any(c.islower() for c in s)),
    ("tem letra maiúscula", lambda s: any(c.isupper() for c in s)),
    ("tem caractere especial", lambda s: any(not c.isalnum() for c in s)),
    ("tem número", lambda s: any(c.isdigit() for c in s)),
]

NIVEIS = {0: "Muito fraca", 1: "Muito fraca", 2: "Fraca", 3: "Média", 4: "Boa", 5: "Forte"}


def gerar_hash(senha):
    return hashlib.sha1(senha.encode("utf-8")).hexdigest().upper()


def consultar_vazamentos(senha):
    hash_completo = gerar_hash(senha)
    prefixo, sufixo = hash_completo[:5], hash_completo[5:]

    resposta = requests.get(API_URL + prefixo, timeout=TIMEOUT)
    resposta.raise_for_status()

    for linha in resposta.text.splitlines():
        hash_sufixo, _, quantidade = linha.partition(":")
        if hash_sufixo.strip() == sufixo:
            return int(quantidade)
    return 0


def avaliar_forca(senha):
    resultados = [(descricao, teste(senha)) for descricao, teste in CRITERIOS]
    pontos = sum(1 for _, ok in resultados if ok)
    return pontos, resultados


def formatar_numero(n):
    return f"{n:,}".replace(",", ".")


def obter_senha(args):
    if args.senha is not None:
        return args.senha
    return getpass.getpass("Digite a senha (não aparece na tela): ")


def main():
    parser = argparse.ArgumentParser(
        description="Verifica se uma senha já apareceu em vazamentos e avalia sua força."
    )
    parser.add_argument(
        "--senha",
        help="senha a verificar (menos seguro: fica no histórico do terminal)",
    )
    args = parser.parse_args()

    senha = obter_senha(args)
    if not senha:
        print("Erro: a senha não pode ser vazia.", file=sys.stderr)
        return 2

    print("\n=== Verificador de Senha Vazada ===\n")

    try:
        vazamentos = consultar_vazamentos(senha)
    except requests.exceptions.Timeout:
        print("Erro: tempo esgotado ao consultar a API.", file=sys.stderr)
        return 2
    except requests.exceptions.ConnectionError:
        print("Erro: sem conexão com a API.", file=sys.stderr)
        return 2
    except requests.exceptions.HTTPError as e:
        print(f"Erro: a API retornou um erro ({e.response.status_code}).", file=sys.stderr)
        return 2

    if vazamentos > 0:
        print(f"[ALERTA] Essa senha já apareceu em {formatar_numero(vazamentos)} vazamentos conhecidos.")
        print("         Evite usá-la em qualquer conta.")
    else:
        print("[OK] Essa senha não foi encontrada em vazamentos conhecidos.")

    pontos, resultados = avaliar_forca(senha)
    print(f"\nForça estimada: {NIVEIS[pontos]} ({pontos}/{len(CRITERIOS)} critérios)")
    for descricao, ok in resultados:
        marca = "✓" if ok else "✗"
        print(f"  [{marca}] {descricao}")

    return 1 if vazamentos > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
