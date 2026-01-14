import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker('fr_FR')  # Données en français

def generer_donnees_clients(nombre=100):
    """
    Génère des données fictives de clients
    """
    
    clients = []
    plans = [
        {'nom': 'Basic', 'prix': 99},
        {'nom': 'Pro', 'prix': 199},
        {'nom': 'Premium', 'prix': 299}
    ]
    
    statuts = ['actif', 'annulé', 'expiré']
    
    for i in range(1, nombre + 1):
        # Date de début aléatoire dans les 2 dernières années
        date_debut = datetime.now() - timedelta(days=random.randint(30, 730))
        
        # Choisir un plan aléatoire
        plan = random.choice(plans)
        
        # Choisir un statut (70% actif, 20% annulé, 10% expiré)
        statut = random.choices(
            statuts, 
            weights=[70, 20, 10]
        )[0]
        
        # Date de fin si le statut n'est pas actif
        if statut == 'actif':
            date_fin = None
        else:
            date_fin = date_debut + timedelta(days=random.randint(30, 365))
        
        client = {
            'id': f'CLI{i:04d}',
            'nom': fake.name(),
            'email': fake.email(),
            'telephone': fake.phone_number(),
            'plan': plan['nom'],
            'prix_mensuel': plan['prix'],
            'date_debut': date_debut.strftime('%Y-%m-%d'),
            'date_fin': date_fin.strftime('%Y-%m-%d') if date_fin else None,
            'statut': statut,
            'ville': fake.city(),
            'score_risque': round(random.uniform(0, 1), 2)  # Risque de churn
        }
        
        clients.append(client)
    
    # Créer un DataFrame pandas
    df = pd.DataFrame(clients)
    
    # Sauvegarder dans un fichier CSV
    df.to_csv('clients_data.csv', index=False, encoding='utf-8')
    
    print(f"✅ {nombre} clients générés et sauvegardés dans 'clients_data.csv'")
    return df

# Générer les données
if __name__ == "__main__":
    df = generer_donnees_clients(150)
    print(df.head())