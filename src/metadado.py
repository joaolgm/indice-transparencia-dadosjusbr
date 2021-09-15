import pandas as pd
import json


class Metadado:

    has_employee_workplace = False
    has_employee_role = False
    base_remuneration = False
    benefits = 0
    discounts = 0

    def __init__(
        self,
        year,
        month,
        agency,
        has_login,
        has_captcha,
        good_url,
        data_access_option,
        output_format,
    ):
        self.year = year
        self.month = month
        self.agency = agency
        self.has_login = has_login
        self.has_captcha = has_captcha
        self.good_url = good_url
        self.data_access_option = data_access_option
        self.output_format = output_format

    def __repr__(self):
        return (
            "<Metadado: year:%s, month:%s, agency: %s, has_login:%s, has_captcha:%s, good_url: %s, data_access_option:%s, output_format:%s, has_employee_workplace: %s, has_employee_role:%s, base_remuneration: %s, benefits:%s, discounts:%s>"
            % (
                self.year,
                self.month,
                self.agency,
                self.has_login,
                self.has_captcha,
                self.good_url,
                self.data_access_option,
                self.output_format,
                self.has_employee_workplace,
                self.has_employee_role,
                self.base_remuneration,
                self.benefits,
                self.discounts,
            )
        )

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)


class DataAccessOption(Metadado):
    api = 0
    scraping = 1
    user_emulation = 2


class InfoCompletenessOptions(Metadado):
    absence = 0
    summary = 1
    details = 2


class OutputFormat(Metadado):
    pdf = 0
    odf = 1
    xls = 2
    json = 3
    html = 4
    csv = 5


def indice_overall(row, indice):
    # Lotação
    if row.workplace == True:
        indice.has_employee_workplace = True
    else:
        indice.has_employee_workplace = False
    # Cargo
    if row.role == True:
        indice.has_employee_role = True
    else:
        indice.has_employee_role = False
    # Remuneração Básica
    if row.wage == True:
        indice.base_remuneration = True
    else:

        indice.base_remuneration = False
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
        indice.benefits = InfoCompletenessOptions.details
    elif row.perks_total == True:
        indice.benefits = InfoCompletenessOptions.summary
    # Detalhamento de Descontos
    if (
        row.discount_prev_contribution == True
        or row.discounts_ceil_retention == True
        or row.discounts_income_tax == True
    ) and row.discounts_total == True:
        indice.discounts = InfoCompletenessOptions.details
    elif row.discounts_total == True:
        indice.discounts = InfoCompletenessOptions.summary

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
            False,
            False,
            False,
            DataAccessOption.user_emulation,
            OutputFormat.xls,
        )
        indice_mar = indice_overall(row, metaindice_mar)
        metadado = (
            "./output/metadado_"
            + indice_mar.agency
            + "_"
            + str(indice_mar.month)
            + "_"
            + str(indice_mar.year)
            + ".json"
        )
        with open(metadado, "w") as outfile:
            outfile.write(indice_mar.toJSON())
    elif row.Index == 4:
        metaindice_abr = Metadado(
            2020,
            4,
            "tjce",
            False,
            False,
            False,
            DataAccessOption.user_emulation,
            OutputFormat.xls,
        )
        indice_abr = indice_overall(row, metaindice_abr)
        metadado = (
            "./output/metadado_"
            + indice_abr.agency
            + "_"
            + str(indice_abr.month)
            + "_"
            + str(indice_abr.year)
            + ".json"
        )
        with open(metadado, "w") as outfile:
            outfile.write(indice_abr.toJSON())
    elif row.Index == 5:
        metaindice_mai = Metadado(
            2020,
            5,
            "tjce",
            False,
            False,
            False,
            DataAccessOption.user_emulation,
            OutputFormat.xls,
        )
        indice_mai = indice_overall(row, metaindice_mai)
        metadado = (
            "./output/metadado_"
            + indice_mai.agency
            + "_"
            + str(indice_mai.month)
            + "_"
            + str(indice_mai.year)
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
            False,
            False,
            False,
            DataAccessOption.scraping,
            OutputFormat.xls,
        )
        indice_mar = indice_overall(row, metaindice_mar)
        metadado = (
            "./output/metadado_"
            + indice_mar.agency
            + "_"
            + str(indice_mar.month)
            + "_"
            + str(indice_mar.year)
            + ".json"
        )
        with open(metadado, "w") as outfile:
            outfile.write(indice_mar.toJSON())
    elif row.Index == 4:
        metaindice_abr = Metadado(
            2020,
            4,
            "mpce",
            False,
            False,
            False,
            DataAccessOption.scraping,
            OutputFormat.xls,
        )
        indice_abr = indice_overall(row, metaindice_abr)
        metadado = (
            "./output/metadado_"
            + indice_abr.agency
            + "_"
            + str(indice_abr.month)
            + "_"
            + str(indice_abr.year)
            + ".json"
        )
        with open(metadado, "w") as outfile:
            outfile.write(indice_abr.toJSON())
    elif row.Index == 5:
        metaindice_mai = Metadado(
            2020,
            5,
            "mpce",
            False,
            False,
            False,
            DataAccessOption.scraping,
            OutputFormat.xls,
        )
        indice_mai = indice_overall(row, metaindice_mai)
        metadado = (
            "./output/metadado_"
            + indice_mai.agency
            + "_"
            + str(indice_mai.month)
            + "_"
            + str(indice_mai.year)
            + ".json"
        )
        with open(metadado, "w") as outfile:
            outfile.write(indice_mai.toJSON())
