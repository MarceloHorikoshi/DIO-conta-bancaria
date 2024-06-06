import textwrap


def menu():
    menu = """
    \n
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova Conta
    [lc]\tListar contas
    [nu]\tNovo Usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def depositar(saldo, valor, extrato, /):  # / obriga a passar argumentos por posição

    if valor.isdigit():
        valor = float(valor)

        if valor > 0:
            saldo += valor
            extrato += f'Depósito: R$ {valor:.2f}\n'
            print(f'Valor de R$ {valor} depositado com sucesso!')

        else:
            print('Operação falhou! O valor informado é inválido')
    else:
        print('Operação falhou! O valor informado é inválido')

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if valor.isdigit():
        valor = float(valor)

        if valor > 0:

            excedeu_saldo = valor > saldo

            excedeu_limite = valor > limite

            excedeu_saques = numero_saques >= limite_saques

            if excedeu_saldo:
                print('Operação falhou! Você não tem saldo suficiente.')

            elif excedeu_limite:
                print('Operação falhou! O valor excede o limite.')

            elif excedeu_saques:
                print('Operação falhou! Número máximo de saques excedido.')

            else:
                saldo -= valor
                extrato += f'Saque: R$ {valor:.2f}\n'
                numero_saques += 1
                print(f'Valor de R$ {valor} sacado com sucesso!')

        else:
            print('Operação falhou! O valor informado é inválido')
    else:
        print('Operação falhou! O valor informado é inválido')

    return saldo, extrato


def exibir_conta(saldo, /, *, extrato): # / posicional e * nomeado
    print('\n ============EXTRATO=============')
    print('Não foram realizadas movimentações.' if not extrato else extrato)
    print(f'\n Saldo: R$ {saldo:.2f}')
    print('\n ================================')


def criar_usuario(usuarios):
    cpf = input('Informe seu CPF (somente numeros): ')
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print('\n@@@ Já existe usuário com esse cpf! @@@')
        return

    nome = input('Informe o seu nome completo: ')
    data_nascimento = input('Informe sua data de nascimento (dd-mm-aaaa: ')
    endereco = input('Informe o seu endereço (logradouro, número - bairro - cidade/sigla estado: ')

    usuarios.append({
        'nome': nome,
        'data_nascimento': data_nascimento,
        'cpf': cpf,
        'endereco': endereco
    })

    print('Usuário criado com sucesso!')


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input('Informe o CPF do usuário (somente numeros: ')
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print('\n Conta criada com sucesso!')
        return {
            'agencia': agencia,
            'numero_conta': numero_conta,
            'usuario': usuario
        }
    print('Usuário não encontrado, fluxo de criação de conta encerrada!')


def listar_contas(contas):
    for conta in contas:
        linha = f"""
        Agência: \t{conta['agencia']}
        C/C:\t\t {conta['numero_conta']}
        Titular: \t {conta['usuario']['nome']}
        """

        print('=' * 100)
        print(textwrap.dedent(linha))


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ''
    numero_saques = 0
    usuarios = []
    contas = []

    while True:

        opcao = menu()

        if opcao == 'd':
            valor = input('Informe o valor do depósito: ')

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == 's':
            valor = input('Informe o valor do saque: ')

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES
            )

        elif opcao == 'e':
            exibir_conta(saldo, extrato=extrato)

        elif opcao == 'nu':
            criar_usuario(usuarios)

        elif opcao == 'nc':
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == 'lc':
            listar_contas(contas)

        elif opcao == 'q':
            print('Obrigado por utilizar os nossos serviços')
            break

        else:
            print('Operação inválida, por favor selecione novamente a operação desejada')

main()