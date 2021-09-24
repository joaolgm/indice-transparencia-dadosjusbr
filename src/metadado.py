import pandas as pd
import json
import checa
import completude


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
        estritamente_tabular,
        formato_consistente,
    ):
        self.ano = ano
        self.mes = mes
        self.id_orgao = id_orgao
        self.nao_requer_login = nao_requer_login
        self.nao_requer_captcha = nao_requer_captcha
        self.acesso_ao_dado = acesso_ao_dado
        self.extensao = extensao
        self.estritamente_tabular = estritamente_tabular
        self.formato_consistente = formato_consistente

    def __repr__(self):
        return (
            "<Metadado: ano: %s, mes: %s, id_orgao: %s, nao_requer_login: %s, nao_requer_captcha: %s, acesso_ao_dado: %s, extensao: %s, estritamente_tabular: %s, formato_consistente: %s, tem_matricula: %s, tem_lotacao: %s, tem_cargo: %s, remuneracao_base: %s, outras_remuneracoes: %s, descontos: %s>"
            % (
                self.ano,
                self.mes,
                self.id_orgao,
                self.nao_requer_login,
                self.nao_requer_captcha,
                self.acesso_ao_dado,
                self.extensao,
                self.estritamente_tabular,
                self.formato_consistente,
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


def map_indice(metaindice, resumo):
    metaindice.tem_matricula = resumo[0]
    metaindice.tem_lotacao = resumo[1]
    metaindice.tem_cargo = resumo[2]
    metaindice.remuneracao_base = resumo[3]

    if resumo[4] == 0:
        metaindice.outras_remuneracoes = OpcoesDetalhamento.AUSENCIA
    elif resumo[4] == 1:
        metaindice.outras_remuneracoes = OpcoesDetalhamento.SUMARIZADO
    else:
        metaindice.outras_remuneracoes = OpcoesDetalhamento.DETALHADO

    if resumo[5] == 0:
        metaindice.descontos = OpcoesDetalhamento.AUSENCIA
    elif resumo[5] == 1:
        metaindice.descontos = OpcoesDetalhamento.SUMARIZADO
    else:
        metaindice.descontos = OpcoesDetalhamento.DETALHADO


data_tj = pd.read_csv("./data/tjce-2020/data.csv")
grouped_data_tj = data_tj.groupby(by=["month"]).first()
data_mp = pd.read_csv("./data/mpce-2020/data.csv")
grouped_data_mp = data_mp.groupby(by=["month"]).first()
data_mpto = pd.read_csv("./data/mpto-2019/data.csv")
grouped_data_mpto = data_mpto.groupby(by=["month"]).first()
data_tjpr = pd.read_csv("./data/tjpr-2019/data.csv")
grouped_data_tjpr = data_tjpr.groupby(by=["month"]).first()

data_checa_completude_mpto = data_mpto.groupby(by=["month"])
completude_metaindice_mpto = []

for data in data_checa_completude_mpto:
    completude_metaindice_mpto.append(completude.checa_completude(data[1]))

for index, row in grouped_data_mpto.iterrows():

    metaindice = Metadado(
        2019,
        index,
        "mpto",
        True,
        True,
        FormaDeAcesso.RASPAGEM_DIFICULTADA,
        Extensao.XLS,
        False,
        False,
    )
    map_indice(metaindice, completude_metaindice_mpto[index - 1])
    metadado = (
        "./output/metadado_"
        + metaindice.id_orgao
        + "_"
        + str(metaindice.mes)
        + "_"
        + str(metaindice.ano)
        + ".json"
    )
    with open(metadado, "w") as outfile:
        outfile.write(metaindice.toJSON())


data_checa_completude_tjpr = data_tjpr.groupby(by=["month"])
completude_metaindice_tjpr = []

for data in data_checa_completude_tjpr:
    completude_metaindice_tjpr.append(completude.checa_completude(data[1]))

for index, row in grouped_data_tjpr.iterrows():

    metaindice = Metadado(
        2019,
        index,
        "tjpr",
        True,
        True,
        FormaDeAcesso.NECESSITA_SIMULACAO_USUARIO,
        Extensao.XLS,
        True,
        True,
    )
    map_indice(metaindice, completude_metaindice_tjpr[index - 1])
    metadado = (
        "./output/metadado_"
        + metaindice.id_orgao
        + "_"
        + str(metaindice.mes)
        + "_"
        + str(metaindice.ano)
        + ".json"
    )
    with open(metadado, "w") as outfile:
        outfile.write(metaindice.toJSON())
