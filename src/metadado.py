import pandas as pd
import json


class Metadado:

    tem_matricula = False
    tem_lotacao = False
    tem_cargo = False
    remuneracao_base = False
    outras_remuneracoes = 0
    descontos = 0

    def __init__(
        self,
        ano,
        mes,
        id_orgao,
        nao_requer_login,
        nao_requer_captcha,
        acesso_ao_dado,
        extensao,
        estritamente_tabular
    ):
        self.ano = ano
        self.mes = mes
        self.id_orgao = id_orgao
        self.nao_requer_login = nao_requer_login
        self.nao_requer_captcha = nao_requer_captcha
        self.acesso_ao_dado = acesso_ao_dado
        self.extensao = extensao
        self.estritamente_tabular = estritamente_tabular

    def __repr__(self):
        return (
            "<Metadado: ano: %s, mes: %s, id_orgao: %s, nao_requer_login: %s, nao_requer_captcha: %s, acesso_ao_dado: %s, extensao: %s, estritamente_tabular: %s, tem_matricula: %s, tem_lotacao: %s, tem_cargo: %s, remuneracao_base: %s, outras_remuneracoes: %s, descontos: %s>"
            % (
                self.ano,
                self.mes,
                self.id_orgao,
                self.nao_requer_login,
                self.nao_requer_captcha,
                self.acesso_ao_dado,
                self.extensao,
                self.estritamente_tabular,
                self.tem_matricula,
                self.tem_lotacao,
                self.tem_cargo,
                self.remuneracao_base,
                self.outras_remuneracoes,
                self.descontos,
            )
        )

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)


class FormaDeAcesso(Metadado):
    ACESSO_DIRETO = 0
    AMIGAVEL_PARA_RASPAGEM = 1
    RASPAGEM_DIFICULTADA = 2
    NECESSITA_SIMULACAO_USUARIO = 3


class OpcoesDetalhamento(Metadado):
    AUSENCIA = 0
    SUMARIZADO = 1
    DETALHADO = 2


class Extensao(Metadado):
    PDF = 0
    ODS = 1
    XLS = 2
    JSON = 3
    CSV = 4


def indice_overall(row, indice):
    # Matrícula
    if row.reg == True:
        indice.tem_matricula = True
    else:
        indice.tem_matricula = False
    # Lotação
    if row.workplace == True:
        indice.tem_lotacao = True
    else:
        indice.tem_lotacao = False
    # Cargo
    if row.role == True:
        indice.tem_cargo = True
    else:
        indice.tem_cargo = False
    # Remuneração Básica
    if row.wage == True:
        indice.remuneracao_base = True
    else:

        indice.remuneracao_base = False
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
        indice.outras_remuneracoes = OpcoesDetalhamento.DETALHADO
    elif row.perks_total == True:
        indice.outras_remuneracoes = OpcoesDetalhamento.SUMARIZADO
    # Detalhamento de Descontos
    if (
        row.discount_prev_contribution == True
        or row.discounts_ceil_retention == True
        or row.discounts_income_tax == True
    ) and row.discounts_total == True:
        indice.descontos = OpcoesDetalhamento.DETALHADO
    elif row.discounts_total == True:
        indice.descontos = OpcoesDetalhamento.SUMARIZADO

    return indice


data_tj = pd.read_csv("./data/tjce-2020/data.csv")
grouped_data_tj = data_tj.groupby(by=["month"]).first()
data_mp = pd.read_csv("./data/mpce-2020/data.csv")
grouped_data_mp = data_mp.groupby(by=["month"]).first()


# Utilizei 3 meses como exemplo
for row in grouped_data_tj.notna().itertuples():
    if row.Index == 3:
        metaindice_mar = Metadado(
            2020,
            3,
            "tjce",
            True,
            True,
            FormaDeAcesso.NECESSITA_SIMULACAO_USUARIO,
            Extensao.XLS,
            False
        )
        indice_mar = indice_overall(row, metaindice_mar)
        metadado = (
            "./output/metadado_"
            + indice_mar.id_orgao
            + "_"
            + str(indice_mar.mes)
            + "_"
            + str(indice_mar.ano)
            + ".json"
        )
        with open(metadado, "w") as outfile:
            outfile.write(indice_mar.toJSON())
    elif row.Index == 4:
        metaindice_abr = Metadado(
            2020,
            4,
            "tjce",
            True,
            True,
            FormaDeAcesso.NECESSITA_SIMULACAO_USUARIO,
            Extensao.XLS,
            False
        )
        indice_abr = indice_overall(row, metaindice_abr)
        metadado = (
            "./output/metadado_"
            + indice_abr.id_orgao
            + "_"
            + str(indice_abr.mes)
            + "_"
            + str(indice_abr.ano)
            + ".json"
        )
        with open(metadado, "w") as outfile:
            outfile.write(indice_abr.toJSON())
    elif row.Index == 5:
        metaindice_mai = Metadado(
            2020,
            5,
            "tjce",
            True,
            True,
            FormaDeAcesso.NECESSITA_SIMULACAO_USUARIO,
            Extensao.XLS,
            False
        )
        indice_mai = indice_overall(row, metaindice_mai)
        metadado = (
            "./output/metadado_"
            + indice_mai.id_orgao
            + "_"
            + str(indice_mai.mes)
            + "_"
            + str(indice_mai.ano)
            + ".json"
        )
        with open(metadado, "w") as outfile:
            outfile.write(indice_mai.toJSON())

for row in grouped_data_mp.notna().itertuples():
    if row.Index == 3:
        metaindice_mar = Metadado(
            2020,
            3,
            "mpce",
            True,
            True,
            FormaDeAcesso.AMIGAVEL_PARA_RASPAGEM,
            Extensao.XLS,
            False
        )
        indice_mar = indice_overall(row, metaindice_mar)
        metadado = (
            "./output/metadado_"
            + indice_mar.id_orgao
            + "_"
            + str(indice_mar.mes)
            + "_"
            + str(indice_mar.ano)
            + ".json"
        )
        with open(metadado, "w") as outfile:
            outfile.write(indice_mar.toJSON())
    elif row.Index == 4:
        metaindice_abr = Metadado(
            2020,
            4,
            "mpce",
            True,
            True,
            FormaDeAcesso.AMIGAVEL_PARA_RASPAGEM,
            Extensao.XLS,
            False
        )
        indice_abr = indice_overall(row, metaindice_abr)
        metadado = (
            "./output/metadado_"
            + indice_abr.id_orgao
            + "_"
            + str(indice_abr.mes)
            + "_"
            + str(indice_abr.ano)
            + ".json"
        )
        with open(metadado, "w") as outfile:
            outfile.write(indice_abr.toJSON())
    elif row.Index == 5:
        metaindice_mai = Metadado(
            2020,
            5,
            "mpce",
            True,
            True,
            FormaDeAcesso.AMIGAVEL_PARA_RASPAGEM,
            Extensao.XLS,
            False
        )
        indice_mai = indice_overall(row, metaindice_mai)
        metadado = (
            "./output/metadado_"
            + indice_mai.id_orgao
            + "_"
            + str(indice_mai.mes)
            + "_"
            + str(indice_mai.ano)
            + ".json"
        )
        with open(metadado, "w") as outfile:
            outfile.write(indice_mai.toJSON())
