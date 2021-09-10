import pandas as pd


def indice_overall(row, index, indice):
    # Lotação
    if row.workplace == True:
        indice[index] += 1
    # Cargo
    if row.role == True:
        indice[index] += 1
    # Remuneração Básica
    if row.wage == True:
        indice[index] += 1
    # Detalhamento de Remuneração Eventual ou Temporária
    if (
        row.funds_eventual_benefits == True
        or row.funds_personal_benefits == True
        or row.funds_trust_position == True
        or row.funds_gratification == True
        or row.funds_daily == True
        or row.funds_origin_pos == True
        or row.funds_others_total == True
    ) and row.funds_total == True:
        indice[index] += 1
    elif row.funds_total == True:
        indice[index] += 0.5
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
        indice[index] += 1
    elif row.perks_total == True:
        indice[index] += 0.5
    # Detalhamento de Descontos
    if (
        row.discount_prev_contribution == True
        or row.discounts_ceil_retention == True
        or row.discounts_income_tax == True
    ) and row.discounts_total == True:
        indice[index] += 1
    elif row.discounts_total == True:
        indice[index] += 0.5

    return indice

# Mapeei meses em números para facilitar
indice_tj = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
indice_mp = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}

data_tj = pd.read_csv("../tjce-2020/data.csv")
grouped_data_tj = data_tj.groupby(by=["month"]).first()
data_mp = pd.read_csv("../mpce-2020/data.csv")
grouped_data_mp = data_mp.groupby(by=["month"]).first()

# Printa a o índice de transparência por mês
for row in grouped_data_tj.notna().itertuples():
    indice = indice_overall(row, row.Index, indice_tj)
print("TJCE: \n", indice)

for row in grouped_data_mp.notna().itertuples():
    indice = indice_overall(row, row.Index, indice_mp)
print("MPCE: \n", indice)
