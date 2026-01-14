import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def graphique_evolution_clients(df):
    """
    Graphique d'évolution du nombre de clients par mois
    """
    
    df['date_debut'] = pd.to_datetime(df['date_debut'])
    df['mois'] = df['date_debut'].dt.to_period('M').astype(str)
    
    # Compter les clients par mois
    evolution = df.groupby('mois').size().reset_index(name='nombre_clients')
    
    fig = px.line(
        evolution, 
        x='mois', 
        y='nombre_clients',
        title=' Évolution du Nombre de Clients par Mois',
        labels={'mois': 'Mois', 'nombre_clients': 'Nombre de Clients'},
        markers=True
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        hovermode='x unified'
    )
    
    return fig

def graphique_repartition_plans(df):
    """
    Camembert de répartition des clients par plan
    """
    
    repartition = df['plan'].value_counts().reset_index()
    repartition.columns = ['plan', 'nombre']
    
    fig = px.pie(
        repartition,
        values='nombre',
        names='plan',
        title=' Répartition des Clients par Plan',
        hole=0.4,  # Donut chart
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    return fig

def graphique_statuts(df):
    """
    Graphique en barres des statuts clients
    """
    
    statuts = df['statut'].value_counts().reset_index()
    statuts.columns = ['statut', 'nombre']
    
    couleurs = {
        'actif': '#2ecc71',
        'annulé': '#e74c3c',
        'expiré': '#f39c12'
    }
    
    statuts['couleur'] = statuts['statut'].map(couleurs)
    
    fig = px.bar(
        statuts,
        x='statut',
        y='nombre',
        title=' Répartition des Clients par Statut',
        labels={'statut': 'Statut', 'nombre': 'Nombre de Clients'},
        color='statut',
        color_discrete_map=couleurs,
        text='nombre'
    )
    
    fig.update_traces(textposition='outside')
    
    return fig

def graphique_revenu_par_plan(df):
    """
    Revenu mensuel par plan d'abonnement
    """
    
    clients_actifs = df[df['statut'] == 'actif']
    
    revenu = clients_actifs.groupby('plan')['prix_mensuel'].sum().reset_index()
    revenu.columns = ['plan', 'revenu']
    
    fig = px.bar(
        revenu,
        x='plan',
        y='revenu',
        title=' Revenu Mensuel par Plan (Clients Actifs)',
        labels={'plan': 'Plan', 'revenu': 'Revenu (MAD)'},
        color='revenu',
        color_continuous_scale='Viridis',
        text='revenu'
    )
    
    fig.update_traces(texttemplate='%{text:,.0f} MAD', textposition='outside')
    
    return fig

def graphique_cohorte_retention(df):
    """
    Heatmap d'analyse de cohorte
    """
    
    df['date_debut'] = pd.to_datetime(df['date_debut'])
    df['mois_cohorte'] = df['date_debut'].dt.to_period('M').astype(str)
    
    cohorte = df.groupby('mois_cohorte').agg({
        'id': 'count',
        'statut': lambda x: (x == 'actif').sum()
    })
    
    cohorte['taux_retention'] = (cohorte['statut'] / cohorte['id'] * 100).round(2)
    
    fig = px.bar(
        cohorte.reset_index(),
        x='mois_cohorte',
        y='taux_retention',
        title=' Taux de Rétention par Cohorte',
        labels={'mois_cohorte': 'Mois de Cohorte', 'taux_retention': 'Taux de Rétention (%)'},
        color='taux_retention',
        color_continuous_scale='RdYlGn'
    )
    
    return fig

def graphique_risque_churn(df):
    """
    Distribution du score de risque de churn
    """
    
    clients_actifs = df[df['statut'] == 'actif']
    
    fig = px.histogram(
        clients_actifs,
        x='score_risque',
        nbins=20,
        title=' Distribution du Score de Risque de Churn (Clients Actifs)',
        labels={'score_risque': 'Score de Risque', 'count': 'Nombre de Clients'},
        color_discrete_sequence=['#e74c3c']
    )
    
    # Ajouter une ligne verticale au seuil de risque (0.7)
    fig.add_vline(x=0.7, line_dash="dash", line_color="red", 
                  annotation_text="Seuil de risque élevé")
    
    return fig

# Test
if __name__ == "__main__":
    from calculs import charger_donnees
    
    df = charger_donnees()
    if df is not None:
        # Afficher un graphique
        fig = graphique_evolution_clients(df)
        fig.show()