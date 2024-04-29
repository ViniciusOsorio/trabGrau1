from math import floor, ceil
from decimal import Decimal
import os

menu = 0
pacotes = []
contPacDia = 0
seguro = 0

veiculos = []

#classe de veículo
class Veiculo:
    identificador = 0
    nome = ''
    cargaMax = 0
    cargaUsada = 0
    volumeMax = 0
    volumeUsado = 0
    tipo = ''
    totalPacotes = 0
    totalEntregas = 0
    totalValor = 0
    totalCarga = 0
    maiorValor = 0
    valorCargaAtu = 0

    carga = []

    def __init__(self, nome, cargaMax, volumeMax, tipo, identificador, carga) -> None:
        self.identificador = identificador
        self.cargaMax = cargaMax
        self.volumeMax = volumeMax
        self.tipo = tipo
        self.nome = nome
        self.carga = carga
        if(len(carga) > 0):
            self.totalPacotes = len(carga)
            for pac in carga:
                self.cargaUsada+=pac.peso
                self.totalCarga+=pac.peso
                self.totalPacotes+=1
                self.totalValor+=pac.valorUnit
                self.valorCargaAtu+=pac.valorUnit
                if(pac.valorUnit > self.maiorValor):
                    self.maiorValor = pac.valorUnit

    def coletarPacote(self):
        
        limparTela()
        pesoColeta = input("\nInforme o peso(Kg) do pacote coletado: ")
        while not pesoColeta.replace(".", "1").isdigit(): #Testando se valor é válido
            pesoColeta = input("Valor Inválido! Favor, informar o peso(Kg) do pacote coletado: ")
        if (self.cargaMax > (self.cargaUsada + float(pesoColeta))): #Testando se novo pacote exederá o peso máximo
            confValor = 0
            seguro = 0
            valorColeta = float(pesoColeta)*1.5
            
            #O valor do transporte do pacote será calculado de acordo com o peso. R$1,50 por kg.
            #Se o peso do pacote for 10* o volume do veículo, será cobrado R$0,80 por Kg excedente
            if (float(pesoColeta) > (float(self.volumeMax) * 10)):
                print(f"{float(pesoColeta)} > {float(self.volumeMax) * 10} = {float(pesoColeta) > (float(self.volumeMax) * 10)}")
                seguro = 0.8 * (float(pesoColeta) - (float(self.volumeMax) * 10))
                
            total = float(valorColeta) + float(seguro)

            print(f"Valor do transporte: R${float(valorColeta):,.2f}")
            print(f'Seguro: R${float(seguro):,.2f}')
            print(f'Total a Pagar: R${float(total):,.2f}')

            confValor = input("\nConfirma valor? S/N\n")
            while (confValor != "S" or confValor != "s" or confValor != "N" or confValor != "n"):
                if (confValor == "S" or confValor == "s"):
                    self.cargaUsada+=float(pesoColeta)
                    self.totalCarga+=float(pesoColeta)
                    self.carga.append(Pacote(self.totalPacotes, pesoColeta, Decimal(float(pesoColeta)*1.5)))
                    self.totalPacotes+=1
                    self.volumeUsado+=1
                    self.valorCargaAtu+=float(total)
                    self.totalValor+=float(total)
                    if float(total) > float(self.maiorValor):
                        self.maiorValor = float(total)
                    print("Pacote incluído.")
                    break
                elif (confValor == "N" or confValor == "n"):
                    print("Valor não-aceito. Cancelando coleta.")
                    input("Pressione ENTER para continuar")
                    break
                else:
                    confValor = input("Opção inválida. Confirma valor? S/N\n")

        else:
            print("\nPeso excederá capacidade do veículo. Cancelando coleta.\n")
            input("Pressione ENTER para continuar")

    def entregarPacote(self):
        limparTela()
        continuarEntrega = True
        print("Pacotes:\n")
        while continuarEntrega:
            ind = 0
            for pac in self.carga:
                ind+=1
                print(f"{ind}- Peso: {pac.peso}kg")
            pacoteEntrega = input("\nQual pacote deseja entregar?\n")
            pacoteEntrega = int(pacoteEntrega)-1
            if(not str(pacoteEntrega).isdigit() or int(pacoteEntrega) > len(self.carga) or int(pacoteEntrega) < 0):
                print("Opção inválida! Informe um pacote a ser removido!")
            else:
                confirmaEntrega = input("\nDeseja realmente remover o pacote? S/N\n")
                match confirmaEntrega:
                    case "S"|"s":
                        self.carga.pop(int(pacoteEntrega))
                        self.volumeUsado-=1
                        self.valorCargaAtu-=float(self.carga[int(pacoteEntrega)].valorUnit)
                        self.cargaUsada-=float(self.carga[int(pacoteEntrega)].peso)
                        print("Pacote entregue!\n")
                        input("Pressione ENTER para continuar")
                        limparTela()
                        prosseguir = 0
                        if(len(self.carga) > 0):
                            while (prosseguir != "S" or prosseguir != "s" or prosseguir != "N" or prosseguir != "n"):
                                prosseguir = input("Deseja fazer mais uma entrega? S/N\n")
                                match prosseguir:
                                    case "S"|"s":
                                        print("Pacotes:")
                                        break
                                    case "N"|"n":
                                        continuarEntrega = False
                                        print("Encerrando entregas")
                                        input("Pressione ENTER para continuar")
                                        break
                                    case _:
                                        print("Opção Inválida!")
                                        input("Pressione ENTER para continuar")
                        else:
                            print("Sem mais pacotes para entregar!")
                            input("Pressione ENTER para continuar")
                            continuarEntrega = False

                    case "N"|"n":
                        while (continuarEntrega):
                            prosseguir2 = input("Deseja continuar a realizar entregas? S/N\n")
                            match prosseguir2:
                                case 'S'|'s':
                                    break
                                case 'N'|'n':
                                    limparTela()
                                    print('Encerrando entrega')
                                    input("Pressione ENTER para continuar")
                                    continuarEntrega = False
                                    break
                                case _:
                                    limparTela()
                                    print('Opção inválida!')
                                    input("Pressione ENTER para continuar")                

    def consultarSit(self):
        print(f"Dados Atuais (Veículo: {self.nome})\n")
        print(f"Informações de Peso:\n- Total de Peso do Dia: {float(self.totalCarga)}kg\n- Peso Em Transporte: {float(self.cargaUsada)}kg\nPeso Máximo: {float(self.cargaMax)}kg\n\n")
        print(f"Informações de Pacotes:\n- Total de Pacotes do Dia: {self.totalPacotes}\n- Pacotes Em Transporte: {len(self.carga)}\nMáximo de Pacotes: {self.volumeMax}\n\n")
        print(f"Informações de Valores:\n- Total do Dia: R${float(self.totalValor):,.2f}\n- Total Em Transporte: R${float(self.valorCargaAtu):,.2f}\nMaior Valor do Dia: R${float(self.maiorValor):,.2f}\n\n")
        input("Pressione ENTER para sair")


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
        limparTela()
        print("Nenhum veículo registrado! Redirecionando para Cadastro de Veículo Novo\n")
        input("Pressione ENTER para continuar")
        return registrar_veic(wheels)
    else:
        while(not fimComecoDia):
            limparTela()
            print("Selecione o veículo que deseja gerenciar:\n")
            counter = 1
            for vehi in wheels:
                print(f"\n{counter}- {vehi.nome}")
                counter+=1
            print(f"\n{counter}- Registrar Novo\n")
            opcaoComecarDia = int(input("Selecione a opção desejada:\n"))
            if counter == opcaoComecarDia:
                fimComecoDia = True
                return registrar_veic(wheels)
            elif (opcaoComecarDia < counter and opcaoComecarDia >= 0):
                limparTela()
                print(f"{wheels[opcaoComecarDia-1].nome} foi selecionado!")
                input("Pressione ENTER para continuar")
                fimComecoDia = True
                return wheels[opcaoComecarDia-1]
            else:
                print("Opção Inválida!")
                input("Pressione ENTER para continuar")


