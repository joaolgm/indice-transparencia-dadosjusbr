import json


def calcula_indice(metadado):
    indice = 0

    # Se não precisa de login, ganha um ponto
    if metadado["has_login"] == False:
        indice += 1

    # Se não precisa de captha, ganha um ponto
    if metadado["has_captcha"] == False:
        indice += 1

    # Se a url é modicável via máquina, ganha um ponto
    if metadado["good_url"] == True:
        indice += 1

    # Se tem api para acessar os dados, ganha um ponto
    if metadado["data_access_option"] == 0:
        indice += 1
    # Se necessita de scraping, ganha meio ponto
    elif metadado["data_access_option"] == 1:
        indice += 0.5

    # Se o dado é disponibilizado em CSV ou ODF, ganha um ponto
    if metadado["output_format"] == 1 or metadado["output_format"] == 5:
        indice += 1

    # Se tem dado de Lotação, ganha um ponto
    if metadado["has_employee_workplace"] == True:
        indice += 1

    # Se tem dado de Cargo, ganha um ponto
    if metadado["has_employee_role"] == True:
        indice += 1

    # Se tem dado de Remuneração Básica, ganha um ponto
    if metadado["base_remuneration"] == True:
        indice += 1

    # Se só tem o dado total de Benefícios, ganha meio ponto
    if metadado["benefits"] == 1:
        indice += 0.5
    # Se detalha o dado de Benefícios, ganha um ponto
    elif metadado["benefits"] == 2:
        indice += 1

    # Se só tem o dado total de Descontos, ganha meio ponto
    if metadado["discounts"] == 1:
        indice += 0.5
    # Se detalha o dado de Discontos, ganha um ponto
    elif metadado["discounts"] == 2:
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
for i in metadado_path:
    with open(i) as json_file:
        data = json.load(json_file)
        indice = calcula_indice(data)
        pp = (
            "Indice de transparência do "
            + data["agency"]
            + " em 0"
            + str(data["month"])
            + "/"
            + str(data["year"])
            + ": "
            + str(indice)
        )
        print(pp)
