
# Import librairies
import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

#Configuration des dimensions & affichage de la page
st.set_page_config(page_title="Emmaüs Connect Project",
                   page_icon=":computer:",
                   layout='wide')

#Importation image accueil
image = Image.open('SRC/Logo_Emmaüs_Connect.png')
image2 = Image.open('SRC/Logo_Emmaüs_Connect_simple.png')
# st.image(image)


# Import dataframes
df = pd.read_csv("SRC/pages/df_final.csv", sep = ",", low_memory=False)
#, encoding='latin1'
df = df[
    df['ANNEE']==2022
]

# Titre Sidebar
st.sidebar.title("**Sélectionnez les critères** :")
st.sidebar.markdown("***")




# FILTRE    
# Menu déroulant CSP
liste_usages =["Possession d'Equipements", 'Accès à Internet', 'Sécurité', 'Achats en ligne', 'Communication', 'Divertissements', 'Services en ligne', 'Emploi / Formation']
usage = st.sidebar.selectbox(
'Sélectionnez un usage', liste_usages
)
dico_usages={"Possession d'Equipements":'EQUIPEMENT', 'Accès à Internet':'INTERNET', 'Sécurité':'SECURITE', 'Achats en ligne':'ACHATS', 'Communication':'COMMUNICATION', 'Divertissements':'DIVERTISSEMENT', 'Services en ligne':'ADMINISTRATIF', 'Emploi / Formation':'EMPLFORM'}
usage = usage.replace(usage,dico_usages[usage])
dico_usages_reverse={'EQUIPEMENT':'Equipements', 'INTERNET':'Internet', 'SECURITE':'Sécurité', 'ACHATS':'Achats en ligne', 'COMMUNICATION':'Communication', 'DIVERTISSEMENT':'Divertissements', 'ADMINISTRATIF':'Services en ligne', 'EMPLFORM':'Emploi / Formation'}

# Inversion Sécurité pour coller aux autres colonnes pour faciliter les boucles
dico_secu = {'Oui':'Non','Non':'Oui'}
df['SECURITE'] = df['SECURITE'].replace(dico_secu)

# Fonction pour centrer le texte
def centered_text(text):
    st.markdown(f"<h3 style='text-align: center;'>{text}</h3>", unsafe_allow_html=True)


# Affichage des titres
if usage == 'EQUIPEMENT':
    centered_text("en 2022 :")
    centered_text("Répartition par catégorie de population")
    centered_text("parmi ceux qui ne possèdent pas d'équipement numérique") 
    centered_text("")
elif usage == 'INTERNET':
    centered_text("en 2022 :")
    centered_text("Répartition par catégorie de population")
    centered_text("parmi ceux qui ne possèdent pas de connexion internet")
    centered_text("")
elif usage == 'SECURITE':
    centered_text("en 2022 :")
    centered_text("Répartition par catégorie de population")
    centered_text("parmi ceux qui ont déjà été victime d'une attaque/arnaque sur internet")
    centered_text("")
elif usage == 'ACHATS':
    centered_text("en 2022 :")
    centered_text("Répartition par catégorie de population")
    centered_text("parmi ceux qui n'ont pas réalisé d'achat en ligne au cour des 12 derniers mois")
    centered_text("")
elif usage == 'COMMUNICATION':
    centered_text("en 2022 :")
    centered_text("Répartition par catégorie de population")
    centered_text("parmi ceux qui n'ont pas utilisé de moyen de communication en ligne au cours des 12 derniers mois")
    centered_text("")
elif usage == 'DIVERTISSEMENT':
    centered_text("en 2022 :")
    centered_text("Répartition par catégorie de population")
    centered_text("parmi ceux qui n'ont pas utilisé internet pour se divertir au cours des 12 derniers mois")
    centered_text("")
elif usage == 'ADMINISTRATIF':
    centered_text("en 2022 :")
    centered_text("Répartition par catégorie de population")
    centered_text("parmi ceux qui n'ont pas réalisé de tâche administrative en ligne au cours des 12 derniers mois")
    centered_text("")
elif usage == 'EMPLFORM':
    centered_text("en 2022 :")
    centered_text("Répartition par catégorie de population")
    centered_text("parmi ceux qui n'ont pas utilisé internet à des fins professionnelles ou de formation au cours des 12 derniers mois")
    centered_text("")


# Fonction de création de Dataframe
def create_df(categorie):
    df_cat = df[[usage, categorie]]
    return df_cat


# Diviser l'espace d'affichage en 2 colonnes
col1, col2 = st.columns(2)

# AGE
# Afficher le premier graphique dans la première colonne
with col1:
    
    categorie = 'AGE'
    df_cat = create_df(categorie)
    # Calculer le compte
    counts = df_cat[
    df_cat[usage]=='Non'
    ][categorie].value_counts()
    # DataFrame des comptes
    df_counts = pd.DataFrame({categorie: counts.index, 'Count': counts.values})
    # Piechart
    fig = px.pie(df_counts, values='Count', names=categorie, title=categorie, hover_name=categorie, width=600, height=600, color=categorie, hole=0.5) #,color_discrete_map={'1':'cyan','0':'darkblue'})
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_traces(pull=[0.2, 0.05, 0.05, 0.05, 0.05, 0.05])
    fig.update_layout(title_font=dict(size=32))
    fig.update_layout(legend=dict(font=dict(size=16)))
    fig.update_traces(marker=dict(line=dict(color='rgba(0,0,0,5)', width=2)))
    st.plotly_chart(fig)
    


