import streamlit as st
import pandas as pd
from calculs import *
from visualisations import *
from emails import *

# Configuration de la page
st.set_page_config(
    page_title="Gestion des Abonnements",
    page_icon="📊",
    layout="wide"
)

# Titre principal
st.title("Système de Gestion des Abonnements")
st.markdown("### Analyse de la Rétention et Reporting")

# Charger les données
@st.cache_data
def load_data():
    return charger_donnees()

df = load_data()

if df is None:
    st.error("Aucune donnée trouvée. Exécutez 'python generate_data.py' d'abord.")
    st.stop()

# Sidebar - Menu de navigation
menu = st.sidebar.selectbox(
    "Menu",
    ["Dashboard", "Clients", "Graphiques", "Emails & Alertes", "Rapports"]
)

# ========== PAGE 1 : DASHBOARD ==========
if menu == "Dashboard":
    st.header("Tableau de Bord Principal")
    
    # Calculer les métriques
    metriques = calculer_metriques(df)
    
    # Afficher les KPIs en colonnes
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Clients",
            value=metriques['total_clients']
        )
    
    with col2:
        st.metric(
            label="Clients Actifs",
            value=metriques['clients_actifs'],
            delta=f"{metriques['taux_retention']}% rétention"
        )
    
    with col3:
        st.metric(
            label="MRR",
            value=f"{metriques['mrr']:,.0f} MAD",
            delta=f"{metriques['arpu']:.0f} MAD/client"
        )
    
    with col4:
        st.metric(
            label="Taux de Churn",
            value=f"{metriques['taux_churn']}%",
            delta=f"-{metriques['clients_annules']} clients",
            delta_color="inverse"
        )
    
    st.markdown("---")
    
    # Graphiques principaux
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(graphique_statuts(df), use_container_width=True)
    
    with col2:
        st.plotly_chart(graphique_repartition_plans(df), use_container_width=True)
    
    # Analyse par plan
    st.subheader("Analyse par Plan d'Abonnement")
    analyse_plan = analyser_par_plan(df)
    st.dataframe(analyse_plan, use_container_width=True)

# ========== PAGE 2 : CLIENTS ==========
elif menu == "Clients":
    st.header("Liste des Clients")
    
    # Filtres
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filtre_statut = st.multiselect(
            "Filtrer par statut",
            options=df['statut'].unique(),
            default=df['statut'].unique()
        )
    
    with col2:
        filtre_plan = st.multiselect(
            "Filtrer par plan",
            options=df['plan'].unique(),
            default=df['plan'].unique()
        )
    
    with col3:
        recherche = st.text_input("Rechercher un client (nom ou email)")
    
    # Appliquer les filtres
    df_filtre = df[df['statut'].isin(filtre_statut) & df['plan'].isin(filtre_plan)]
    
    if recherche:
        df_filtre = df_filtre[
            df_filtre['nom'].str.contains(recherche, case=False) |
            df_filtre['email'].str.contains(recherche, case=False)
        ]
    
    # Afficher le nombre de résultats
    st.info(f"{len(df_filtre)} clients affichés")
    
    # Tableau des clients
    st.dataframe(
        df_filtre[['id', 'nom', 'email', 'plan', 'prix_mensuel', 'statut', 'score_risque']],
        use_container_width=True,
        hide_index=True
    )
    
    # Clients à risque
    st.subheader("Clients à Risque de Churn")
    clients_risque = identifier_clients_risque(df, seuil=0.7)
    
    if len(clients_risque) > 0:
        st.warning(f"{len(clients_risque)} clients présentent un risque élevé de churn !")
        st.dataframe(clients_risque, use_container_width=True, hide_index=True)
    else:
        st.success("Aucun client à risque détecté")

# ========== PAGE 3 : GRAPHIQUES ==========
elif menu == "Graphiques":
    st.header("Visualisations et Analyses")
    
    # Onglets pour différents types de graphiques
    tab1, tab2, tab3, tab4 = st.tabs([
        "Évolution", "Revenus", "Cohortes", "Risque Churn"
    ])
    
    with tab1:
        st.plotly_chart(graphique_evolution_clients(df), use_container_width=True)
    
    with tab2:
        st.plotly_chart(graphique_revenu_par_plan(df), use_container_width=True)
    
    with tab3:
        st.plotly_chart(graphique_cohorte_retention(df), use_container_width=True)
        
        st.info("Une cohorte regroupe tous les clients inscrits le même mois. "
                "Le graphique montre le taux de rétention pour chaque cohorte.")
    
    with tab4:
        st.plotly_chart(graphique_risque_churn(df), use_container_width=True)
        
        clients_risque = len(df[(df['statut'] == 'actif') & (df['score_risque'] >= 0.7)])
        st.warning(f"{clients_risque} clients actifs présentent un score de risque >= 0.7")

