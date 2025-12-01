# new_classes.py

class MembroUniversidade:
    def __init__(self, nome: str, email: str, matricula: str):
        self.nome = nome
        self.email = email
        self.matricula = matricula

    def exibir_dados(self):
        print("\nDados do membro")
        print("Nome:", self.nome)
        print("Email:", self.email)
        print("Matricula:", self.matricula)

    def to_tuple(self):
        """Retorna (nome, email, matricula) — útil para inserir no DB."""
        return (self.nome, self.email, self.matricula)

    @classmethod
    def from_tuple(cls, tup):
        """Cria objeto a partir de tupla (nome, email, matricula)."""
        if not tup:
            return None
        return cls(*tup)


class Disciplina:
    def __init__(self, codigo, descricao, periodo, carga_horaria, nome):
        self.codigo = codigo
        self.descricao = descricao
        self.periodo = periodo
        self.carga_horaria = carga_horaria
        self.nome = nome

    def exibir_dados(self):
        print("\nDados da disciplina")
        print("Nome:", self.nome)
        print("Codigo:", self.codigo)
        print("Descricao:", self.descricao)
        print("Periodo:", self.periodo)
        print("Carga horaria:", self.carga_horaria)


class Aluno(MembroUniversidade):
    def __init__(self, nome, email, matricula, coeficiente_rendimento):
        super().__init__(nome, email, matricula)
        self.coeficiente_rendimento = coeficiente_rendimento

    def exibir_dados(self):
        super().exibir_dados()
        print("Coeficiente de rendimento:", self.coeficiente_rendimento)


class Professor(MembroUniversidade):
    def __init__(self, nome, email, matricula, departamento, titulacao, salario):
        super().__init__(nome, email, matricula)
        self.departamento = departamento
        self.titulacao = titulacao
        self.salario = salario

    def exibir_dados(self):
        super().exibir_dados()
        print("Departamento:", self.departamento)
        print("Titulacao:", self.titulacao)
        print("Salario:", self.salario)
