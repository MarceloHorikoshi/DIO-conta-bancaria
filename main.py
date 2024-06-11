from abc import ABC, abstractproperty, abstractmethod
from datetime import datetime


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:

            print('Operação falhou, saldo insuficiente!')

        elif valor > 0:

            self._saldo -= valor
            print('Saque realizado com sucesso!')
            return True

        else:

            print('Valor informado não é um numero válido!')

        return False

    def depositar(self, valor):

        if valor > 0:
            self._saldo += valor
            print('Deposito realizado com sucesso!')

        else:
            print('Operação falhou, valor não é válido')
            return False

        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes
             if transacao['tipo'] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques
        limite_saques

        if excedeu_limite:
            print('Valor do saque excede o limite')

        elif excedeu_saques:
            print('Execedeu quantidade máximo de saques!')

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return (f'Agência: {self.agencia}'
                f'C/C:\t\t{self.numero}'
                f'Titular:\{self.cliente.nome}')


class Historico:
    def __init__(self):
        self._trasacoes = []

    @property
    def transacoes(self):
        return self._trasacoes

    def adicionar_transacao(self, transacao):
        self._trasacoes.append(
            {
                'tipo': transacao.__class__.__name__,
                'valor': transacao.valor,
                'data': datetime.now().strftime('%d-%m-%Y %H:%M:%s'),
            }
        )


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
            