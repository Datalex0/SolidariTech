
# Import librairies
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import plotly.express as px
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
# st.sidebar.image(image2)

# Import dataframes
df = pd.read_csv("SRC/pages/df_final_age.csv", sep = ",", low_memory=False)
#, encoding='latin1'


# Titre Sidebar
st.sidebar.title("**Sélectionnez les critères** :")
st.sidebar.markdown("***")

# FILTRES

# Double Curseur AGE
min_age, max_age = st.sidebar.slider(
'Âge :',
min_value = 0, 
max_value = 100, 
value = (0,100),
step = 10)

# Menu déroulant des SEXES
liste_sexes =['Homme + Femme', 'Homme', 'Femme']
sexe = st.sidebar.selectbox(
'Sexe', liste_sexes
)
if sexe=='Homme + Femme':
    sexe='m'
    
# Menu déroulant CSP
liste_csp =['Toutes', 'Employé', 'Ouvrier', 'Profession Intermédiaire', 'Cadre', 'Indépendant', 'Père/Mère au foyer', 'Retraité', 'Autre inactif']
csp = st.sidebar.selectbox(
'Catégorie Socio-Professionnelle', liste_csp
)
if csp=='Toutes':
    csp=''
elif csp=='Père/Mère au foyer':
    csp='foyer'
elif csp=='Indépendant':
    csp="chef d'entreprise"
    
# Menu déroulant Diplôme
liste_diplomes =['Tous', 'BEPC', 'Diplômé du supérieur', 'BAC', 'Non diplômé', '12-17 ans']
diplome = st.sidebar.selectbox(
'Diplôme', liste_diplomes
)
if diplome=='Tous':
    diplome=''

# Menu déroulant REGION
liste_regions =['Toutes', 'Ile de France', 'Auvergne Rhone Alpes', 'Hauts de France', 'Nouvelle Aquitaine', 'Occitanie', 'Grand Est', 'PACA', 'Pays de la Loire', 'Normandie', 'Bretagne', 'Bourgogne Franche Comté', 'Centre Val de Loire', 'Corse']
region = st.sidebar.selectbox(
'Région', liste_regions
)
if region=='Toutes':
    region=''
    

# Menu déroulant taille Agglo
liste_agglo =['Toutes', 'Agglomération parisienne', 'Plus de 100 000 hab.', '20 000 à 100 000 hab.', '2 000 à 20 000 hab.', 'Communes rurales']
agglo = st.sidebar.selectbox(
"Taille de l'agglomération", liste_agglo
)
if agglo=='Toutes':
    agglo=''


# Inversion Sécurité pour coller aux autres colonnes pour faciliter les boucles
dico_secu = {'Oui':'Non','Non':'Oui'}
df['SECURITE'] = df['SECURITE'].replace(dico_secu)

# Liste usages
categories = ["POSSESSION D'EQUIPEMENTS", 'ACCES A INTERNET', 'DIVERTISSEMENT', 'EMPLOI / FORMATION', 'COMMUNICATION', 'ADMINISTRATIF', 'ACHATS', 'SECURITE']    

df = df.rename({'EMPLFORM':'EMPLOI / FORMATION','INTERNET':'ACCES A INTERNET','EQUIPEMENT':"POSSESSION D'EQUIPEMENTS"}, axis='columns')

df1 = df[
    (df.SEXE.str.contains(sexe)) & (df['AGE']<=max_age) & (df['AGE']>=min_age) & (df.CSP.str.contains(csp)) & (df.AGGLOMERATION.str.contains(agglo)) & (df.DIPLOME.str.contains(diplome)) & (df.REGION.str.contains(region))
    ]

# Fonction pour centrer le texte
def centered_text(text):
    st.markdown(f"<h3 style='text-align: center;'>{text}</h3>", unsafe_allow_html=True)
    

centered_text("Répartition pour les différentes catégories de population")
centered_text("des usages les moins réalisés") 




df2 = df1[
df1['ANNEE']==2022
]


dico_percent = {}
for i in range(len(categories)) :
    dico_percent[categories[i]]=(df2[categories[i]].value_counts()['Non'])*100/(df2[categories[i]].value_counts().sum())

df_percent = pd.Series(dico_percent)
df_percent = df_percent.sort_values(ascending=False)
#st.write(df_percent)

# Diviser l'espace d'affichage en deux colonnes
# col1, col2 = st.columns(2)


# Afficher le premier graphique dans la première colonne
# with col1:

    # Piechart
fig = px.pie(df_percent, values=0, names=df_percent.index, title=" ", hover_name=df_percent.index, width=1200, height=900, color=0, hole=0.5) #,color_discrete_map={'1':'cyan','0':'darkblue'})
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.update_traces(pull=[0.2, 0.05, 0.05, 0.05, 0.05, 0.05])
fig.update_layout(title_font=dict(size=32))
fig.update_layout(legend=dict(font=dict(size=16)))
fig.update_traces(marker=dict(line=dict(color='rgba(0,0,0,5)', width=2)))
# Afficher le graphique
st.plotly_chart(fig)


# Afficher le deuxième graphique dans la deuxième colonne
# with col2:
    
#     fig = px.bar(df_percent, x=df_percent.index, y=0, title=" ", hover_name=df_percent.index, hover_data=0, width=650, height=600, color=0)
#     fig.update_layout(title_font=dict(size=32))
#     fig.update_layout(legend=dict(font=dict(size=16), title_text='Légende'))
#     # Afficher le graphique
#     st.plotly_chart(fig)
    
    #labels={'x':'Régions','Percent':'%'},