#função de início de dia
def registrar_veic(wheels):    
    cargaMax = 0
    volumeMax = 0
    limparTela()

    print("Cadastro do Veículo:")
    #Entrada de dado: capacidade de carga máxima

    nome = input("Informe o nome do veículo:\n")

    cargaMax = input("\nInforme a capacidade de carga máxima (Kg):\n")

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
    volumeMax = input("\nAgora, informe a capacidade de volume máxima (m³):\n")

    #Validar dado: capacidade de volume máximo - testando se o dado informado é um número e tratando para que seja int
    if (str(volumeMax).replace(".", "1").isdigit()):
        volumeMax = int(floor(float(volumeMax)))
        print(volumeMax, type(volumeMax))

    while not (str(volumeMax).replace(".", "1").isdigit()):
        volumeMax = input("Valor inválido. Informe valor válido para capacidade de volume máxima (m³):\n")
        if (str(volumeMax).isdigit()):
            volumeMax = int(floor(float(volumeMax)))
            print(volumeMax, type(volumeMax))
    
    tipo = input("Informe o tipo de veículo:\n")

    print(f"\nVeículo registrado!\n\n")
    input("Pressione ENTER para continuar")

    return Veiculo(nome, cargaMax, volumeMax, tipo, len(wheels), [])


#Laço de repetição do sistema. Ao encerrar o dia, usuário pode escolher reiniciar o sistema.
def sistema(veiculos):

    sisVeiculos = veiculos
    continuar = True
    veiSelecionado = 0

    while continuar:
        limparTela()
        #Mensagem de início
        print("Bem-vindo ao sistema de controle de carga!")
        if (veiSelecionado == 0):
            print("Vamos selecionar o veículo para começar o dia!")
            input("Pressione ENTER para continuar")
            veiSelecionado = comecarDia(sisVeiculos)
            sisVeiculos.append(veiSelecionado)
        else:            
            #Menu de ações
            print(f"{veiSelecionado.identificador}- {veiSelecionado.nome}\nCapacidade (kg): {veiSelecionado.cargaMax}\nCapacidade (m³): {veiSelecionado.volumeMax}")
            print("Ações Possíveis:\n",
                "1- Mudar veículo\n",
                "2- Realizar Parada\n",
                "3- Consultar Situação\n",
                "4- Mostrar Pacotes\n",
                "5- Encerrrar o Dia\n",
                "6- Gerar Relatório\n",
                "7- Encerrar o Sistema")
            menu = input("Informe sua opção: ")

            match menu:
                case "1": #Inicio do dia
                    veiSelecionado = comecarDia(sisVeiculos)
                    sisVeiculos.append(veiSelecionado)

                case "2": #Parada
                    operacao = 0

                    while (operacao != "c" and operacao != "C"):                        
                        limparTela()
                        operacao = input("\nInforme a opção de parada:\na- Coletar Pacote\nb- Entregar Pacote\nc- Retomar Viagem\n\n")
                        match operacao: #Opções das ações de paradas
                            case "A"|"a": #Coletar pacote
                                # coleta()
                                veiSelecionado.coletarPacote()

                            case "B"|"b":
                                # entrega()
                                if(int(len(veiSelecionado.carga)) > 0):
                                    veiSelecionado.entregarPacote()
                                else:
                                    limparTela()
                                    print("Veículo não possui carga.")
                                    input("Pressione ENTER para continuar")

                            case "C"|"c":
                                limparTela()
                                print("Segue viagem")
                                input("Pressione ENTER para continuar")
                            case _:
                                limparTela()
                                print("Opção Inválida!")
                                input("Pressione ENTER para continuar")


                case "3": #consultar situação
                    limparTela()
                    veiSelecionado.consultarSit()

                case "4": #listar pacotes
                    limparTela()
                    # for x in veiSelecionado.carga:
                    print(veiSelecionado.carga)
                    input("ENTER")

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
veiculos = [
    Veiculo('Caminhão de Entrega', 200, 80, 'caminhão', 0, [Pacote(0, 20, 30), Pacote(1, 10, 15)]),
#     Veiculo('Moto de Entrega', 20, 4, 'moto', 1, []),
#     Veiculo('Carro de Entrega', 50, 20, 'carro', 2, [])
]

sistema(veiculos)

#Fim do códgio