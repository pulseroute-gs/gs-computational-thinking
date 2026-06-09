# Para o funcionamento desse código, é necessário ter a biblioteca requests baixada, caso não tenha, por meio do terminal, digite o seguinte para o funcionamento correto do código: pip install requests

import requests # Biblioteca usada para fazer requisições para a API OpenRouteService selecionada pelo nosso grupo como base de dados
import random # Biblioteca usada para sortear um número aleatório para calcular um desvio padrão de uma média feita no código

# Em relação ao conteúdo do código, além do contéudo dado em sala de aula, foi utilizado validação de entrada e acesso a API com try/except, além de manipulação de dicionários e APIs.

# A gente pensou sobre esconder a chave da API, mas como o projeto será entregue somente com o código em um arquivo .py, achamos desnecessário esconder, por isso deixamos ela exposta aqui mesmo
API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjI5ZTRmMDdlY2EwMTQwMWFiZTlkYWIwMzAxYWZkYmUxIiwiaCI6Im11cm11cjY0In0=" # Essa é a chave da nossa API

historico = [] # Lista para armazenar dicionários, onde cada um contém uma rota com a sua origem, destino, distância e tempo de duração

def entrada_invalida(): # Função para mostrar o usuário que a entrada inserida é inválida
    print('\nEntrada inválida!')
    print('Tente novamente!')

def sobre_projeto(): # Função para apresentar uma breve descrição textual da nossa solução
    print("\n=== SOBRE O PROJETO ===\n")
    print("O PulseRoute é um sistema inteligente")
    print("de mobilidade emergencial baseado em")
    print("geolocalização via satélite e")
    print("comunicação orbital para otimizar")
    print("rotas de ambulâncias em cidades.")

def iniciar_trajeto(): # Essa função serve para simular um trajeto de um sistema de navegação padrão no mercado usando uma API de cálculo de trajeto real
    
    # Como estamos lidando com essa API, não estamos pedindo endereços ao usuário pois isso exigiria transformar o texto em coordenadas exatas, por isso resolvemos utilizar localizações pré-definidas acompanhadas de suas coordenadas para sermos mais exatos
    locais = {
        1: ("Avenida Sapopemba", -23.6006133, -46.5120845),
        2: ("Avenida Paulista", -23.5614, -46.6559),
        3: ("Aeroporto Congonhas", -23.6261, -46.6566),
        4: ("Estação da Luz", -23.5344, -46.6339),
        5: ("Hospital Israelita Albert Einstein - Morumbi", -23.5999746, -46.7152573),
        6: ("Hospital Sírio-Libanês | Bela Vista", -23.5572102, -46.6537296),
        7: ("Hospital das Clínicas FMUSP", -23.5577989, -46.6698598),
        8: ("Hospital Infantil Sabará", -23.5497488, -46.6594652),
        9: ("Hospital Beneficência Portuguesa", -23.5667198, -46.6417744),
        10: ("Hospital São Paulo", -23.5977426, -46.6436056),
        11: ("Marginal Pinheiros - Ponte Eusébio Matoso", -23.5721994, -46.7011593),
        12: ("Marginal Tietê - Tatuapé", -23.5279757, -46.5851537)
    }

    for chave, valor in locais.items(): # Laço para printar as opções de locais pré-definidos
        print(f"{chave} - {valor[0]}")

    while True: # Laço para validar a entrada do usuário
        try:
            origem_opcao = int(input("\nPonto de partida da ambulância: "))
            destino_opcao = int(input("Destino final do atendimento: "))

            if origem_opcao == destino_opcao:
                print('Você precisa selecionar 2 localidades diferentes para conseguir fazer um trajeto!')

            elif (origem_opcao in locais) and (destino_opcao in locais):
                break
            
            else:
                entrada_invalida()

        except ValueError:
            entrada_invalida()

    origem = locais[origem_opcao]
    destino = locais[destino_opcao]

    origem_nome = origem[0]
    origem_lat = origem[1]
    origem_lon = origem[2]

    destino_nome = destino[0]
    destino_lat = destino[1]
    destino_lon = destino[2]

    url = "https://api.openrouteservice.org/v2/directions/driving-car" # Link da nossa API

    headers = {
        "Authorization": API_KEY, # Nossa chave da API
        "Content-Type": "application/json" # Informa ao servidor o formato dos dados a serem enviados
    }

    body = { # Coordenadas da origem e destino selecionados pelo usuário
        "coordinates": [
            [origem_lon, origem_lat],
            [destino_lon, destino_lat]
        ]
    }

    try: # A estrutura do try/except foi utilizada para tentar acessar a API e mostrar o erro caso apareça  
        response = requests.post( # Pedido para a API
            url,
            json=body,
            headers=headers,
            timeout=15
        )

        dados = response.json() # Dados retornados pela API

        distancia = dados["routes"][0]["summary"]["distance"]/1000 # Dividimos a distância por 1000 para armazenarmos em KM 
        tempo = dados["routes"][0]["summary"]["duration"]/60 # Dividimos o tempo por 60 para armazenarmos em minutos
        
        missao_atual = { # Dicionário com os dados da rota simulada para o usuário
            "origem": origem_nome,
            "destino": destino_nome,
            "distancia_km": distancia,
            "tempo_min": tempo,
        }

        historico.append(missao_atual) # Rota adicionada no histórico

        print("\nROTA INICIADA")
        print(f"Origem: {origem_nome}")
        print(f"Destino: {destino_nome}")
        print(f"Distância: {distancia:.2f} km")
        print(f"Tempo: {tempo:.2f} min")

    except requests.exceptions.Timeout: # Tempo excedido
        print("Timeout da API.")

    except Exception as erro: # Caso aconteça algum erro diferente, ele será mostrado aq
        print("Erro:", erro)

