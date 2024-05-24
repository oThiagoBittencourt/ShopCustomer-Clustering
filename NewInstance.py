import pandas as pd
from pickle import load

def new_instance(gender:str, age:int, annualIncome:int, spendingScore:int, profession:str, workExperience:int, familySize:int):
    shop_customers_cluster_model = load(open("Training/Models/shop_customers_clusters_2024.pkl", "rb"))
    colunas_categoricas = pd.read_pickle("Training/Models/colunas_categoricas.pkl")
    normalizador = load(open("Training/Models/Normalizer.pkl", "rb"))
    dados_categoricos_base = pd.DataFrame(columns=colunas_categoricas)

    df_base = pd.DataFrame([[gender, age, annualIncome, spendingScore, profession, workExperience, familySize]], columns=['Gender', 'Age', 'AnnualIncome', 'SpendingScore', 'Profession', 'WorkExperience', 'FamilySize'])

    # SEPARAÇÃO DOS DATAFRAMES
    dados_numericos = df_base[['Age', 'AnnualIncome', 'SpendingScore', 'WorkExperience', 'FamilySize']]
    dados_categoricos = df_base[['Gender', 'Profession']]

    # NORMALIZAÇÃO DOS DADOS CATEGÓRICOS
    dados_categoricos_normalizados = pd.get_dummies(data=dados_categoricos, prefix_sep='_', dtype=int)

    # NORMALIZAÇÃO DOS DADOS NUMÉRICOS
    dados_numericos_normalizados = normalizador.transform(dados_numericos)
    dados_numericos_normalizados = pd.DataFrame(data = dados_numericos_normalizados, columns=['Age', 'AnnualIncome', 'SpendingScore', 'WorkExperience', 'FamilySize'])

    # JUNÇÃO DOS DADOS NORMALIZADOS COM A BASE DE COLUNAS
    dados_completos = pd.concat([dados_categoricos_base, dados_categoricos_normalizados], axis=0)
    dados_completos = dados_completos.where(pd.notna(dados_completos), other=0)
    dados_completos = dados_numericos_normalizados.join(dados_completos, how='left')

    # EXECUÇÃO DO PREDICT
    predict = shop_customers_cluster_model.predict(dados_completos)
    centroide = shop_customers_cluster_model.cluster_centers_[shop_customers_cluster_model.predict(dados_completos)]

    print("\n### DADOS TÉCNICOS ###")
    print(f"Índice do grupo da nova instância: {predict}")
    print(f"Centroide da nova instância: {centroide}")

    centroide_list = list(centroide[0])

    # Dados Numéricos Centroide
    centroide_numericos = centroide_list[0], centroide_list[1], centroide_list[2], centroide_list[3], centroide_list[4]
    dados_numericos_centroide = pd.DataFrame([centroide_numericos], columns=['Age', 'AnnualIncome', 'SpendingScore', 'WorkExperience', 'FamilySize'])
    dados_normalizados_legiveis = normalizador.inverse_transform(dados_numericos_centroide)
    dados_numericos_centroide = pd.DataFrame([[round(dados_normalizados_legiveis[0][0]), round(dados_normalizados_legiveis[0][1]), round(dados_normalizados_legiveis[0][2]), round(dados_normalizados_legiveis[0][3]), round(dados_normalizados_legiveis[0][4])]], columns=['Age', 'AnnualIncome', 'SpendingScore', 'WorkExperience', 'FamilySize'])

    # Dados Categóricos Centroide
    centroide_categoricos = pd.DataFrame(columns=colunas_categoricas)
    centroide_categoricos.loc[0] = [round(centroide_list[5]), round(centroide_list[6]), round(centroide_list[7]), round(centroide_list[8]), round(centroide_list[9]), round(centroide_list[10]), round(centroide_list[11]), round(centroide_list[12]), round(centroide_list[13]), round(centroide_list[14]), round(centroide_list[15])]
    dados_categoricos_centroide = pd.from_dummies(centroide_categoricos, sep='_')

    centroide_final_legivel = dados_numericos_centroide.join(dados_categoricos_centroide, how='left')

    print("\n### DADOS LEGÍVEIS ###")
    print(centroide_final_legivel)
    input("\nAperte Enter para prosseguir...")