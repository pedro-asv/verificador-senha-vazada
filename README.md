
# 🔐 Verificador de Senha Vazada

Ferramenta de linha de comando (CLI) em Python que verifica se uma senha já
apareceu em vazamentos de dados conhecidos — **sem nunca enviar a senha real
pela internet** — e avalia a força dela.

## Por que esse projeto

Durante meu estágio em Tecnologia da Informação, trabalhei diretamente com
digitalização e proteção de dados cadastrais sensíveis, aplicando noções da
LGPD. Esse projeto nasceu dessa vivência: é uma ferramenta prática que aplica
o mesmo tipo de preocupação — proteção de dados sensíveis — só que aplicada
a senhas.

## Como funciona: o modelo k-Anonymity

O maior risco de uma ferramenta desse tipo seria óbvio: para checar se uma
senha vazou, seria preciso... mandar a senha pra algum lugar? Não. A API
pública do [Have I Been Pwned](https://haveibeenpwned.com/) resolve isso com
um modelo chamado **k-Anonymity**:

1. A senha é transformada em um hash **SHA-1**, localmente, no seu computador.
2. Só os **5 primeiros caracteres** desse hash são enviados para a API.
3. A API responde com **todos** os hashes conhecidos que começam com esse
   mesmo prefixo — geralmente algumas centenas deles. Ela não sabe (e não
   tem como saber) qual desses é o seu.
4. A comparação final — decidir se a *sua* senha está na lista — acontece
   **localmente**, no seu próprio computador.

Resultado: nem a API, nem alguém interceptando a conexão, consegue
descobrir sua senha a partir da requisição.

## Instalação

```bash
git clone https://github.com/pedro-asv/verificador-senha-vazada.git
cd verificador-senha-vazada
pip install -r requirements.txt
```

## Uso

Modo recomendado — a senha é digitada de forma oculta (não aparece na tela
nem fica salva no histórico do terminal):

```bash
python verificador.py
```

Modo alternativo (menos seguro — evite em máquina compartilhada):

```bash
python verificador.py --senha "suasenha123"
```

### Exemplo de saída

```
=== Verificador de Senha Vazada ===

[ALERTA] Essa senha já apareceu em 3.730.471 vazamentos conhecidos.
         Evite usá-la em qualquer conta.

Força estimada: Média (3/5 critérios)
  [✓] tem pelo menos 8 caracteres
  [✓] tem letra minúscula
  [✗] tem letra maiúscula
  [✗] tem caractere especial
  [✓] tem número
```

O programa também retorna um **exit code** (0 = segura, 1 = vazada, 2 = erro),
o que permite usá-lo dentro de scripts maiores de automação.

## Tecnologias

- Python 3
- [`requests`](https://pypi.org/project/requests/) — chamadas HTTP
- `hashlib` (biblioteca padrão) — geração do hash SHA-1
- `argparse` (biblioteca padrão) — interface de linha de comando
- API pública [Have I Been Pwned](https://haveibeenpwned.com/API/v3) (modelo k-Anonymity)

## Possíveis melhorias futuras

- [ ] Verificação em lote, a partir de um arquivo com várias senhas
- [ ] Interface web simples (Flask)
- [ ] Sugestão automática de senha forte quando a informada for fraca

## Autor

**Pedro Augusto** — Desenvolvedor Full-Stack Júnior
[LinkedIn](https://linkedin.com/in/pedro-augusto-4103b6258) · [GitHub](https://github.com/pedro-asv)
