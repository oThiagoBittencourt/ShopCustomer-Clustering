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

    print(dados_completos.columns)

    # EXECUÇÃO DO PREDICT
    predict = shop_customers_cluster_model.predict(dados_completos)
    centroide = shop_customers_cluster_model.cluster_centers_[shop_customers_cluster_model.predict(dados_completos)]

    print(f"índice do grupo da nova instancia: {predict}")
    print(f"Centroide da nova instancia: {centroide}")