from math import floor, ceil
from decimal import Decimal

continuar = True
menu = 0
cargaMax = 800
cargaUsada = 0
volumeMax = 20
volumeUsado = 0
pacotes = []
contPacDia = 0
seguro = 0

#Classe de pacote individual
class Pacote:
    identificador = 0
    peso = 0
    valorUnit = 0

    def __init__(self, identificador, peso, valor) -> None:
        self.identificador = identificador
        self.peso = peso
        self.valorUnit = valor



#Mensagem de início
print("Bem-vindo ao sistema de controle de carga!")

#Laço de repetição do sistema. Ao encerrar o dia, usuário pode escolher reiniciar o sistema.
while continuar:
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

            cargaMax = 0
            volumeMax = 0

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

        case "2": #Parada
            operacao = 0

            while operacao != "c":

                operacao = input("\nInforme a opção de parada:\na- Coletar Pacote\nb- Entregar Pacote\nc- Retomar Viagem\n\n")
                match operacao: #Opções das ações de paradas
                    case "a": #Coletar pacote
                        
                        pesoColeta = input("\nInforme o peso(Kg) do pacote coletado: ")
                        if not pesoColeta.replace(".", "1").isdigit(): #Testando se valor é válido
                            pesoColeta = input("Valor inválido! Favor, informar o peso(Kg) do pacote coletado: ")
                            print(float(pesoColeta))
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
                                    pacotes.append(pac)
                                    contPacDia+=1
                                    print("Pacote incluído.")
                                    break
                                elif (confValor == "N" or confValor == "n"):
                                    print("Valor não-aceito. Cancelando coleta.")
                                    break
                                else:
                                    confValor = input("Opção inválida. Confirma valor? S/N\n")

                        else:
                            print("\nPeso excederá capacidade do veículo. Cancelando coleta.\n")

                    case "b":                        
                        continuarEntrega = True
                        pacoteEscolhido = 0
                        print("Pacotes:\n")
                        while continuarEntrega:                            
                            for pac in pacotes:
                                print(f"{pac.identificador + 1}- Peso: {pac.peso}kg")
                            pacoteEntrega = input("Qual pacote deseja entregar?")
                            if(not pacoteEntrega.isdigit()):
                                print("Opção inválida! Informe um pacote a ser removido!")
                            else:
                                index = 0
                                for pac in pacotes:
                                    print(pac)
                                    if(pacoteEntrega == pac.identificador):
                                        entregaPacote = input("Deseja realmente remover o pacote? S/N")
                                        match entregaPacote:
                                            case "S","s":
                                                pacotes.remove(pac)                                                
                                                prosseguir = input("Pacote entregue!\nDeseja fazer mais uma entrega? S/N\n")
                                                match prosseguir:
                                                    case "S","s":
                                                        print("Pacotes:")
                                                    case "N","n":
                                                        continuarEntrega = False
                                                        print("Encerrando entregas")
                                                    case _:
                                                        print("Opção Inválida!")
                                            case "N","n":
                                                prosseguir = input("Deseja continuar a realizar entregas? S/N")


                    case "c":
                        print("Segue viagem")
                    case _:
                        print("Opção Inválida!")


        case "3":
            print("Em Breve")

        case "4":
            print("Em Breve")

        case "5":
            print("Em Breve")

        case "6":
            print("Em Breve")

        case "7":
            #Mensagem de encerramento
            opcao = input("Deseja realmente encerrar o programa? S/N\n")
            if (opcao == 'S' or opcao == 's'):
                continuar = False

        case _:
            print("\nOpção informada é inválida, favor, tentar novamente.\n")

#Fim do códgio