def simular_pulseroute(): # Essa função serve para simular como funcionaria nosso sistema mostrando o tempo economizado
    if len(historico) == 0:
        print('\nNão existe nenhuma missão salva!')
        print('Inicie uma missão e depois volte para fazer essa simulação! ')

    else:
        print('Digite o número da missão que deseja simular: \n')
        
        count = 1
        print('Digite 0 - Retornar ao menu principal ')
        for missao in historico: # Laço para mostrar todas as missões armazenadas
            print(f'Digite {count} - {missao["origem"]} até {missao["destino"]}')
            count+=1

        while True: # Esse laço não é um menu secundário, foi usado somente para caso o usuário tenha digitado um número fora do esperado, o sistema peça novamente uma nova entrada
            try: # Usado para garantir que o usuário não vai cometer um erro de ValueError
                missao_escolhida = int(input('\n'))
                if missao_escolhida == 0: # Se o usuário quiser voltar ao menu principal
                    break

                elif 0 < missao_escolhida < count: # Verificação se a entrada do usuário existe no histórico de missões
                    missao_atual = historico[missao_escolhida-1]

                    semaforos = int(missao_atual["distancia_km"]*1000 // 500) # Aqui realizamos um cálculo de uma média para dizer que a cada 500 metros temos 1 semáforo

                    semaforos = semaforos + random.randint(-2, 2) # Aqui para considerar um desvio da média, sorteamos um valor aleatório para somar a essa média

                    if semaforos < 0: # Caso esse desvio resulte num valor negativo iria causar um erro. Então esse if serve para considerar esse erro
                        semaforos = 0

                    tempo_original = missao_atual["tempo_min"] # Recebe o tempo padrão do trajeto

                    tempo_otimizado = calculo_tempo(tempo_original, semaforos) # Faz o cálculo da economia de tempo com a quantidade de semáforos determinado pelo nosso sistema e retorna esse valor para podermos guardar no dicionário

                    missao_atual["tempo_otimizado"] = tempo_otimizado # Armazena esse dado na missão

                    print("\nPULSE ROUTE")
                    print(f"Semáforos simulados: {semaforos}")
                    print(f"Tempo original (sem o PULSEROUTE): {tempo_original:.2f} min")
                    print(f"Tempo do trajeto com o PULSEROUTE: {(tempo_original-tempo_otimizado):.2f} min")
                    print(f"Tempo economizado com o PULSEROUTE: {tempo_otimizado:.2f} min")
                    break

                else:
                    entrada_invalida()

            except ValueError:
                entrada_invalida()

def historico_missoes(): # Função para mostrar todos os dados armazenados de determinado trajeto salvo no sistema
    if len(historico) == 0:
        print('\nNão existe nenhuma missão salva!')
        print('Inicie no mínimo uma missão e depois volte para poder utilizar essa funcionalidade! ')

    else:
        count = 1
        for missao_atual in historico: # Laço para mostrar todas as missões armazenadas
            print("\n" + "=" * 55)
            print(f'\nMissão {count} - {missao_atual["origem"]} até {missao_atual["destino"]}')
            print(f'Esse trajeto possui uma distância de: {missao_atual["distancia_km"]:.2f} km e uma duração (sem o PULSEROUTE) de {missao_atual["tempo_min"]:.2f} min')

            if "tempo_otimizado" in missao_atual:
                print(f'Com a utilização do PULSEROUTE, a economia de tempo desse trajeto foi de {missao_atual["tempo_otimizado"]:.2f} min !')

            count+=1

def gerar_relatorio(): # Essa função serve somente para fazer um relátorio da média de dados do nosso sistema 
    total = len(historico)
    if total == 0:
        print('\nNão existe nenhuma missão salva!')
        print('Inicie uma missão e depois volte para fazer essa simulação! ')
    
    else:
        print("\n=== RELATÓRIO OPERACIONAL ===\n")
        
        # Essas variáveis vão servir para realizar uma média do tempo otimizado pelo nosso sistema e do tempo normal do trajeto 
        tempo_normal = 0 
        tempo_otimizado = 0
        quantidade = 0

        for missao in historico:
            if "tempo_otimizado" in missao: # Aqui verificamos se a pessoa fez a simulação com o PULSEROUTE, verificando a existência dessa chave no dicionário
                # Caso ela exista, somamos esses dados para calcular uma média
                tempo_normal += missao["tempo_min"] 
                tempo_otimizado += missao["tempo_otimizado"] 
                quantidade += 1 

        if tempo_otimizado > 0: # Verificação se existe no mínimo uma rota simulada com nosso projeto
            media_normal = tempo_normal/quantidade
            media_economizada = tempo_otimizado/quantidade

            media_otimizada = media_normal - media_economizada # Média do tempo economizado com nosso sistema

            percentual = (media_economizada * 100) / media_normal  # Aqui calculamos um percentual de quanto tempo foi economizado em média com nosso produto

            print(f'A quantidade de rotas usadas nessa análise foram de: {quantidade}')
            print(f"A média do tempo normal dos trajetos é de: {media_normal:.2f} min")
            print(f"A média do tempo dos trajetos com o PULSEROUTE foi de: {media_otimizada:.2f} min")
            print(f"A redução média de tempo nos trajetos com o PULSEROUTE foi de: {media_economizada:.2f} min")
            print(f"A média percentual do ganho de tempo com o PULSEROUTE foi de: {percentual:.2f}%")

        else:
            print("Nenhuma rota foi simulada com o PULSEROUTE!")
            print('Faça alguma simulação e depois retorne!\n')
        
def calculo_tempo(tempo_inicial, quantidade_semaforos): # Essa função serve para retornar a economia de tempo com o PULSEROUTE
    ti = tempo_inicial
    qt = quantidade_semaforos

    print("\n=== LEGENDA MATEMÁTICA ===\n") # Legenda das variáveis da nossa função de cálculo de economia de tempo
    print('T(x) = Tempo final com a otimização do PULSEROUTE')
    print('ti = Tempo normal do trajeto (sem o PULSEROUTE)')
    print('qt = Quantidade de semáforos do trajeto\n')
    print("Função: T(x) = ti × 0.99^qt\n")
    
    resultado = ti * (0.99 ** qt) # Calcula o resultado dessa equação

    print("\n=== CÁLCULO MATEMÁTICO ===\n") # Mostra o passo a passo do cálculo matemático
    print(f'T(x) = {ti:.2f} × 0.99^({qt})')
    print(f'T(x) = {ti:.2f} X {(0.99 ** qt):.2f}')
    print(f'T(x) = {resultado:.2f}') 

    print('\nA seguir temos uma tabela para analisar os resultados dessa função:')
    print("\n=== ANÁLISE EXPONENCIAL ===\n") # Aqui fazemos uma tabela para mostrar os resultados da função em determinados pontos

    print("Semáforos | Tempo Previsto")

    salto = 1

    if qt > 15: # Se a quantidade de semáforos for muito grande, ele irá printar de 2 em 2 para redução do tamanho da tabela
        salto = 2

    for i in range(0,qt+1,salto): # Aqui a tabela é printada com a quantidade recebida de semafóros mostrando o resultado de tempo com cada semáforo
        tempo = ti * (0.99 ** i)
        print(f"{i:^10} | {tempo:.2f} min")

    economia = ti - resultado # Calcula a economia de tempo com o PULSEROUTE
    
    return economia # Retorna essa economia onde a função foi chamada

def main():
    while True:
        print("\n" + "=" * 55)
        print("         PULSEROUTE EMERGENCY SYSTEM")
        print("=" * 55)
        print("1 - Sobre o Projeto") # Funcionalidade para explicar projeto
        print("2 - Iniciar missão de emergência") # Funcionalidade para criar um trajeto entre 2 localidades pré-definidas e receber dados da API
        print("3 - Simular PULSEROUTE") # Funcionalidade para simular o funcionamento do PulseRoute, estipulando quantidade de semáforos, e usar o cálculo da funcionalidade 6
        print("4 - Consultar histórico de missões") # Funcionalidade para consultar trajetos salvos no sistema
        print("5 - Relatório de tempo salvo nas emergências") # Funcionalidade para criar um relatório de médias dos trajetos realizados
        print("6 - Calcular economia de tempo com o PULSEROUTE") # Funcionalidade para calcular a economia de tempo com uma função exponencial
        print("7 - Sair") # Encerrar funcionamento do sistema

        opcao = input("\nEscolha uma opção: ")

        match opcao:
            case '1':
                sobre_projeto()

            case '2':
                iniciar_trajeto()

            case '3':
                simular_pulseroute()

            case '4':
                historico_missoes()

            case '5':
                gerar_relatorio()

            case '6':
                while True:
                    try:
                        print('\nBem-vindo ao simulador de cálculo de tempo economizado com o PULSEROUTE.\n')
                        print('Esta opção calcula o ganho de eficiência de tempo (em minutos) gerado pela intervenção')
                        print('dos semáfotos inteligentes na rota da ambulância através do sistema.\n')
                        print('Para iniciar o cálculo, digite o tempo do trajeto em minutos (sem o PULSEROUTE): ')
                        temp = int(input(''))

                        if temp <= 0: # Se o usuário digitar um número menor ou igual a zero, ele terá que digitar novamente
                            entrada_invalida()
                        
                        else:
                            print('\nDigite a quantidade de semáforos para calcular o tempo otimizado com o PULSEROUTE')
                            print('(ou 0 para voltar ao menu principal): ')
                            quant = int(input(''))

                            if quant == 0: # Se ele digitar zero, ele voltará ao menu principal
                                break
                            
                            else:
                                economia = calculo_tempo(temp, quant) # Aqui a função calculo_tempo é chamada com o tempo e quantidade de semáforos determinada pelo usuário e recebe o resultado da economia e armazena nessa respectiva variável

                                print(f"\nTempo original (sem o PULSEROUTE): {temp:.2f} min")
                                print(f"Tempo do trajeto com o PULSEROUTE: {(temp-economia):.2f} min")
                                print(f"Tempo economizado com o PULSEROUTE: {economia:.2f} min")
                                
                                print('\nDeseja testar outra quantidade? \n')
                                
                                while True: # Verificação se o usuário deseja repetir essa funcionalidade novamente
                                    novamente = input('Digite: (s/n)\n')
                                    
                                    if novamente == 'n' or novamente == 's':
                                        break
                                    
                                    entrada_invalida()

                                if novamente == 'n':
                                    break
                    
                    except ValueError:
                        entrada_invalida()

            case '7':
                print('\nAgradecemos pela utilização do nosso sistema')
                print('Volte sempre!')
                break
            
            case _:
                print("\nOpção inválida!")
                print('Tente novamente!')

if __name__ == "__main__":
    main()