# Application de Gestion d'Abonnements

Application web interactive développée avec **Streamlit** pour gérer et analyser les abonnements clients.


## Fonctionnalités

  1. Analyse des Données
- Calcul automatique du chiffre d'affaires total
- Statistiques détaillées par type d'abonnement
- Analyse de la répartition des clients

  2. Visualisations Interactives
- Graphiques en barres pour les revenus par type
- Diagrammes circulaires pour la distribution des abonnements
- Graphiques d'évolution temporelle
- Tableaux de bord dynamiques

  3. Gestion des Communications
- Génération automatique d'emails personnalisés
- Templates d'emails pour différentes occasions
- Prévisualisation avant envoi

  4. Génération de Rapports
- Rapports PDF téléchargeables
- Exports CSV des données
- Résumés statistiques détaillés

---

## Technologies Utilisées

- **Python 3.9+**
- **Streamlit** - Framework web
- **Pandas** - Manipulation de données
- **Matplotlib & Seaborn** - Visualisations statiques
- **Plotly** - Graphiques interactifs
- **NumPy** - Calculs numériques

---

## Installation Locale

 . Prérequis
- Python 3.9 ou supérieur installé
- pip (gestionnaire de packages Python)

 . Étapes d'installation

    1. **Cloner le repository**
    ```bash
    git clone https://github.com/VOTRE-USERNAME/gestion-abonnements.git
    cd gestion-abonnements
    ```

    2. **Installer les dépendances**
    ```bash
    pip install -r requirements.txt
    ```

    3. **Lancer l'application**
    ```bash
    streamlit run app.py
    ```

    4. **Ouvrir dans le navigateur**
    L'application s'ouvrira automatiquement à l'adresse : `http://localhost:8501`

---

## Utilisation

### Premier Lancement
Au premier démarrage, l'application génère automatiquement des données de test (50 clients fictifs).

 . Navigation
L'application comporte plusieurs sections accessibles via la barre latérale :
1. **Tableau de bord** - Vue d'ensemble des KPIs
2. **Analyse des données** - Statistiques détaillées
3. **Visualisations** - Graphiques interactifs
4. **Gestion des emails** - Communication clients
5. **Rapports** - Génération de documents

---

## Structure du Projet
```
gestion-abonnements/
├── app.py                  # Application principale Streamlit
├── calculs.py              # Fonctions de calcul du CA et statistiques
├── visualisations.py       # Création des graphiques
├── emails.py               # Gestion des emails
├── generate_data.py        # Génération de données de test
├── clients_data.csv        # Données des clients (généré automatiquement)
├── emails_relance.csv      # Emails de relance envoyés aux clients
├── alertes_churn.csv       # Alertes de risque de désabonnement
├── requirements.txt        # Dépendances Python
└── README.md              # Documentation (ce fichier)
```

---
## Format des Données

Le fichier `clients_data.csv` contient les colonnes suivantes :
- **ID** : Identifiant unique du client
- **Nom** : Nom du client
- **Email** : Adresse email
- **Type_Abonnement** : Basic, Premium ou Enterprise
- **Prix_Mensuel** : Montant mensuel en MAD
- **Date_Inscription** : Date de début d'abonnement
- **Statut** : Actif ou Inactif

---
## Dépannage

     Problème 1 : Module non trouvé
**Solution** : Réinstallez les dépendances
```bash
pip install -r requirements.txt --upgrade
```

     Problème 2 : Le fichier CSV n'existe pas
**Solution** : Exécutez le script de génération de données
```bash
python generate_data.py
```

     Problème 3 : Port déjà utilisé
**Solution** : Spécifiez un autre port
```bash
streamlit run app.py --server.port 8502
```

---

# Auteur

**[Ikram KANBOUCH / Bothayna BESSAR]**
- Projet académique - [Nom de votre école/université]
- Date : Janvier 2026

---

# Licence

Ce projet est développé à des fins éducatives.



# Remerciements

- Professeur [M.MAWANE]
- Streamlit pour le framework
- La communauté Python

---

# Contact

Pour toute question ou suggestion :
- Email : botaynabessar@gmail.com
- GitHub : [@botaynabessar](https://github.com/botaynabessar)

---

**Note** : Cette application est un projet académique et les données utilisées sont fictives.