from math import floor, ceil
from decimal import Decimal
import os

menu = 0
pacotes = []
contPacDia = 0
seguro = 0

veiculos = []

def msg(tMsg):
    match tMsg:
        case 'cont':
            return input("Pressione ENTER para continuar")


#classe de veículo
class Veiculo:
    identificador = 0
    nome = ''
    cargaMax = 0
    cargaUsada = 0
    volueMax = 0
    volumeUsado = 0
    tipo = ''
    totalPacotes = 0

    veicSelecionado = ''

    carga = []

    def __init__(self, nome, cargaMax, volumeMax, tipo, identificador) -> None:
        self.identificador = identificador
        self.cargaMax = cargaMax
        self.volueMax = volumeMax
        self.tipo = tipo
        self.nome = nome

    def coletarPacote(cargaMax, volumeMax, cargaUsada, volumeUsado, totalPacotes, carga):
        
        limparTela()
        pesoColeta = input("\nInforme o peso(Kg) do pacote coletado: ")
        while not pesoColeta.replace(".", "1").isdigit(): #Testando se valor é válido
            pesoColeta = input("Valor Inválido! Favor, informar o peso(Kg) do pacote coletado: ")
        if (cargaMax > (cargaUsada + float(pesoColeta))): #Testando se novo pacote exederá o peso máximo
            confValor = 0
            seguro = 0
            valorColeta = float(pesoColeta)*1.5
            
            #O valor do transporte do pacote será calculado de acordo com o peso. R$1,50 por kg.
            #Se o peso do pacote for 10* o volume do veículo, será cobrado R$0,80 por Kg excedente
            if (float(pesoColeta) > float(volumeMax) * 10):
                seguro = 0.8 * (float(pesoColeta) - (float(volumeMax) * 10))
                
            total = float(valorColeta) + float(seguro)

            print(f"Valor do transporte: R${float(valorColeta):,.2f}")
            print(f'Seguro: R${float(seguro):,.2f}')
            print(f'Total a Pagar: R${float(total):,.2f}')

            confValor = input("\nConfirma valor? S/N\n")
            while (confValor != "S" or confValor != "s" or confValor != "N" or confValor != "n"):
                if (confValor == "S" or confValor == "s"):
                    cargaUsada += float(pesoColeta)
                    pac = Pacote(contPacDia, pesoColeta, Decimal(float(pesoColeta)*1.5))
                    carga.append(pac)
                    totalPacotes+=1
                    volumeUsado+=1
                    print("Pacote incluído.")
                    break
                elif (confValor == "N" or confValor == "n"):
                    print("Valor não-aceito. Cancelando coleta.")
                    msg('cont')
                    break
                else:
                    confValor = input("Opção inválida. Confirma valor? S/N\n")

        else:
            print("\nPeso excederá capacidade do veículo. Cancelando coleta.\n")
            msg('cont')

    def entregarPacote(cargaMax, volumeMax, cargaUsada, volumeUsado, totalPacotes, carga):
        continuarEntrega = True
        print("Pacotes:\n")
        while continuarEntrega:                            
            for pac in carga:
                print(f"{pac.identificador + 1}- Peso: {pac.peso}kg")
            pacoteEntrega = input("Qual pacote deseja entregar?")
            if(not pacoteEntrega.isdigit() or pacoteEntrega > len(carga) + 1):
                print("Opção inválida! Informe um pacote a ser removido!")
            else:            
                for x in len(carga):
                    print(carga[x])
                    if(pacoteEntrega == carga[x].identificador):
                        entregaPacote = input("Deseja realmente remover o pacote? S/N")
                        match entregaPacote:
                            case "S","s":
                                carga.remove(pac)                                                
                                prosseguir = input("Pacote entregue!\nDeseja fazer mais uma entrega? S/N\n")
                                match prosseguir:
                                    case "S","s":
                                        print("Pacotes:")
                                    case "N","n":
                                        continuarEntrega = False
                                        print("Encerrando entregas")
                                        msg('cont')
                                        break
                                    case _:
                                        print("Opção Inválida!")
                                        msg('cont')
                            case "N","n":                                                
                                while (prosseguir != "S" or prosseguir != "s" or prosseguir != "N" or prosseguir != "n"):
                                    prosseguir = input("Deseja continuar a realizar entregas? S/N")
                                    match prosseguir:
                                        case 'S','s':
                                            break
                                        case 'N','n':
                                            limparTela()
                                            print('Encerrando entrega')
                                            msg('cont')
                                            break
                                        case _:
                                            limparTela()
                                            print('Opção inválida!')
                                            msg('cont')
#Classe de pacote individual
class Pacote:
    identificador = 0
    peso = 0
    valorUnit = 0

    def __init__(self, identificador, peso, valor) -> None: #função construtora
        self.identificador = identificador
        self.peso = peso
        self.valorUnit = valor

#função de limpar tela
def limparTela():
    os.system('cls' if os.name == 'nt' else 'clear')

