# Importando as bibliotecas necessárias:
import pandas as pd
import io


# Criando a função para exportar em Excel:
def ConvertExcel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Divergências")
    return output.getvalue()


# Criando a função para exportar em CSV:
def ConvertCSV(df):
    output = io.StringIO()
    df.to_csv(output, index=False, sep=";")
    return output.getvalue().encode("utf-8")