# SEXE
# Afficher le deuxième graphique dans la deuxième colonne
with col2:

    categorie='SEXE'
    df_cat = create_df(categorie)
    # Calculer le compte
    counts = df_cat[
    df_cat[usage]=='Non'
    ][categorie].value_counts()
    # DataFrame des comptes
    df_counts = pd.DataFrame({usage: counts.index, 'Percent': counts.values*100/counts.values.sum()})
    # Piechart
    fig = px.bar(df_counts, x=counts.index, y='Percent', labels={'x':'Genre','Percent':'%'}, title='GENRE', hover_name=counts.index, hover_data='Percent', text=round(df_counts['Percent'],2), width=600, height=600, color=counts.index, color_discrete_map={'Femme':'purple','Homme':'royalblue'})
    fig.update_layout(title_font=dict(size=32))
    fig.update_layout(legend=dict(font=dict(size=16), title_text='Légende'))
    # Afficher le graphique
    st.plotly_chart(fig)
    #dico_sexe = {"Femme":29372007, "Homme":26894758}
    #col_1, col_2 = st.columns(2)
    #col_1.metric(label=df_counts[usage][0], value=round(df_counts['Percent'][0]*0.01*dico_sexe[df_counts[usage][0]]))
    #col_2.metric(label=df_counts[usage][1], value=round(df_counts['Percent'][1]*0.01*dico_sexe[df_counts[usage][1]]))
        


st.write("***")
    



# Diviser l'espace d'affichage en 2 colonnes
col3, col4 = st.columns(2)


# CATEGORIE SOCIO-PROFESSIONNELLE
# Afficher le troisième graphique dans la troisième colonne
with col3:

    categorie = 'CSP'
    df_cat = create_df(categorie)
    # Calculer le compte
    counts = df_cat[
    df_cat[usage]=='Non'
    ][categorie].value_counts()
    # DataFrame des comptes
    df_counts = pd.DataFrame({categorie: counts.index, 'Count': counts.values})
    # Piechart
    fig = px.pie(df_counts, values='Count', names=categorie, title='CATEGORIE SOCIO-PROFESSIONNELLE', hover_name=categorie, width=600, height=600, color=categorie, hole=0.5) #,color_discrete_map={'1':'cyan','0':'darkblue'})
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_traces(pull=[0.2, 0.05, 0.05, 0.05, 0.05, 0.05])
    fig.update_layout(title_font=dict(size=32))
    fig.update_layout(legend=dict(font=dict(size=16)))
    # Afficher le graphique
    st.plotly_chart(fig)
    




# TAILLE D'AGGLOMERATION
# Afficher le premier graphique dans la première colonne
with col4:
    
    categorie = 'AGGLOMERATION'
    df_cat = create_df(categorie)
    # Calculer le compte
    counts = df_cat[
    df_cat[usage]=='Non'
    ][categorie].value_counts()
    # DataFrame des comptes
    df_counts = pd.DataFrame({categorie: counts.index, 'Count': counts.values})
    # Piechart
    fig = px.pie(df_counts, values='Count', names=categorie, title=categorie, hover_name=categorie, width=600, height=600, color=categorie, hole=0.5) #,color_discrete_map={'1':'cyan','0':'darkblue'})
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_traces(pull=[0.2, 0.05, 0.05, 0.05, 0.05, 0.05])
    fig.update_layout(title_font=dict(size=32))
    fig.update_layout(legend=dict(font=dict(size=16)))
    # Afficher le graphique
    st.plotly_chart(fig)



st.write("***")



# Diviser l'espace d'affichage en 2 colonnes
col5, col6 = st.columns(2)


# REGION
# Afficher le deuxième graphique dans la deuxième colonne
with col5:

    categorie='REGION'
    df_cat = create_df(categorie)
    # Calculer le compte
    counts = df_cat[
    df_cat[usage]=='Non'
    ][categorie].value_counts()
    # DataFrame des comptes
    df_counts = pd.DataFrame({usage: counts.index, 'Percent': counts.values*100/counts.values.sum()})
    # Piechart
    fig = px.bar(df_counts, x=counts.index, y='Percent',labels={'x':'Régions','Percent':'%'}, title=categorie, hover_name=counts.index, hover_data='Percent', text=round(df_counts['Percent'],2), width=650, height=600, color=counts.index)
    fig.update_layout(title_font=dict(size=32))
    fig.update_layout(legend=dict(font=dict(size=16), title_text='Légende'))
    # Afficher le graphique
    st.plotly_chart(fig)
    


# DIPLOME
# Afficher le troisième graphique dans la troisième colonne
with col6:

    categorie = 'DIPLOME'
    df_cat = create_df(categorie)
    # Calculer le compte
    counts = df_cat[
    df_cat[usage]=='Non'
    ][categorie].value_counts()
    # DataFrame des comptes
    df_counts = pd.DataFrame({categorie: counts.index, 'Count': counts.values})
    # Piechart
    fig = px.pie(df_counts, values='Count', names=categorie, title=categorie, hover_name=categorie, width=600, height=600, color=categorie, hole=0.5) #,color_discrete_map={'1':'cyan','0':'darkblue'})
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_traces(pull=[0.2, 0.05, 0.05, 0.05, 0.05, 0.05])
    fig.update_layout(title_font=dict(size=32))
    fig.update_layout(legend=dict(font=dict(size=16)))
    # Afficher le graphique
    st.plotly_chart(fig)
    
    st.sidebar.write("***")
    st.sidebar.image(image2)
