import pandas as pd
import numpy as np
from datetime import datetime

def charger_donnees():
    """
    Charge les données depuis le fichier CSV
    """
    try:
        df = pd.read_csv('clients_data.csv')
        return df
    except FileNotFoundError:
        print(" Fichier clients_data.csv non trouvé. Exécutez generate_data.py d'abord.")
        return None

def calculer_metriques(df):
    """
    Calcule toutes les métriques importantes
    """
    
    metriques = {}
    
    # Nombre total de clients
    metriques['total_clients'] = len(df)
    
    # Clients actifs
    clients_actifs = df[df['statut'] == 'actif']
    metriques['clients_actifs'] = len(clients_actifs)
    
    # Clients annulés
    clients_annules = df[df['statut'] == 'annulé']
    metriques['clients_annules'] = len(clients_annules)
    
    # Taux de churn (taux d'attrition)
    metriques['taux_churn'] = round(
        (metriques['clients_annules'] / metriques['total_clients']) * 100, 2
    )
    
    # Taux de rétention
    metriques['taux_retention'] = round(
        (metriques['clients_actifs'] / metriques['total_clients']) * 100, 2
    )
    
    # Revenu Mensuel Récurrent (MRR)
    metriques['mrr'] = clients_actifs['prix_mensuel'].sum()
    
    # Revenu moyen par client
    metriques['arpu'] = round(
        clients_actifs['prix_mensuel'].mean(), 2
    )
    
    # Valeur à vie moyenne (LTV estimée sur 12 mois)
    metriques['ltv_moyen'] = round(metriques['arpu'] * 12, 2)
    
    return metriques

def analyser_par_plan(df):
    """
    Analyse des clients par type d'abonnement
    """
    analyse = df.groupby('plan').agg({
        'id': 'count',
        'prix_mensuel': 'sum',
        'statut': lambda x: (x == 'actif').sum()
    }).rename(columns={
        'id': 'nombre_clients',
        'prix_mensuel': 'revenu_total',
        'statut': 'clients_actifs'
    })
    
    return analyse

def analyser_cohortes(df):
    """
    Analyse de cohorte par mois d'inscription
    """
    df['date_debut'] = pd.to_datetime(df['date_debut'])
    df['mois_cohorte'] = df['date_debut'].dt.to_period('M')
    
    cohortes = df.groupby('mois_cohorte').agg({
        'id': 'count',
        'statut': lambda x: (x == 'actif').sum()
    }).rename(columns={
        'id': 'total',
        'statut': 'actifs'
    })
    
    cohortes['taux_retention'] = round(
        (cohortes['actifs'] / cohortes['total']) * 100, 2
    )
    
    return cohortes

def identifier_clients_risque(df, seuil=0.7):
    """
    Identifie les clients à risque de churn
    """
    clients_risque = df[
        (df['statut'] == 'actif') & 
        (df['score_risque'] >= seuil)
    ].sort_values('score_risque', ascending=False)
    
    return clients_risque[['id', 'nom', 'email', 'plan', 'score_risque']]

# Test des fonctions
if __name__ == "__main__":
    df = charger_donnees()
    if df is not None:
        metriques = calculer_metriques(df)
        print("\n MÉTRIQUES PRINCIPALES :")
        for key, value in metriques.items():
            print(f"  {key}: {value}")
        
        print("\n ANALYSE PAR PLAN :")
        print(analyser_par_plan(df))
        
        print("\n CLIENTS À RISQUE :")
        print(identifier_clients_risque(df))