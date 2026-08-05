PRAGMA foreign_keys = OFF;

DROP TABLE IF EXISTS projets;
DROP TABLE IF EXISTS employes;
DROP TABLE IF EXISTS services;
DROP TABLE IF EXISTS departements_france;

PRAGMA foreign_keys = ON;

CREATE TABLE departements_france (
    code_insee VARCHAR(3) PRIMARY KEY,
    nom_departement VARCHAR(100) NOT NULL,
    region VARCHAR(100) NOT NULL
);

CREATE TABLE services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_service VARCHAR(100) NOT NULL UNIQUE,
    budget INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE employes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    salaire INTEGER NOT NULL,
    date_embauche DATE NOT NULL,
    service_id INTEGER,
    manager_id INTEGER,
    code_departement_naissance VARCHAR(3),
    FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE SET NULL,
    FOREIGN KEY (manager_id) REFERENCES employes(id) ON DELETE SET NULL,
    FOREIGN KEY (code_departement_naissance) REFERENCES departements_france(code_insee)
);

CREATE TABLE projets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_projet VARCHAR(100) NOT NULL,
    budget_alloue INTEGER NOT NULL,
    statut VARCHAR(20) CHECK(statut IN ('EN_COURS', 'TERMINE', 'EN_ATTENTE')) DEFAULT 'EN_COURS',
    chef_projet_id INTEGER,
    FOREIGN KEY (chef_projet_id) REFERENCES employes(id) ON DELETE SET NULL
);