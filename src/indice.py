import json


def calcula_indice(metadado):
    indice = 0

    # Se não precisa de login, ganha um ponto
    if metadado["nao_requer_login"] == True:
        indice += 1

    # Se não precisa de captha, ganha um ponto
    if metadado["nao_requer_captcha"] == True:
        indice += 1

    # Se tem api para acessar os dados, ganha um ponto
    if metadado["acesso_ao_dado"] == 0:
        indice += 1
    # Se necessita de scraping, ganha meio ponto
    elif metadado["acesso_ao_dado"] == 1:
        indice += 0.5

    # Se tem dado de Matrícula, ganha um ponto
    if metadado["tem_matricula"] == True:
        indice += 1

    # Se tem dado de Lotação, ganha um ponto
    if metadado["tem_lotacao"] == True:
        indice += 1

    # Se tem dado de Cargo, ganha um ponto
    if metadado["tem_cargo"] == True:
        indice += 1

    # Se tem dado de Remuneração Básica, ganha um ponto
    if metadado["remuneracao_base"] == True:
        indice += 1

    # Se só tem o dado total de Benefícios, ganha meio ponto
    if metadado["outras_remuneracoes"] == 1:
        indice += 0.5
    # Se detalha o dado de Benefícios, ganha um ponto
    elif metadado["outras_remuneracoes"] == 2:
        indice += 1

    # Se só tem o dado total de Descontos, ganha meio ponto
    if metadado["descontos"] == 1:
        indice += 0.5
    # Se detalha o dado de Discontos, ganha um ponto
    elif metadado["descontos"] == 2:
        indice += 1
    
    # Se o dado é estritamente tabular, ganha um ponto
    if metadado["estritamente_tabular"] == True:
        indice += 1

    return indice


metadado_path = [
    "./output/metadado_mpce_3_2020.json",
    "./output/metadado_mpce_4_2020.json",
    "./output/metadado_mpce_5_2020.json",
    "./output/metadado_tjce_3_2020.json",
    "./output/metadado_tjce_4_2020.json",
    "./output/metadado_tjce_5_2020.json",
]
indice_maximo = 10  # Máximo de pontos que um órgão pode atingir
for i in metadado_path:
    with open(i) as json_file:
        data = json.load(json_file)
        indice = (calcula_indice(data) / indice_maximo) * 100
        pp = (
            "Indice de transparência do "
            + data["id_orgao"]
            + " em 0"
            + str(data["mes"])
            + "/"
            + str(data["ano"])
            + ": "
            + str(indice)
            + "%"
        )
        print(pp)
