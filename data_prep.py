import pandas as pd



#Function that regroups "communes" into "départements"
def df_departement(df,departement_data,year):
    #we first take 1 year into account
    df_elec=df.loc[df['Année']==year]
    #we drop null values from our dataframe
    df_elec.dropna(subset=['Code INSEE de la commune','Consommation annuelle moyenne de la commune (MWh)','Nom de la commune'])

    df_elec = df_elec.rename(columns={'Code INSEE de la commune':'code_commune_INSEE'})

    df_elec['code_commune_INSEE']=df_elec['code_commune_INSEE'].astype(str)
    INSEE_codes = set(df_elec['code_commune_INSEE'])
    #Here, we match our provided data with "département" names 
    departement_data=departement_data.loc[departement_data['code_commune_INSEE'].isin(INSEE_codes)]
    departement_data['code_commune_INSEE']=departement_data['code_commune_INSEE'].astype(int)
    df_elec['code_commune_INSEE']=df_elec['code_commune_INSEE'].astype(int)
    #we finally merge our data with some cleaning afterwards
    new_elec= pd.merge(departement_data, df_elec,how='inner', on='code_commune_INSEE' )
    new_elec.drop_duplicates(subset=['Consommation annuelle moyenne de la commune (MWh)','Nom de la commune'])
    new_elec.dropna(subset=['Nom de la commune'])
    new_elec=new_elec[['nom_departement','Consommation annuelle moyenne de la commune (MWh)', 'Nom de la commune']]
    new_elec= new_elec.groupby(['nom_departement']).sum()
    
    
    return new_elec
   
