import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

# Charger les données
data = pd.read_csv('nouveau_jumia_telephones.csv')

# Vérifier les colonnes
print("Colonnes du dataset:")
print(data.columns)

# Préparation des données
X = data.drop('prix', axis=1)
y = data['prix']

# Encodage des variables catégorielles
X = pd.get_dummies(X, columns=['nom_du_produit'])

# Séparer les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entraîner le modèle
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Sauvegarder le modèle et les colonnes
joblib.dump(model, 'model.pkl')
joblib.dump(X.columns.tolist(), 'model_columns.pkl')

# Vérifier la performance du modèle
train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)

print(f"Score d'entraînement: {train_score}")
print(f"Score de test: {test_score}")
print("Modèle et colonnes sauvegardés avec succès.")