def comecarDia(wheels):
    fimComecoDia = False
    if len(wheels) == 0:
        print("Nenhum veículo registrado! Redirecionando para Cadastro de Veículo Novo\n")
        msg('cont')
        registrar_veic()
    else:
        while(not fimComecoDia):
            limparTela()
            print("Selecione o veículo que deseja gerenciar:\n")
            counter = 1
            for vehi in wheels:
                print(f"\n{counter}- {vehi.nome}")
                counter+=1
            print(f"\n{counter}- Registrar Novo")
            opcaoComecarDia = int(input("Selecione a opção desejada:"))
            if counter == opcaoComecarDia:
                registrar_veic()
                fimComecoDia = True
            elif (opcaoComecarDia < counter and opcaoComecarDia >= 0):
                limparTela()
                print(f"{wheels[opcaoComecarDia-1].nome} foi selecionado!")
                msg('cont')
                fimComecoDia = True
            else:
                print("Opção Inválida!")
                msg('cont')


#função de início de dia
def registrar_veic():    
    cargaMax = 0
    volumeMax = 0
    limparTela()

    print("Cadastro do Veículo:")
    #Entrada de dado: capacidade de carga máxima
    cargaMax = input("Por Favor, informe a capacidade de carga máxima (Kg):\n")

    #Validar dado: capacidade de carga máxima - testando se o dado informado é um número e tratando para que seja float
    print(cargaMax.isdigit())
    if (str(cargaMax.replace(".","1")).isdigit()):
        cargaMax = float(cargaMax)
        # print(cargaMax, type(cargaMax))

    while not (str(cargaMax).replace(".", "1").isdigit() or type(cargaMax) != str):
        print(cargaMax)
        cargaMax = input("Valor inválido. Informe valor válido para capacidade de carga máxima (Kg):\n")
        if (str(cargaMax).replace(".","1").isdigit()):
            cargaMax = float(cargaMax)
            # print(cargaMax, type(cargaMax))
    

    #Entrada de dado: capacidade de volume máximo
    volumeMax = input("Agora, informe a capacidade de volume máxima (m³):\n")

    #Validar dado: capacidade de volume máximo - testando se o dado informado é um número e tratando para que seja int
    if (str(volumeMax).replace(".", "1").isdigit()):
        volumeMax = int(floor(float(volumeMax)))
        print(volumeMax, type(volumeMax))

    while not (str(volumeMax).replace(".", "1").isdigit()):
        volumeMax = input("Valor inválido. Informe valor válido para capacidade de volume máxima (m³):\n")
        if (str(volumeMax).isdigit()):
            volumeMax = int(floor(float(volumeMax)))
            print(volumeMax, type(volumeMax))
    print("\nDados do caminhão registrado!\nPeso máximo:", cargaMax,"kg\nVolume Máximo:", volumeMax,"m³\n\n")
    msg('cont')


#Laço de repetição do sistema. Ao encerrar o dia, usuário pode escolher reiniciar o sistema.
def sistema(veiculos):

    sisVeiculos = veiculos
    continuar = True

    while continuar:
        limparTela()
        #Mensagem de início
        print("Bem-vindo ao sistema de controle de carga!")
        #Menu de ações
        print("Ações Possíveis:\n",
            "1- Iniciar o Dia\n",
            "2- Realizar Parada\n",
            "3- Consultar Situação\n",
            "4- Mostrar Pacotes\n",
            "5- Encerrrar o Dia\n",
            "6- Gerar Relatório\n",
            "7- Encerrar o Sistema")
        menu = input("Informe sua opção: ")

        match menu:
            case "1": #Inicio do dia
                comecarDia(sisVeiculos)

            case "2": #Parada
                operacao = 0

                limparTela()

                while operacao != "c":
                    operacao = input("\nInforme a opção de parada:\na- Coletar Pacote\nb- Entregar Pacote\nc- Retomar Viagem\n\n")
                    match operacao: #Opções das ações de paradas
                        case "a": #Coletar pacote
                            coleta()

                        case "b":
                            entrega()

                        case "c":
                            limparTela()
                            print("Segue viagem")
                        case _:
                            limparTela()
                            print("Opção Inválida!")


            case "3": #consultar situação
                limparTela()
                print("Em Breve")

            case "4": #listar pacotes
                limparTela()
                print("Em Breve")

            case "5": #finalizar dia
                limparTela()
                print("Em Breve")

            case "6": #gerar relatório
                limparTela()
                print("Em Breve")

            case "7":
                limparTela()
                #Mensagem de encerramento
                opcao = input("Deseja realmente encerrar o programa? S/N\n")
                if (opcao == 'S' or opcao == 's'):
                    continuar = False

            case _:
                limparTela()
                print("\nOpção informada é inválida, favor, tentar novamente.\n")

#self, nome, cargaMax, volumeMax, tipo, identificador
# veiculos = [
#     Veiculo('Caminhão de Entrega', 200, 80, 'caminhão', 0),
#     Veiculo('Moto de Entrega', 20, 4, 'moto', 1),
#     Veiculo('Carro de Entrega', 50, 20, 'carro', 2)
# ]

sistema(veiculos)

#Fim do códgio