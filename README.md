# IntelligenceArtificiellePython
Ensemble de petits codes python relatif à l'IA

des notebooks à ouvrir avec [colab](https://colab.research.google.com) de préférence ou avec les notebooks de la suite [anaconda](https://www.anaconda.com/distribution/) : 


## Logique classique  
- **DP et DPPLL** : implémentez et optimiser les algorithmes classiques de résolution. Voir [ici le sujet](./TPOldSolver.md).

## Réseaux de neurones
### Eléments de définition
 petits exemples pour comprendre les réseaux simples
  - [TestET.ipynb](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/blob/master/TestET.ipynb)	: importance du neurone "BIAS" pour l'apprentissage :  exemple du  ET logique appris par un réseau de neurones avec tensorflow (notebook python).
  - [TestOUX.ipynb](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/blob/master/TestOUX.ipynb)	: importance d'une couche intermédiaire pour l'apprentissage :  exemple du  OU eXclusif logique appris par un réseau de neurones avec tensorflow (notebook python).
### Petits réseaux de démos
  - [DetectionSignes.ipynb](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/blob/master/DetectionSignesArithmetique.ipynb)	: petit notebook python montrant la définition d'un réseau de neurones avec tensorflow pour l'apprentissage de détection de signes arithmétiques.
  - [DetectionAlertes.ipynb](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/blob/master/DetectionAlertes.ipynb)   :  petit exercice en notebook python de la détection très simple de messages douteux par réseaux de neurones
  - [SolutionDetectionAlertes.ipynb](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/blob/master/SolutionDetectionAlertes.ipynb)   : solution au petit exercice en notebook python de la détection très simple de messages douteux par réseaux de neurones
  - [ClasserMail.ipynb](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/blob/master/ClasserMail.ipynb)   :  petit exercice en notebook python de la classification très simple de mails par réseaux de neurones
  - [SolutionClasserMail.ipynb](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/blob/master/SolutionClasserMail.ipynb)   : solution au petit exercice en notebook python de la classification très simple de mails par réseaux de neurones
  - [PredireReussite.ipynb](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/blob/master/PredireReussite.ipynb)   : Exercice de prédiction de réussite scolaire selon le contexte personnel et social
  - [PredireReussiteSolution.ipynb](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/blob/master/PredireReussiteSolution.ipynb)   : Solution à l'exercice de prédiction de réussite scolaire selon le contexte personnel et social. Solution où le réseau donne 1 seule valeur de sortie, à multiplier pour estimer la note à l'examen
  - [PredireReussiteSolutionBis.ipynb](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/blob/master/PredireReussiteSolutionBis.ipynb)   : Un autre solution à l'exercice de prédiction de réussite scolaire selon le contexte personnel et social. Solution où le réseau donne 8 valeurs de sortie, estimant les probabilité d'obtenir des notes entre Echec (neurone 0) et AA (neurone 7)
  
  
### Quasi deep-learning
  - [SolutionTPDetectionDeSentiments.ipynb](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/blob/master/SolutionTPDetectionDeSentiments.ipynb)	: notebook en python montrant l'apprentissage par réseaux de neurones pour la classification de textes.
  - [TPClassementDeTheses.ipynb](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/blob/master/TPClassementDeTheses.ipynb)	: notebook en python sur le TP de classement automatique de thèses scientifiques.
  - [TPFakeNews.ipynb](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/blob/master/TPFakeNews.ipynb)	: notebook en python sur le TP de classement automatique de fake news.
  - [TPChampis.ipynb](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/blob/master/TPChampis.ipynb)	: notebook en python sur le TP de classement automatique de champignons.
  - [TPProducts.ipynb](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/blob/master/TPProducts.ipynb)	: notebook en python sur le TP de classement automatique d'avis sur des produits.

### Réseaux récurrents
  - [memoryNN_rnn](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/blob/master/memoryNN_rnn.ipynb): notebook en python, démo de réseau LSTM pour l'apprentissage de courbes "simples" de valeurs 
  - [memoryNN_lstm](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/blob/master/memoryNN_lstm.ipynb): notebook en python, démo de réseau LSTM pour l'apprentissage de courbes de valeurs
  - [memoryNN_gru](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/blob/master/memoryNN_gru.ipynb): notebook en python, démo de réseau LSTM pour l'apprentissage de courbes de valeurs "simples"
  - [gru_text](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/blob/master/gru_text.ipynb): notebook en python, utilisation de réseau GRU pour l'apprentissage de texte 

### Hugging face
  - [introHuggingFace.ipynb](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/blob/master/introHuggingFace.ipynb): notebook en python sur le TP de découverte de Huggingface.
  - [introHuggingFaceDatasets.ipynb](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/blob/master/introHuggingFaceDatasets.ipynb): notebook en python pour expliquer la récupération de datasets à partir de Huggingface.


## Logique floue 
- [logique_floue.ipynb](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/blob/master/logique_floue.ipynb) : notebook python montrant l'utilisation de la logique floue pour prendre une décision sur l'urgence de freiner en fonction de la position et de la taille d'un piéton sur le trottoir. Les règles semblent peut complètes; proposer une amélioration...
- [choixSejourLogiqueFloue.ipynb](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/blob/master/choixSejourLogiqueFloue.ipynb)	: notebook python montrant l'utilisation de la logique floue pour prendre une décision sur la longueur de congés
- [IntrusionLogiqueFloueToDO.ipynb](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/blob/master/IntrusionLogiqueFloueToDO.ipynb)	: Petit exercice en notebook python montrant l'utilisation de la logique floue pour la détection d'intrusion
- [choixClimLogiqueFloue.ipynb](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/blob/master/choixClimLogiqueFloue.ipynb) : TP en notebook python sur l'aide à la décision pour la régulation d'un climatiseur.
- [choixActiviteLogiqueFloue.ipynb](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/blob/master/choixActiviteLogiqueFloue.ipynb) : TP en notebook python sur l'aide à la décision pour le choix de la durée d'une activité physique extérieure.
- [PerformanceLogiqueFloue.ipynb](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/blob/master/PerformanceLogiqueFloue.ipynb) : TP en notebook python sur l'aide à la prédiction sur la compétence d'une personne selon ses résultats et son comportement social.

## Machine Learning
- [TPMLIntroGym.ipynb](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/blob/master/TPMLIntroGym.ipynb) : présentation de l'environnement de test [Gym](https://gym.openai.com) (Open AI)

### Recuit Simulé
- [recuitSimule01.ipynb](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/blob/master/recuitSimule01.ipynb) : notebook python sur l'utilisation de l'algorithme du recuit simulé pour le problème du voyageur de commerce.

### Particles Swarm Optimization (PSO)
- [PSO.ipynb](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/blob/master/PSO.ipynb) : notebook python sur l'utilisation de l'algorithme de Particles Swam Optimisation (PSO) pour la recherche de la valeur minimale d'une fonction comportant de nombreux minima locaux.

### Algorithmes génétiques

- [MLGymGALunar.ipynb](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/blob/master/MLGymGALunar.ipynb) : sujet sur la réalisation d'un algo génétique pour l'environnement Lunar Lander.
- [MLGymGAMoutainCar.ipynb](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/blob/master/MLGymGAMoutainCar.ipynb) : sujet sur la réalisation d'un algo génétique pour l'environnement MoutainCar. 
<!-- [TPMLGymQLearning.ipynb](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/blob/master/TPMLGymQLearning.ipynb) : sujet sur la réalisation d'un algo de Q-Learning pour l'évolution dans un labyrinthe gelé de Gym.-->


### [QLearning](#tpqlearning) 
A partir d'un exemple de QLearning pour le problème du lac gelé de OpenAI : 
 - [GymFrozenLakeQLearning.ipynb](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/blob/master/GymFrozenLakeQLearning.ipynb) : solution au sujet de Q-Learning simple sur l'environnement "Lac Gelé" de Gym.
<!--- [GymFrozenLakeDoubleQLearning-Solution.ipynb](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/blob/master/GymFrozenLakeDoubleQLearning-Solution.ipynb) : solution au sujet de Double Q-Learning sur l'environnement "Lac Gelé" de Gym .-->

- implémentez le **Double QLearning**
  - vérifier la performance du simple QLearning vs le Double QLearning
- implémentez le **Delayed QLearning**
  - vérifier la performance du simple QLearning vs le Double QLearning vs le Delayed Q-Learning, et le Delayed Double QLearning
- Reprenez ces algorithmes que vous avez développés et appliquez-les sur l'environnement **CliffWalking-v0** (point 
  de départ en x, arrivée en T, coût de -1 par action sur o, -100 par action sur C).
    - attention, aucune récompense (reward) en arrivant sur le but.... 
    - Voir ici un exemple de sortie pour le [DoubleQLearning appliqué au CliffWalking](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/blob/master/GymCLIFFDoubleQLearningTODO.ipynb)

- Reprenez ces algorithmes que vous avez développés et appliquez-les sur l'environnement **Taxi-v3**.
  - Voir ici un exemple de sortie pour le [DoubleQLearning appliqué au Taxi](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/blob/master/GymTaxiDoubleQLearningTODO.ipynb)

- L'environnement frozenlake permet de montrer la performance du QLearning dans un environnement non déterministe, le 
  l'environnement CLiffWalking permet de montrer que le QLearning fonctionne même s'il n'y a aucune récompense, 
  l'environnement taxi montre la performance du QLearning pour construire *des* solutions.
---
- Donnez la forme de la matrice Q s'il fallait appliquer le Q-Learning à l'environnement **CartPole-v1**. Expliquez 
  ce qu'est le **Deep Q-Learning**.
- Expliquez comment le QLearning mixé à un algorithme de MCTS peut être utilisé dans le monde du gaming. Donnez des 
  exemples.

- Citez des exemples réels d'applications industrielles, commerciales du Q-Learning
----
