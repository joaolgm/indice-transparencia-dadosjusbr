import checa


def checa_completude(lista):

    retorno = []
    limiar_base = int(len(lista) * 0.2)
    limiar_teto = int(len(lista) * 0.8)

    retorno.append(checa_matricula(lista, limiar_base))
    retorno.append(checa_lotacao(lista, limiar_base))
    retorno.append(checa_cargo(lista, limiar_base))
    retorno.append(checa_remuneracao_base(lista, limiar_base))
    retorno.append(checa_outras_remuneracoes(lista, limiar_teto))
    retorno.append(checa_descontos(lista, limiar_teto))
    return retorno


def checa_matricula(valor, limiar_base):
    limiar = 0
    for row in valor.iterrows():
        if row[1].reg == None:
            limiar += 1
    if limiar >= limiar_base:
        return False
    else:
        return True


def checa_lotacao(valor, limiar_base):
    limiar = 0
    for row in valor.iterrows():
        if checa.validez(row[1].workplace) == False:
            limiar += 1
    if limiar >= limiar_base:
        return False
    else:
        return True


def checa_cargo(valor, limiar_base):
    limiar = 0
    for row in valor.iterrows():
        if checa.validez(row[1].role) == False:
            limiar += 1
    if limiar >= limiar_base:
        return False
    else:
        return True


def checa_remuneracao_base(valor, limiar_base):
    limiar = 0
    for row in valor.iterrows():
        if checa.validez(row[1].wage) == False:
            limiar += 1
    if limiar >= limiar_base:
        return False
    else:
        return True


def checa_outras_remuneracoes(valor, limiar_teto):
    limiar_sumarizado = 0
    limiar_detalhado = 0
    for row in valor.iterrows():
        if (
            checa.validez(row[1].perks_food) == True
            or checa.validez(row[1].perks_vacation) == True
            or checa.validez(row[1].perks_transportation) == True
            or checa.validez(row[1].perks_pre_school) == True
            or checa.validez(row[1].perks_health) == True
            or checa.validez(row[1].perks_birth) == True
            or checa.validez(row[1].perks_housing) == True
            or checa.validez(row[1].perks_subsistence) == True
            or checa.validez(row[1].perks_compensatory_leave) == True
            or checa.validez(row[1].perks_pecuniary) == True
            or checa.validez(row[1].perks_vacation_pecuniary) == True
            or checa.validez(row[1].perks_furniture_transport) == True
            or checa.validez(row[1].perks_premium_license_pecuniary) == True
        ) and checa.validez(row[1].perks_total) == True:
            limiar_detalhado += 1
        elif checa.validez(row[1].perks_total) == True:
            limiar_sumarizado += 1

    if (limiar_sumarizado <= limiar_teto) and (limiar_detalhado <= limiar_teto):
        return 0
    elif limiar_sumarizado >= limiar_detalhado:
        return 1
    else:
        return 2


def checa_descontos(valor, limiar_teto):
    limiar_sumarizado = 0
    limiar_detalhado = 0
    for row in valor.iterrows():
        if (
            checa.validez(row[1].discount_prev_contribution) == True
            or checa.validez(row[1].discounts_ceil_retention) == True
            or checa.validez(row[1].discounts_income_tax) == True
        ) and checa.validez(row[1].discounts_total) == True:
            limiar_detalhado += 1
        elif checa.validez(row[1].discounts_total) == True:
            limiar_sumarizado += 1

    if limiar_sumarizado < limiar_teto and limiar_detalhado < limiar_teto:
        return 0
    elif limiar_sumarizado >= limiar_detalhado:
        return 1
    else:
        return 2
