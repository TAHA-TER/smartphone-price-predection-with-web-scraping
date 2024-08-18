from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# Chemin vers votre WebDriver
driver_path = r'C:\Program Files (x86)\chromedriver.exe'

# Initialisation des options Chrome
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')

# Initialisation du service WebDriver
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Ouvrir la page de Jumia
    driver.get('https://www.jumia.ma/telephones-smartphones/')

    # Attendre un peu pour le chargement de la page
    time.sleep(5)

    # Initialiser la liste des produits
    jumia_products = []

    # Gérer la pagination et capturer les informations de tous les produits sur Jumia
    while True:
        try:
            # Attendre que les éléments soient chargés
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//a[@class="core"]'))
            )

            # Re-localiser les éléments des produits sur la page courante
            jumia_product_elements = driver.find_elements(By.XPATH, '//a[@class="core"]')
            for i in range(len(jumia_product_elements)):
                try:
                    # Re-localiser les éléments pour éviter l'erreur de référence d'élément obsolète
                    jumia_product_elements = driver.find_elements(By.XPATH, '//a[@class="core"]')
                    product_element = jumia_product_elements[i]
                    
                    # Capturer les informations de base
                    product_name = product_element.find_element(By.XPATH, './/h3[@class="name"]').text
                    product_price = product_element.find_element(By.XPATH, './/div[@class="prc"]').text

                    # Cliquer sur le produit pour accéder à la page de détails
                    driver.execute_script("arguments[0].click();", product_element)

                    # Attendre le chargement de la page de détails
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//div[@class="markup -pam"]'))
                    )

                    # Extraire les spécifications
                    try:
                        product_specifications = driver.find_element(By.XPATH, '//div[@class="markup -pam"]').text
                        # Remplacer les retours à la ligne par des espaces
                        product_specifications = product_specifications.replace('\n', ' ')
                    except:
                        product_specifications = "N/A"  # Si les spécifications ne sont pas disponibles

                    jumia_products.append((product_name, product_price, product_specifications))

                    # Retourner à la page précédente
                    driver.back()

                    # Attendre le chargement de la page des résultats
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//a[@class="core"]'))
                    )
                except Exception as e:
                    print(f"Erreur lors de la capture des informations du produit: {e}")
                    continue

            # Vérifier s'il y a une page suivante
            next_page = driver.find_elements(By.XPATH, '//a[@aria-label="Page suivante"]')
            if next_page:
                driver.execute_script("arguments[0].click();", next_page[0])
                # Attendre le chargement de la page suivante
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//a[@class="core"]'))
                )
            else:
                break  # Pas de page suivante, sortir de la boucle
        except Exception as e:
            print(f"Erreur lors de la capture des produits: {e}")
            break

    # Sauvegarder les données dans un fichier CSV
    with open('jumia_telephones.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nom du Produit', 'Prix', 'Spécifications'])
        writer.writerows(jumia_products)

    # Afficher les produits pour vérification
    for product in jumia_products:
        print(f"Produit sur Jumia : {product[0]}")
        print(f"Prix sur Jumia : {product[1]}")
        print(f"Spécifications sur Jumia : {product[2]}")

finally:
    # Fermer le navigateur à la fin
    driver.quit()
