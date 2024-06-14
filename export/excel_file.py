# Importando as bibliotecas necessárias:
import pandas as pd
import io


# Criando a função para exportar em Excel:
def convert_df_to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Divergências")
    return output.getvalue()
