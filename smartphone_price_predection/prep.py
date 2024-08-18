import pandas as pd
import re

# Fonction pour extraire la taille de l'écran, la RAM et le stockage à partir des spécifications
def extract_specs(specs):
    if not isinstance(specs, str):
        return {'screen_size': None, 'ram': None, 'storage': None}
    screen_size = re.search(r'(\d{1,2}\.\d{1,2})["\']', specs)
    ram = re.search(r'(\d+)\s*GB\s*RAM', specs, re.IGNORECASE)
    storage = re.search(r'(\d+)\s*GB\s*(?:ROM|Storage|Stockage)', specs, re.IGNORECASE)
    
    return {
        'screen_size': screen_size.group(1) if screen_size else None,
        'ram': ram.group(1) if ram else None,
        'storage': storage.group(1) if storage else None
    }

# Fonction pour extraire les mêmes informations à partir du nom du produit
def extract_from_name(name):
    if not isinstance(name, str):
        return {'screen_size': None, 'ram': None, 'storage': None}
    screen_size = re.search(r'(\d{1,2}\.\d{1,2})["\']', name)
    ram = re.search(r'(\d+)\s*GB\s*RAM', name, re.IGNORECASE)
    storage = re.search(r'(\d+)\s*GB\s*(?:ROM|Storage|Stockage)', name, re.IGNORECASE)
    
    return {
        'screen_size': screen_size.group(1) if screen_size else None,
        'ram': ram.group(1) if ram else None,
        'storage': storage.group(1) if storage else None
    }

# Chemin vers le fichier CSV
csv_file_path = 'jumia_telephones.csv'

# Lire le fichier CSV
df = pd.read_csv(csv_file_path)

# Appliquer les fonctions pour extraire les spécifications pour chaque ligne
specs_extracted = df['Spécifications'].apply(extract_specs).apply(pd.Series)
name_extracted = df['Nom du Produit'].apply(extract_from_name).apply(pd.Series)

# Renommer les colonnes extraites
specs_extracted.rename(columns={'screen_size': 'screen_size_specs', 'ram': 'ram_specs', 'storage': 'storage_specs'}, inplace=True)
name_extracted.rename(columns={'screen_size': 'screen_size_name', 'ram': 'ram_name', 'storage': 'storage_name'}, inplace=True)

# Combiner les spécifications extraites avec le dataframe original
df_combined = pd.concat([df, specs_extracted, name_extracted], axis=1)

# Choisir les valeurs non nulles entre les spécifications et le nom du produit
df_combined['taille_ecran'] = df_combined[['screen_size_specs', 'screen_size_name']].bfill(axis=1).iloc[:, 0]
df_combined['ram'] = df_combined[['ram_specs', 'ram_name']].bfill(axis=1).iloc[:, 0]
df_combined['stockage'] = df_combined[['storage_specs', 'storage_name']].bfill(axis=1).iloc[:, 0]

# Supprimer les colonnes intermédiaires
df_final = df_combined[['Nom du Produit', 'Prix', 'taille_ecran', 'ram', 'stockage']]

# Renommer les colonnes
df_final.rename(columns={
    'Nom du Produit': 'nom_du_produit',
    'Prix': 'prix',
    'taille_ecran': 'taille_ecran',
    'ram': 'ram',
    'stockage': 'stockage'
}, inplace=True)

# Supprimer les doublons de colonnes de RAM
df_final = df_final.loc[:,~df_final.columns.duplicated()]

# Sauvegarder le nouveau dataframe dans un fichier CSV
df_final.to_csv('nouveau_jumia_telephones.csv', index=False)

print("Extraction et sauvegarde terminées.")
