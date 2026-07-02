class Pessoa: 
    def __init__(self, nome, idade, cabelo, peso):
        self.nome = nome
        self.__idade = idade
        self.cabelo = cabelo
        self.peso = peso


        
    def apresentar(self):
            print(f"Olá, meu nome é {self.nome}, tenho {self.__idade} anos, meu cabelo é {self.cabelo}, e meu peso é {self.peso}.")

    def get_idade(self):
        return self.__idade #Encapsulamento para proteaçao de dados, nao permitindo que a idade seja alterada diretamente.

p1 = Pessoa("João", 25, "roxo", 70)
p1.apresentar()

p2 = Pessoa("Maria", 30, "castanho", 60)
p2.apresentar()

print("A idade de", p1.nome, "é", p1.get_idade())


class Aluno(Pessoa):
    def __init__(self, nome, idade, cabelo, peso, matricula):
        super().__init__(nome, idade, cabelo, peso) # Forma de chamar o construtor da classe pai (Pessoa) para inicializar os atributos herdados.
        self.matricula = matricula

    def apresentarm(self):
        super().apresentarm()

print(f"Minha matrícula é {self.matricula}.")