import random
import math

tamanho_população = 5
caracteristicas = 5

def gerações_população():
    população = []
    for _ in range(tamanho_população):

        rgb = []
        for i in range(3): 

            mistura = random.uniform(0, 1)  
            laranja = (255, 165, 0)[i]
            preto = 0  
            cor_resultante = int(mistura * laranja + (1 - mistura) * preto)
            rgb.append(cor_resultante)
        
        tamanho = random.randint(0, 100)
        peso = random.randint(0, 100)
        individual = rgb + [tamanho, peso]
        população.append(individual)
    return população


população = gerações_população()

def distância_euclidiana(color1, color2):
    return math.sqrt((color1[0] - color2[0])**2 + (color1[1] - color2[1])**2 + (color1[2] - color2[2])**2)

def fitness_função(individual):
    rgb = individual[:3]
    
    cor_ideal = (128, 82, 0)  

    fitness = 1 / (distância_euclidiana(rgb, cor_ideal) + 1e-6)
    return fitness

#Roleta
def seleção_roleta(população):
    total_fitness = sum(fitness_função(individual) for individual in população)
    seleção_probabilidade = [fitness_função(individual) / total_fitness for individual in população]
    escolha = random.choices(população, weights=seleção_probabilidade, k=1)
    return escolha[0]

#Cross-over
def crossover_um_ponto(pai1, pai2):
    ponto = random.randint(1, len(pai1) - 1)
    filho1 = pai1[:ponto] + pai2[ponto:]
    filho2 = pai2[:ponto] + pai1[ponto:]
    return filho1, filho2

def crossover_uniforme(pai1, pai2):
    filho1 = [random.choice([pai1[i], pai2[i]]) for i in range(len(pai1))]
    filho2 = [random.choice([pai1[i], pai2[i]]) for i in range(len(pai1))]
    return filho1, filho2

def crossover_aritmético(pai1, pai2):
    mistura = random.uniform(0, 1)
    filho1 = [int(mistura * pai1[i] + (1 - mistura) * pai2[i]) for i in range(len(pai1))]
    filho2 = [int((1 - mistura) * pai1[i] + mistura * pai2[i]) for i in range(len(pai1))]
    return filho1, filho2

#Mutação
def random_mutação(individual):
    gene = random.randint(0, 2)
    individual[gene] += random.randint(0, 255)
    return individual

def pequena_mutação(individual):
    gene = random.randint(0, 2)
    individual[gene] += random.randint(0, 10)
    return individual

def mutação_dirigida(individual):
    target = (128, 82, 0)  
    gene = random.randint(0, 2)
    individual[gene] = int((individual[gene] + target[gene]) / 2)
    return individual


def algoritmo_genético():
    gerações = 5

    while True:  
        população = gerações_população()
        print(f"\nPopulação Inicial: {população}")

        #Roleta
        confirmar = input("\nDeseja realizar a Seleção por Roleta? (S/N): ").strip().lower()
        if confirmar == 'n':
            nova_população = gerações_população() 
            print("Processo de seleção interrompido.")
            continuar = input("Gostaria de sair ou gerar uma nova primeira geração? (Sair/Nova): ").strip().lower()
            if continuar == "sair":
                print("Saindo do processo.")
                break
            elif continuar == "nova":
                print("Gerando nova primeira geração.")
                continue  
        
        if confirmar == 's':
            pai1 = seleção_roleta(população)
            pai2 = seleção_roleta(população)
            print(f"\n** Roleta **")
            print(f"Pai 1: {pai1}, Pai 2: {pai2}")

            #Cross-over
            confirmar = input("\nDeseja realizar o Crossover? (S/N): ").strip().lower()
            if confirmar == 's':
                print("\n** Crossover **")
                print("\nMétodos de Crossover:")
                print("1. Crossover um ponto")
                print("2. Crossover uniforme")
                print("3. Crossover aritmético")

                print("\n** Resultados do Crossover **")

                filho1_um_ponto, filho2_um_ponto = crossover_um_ponto(pai1, pai2)
                print(f"\nCrossover um ponto:")
                print(f"Filho 1: {filho1_um_ponto}")
                print(f"Filho 2: {filho2_um_ponto}")
                
                filho1_uniforme, _ = crossover_uniforme(pai1, pai2)  
                print(f"\nCrossover uniforme:")
                print(f"Filho 1: {filho1_uniforme}")
                
                filho1_aritmetico, _ = crossover_aritmético(pai1, pai2)  
                print(f"\nCrossover aritmético:")
                print(f"Filho 1: {filho1_aritmetico}")

                nova_população = [pai1, pai2, filho1_um_ponto, filho2_um_ponto, filho1_uniforme, filho1_aritmetico]
                print("\nNova geração gerada.")
                print(nova_população)

                #Mutação
                confirmar_mutação = input("\nDeseja realizar a Mutação? (S/N): ").strip().lower()
                if confirmar_mutação == 's':
                    print("\n** Mutação **")

                    individuo_sorteado = random.choice(nova_população)
                    print(f"\nIndivíduo sorteado para a mutação: {individuo_sorteado}")

                    print("\nMétodos de Mutação:")

                    print("\nMétodo de mutação: Aleatória")
                    individuo_mutado_aleatorio = random_mutação(individuo_sorteado.copy())
                    print(f"Indivíduo após mutação aleatória: {individuo_mutado_aleatorio}")

                    print("\nMétodo de mutação: Pequena Mutação")
                    individuo_mutado_pequeno = pequena_mutação(individuo_sorteado.copy())
                    print(f"Indivíduo após pequena mutação: {individuo_mutado_pequeno}")

                    print("\nMétodo de mutação: Mutação Dirigida")
                    individuo_mutado_dirigido = mutação_dirigida(individuo_sorteado.copy())
                    print(f"Indivíduo após mutação dirigida: {individuo_mutado_dirigido}")

                else:
                    print("Processo de mutação interrompido.")
            else:
                print("Processo de crossover interrompido.")
            
        continuar = input("\nDeseja realizar outra geração de população? (S/N): ").strip().lower()
        if continuar == 'n':
            sair = input("Gostaria de sair ou gerar uma nova primeira geração? (Sair/Nova): ").strip().lower()
            if sair == 'sair':
                print("Saindo do processo.")
                break  
            elif sair == 'nova':
                print("Gerando nova primeira geração.")
                continue  

algoritmo_genético()
