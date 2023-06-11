# BdeEnsisaAde

[![License](https://img.shields.io/github/license/bdensisa/ade)](LICENSE)
[![Issues](https://img.shields.io/github/issues/bdensisa/ade)]()
[![Pull Requests](https://img.shields.io/github/issues-pr/bdensisa/ade)]()
[![Code Size](https://img.shields.io/github/languages/code-size/bdensisa/ade)]()
[![CodeFactor](https://www.codefactor.io/repository/github/bdensisa/ade/badge)](https://www.codefactor.io/repository/github/bdensisa/ade)
[![Open Source Helpers](https://www.codetriage.com/bdensisa/ade/badges/users.svg)](https://www.codetriage.com/bdensisa/ade)

Scrapper d'ADE pour afficher les emplois du temps dans l'application du BDE.

## Installation

```bash
pip install -r requirements.txt
```

## Variables d'environnement

| Name        | Description         |
| ----------- | ------------------- |
| DB_HOST     | MySQL database host |
| DB_NAME     | MySQL database name |
| DB_USER     | MySQL user name     |
| DB_PASSWORD | MySQL user password |

## Structure de la base de données

```sql
CREATE TABLE `Users` (
  `id` varchar(32) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `option` varchar(255) NOT NULL,
  `year` varchar(255) NOT NULL,
  `expiration` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `UserCourses` (
  `ade_uid` varchar(255) NOT NULL,
  `user_id` varchar(32) NOT NULL,
  `title` text NOT NULL,
  `start` varchar(255) NOT NULL,
  `end` varchar(255) NOT NULL,
  `location` text NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`ade_uid`,`user_id`)
);
```

## Configuration

Pour accéder aux emplois du temps, il faut renseigner les identifiants de connexion à ADE dans le fichier `credentials.json`:

```json
{
    "username": "prenom.nom@uha.fr",
    "password": "MySuperPassword"
}
```
