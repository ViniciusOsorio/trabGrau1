from math import floor, ceil

continuar = True
menu = 0
cargaMax = 0
volumeMax = 0

#Mensagem de início
print("Bem-vindo ao sistema de controle de carga!")

#Laço de repetição do sistema. Ao encerrar o dia, usuário pode escolher reiniciar o sistema.
while continuar:
    #Menu de ações
    print("Ações Possíveis:")
    print("\n1- Iniciar o Dia\n2- Realizar Parada\n3- Consultar Situação\n4- Mostrar Pacotes\n5- Encerrrar o Dia\n6- Gerar Relatório\n7- Encerrar o Sistema")
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
                print(cargaMax, type(cargaMax))

            while not (str(cargaMax).replace(".", "1").isdigit() or type(cargaMax) != str):
                print(cargaMax)
                cargaMax = input("Valor inválido. Informe valor válido para capacidade de carga máxima (Kg):\n")
                if (str(cargaMax).replace(".","1").isdigit()):
                    cargaMax = float(cargaMax)
                    print(cargaMax, type(cargaMax))
            

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

        case "2":
            print("Em Breve")

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