# ========== PAGE 4 : EMAILS & ALERTES ==========
elif menu == "Emails & Alertes":
    st.header("Système d'Emails Automatiques et Alertes")
    
    tab1, tab2 = st.tabs(["Emails de Relance", "Alertes Churn"])
    
    with tab1:
        st.subheader("Emails de Relance - Clients Inactifs")
        
        clients_inactifs = df[df['statut'].isin(['annulé', 'expiré'])]
        st.info(f"{len(clients_inactifs)} clients inactifs à relancer")
        
        if st.button("Générer les Emails de Relance"):
            with st.spinner("Génération en cours..."):
                emails_df = simuler_envoi_emails(df)
                st.success(f"{len(emails_df)} emails générés avec succès !")
                
                # Aperçu des emails
                st.subheader("Aperçu des Emails")
                for _, email in emails_df.head(3).iterrows():
                    with st.expander(f"Email pour {email['nom']}"):
                        st.write(f"**À:** {email['destinataire']}")
                        st.write(f"**Sujet:** {email['sujet']}")
                        st.text_area("Corps:", email['corps'], height=200, disabled=True)
    
    with tab2:
        st.subheader("Alertes pour l'Équipe Marketing")
        
        seuil = st.slider("Seuil de risque", 0.0, 1.0, 0.7, 0.05)
        
        if st.button("Générer les Alertes"):
            with st.spinner("Génération des alertes..."):
                alertes_df = generer_alertes_equipe(df, seuil=seuil)
                
                if len(alertes_df) > 0:
                    st.error(f"{len(alertes_df)} clients nécessitent une attention immédiate !")
                    
                    # Afficher les alertes
                    for _, alerte in alertes_df.iterrows():
                        with st.expander(f"{alerte['nom']} - Score: {alerte['score_risque']}"):
                            st.write(f"**Client ID:** {alerte['client_id']}")
                            st.write(f"**Email:** {alerte['email']}")
                            st.write(f"**Score de risque:** {alerte['score_risque']}")
                            st.text_area("Message d'alerte:", alerte['corps'], height=200, disabled=True)
                else:
                    st.success("Aucune alerte au seuil spécifié")

