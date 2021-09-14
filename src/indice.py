import pandas as pd


def indice_overall(row, indice):
    # Lotação
    if row.workplace == True:
        indice["HasEmployeeWorkplace"] = 1
    # Cargo
    if row.role == True:
        indice["HasEmployeeRole"] = 1
    # Remuneração Básica
    if row.wage == True:
        indice["BaseRemuneration"] = 1
    # Detalhamento de Indenizações
    if (
        row.perks_food == True
        or row.perks_vacation == True
        or row.perks_transportation
        or row.perks_pre_school == True
        or row.perks_health == True
        or row.perks_birth == True
        or row.perks_housing == True
        or row.perks_subsistence == True
        or row.perks_compensatory_leave == True
        or row.perks_pecuniary == True
        or row.perks_vacation_pecuniary == True
        or row.perks_furniture_transport == True
        or row.perks_premium_license_pecuniary == True
    ) and row.perks_total == True:
        indice["Benefits"] = 2
    elif row.perks_total == True:
        indice["Benefits"] = 1
    # Detalhamento de Descontos
    if (
        row.discount_prev_contribution == True
        or row.discounts_ceil_retention == True
        or row.discounts_income_tax == True
    ) and row.discounts_total == True:
        indice["Discounts"] = 2
    elif row.discounts_total == True:
        indice["Discounts"] = 1

    return indice


# Para efeito de teste, AGENCYID ainda se repete para todos os meses
metaindice = {
    "Year": 2020,
    "Month": 1,
    "AgencyID": "60620ad4a09c6aa6f8a3dd86",
    "HasLogin": False,
    "HasCaptcha": False,
    "IsURLGood": False,
    "OutputFormat": 2,
    "DataAccess": 1,
    "HasEmployeeRole": 0,
    "HasEmployeeWorkplace": 0,
    "BaseRemuneration": 0,
    "Benefits": 0,
    "Discounts": 0,
}

data_tj = pd.read_csv("./tjce-2020/data.csv")
grouped_data_tj = data_tj.groupby(by=["month"]).first()
data_mp = pd.read_csv("./mpce-2020/data.csv")
grouped_data_mp = data_mp.groupby(by=["month"]).first()


# Utilizei 3 meses como exemplo
for row in grouped_data_tj.notna().itertuples():
    if row.Index == 3:
        indice_mar = indice_overall(row, metaindice)
        print("\n TJCE - MARÇO: \n", indice_mar)
    elif row.Index == 4:
        indice_abr = indice_overall(row, metaindice)
        print("\n TJCE - ABRIL: \n", indice_abr)
    elif row.Index == 5:
        indice_mai = indice_overall(row, metaindice)
        print("\n TJCE - MAIO: \n", indice_mai)

for row in grouped_data_mp.notna().itertuples():
    if row.Index == 3:
        indice_mar = indice_overall(row, metaindice)
        print("\n MPCE - MARÇO: \n", indice_mar)
    elif row.Index == 4:
        indice_abr = indice_overall(row, metaindice)
        print("\n MPCE - ABRIL: \n", indice_abr)
    elif row.Index == 5:
        indice_mai = indice_overall(row, metaindice)
        print("\n MPCE - MAIO: \n", indice_mai)
