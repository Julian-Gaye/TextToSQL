INSERT INTO departements_france (code_insee, nom_departement, region) VALUES
('75', 'Paris', 'Île-de-France'),
('69', 'Rhône', 'Auvergne-Rhône-Alpes'),
('13', 'Bouches-du-Rhône', 'Provence-Alpes-Côte d''Azur'),
('59', 'Nord', 'Hauts-de-France'),
('33', 'Gironde', 'Nouvelle-Aquitaine');

INSERT INTO services (nom_service, budget) VALUES
('Direction Générale', 500000),
('Tech & Data', 350000),
('Marketing & Com', 150000),
('Ressources Humaines', 100000);

INSERT INTO employes (id, nom, prenom, email, salaire, date_embauche, service_id, manager_id, code_departement_naissance) VALUES
(1, 'Eiffel', 'Gustave', 'g.eiffel@entreprise.com', 120000, '2018-01-15', 1, NULL, '75');

INSERT INTO employes (id, nom, prenom, email, salaire, date_embauche, service_id, manager_id, code_departement_naissance) VALUES
(2, 'Lovelace', 'Ada', 'a.lovelace@entreprise.com', 85000, '2019-03-01', 2, 1, '69'),
(3, 'Bernays', 'Edward', 'e.bernays@entreprise.com', 75000, '2020-06-15', 3, 1, '75');

INSERT INTO employes (id, nom, prenom, email, salaire, date_embauche, service_id, manager_id, code_departement_naissance) VALUES
(4, 'Turing', 'Alan', 'a.turing@entreprise.com', 65000, '2021-09-01', 2, 2, '75'),
(5, 'Hamilton', 'Margaret', 'm.hamilton@entreprise.com', 62000, '2022-01-10', 2, 2, '33');

INSERT INTO employes (id, nom, prenom, email, salaire, date_embauche, service_id, manager_id, code_departement_naissance) VALUES
(6, 'Ogilvy', 'David', 'd.ogilvy@entreprise.com', 50000, '2022-05-20', 3, 3, '13'),
(7, 'Gainsbourg', 'Jane', 'j.gainsbourg@entreprise.com', 48000, '2023-02-14', 3, 3, '59');

INSERT INTO projets (nom_projet, budget_alloue, statut, chef_projet_id) VALUES
('Refonte Plateforme Cloud', 120000, 'EN_COURS', 2),
('Implémentation LLM SQL', 45000, 'EN_COURS', 4),
('Campagne Rebranding Q4', 30000, 'TERMINE', 3),
('Programme Bien-être au travail', 10000, 'EN_ATTENTE', 1);