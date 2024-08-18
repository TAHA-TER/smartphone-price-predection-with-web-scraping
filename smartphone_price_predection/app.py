from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)

# Charger le modèle et les colonnes
model = joblib.load('model.pkl')
model_columns = joblib.load('model_columns.pkl')

# Route pour afficher le formulaire de prédiction
@app.route('/')
def home():
    return render_template('index.html')

# Route pour effectuer les prédictions
@app.route('/predict', methods=['POST'])
def predict():
    try:
        marque = request.form.get('marque')
        screen_size = float(request.form.get('screen_size'))
        ram = int(request.form.get('ram'))
        stockage = int(request.form.get('stockage'))
        
        # Préparer les données pour la prédiction
        input_data = pd.DataFrame([[marque, screen_size, ram, stockage]], 
                                  columns=['nom_du_produit', 'taille_ecran', 'ram', 'stockage'])
        
        # Encodage de la variable catégorielle
        input_data = pd.get_dummies(input_data, columns=['nom_du_produit'])
        missing_cols = set(model_columns) - set(input_data.columns)
        for col in missing_cols:
            input_data[col] = 0
        input_data = input_data[model_columns]
        
        # Vérification des données d'entrée
        print("Données d'entrée après encodage et alignement:")
        print(input_data)
        
        # Vérifier les types de données
        print("Types des données:")
        print(input_data.dtypes)
        
        # Vérifier les valeurs manquantes
        print("Valeurs manquantes:")
        print(input_data.isnull().sum())
        
        if not all([np.issubdtype(input_data[col].dtype, np.number) for col in input_data.columns]):
            raise ValueError("Les données d'entrée contiennent des valeurs non numériques")
        
        if input_data.isnull().values.any():
            raise ValueError("Les données d'entrée contiennent des valeurs manquantes")
        
        # Faire la prédiction
        prediction = model.predict(input_data)[0]
        
        print(f"Prédiction: {prediction}")
        
        return render_template('index.html', prediction_text=f'Prix estimé du téléphone: {prediction:.2f} DHS')
    
    except Exception as e:
        return render_template('index.html', prediction_text=f'Erreur: {e}')

if __name__ == "__main__":
    app.run(debug=True)
