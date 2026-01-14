import pandas as pd
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def generer_email_relance(client):
    """
    Génère le contenu d'un email de relance
    """
    
    sujet = f" {client['nom']}, votre abonnement nécessite votre attention"
    
    corps = f"""
    Bonjour {client['nom']},
    
    Nous avons remarqué que votre abonnement {client['plan']} est actuellement inactif.
    
    Nous serions ravis de vous revoir parmi nos clients actifs !
    
     Offre spéciale : 20% de réduction sur votre prochain renouvellement
    
    Pour réactiver votre compte, cliquez ici : [LIEN]
    
    Cordialement,
    L'équipe Gestion Abonnements
    
    ---
    Prix mensuel : {client['prix_mensuel']} MAD
    """
    
    return sujet, corps

def simuler_envoi_emails(df):
    """
    Simule l'envoi d'emails aux clients inactifs
    """
    
    # Clients à relancer (annulés ou expirés)
    clients_relancer = df[df['statut'].isin(['annulé', 'expiré'])]
    
    emails_generes = []
    
    for _, client in clients_relancer.iterrows():
        sujet, corps = generer_email_relance(client)
        
        email_info = {
            'destinataire': client['email'],
            'nom': client['nom'],
            'sujet': sujet,
            'corps': corps,
            'date_envoi': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        
        emails_generes.append(email_info)
    
    # Sauvegarder les emails générés
    df_emails = pd.DataFrame(emails_generes)
    df_emails.to_csv('emails_relance.csv', index=False, encoding='utf-8')
    
    print(f" {len(emails_generes)} emails de relance générés et sauvegardés")
    return df_emails

def generer_email_alerte_churn(client):
    """
    Email d'alerte pour client à risque
    """
    
    sujet = f" ALERTE : {client['nom']} présente un risque de churn élevé"
    
    corps = f"""
    ALERTE ÉQUIPE MARKETING
    
    Client à risque détecté :
    
    Nom : {client['nom']}
    Email : {client['email']}
    Plan : {client['plan']}
    Score de risque : {client['score_risque']}/1.0
    
    Actions recommandées :
    - Contacter le client sous 48h
    - Proposer une offre personnalisée
    - Demander un feedback
    
    Ce message est généré automatiquement par le système.
    """
    
    return sujet, corps

def generer_alertes_equipe(df, seuil=0.7):
    """
    Génère des alertes pour l'équipe marketing
    """
    
    clients_risque = df[
        (df['statut'] == 'actif') & 
        (df['score_risque'] >= seuil)
    ]
    
    alertes = []
    
    for _, client in clients_risque.iterrows():
        sujet, corps = generer_email_alerte_churn(client)
        
        alerte = {
            'client_id': client['id'],
            'nom': client['nom'],
            'email': client['email'],
            'score_risque': client['score_risque'],
            'sujet': sujet,
            'corps': corps,
            'date_alerte': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        
        alertes.append(alerte)
    
    df_alertes = pd.DataFrame(alertes)
    df_alertes.to_csv('alertes_churn.csv', index=False, encoding='utf-8')
    
    print(f" {len(alertes)} alertes générées pour l'équipe")
    return df_alertes

# Test
if __name__ == "__main__":
    from calculs import charger_donnees
    
    df = charger_donnees()
    if df is not None:
        # Générer emails de relance
        print("\n GÉNÉRATION DES EMAILS DE RELANCE :")
        emails = simuler_envoi_emails(df)
        print(emails.head())
        
        # Générer alertes
        print("\n GÉNÉRATION DES ALERTES CHURN :")
        alertes = generer_alertes_equipe(df)
        print(alertes.head())