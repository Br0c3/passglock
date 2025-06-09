# PassGlock

PassGlock est un gestionnaire de mots de passe sécurisé développé dans l'intention de ne sauvegarder aucun mot de passe coté serveur.

## Fonctionnalités

- Stockage sécurisé des mots de passe dans des fichiers sous la responsabilité de l'utilisateur
- Chiffrement des données sensibles
- Interface utilisateur simple d’utilisation
- Génération de mots de passe forts

## Chiffrement

Les mots de passe sont chiffré d'une manière plutôt originale en utilisant un dizaine d'algorithmes de chiffrement dans un ordre différent en fonction de la clé d'ordre générer a partie du mot de passe d l'utilisateur. 

Ainsi chaque coffre est chiffrer d'une manière différente . Et pour rajouter une couche de sécurité, les mots de passe chiffrés sont encore chiffrés avec un chiffrement AES. 

## Utilisation

1. Lancez l’application en allant sur le lien :https://passglock.onrender.com/
   
2. Suivez les instructions à l’écran pour créer et télécharger vos coffres.

## Dépendances

- Python 3.10
- cryptography 43.0.0
- Django 5.1
- tabulate 0.9.0
- tailwindcss cli 4.1.8
- daisyui

Installez les dépendances avec :
```bash
pip install -r requirements.txt
npm init -y
npm install tailwindcss @tailwindcss/cli
npm i -D daisyui@latest
```


## Sécurité

- Les mots de passe sont chiffrés et ne sont absolument pas stocké.
- Les mots de passe sont mis sous l'entière responsabilité de l'utilisateur.
- Utilisez un mot de passe maître fort pour protéger l’accès à vos données.

## Contribution

Les contributions sont les bienvenues ! Veuillez ouvrir une issue ou une pull request.

## Licence

Ce projet est sous licence MIT.
