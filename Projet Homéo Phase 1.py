#!/usr/bin/env python
# coding: utf-8

# In[1]:


file_path = "C:/Users/sencr_g7t30st/Documents/Projet IA Homéopathie/Data_test.txt"

# Lire le contenu du fichier
with open(file_path, "r", encoding="utf-8") as file:
    lines = file.readlines()


# In[3]:


#print(lines)


# In[5]:


# Initialisation des tables
remedies = set()  # Stockage des remèdes uniques
symptoms = set()  # Stockage des symptômes uniques
remedy_symptom = []  # Liens entre remèdes et symptômes

# Variables de suivi
current_remedy = None

# Parcours des lignes du fichier
for line in lines:
    line = line.strip()  # Suppression des espaces et sauts de ligne
    #print(line)
    if line.startswith("#"):  # Remède ou catégorie de symptômes
        if "]" in line:  # Cas où il y a un crochet dans la ligne pour identifier les remedes
            #current_remedy = line.split(" ")[0][1:]
            #remedies.add(current_remedy)
            current_remedy = line[1:]
            remedies.add(line[1:])
    elif line.startswith("-") and current_remedy:  # Symptôme associé à un remède
        symptom = line[1:].strip()
        symptoms.add(symptom)
        remedy_symptom.append((current_remedy, symptom))

# Affichage des résultats partiels
len(remedies), len(symptoms), len(remedy_symptom)


# In[6]:


#print(remedies)


# In[8]:


#print(symptoms)


# In[19]:


#print(remedy_symptom)


# In[10]:


import sqlite3

# Connexion à la base de données (création si inexistante)
conn = sqlite3.connect("C:/Users/sencr_g7t30st/Documents/Projet IA Homéopathie/ProjectHomeo.db")
cursor = conn.cursor()

# Création des tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS remedies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS symptoms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT UNIQUE NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS remedy_symptom (
    remedy_id INTEGER,
    symptom_id INTEGER,
    FOREIGN KEY (remedy_id) REFERENCES remedies(id),
    FOREIGN KEY (symptom_id) REFERENCES symptoms(id),
    PRIMARY KEY (remedy_id, symptom_id)
)
""")


# In[ ]:





# In[ ]:





# In[12]:


# Insertion des remèdes
#remedies = ["Abies canadensis", "Abrotanum", "Aconitum napellus", "Actaea racemosa", "Agaricus muscarius", "Agnus castus", "Ailanthus glandulosa", "Allium cepa", "Aloe socotrina"]
cursor.executemany("INSERT OR IGNORE INTO remedies (name) VALUES (?)", [(r,) for r in remedies])

# Insertion des symptômes
#symptoms = ["Anxiété intense", "Peur de la mort", "Vertiges au réveil", "Douleurs musculaires", "Sensation de brûlure dans l'estomac"]
cursor.executemany("INSERT OR IGNORE INTO symptoms (description) VALUES (?)", [(s,) for s in symptoms])

# Insertion des relations remède-symptôme
#remedy_symptom = [(1, 1), (1, 2), (2, 3), (3, 4), (4, 5)]
cursor.executemany("INSERT OR IGNORE INTO remedy_symptom (remedy_id, symptom_id) VALUES (?, ?)", remedy_symptom)

# Valider et fermer la connexion
conn.commit()
conn.close()

print("Base de données créée et alimentée avec succès !")


# In[17]:


import sqlite3
import pandas as pd

def export_tables_to_csv(db_path='ProjectHomeo.db', output_dir='./'):
    # Connexion à la base de données SQLite
    conn = sqlite3.connect(db_path)
    
    # Liste des tables à exporter
    tables = ['remedies', 'symptoms', 'remedy_symptom']
    
    for table in tables:
        df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
        output_path = f"{output_dir}/{table}.csv"
        df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"✅ Table {table} exportée vers {output_path}")

    # Fermeture de la connexion
    conn.close()


# In[18]:


export_tables_to_csv(db_path='C:/Users/sencr_g7t30st/Documents/Projet IA Homéopathie/ProjectHomeo.db', output_dir='Exports')


# In[ ]:




