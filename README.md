# Classification d'images - Apprentissage supervisé - Scikit Learn

Mise en place d'un model de machine learning sur la classification d'images.
Le model essaye de prédire si l'image que l'on lui fait passer en entrée est une tête de chien, de chat, d'ours etc.
Le taux de précision est au-delà des 80% lorsque l'image passée en entrée correspond à celles avec lesquelles il a été entrainé, autrement dit il faut que l'image soit belle est bien une tête d'animal centrée au premier plan.

## Process
- Récupération/création d'un dataset labelisé qui contient des images de tête d'animaux
- Pre processing des données : redimension, RGB -> grayscale, Histogramme de gradient orienté (HOG)
- Entrainement et optimisation d'un model avec l'estimateur SVM
- Deploiement du model sur un dashboard public

Un jupyter notebook est accesible, il reprend les étapes ci-dessus de manière plus approfondie.
Le déploiement est effectué grace à heroku et est accessible [ici](https://image-head-classifier.herokuapp.com/)
___

<img width="100%" src="https://user-images.githubusercontent.com/73102263/107666945-6412aa00-6c8f-11eb-8c22-c5f146d7125d.jpg"/>