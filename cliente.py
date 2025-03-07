import requests

API_URL = "http://127.0.0.1:5000/movimentacao"


def obter_tipo_movimentacao():
    while True:
        tipo = input("Informe o tipo de movimentação (entrada/saida): ").strip().lower()
        if tipo in ['entrada', 'saida']:
            return tipo
        print("Tipo inválido! Digite 'entrada' ou 'saida'.")


def obter_valor():
    while True:
        try:
            valor = float(input("Informe o valor da movimentação: "))
            if valor > 0:
                return valor
            else:
                print("O valor deve ser maior que zero.")
        except ValueError:
            print("Entrada inválida! Digite um número válido.")


def enviar_movimentacao(tipo, valor):
    dados = {"tipo": tipo, "valor": valor}
    resposta = requests.post(API_URL, json=dados)

    # Verifique o status da resposta
    if resposta.status_code == 201:
        print("\n✅ Movimentação registrada com sucesso!\n")
    else:
        # Se o status não for 201, exibe o código de status e a resposta bruta
        print(f"\n❌ Erro ao registrar movimentação. Código de status: {resposta.status_code}")

        try:
            # Tenta interpretar a resposta como JSON
            print("Detalhes do erro:", resposta.json())
        except ValueError:
            # Caso não consiga interpretar como JSON, mostra a resposta bruta
            print("Resposta não é um JSON válido. Conteúdo da resposta:", resposta.text)


def main():
    while True:
        tipo = obter_tipo_movimentacao()
        valor = obter_valor()
        enviar_movimentacao(tipo, valor)

        continuar = input("Deseja adicionar outra movimentação? (s/n): ").strip().lower()
        if continuar != 's':
            print("\n📌 Encerrando o programa...")
            break


if __name__ == "__main__":
    main()