# TextToSQL — Agent IA de Langage Naturel vers SQL

> Transforme des questions en langage naturel en requêtes SQL validées et sécurisées grâce à un pipeline multi-agents LangGraph.

---

## Présentation

**TextToSQL** est une application agentique qui prend une question utilisateur en langage naturel et génère, valide, puis exécute automatiquement la requête SQL correspondante sur une base de données SQLite.

Le pipeline est construit avec **LangGraph** et orchestre deux agents LLM spécialisés (générateur et validateur) connectés au sein d'un graphe à état, avec une logique de réessai automatique, une vérification syntaxique et des sorties structurées.

---

## Fonctionnalités

- **Agent Générateur** — Génère une requête SQL `SELECT` à partir d'une question en langage naturel, en utilisant des outils pour inspecter le schéma et les valeurs réelles de la base.
- **Vérification Syntaxique** — Valide la requête syntaxiquement via `EXPLAIN QUERY PLAN` de SQLite, avant toute évaluation par un agent.
- **Agent Validateur** — Un second agent LLM qui vérifie la *logique métier* de la requête : jointures correctes, filtres appropriés, fidélité à l'intention de l'utilisateur.
- **Boucle d'auto-correction** — Si la requête est syntaxiquement incorrecte ou logiquement erronée, le graphe la régénère automatiquement (jusqu'à 3 tentatives).
- **Garde de Sécurité** — Les instructions `DELETE`, `DROP`, `UPDATE` et `INSERT` sont bloquées avant toute exécution.
- **Sorties Structurées** — Les deux agents utilisent des modèles Pydantic pour garantir des réponses typées et validées par schéma.

---

## Schéma du Graphe

```mermaid
flowchart TD
    START(["▶ DÉBUT"]):::startNode

    subgraph LOOP ["🔄 Boucle de Génération"]
        direction LR
        GEN["🤖 agent_generator\nGénère la requête SQL"]:::agentNode
        TOOLS["🔧 tools\n· get_schema\n· get_distinct_values"]:::toolNode
        GEN <-->|"appels d'outils"| TOOLS
    end

    SYN{{"⚙️ check_syntax\nEXPLAIN QUERY PLAN"}}:::syntaxNode
    VAL["✅ agent_validator\nVérifie la logique métier"]:::agentNode
    EXEC["▶ execute_sql\nExécute la requête SQLite"]:::execNode
    END_OK(["🟢 FIN — Succès"]):::successNode
    END_ERR1(["🔴 FIN — Échec"]):::failNode
    END_ERR2(["🔴 FIN — Échec"]):::failNode

    START --> GEN
    GEN -- "terminé ✅" --> SYN

    SYN -- "✅ valide" --> VAL
    SYN -- "❌ erreur syntaxique\ntentatives < 3" --> GEN
    SYN -- "❌ tentatives ≥ 3" --> END_ERR1

    VAL -- "✅ valide" --> EXEC
    VAL -- "❌ erreur logique/métier\ntentatives < 3" --> GEN
    VAL -- "❌ tentatives ≥ 3" --> END_ERR2

    EXEC --> END_OK

    classDef startNode   fill:#22c55e,color:#fff,stroke:none,font-weight:bold
    classDef agentNode   fill:#6366f1,color:#fff,stroke:#818cf8,stroke-width:2px
    classDef toolNode    fill:#3b82f6,color:#fff,stroke:#60a5fa,stroke-width:2px
    classDef syntaxNode  fill:#f59e0b,color:#000,stroke:#fbbf24,stroke-width:2px
    classDef execNode    fill:#10b981,color:#fff,stroke:#34d399,stroke-width:2px
    classDef failNode    fill:#ef4444,color:#fff,stroke:none
    classDef successNode fill:#22c55e,color:#fff,stroke:none
```

---

## Stack Technique

| Bibliothèque | Utilisation |
|---|---|
| [LangGraph](https://github.com/langchain-ai/langgraph) | Orchestration du graphe multi-agents avec état |
| [LangChain](https://github.com/langchain-ai/langchain) | Création des agents, binding des outils, templates de prompts |
| [Google Gemini](https://ai.google.dev/) (`gemini-3.1-flash-lite`) | LLM sous-jacent pour les deux agents |
| [Pydantic](https://docs.pydantic.dev/) | Validation des sorties structurées |
| [SQLite](https://www.sqlite.org/) | Base de données relationnelle locale |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Gestion des variables d'environnement |

---

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/your-username/TextToSQL.git
cd TextToSQL
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Configurer la clé API

Créez un fichier `.env` à la racine du projet :

```env
GOOGLE_API_KEY=votre_clé_api_google_ici
```

> Obtenez une clé API gratuite sur [aistudio.google.com](https://aistudio.google.com/).

### 4. Lancer l'application

```bash
python main.py
```

---

## Exemple d'utilisation

**Entrée :**
```
Donne moi la liste des personnes qui travaillent dans la tech
```

**Trace d'exécution :**
```
Agent Générateur
  → Utilisation du tool 'get_schema'
  → Utilisation du tool 'get_distinct_values'
Vérification syntaxique
Agent Validateur
  → Utilisation du tool 'get_schema'
  → Utilisation du tool 'get_distinct_values'
Exécution requête
```

**Résultat :**
```sql
SELECT e.nom, e.prenom
FROM employes e
JOIN services s ON e.service_id = s.id
WHERE s.nom_service = 'Tech & Data';
```
```
Résultats : [('Lovelace', 'Ada'), ('Turing', 'Alan'), ('Hamilton', 'Margaret')]
```

---

## Schéma de la Base de Données

```mermaid
erDiagram
    DEPARTEMENTS_FRANCE {
        VARCHAR code_insee PK
        VARCHAR nom_departement
        VARCHAR region
    }

    SERVICES {
        INTEGER id PK
        VARCHAR nom_service
        INTEGER budget
    }

    EMPLOYES {
        INTEGER id PK
        VARCHAR nom
        VARCHAR prenom
        VARCHAR email
        INTEGER salaire
        DATE date_embauche
        INTEGER service_id FK
        INTEGER manager_id FK
        VARCHAR code_departement_naissance FK
    }

    PROJETS {
        INTEGER id PK
        VARCHAR nom_projet
        INTEGER budget_alloue
        VARCHAR statut
        INTEGER chef_projet_id FK
    }

    SERVICES ||--o{ EMPLOYES : "contient"
    DEPARTEMENTS_FRANCE ||--o{ EMPLOYES : "lieu_naissance"
    EMPLOYES ||--o{ EMPLOYES : "manage"
    EMPLOYES ||--o{ PROJETS : "dirige"
```