# ========== PAGE 5 : RAPPORTS ==========
elif menu == "Rapports":
    st.header("Génération de Rapports")
    
    st.subheader("Rapport Mensuel de Performance")
    
    # Calculer les métriques
    metriques = calculer_metriques(df)
    
    # Options de rapport
    col1, col2 = st.columns(2)
    
    with col1:
        type_rapport = st.selectbox(
            "Type de rapport",
            ["Rapport Complet", "Rapport Financier", "Rapport Clients", "Rapport Churn"]
        )
    
    with col2:
        format_export = st.selectbox(
            "Format d'export",
            ["CSV", "Excel", "Texte"]
        )
    
    # Bouton de génération
    if st.button("Générer le Rapport"):
        st.markdown("---")
        
        # ========== RAPPORT COMPLET ==========
        if type_rapport == "Rapport Complet":
            st.subheader("Rapport Complet de Performance")
            
            # Section 1 : Métriques Clés
            st.markdown("### 1. Métriques Clés")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Clients", metriques['total_clients'])
                st.metric("Clients Actifs", metriques['clients_actifs'])
            with col2:
                st.metric("MRR", f"{metriques['mrr']:,.0f} MAD")
                st.metric("ARPU", f"{metriques['arpu']:.0f} MAD")
            with col3:
                st.metric("Taux de Churn", f"{metriques['taux_churn']}%")
                st.metric("Taux de Rétention", f"{metriques['taux_retention']}%")
            
            # Section 2 : Analyse par Plan
            st.markdown("### 2. Analyse par Plan d'Abonnement")
            analyse_plan = analyser_par_plan(df)
            st.dataframe(analyse_plan, use_container_width=True)
            
            # Section 3 : Cohortes
            st.markdown("### 3. Analyse de Cohorte")
            cohortes = analyser_cohortes(df)
            st.dataframe(cohortes.tail(6), use_container_width=True)
            
            # Section 4 : Clients à Risque
            st.markdown("### 4. Clients à Risque")
            clients_risque = identifier_clients_risque(df, seuil=0.7)
            st.warning(f"{len(clients_risque)} clients à risque détectés")
            st.dataframe(clients_risque.head(10), use_container_width=True)
        
        # ========== RAPPORT FINANCIER ==========
        elif type_rapport == "Rapport Financier":
            st.subheader("Rapport Financier")
            
            st.markdown("### Revenus")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("MRR (Revenu Mensuel Récurrent)", f"{metriques['mrr']:,.0f} MAD")
                st.metric("ARR (Revenu Annuel)", f"{metriques['mrr'] * 12:,.0f} MAD")
            with col2:
                st.metric("ARPU (Revenu Moyen/Client)", f"{metriques['arpu']:.0f} MAD")
                st.metric("LTV Moyen (Valeur Vie Client)", f"{metriques['ltv_moyen']:,.0f} MAD")
            
            st.markdown("### Répartition des Revenus par Plan")
            
            clients_actifs = df[df['statut'] == 'actif']
            revenu_plan = clients_actifs.groupby('plan')['prix_mensuel'].sum().reset_index()
            revenu_plan.columns = ['Plan', 'Revenu Mensuel (MAD)']
            revenu_plan['% du Total'] = (revenu_plan['Revenu Mensuel (MAD)'] / metriques['mrr'] * 100).round(2)
            
            st.dataframe(revenu_plan, use_container_width=True, hide_index=True)
            
            st.markdown("### Projections")
            st.info(f"**Projection Trimestrielle:** {metriques['mrr'] * 3:,.0f} MAD")
            st.info(f"**Projection Annuelle:** {metriques['mrr'] * 12:,.0f} MAD")
        
        # ========== RAPPORT CLIENTS ==========
        elif type_rapport == "Rapport Clients":
            st.subheader("Rapport Clients")
            
            st.markdown("### Vue d'ensemble")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Clients", metriques['total_clients'])
            with col2:
                st.metric("Nouveaux Clients (30j)", len(df[pd.to_datetime(df['date_debut']) >= pd.Timestamp.now() - pd.Timedelta(days=30)]))
            with col3:
                st.metric("Clients Perdus", metriques['clients_annules'])
            
            st.markdown("### Répartition par Statut")
            statut_count = df['statut'].value_counts().reset_index()
            statut_count.columns = ['Statut', 'Nombre']
            st.dataframe(statut_count, use_container_width=True, hide_index=True)
            
            st.markdown("### Répartition Géographique (Top 10 Villes)")
            villes = df['ville'].value_counts().head(10).reset_index()
            villes.columns = ['Ville', 'Nombre de Clients']
            st.dataframe(villes, use_container_width=True, hide_index=True)
        
        # ========== RAPPORT CHURN ==========
        elif type_rapport == "Rapport Churn":
            st.subheader("Rapport d'Analyse du Churn")
            
            st.markdown("### Métriques de Churn")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Taux de Churn", f"{metriques['taux_churn']}%")
            with col2:
                st.metric("Clients Annulés", metriques['clients_annules'])
            with col3:
                clients_risque_count = len(df[(df['statut'] == 'actif') & (df['score_risque'] >= 0.7)])
                st.metric("Clients à Risque", clients_risque_count)
            
            st.markdown("### Clients à Haut Risque")
            clients_risque = identifier_clients_risque(df, seuil=0.7)
            
            if len(clients_risque) > 0:
                st.error(f"{len(clients_risque)} clients nécessitent une intervention immédiate")
                st.dataframe(clients_risque, use_container_width=True, hide_index=True)
                
                # Recommandations
                st.markdown("### Recommandations")
                st.warning("""
                **Actions prioritaires :**
                1. Contacter les clients à risque dans les 48h
                2. Proposer des offres personnalisées
                3. Demander un feedback détaillé
                4. Offrir un support premium temporaire
                """)
            else:
                st.success("Aucun client à haut risque détecté")
            
            st.markdown("### Analyse du Churn par Plan")
            churn_plan = df[df['statut'] == 'annulé'].groupby('plan').size().reset_index()
            churn_plan.columns = ['Plan', 'Clients Annulés']
            st.dataframe(churn_plan, use_container_width=True, hide_index=True)
        
        # Export des données
        st.markdown("---")
        st.subheader("Export du Rapport")
        
        if format_export == "CSV":
            csv = df.to_csv(index=False, encoding='utf-8')
            st.download_button(
                label="Télécharger en CSV",
                data=csv,
                file_name=f"rapport_{type_rapport.replace(' ', '_').lower()}.csv",
                mime="text/csv"
            )
        
        elif format_export == "Excel":
            # Note : Nécessite openpyxl
            from io import BytesIO
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Données', index=False)
                analyser_par_plan(df).to_excel(writer, sheet_name='Par Plan')
                identifier_clients_risque(df).to_excel(writer, sheet_name='Clients à Risque', index=False)
            
            st.download_button(
                label="Télécharger en Excel",
                data=output.getvalue(),
                file_name=f"rapport_{type_rapport.replace(' ', '_').lower()}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        else:  # Texte
            rapport_texte = f"""
===========================================
RAPPORT DE GESTION DES ABONNEMENTS
===========================================

Date de génération : {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}

MÉTRIQUES PRINCIPALES
---------------------
Total Clients : {metriques['total_clients']}
Clients Actifs : {metriques['clients_actifs']}
Clients Annulés : {metriques['clients_annules']}
Taux de Churn : {metriques['taux_churn']}%
Taux de Rétention : {metriques['taux_retention']}%

FINANCES
--------
MRR : {metriques['mrr']:,.0f} MAD
ARPU : {metriques['arpu']:.0f} MAD
LTV Moyen : {metriques['ltv_moyen']:,.0f} MAD

CLIENTS À RISQUE
----------------
Nombre : {len(identifier_clients_risque(df, seuil=0.7))}

===========================================
            """
            
            st.download_button(
                label="Télécharger en TXT",
                data=rapport_texte,
                file_name=f"rapport_{type_rapport.replace(' ', '_').lower()}.txt",
                mime="text/plain"
            )
        
        st.success("Rapport généré avec succès !")

# ========== FOOTER ==========
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    Système de Gestion des Abonnements | Développé avec Streamlit & Python<br>
    Version 1.0 | 2026
</div>
""", unsafe_allow_html=True)