# 🌐 Ryu App - Gestionnaire de Règles OpenFlow

Une application web pour la gestion intuitive des règles de flux OpenFlow sur des contrôleurs réseau Ryu.

## 📋 Table des matières

- [À propos](#à-propos)
- [Fonctionnalités](#fonctionnalités)
- [Architecture](#architecture)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [API REST](#api-rest)
- [Structure du projet](#structure-du-projet)
- [Licence](#licence)

## 🎯 À propos

**Ryu App** est une interface de gestion graphique pour les contrôleurs réseau Ryu, permettant aux administrateurs réseau de :
- Visualiser l'état des commutateurs OpenFlow et leurs flux actifs
- Créer et configurer des règles de routage personnalisées
- Supprimer des règles existantes sans intervention en ligne de commande

Cette application repose sur l'architecture **Software-Defined Networking (SDN)** et communique avec l'API REST du contrôleur Ryu pour une gestion centralisée du trafic réseau.

## ✨ Fonctionnalités

### Interface Web (Flask)
- **Tableau de bord** : Affiche les commutateurs actifs et leurs flux en temps réel
- **Ajout de règles** : Formulaire intuitif pour créer des flux avec :
  - ID du commutateur (DPID)
  - Priorité de la règle
  - Critères de correspondance (port d'entrée, adresses MAC source/destination)
  - Port de sortie
- **Suppression de règles** : Suppression rapide des flux existants
- **Gestion d'erreurs** : Messages flash informatifs pour chaque action

### API REST (Ryu)
- `GET /stats/switches` : Liste des commutateurs connectés
- `GET /stats/flow/{dpid}` : Flux d'un commutateur spécifique
- `POST /stats/flowentry/add` : Ajouter un flux
- `POST /stats/flowentry/delete` : Supprimer un flux

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Flask Web Interface                       │
│              (templates/ + flask_app.py)                    │
└────────────────────┬────────────────────────────────────────┘
                     │
         HTTP Requests (REST API)
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Ryu Controller REST API                         │
│          (Port 8080 - localhost:8080)                       │
└────────────────────┬────────────────────────────────────────┘
                     │
         OpenFlow Protocol (1.3)
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│            Commutateurs OpenFlow (Switches)                 │
│              Gestion des flux réseau                        │
└─────────────────────────────────────────────────────────────┘
```

## 📦 Prérequis

- **Python 3.7+**
- **Ryu** : Contrôleur OpenFlow
- **Flask** : Framework web
- **Requests** : Client HTTP Python
- **Accès à une API REST Ryu** sur `http://localhost:8080`

## 🚀 Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/Uriel-Ondo/ryu_app.git
cd ryu_app
```

### 2. Créer un environnement virtuel (recommandé)

```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

Ou manuellement :
```bash
pip install flask requests ryu
```

## ⚙️ Configuration

### Démarrer le contrôleur Ryu

Avant de lancer l'application Flask, démarrez le contrôleur Ryu avec l'app de gestion des flux :

```bash
ryu-manager simple_flows_rest.py
```

L'API REST sera disponible sur `http://localhost:8080`

### Ajuster l'URL de l'API Ryu

Modifiez la variable `RYU_REST_API` dans `flask_app.py` si votre contrôleur Ryu s'exécute sur une autre adresse/port :

```python
RYU_REST_API = 'http://localhost:8080'  # À modifier selon votre configuration
```

### Clé secrète Flask

Modifiez la clé secrète dans `flask_app.py` pour la production :

```python
app.secret_key = 'your_secret_key'  # Remplacez par une clé forte
```

## 🎮 Utilisation

### Lancer l'application

```bash
python flask_app.py
```

L'application sera accessible sur `http://localhost:5000`

### Fonctionnalités principales

1. **Accueil** : Consultez tous les flux actifs sur vos commutateurs
2. **Ajouter une règle** : Cliquez sur "Ajouter un flux" et remplissez le formulaire
3. **Supprimer une règle** : Cliquez sur "Supprimer un flux" et sélectionnez la règle

## 🔌 API REST

### Endpoints Ryu

#### Lister les flux (GET)
```bash
curl http://localhost:8080/stats/flow/{dpid}
```

#### Ajouter un flux (POST)
```bash
curl -X POST http://localhost:8080/stats/flowentry/add \
  -H "Content-Type: application/json" \
  -d '{
    "dpid": 1,
    "priority": 100,
    "match": {
      "in_port": 1,
      "dl_src": "00:00:00:00:00:01",
      "dl_dst": "00:00:00:00:00:02"
    },
    "actions": [{"type": "OUTPUT", "port": 2}]
  }'
```

#### Supprimer un flux (POST)
```bash
curl -X POST http://localhost:8080/stats/flowentry/delete \
  -H "Content-Type: application/json" \
  -d '{
    "dpid": 1,
    "match": {
      "in_port": 1,
      "dl_src": "00:00:00:00:00:01",
      "dl_dst": "00:00:00:00:00:02"
    }
  }'
```

## 📁 Structure du projet

```
ryu_app/
├── flask_app.py              # Application Flask principale
├── simple_flows_rest.py      # Module Ryu pour l'API REST
├── templates/                # Templates HTML
│   ├── index.html           # Page d'accueil
│   ├── add_flow.html        # Formulaire d'ajout de flux
│   └── delete_flow.html     # Formulaire de suppression
├── README.md                # Ce fichier
├── LICENSE                  # Licence MIT
└── requirements.txt         # Dépendances Python
```

## 🔐 Sécurité

⚠️ **Recommandations pour la production** :
- Changez la clé secrète Flask
- Utilisez HTTPS (ajoutez SSL/TLS)
- Implémentez une authentification utilisateur
- Limitez l'accès à l'API REST du contrôleur Ryu
- Validez et sanitisez toutes les entrées utilisateur

## 🛠️ Dépannage

### L'API Ryu ne répond pas
- Vérifiez que le contrôleur Ryu est lancé : `ryu-manager simple_flows_rest.py`
- Vérifiez l'adresse/port dans `RYU_REST_API`
- Testez la connexion : `curl http://localhost:8080/stats/switches`

### Les flux ne s'affichent pas
- Assurez-vous qu'au moins un commutateur OpenFlow est connecté au contrôleur
- Vérifiez les logs du contrôleur Ryu

### Erreur 500 sur l'interface Flask
- Consultez les logs Flask pour les détails de l'erreur
- Vérifiez la connexion à l'API Ryu

## 📚 Ressources utiles

- [Documentation Ryu](https://ryu.readthedocs.io/)
- [OpenFlow 1.3 Specification](https://opennetworking.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Software-Defined Networking (SDN)](https://www.opennetworking.org/)

## 📝 Licence

Ce projet est sous licence **MIT**. Consultez le fichier [LICENSE](LICENSE) pour plus de détails.

---

**Auteur** : Uriel-Ondo  
**Créé** : Juin 2025  
**Dernière mise à jour** : Mars 2026
