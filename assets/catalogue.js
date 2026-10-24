/* =====================================================================
   Catalogue des ressources du site IntelligenceArtificiellePython
   ---------------------------------------------------------------------
   Pour ajouter un notebook : copier une entrée existante dans le bon
   thème / groupe, puis adapter. Les champs :

     file      chemin du fichier dans le dépôt (obligatoire)
     title     titre lisible
     type      "demo" | "exo" | "tp" | "td" | "sujet" | "cours"
     desc      une ou deux phrases
     libs      bibliothèques principales (affichées en étiquettes)
     data      fichiers de données / scripts à placer à côté
     solutions [{ file, title }]  corrigés rattachés à l'exercice
     lang      "en" si le support est en anglais
     note      remarque courte (prérequis, installation...)

   Les liens Colab et GitHub sont construits automatiquement à partir
   de "file" (Colab uniquement pour les .ipynb).
   ===================================================================== */

window.SITE = {
  repo: "EmmanuelADAM/IntelligenceArtificiellePython",
  branch: "master",
  author: "Emmanuel Adam",
};

window.CATALOGUE = [
  /* ---------------------------------------------------------------- */
  {
    id: "logique",
    title: "Logique classique",
    tagline: "Satisfiabilité, DP, DPLL",
    intro:
      "Encoder un problème en formule booléenne, puis écrire et accélérer les solveurs historiques.",
    groups: [
      {
        title: "Sujets",
        items: [
          {
            file: "TPOldSolver.md",
            title: "Solveurs DP et DPLL",
            type: "sujet",
            desc: "Optimiser l'algorithme de Davis-Putnam fourni, implémenter DPLL avec propagation unitaire, puis retourner le modèle trouvé.",
            libs: ["Python"],
            data: ["DavisPutman.py", "uf50.zip", "uuf50.zip", "uuf150-01.cnf"],
          },
          {
            file: "TPComplexBooleen.md",
            title: "Coloration de graphes et sudoku en SAT",
            type: "sujet",
            desc: "Traduire une coloration de carte à 4 couleurs puis un sudoku en clauses, et les faire résoudre par un solveur.",
            libs: ["Python"],
            data: ["sudoku.png", "sudokuARemplir.png"],
          },
        ],
      },
    ],
  },

  /* ---------------------------------------------------------------- */
  {
    id: "neurones",
    title: "Réseaux de neurones",
    tagline: "Du ET logique au texte",
    intro:
      "On part d'un seul neurone qui apprend le ET, on comprend pourquoi le OU exclusif exige une couche cachée, puis on classe des données, des textes et des séquences.",
    groups: [
      {
        title: "Premiers neurones",
        items: [
          {
            file: "TestET.ipynb",
            title: "Apprendre le ET logique",
            type: "demo",
            desc: "Un réseau minimal apprend le ET. Montre le rôle du neurone de biais dans l'apprentissage.",
            libs: ["TensorFlow"],
          },
          {
            file: "TestOUX.ipynb",
            title: "Apprendre le OU exclusif",
            type: "demo",
            desc: "Le XOR n'est pas linéairement séparable : il faut une couche intermédiaire.",
            libs: ["TensorFlow"],
          },
          {
            file: "TestET-TensorBoard.ipynb",
            title: "Le ET suivi dans TensorBoard",
            type: "demo",
            desc: "Même exemple que le ET, avec les courbes d'apprentissage affichées dans TensorBoard.",
            libs: ["TensorFlow", "TensorBoard"],
          },
        ],
      },
      {
        title: "Classer des données",
        items: [
          {
            file: "DetectionSignesArithmetique.ipynb",
            title: "Reconnaître des signes arithmétiques",
            type: "demo",
            desc: "Un réseau apprend à distinguer +, −, × et ÷ dessinés sur une grille de 3×3 pixels.",
            libs: ["TensorFlow"],
          },
          {
            file: "DetectionAlertes.ipynb",
            title: "Détecter des messages douteux",
            type: "exo",
            desc: "Repérer les mails douteux à partir des seuls mots-clés de leur sujet.",
            libs: ["TensorFlow"],
            solutions: [
              { file: "SolutionDetectionAlertes.ipynb", title: "Corrigé" },
              { file: "SolutionDetectionAlertesTensorBoard.ipynb", title: "Corrigé avec TensorBoard" },
            ],
          },
          {
            file: "ClasserMail.ipynb",
            title: "Classer des mails",
            type: "exo",
            desc: "Ranger automatiquement des mails par catégorie d'après les mots-clés de leur sujet.",
            libs: ["TensorFlow"],
            solutions: [{ file: "SolutionClasserMail.ipynb", title: "Corrigé" }],
          },
          {
            file: "PredireReussite.ipynb",
            title: "Prédire la réussite scolaire",
            type: "exo",
            desc: "Estimer la note d'un étudiant à partir de son contexte personnel et social.",
            libs: ["TensorFlow"],
            data: ["student_prediction_td.csv"],
          },
          {
            file: "TDTitanic.ipynb",
            title: "Survie sur le Titanic",
            type: "td",
            desc: "Normaliser les données des passagers avec Pandas, puis prédire leur chance de survie.",
            libs: ["TensorFlow", "Pandas"],
          },
          {
            file: "TPChampis.ipynb",
            title: "Champignons comestibles ou toxiques",
            type: "tp",
            desc: "Tester cinq architectures pour prédire la comestibilité d'un champignon à partir de ses caractéristiques.",
            libs: ["TensorFlow", "TensorBoard"],
            data: ["mushrooms.csv"],
          },
        ],
      },
      {
        title: "Classer des textes",
        intro: "Représentation en sac de mots, puis classification par réseau dense.",
        items: [
          {
            file: "SolutionTPDetectionDeSentiments.ipynb",
            title: "Détecter le sentiment d'une critique",
            type: "demo",
            desc: "Exemple complet sur des critiques de films : nettoyage, vocabulaire, sac de mots, apprentissage.",
            libs: ["TensorFlow", "NLTK"],
          },
          {
            file: "TPFakeNews.ipynb",
            title: "Repérer les fake news",
            type: "tp",
            desc: "Prédire si un article est une fausse information.",
            libs: ["TensorFlow", "NLTK"],
            data: ["train.csv", "test.csv"],
          },
          {
            file: "TPFakeSMS.ipynb",
            title: "Repérer les SMS frauduleux",
            type: "tp",
            desc: "Distinguer les SMS légitimes du spam.",
            libs: ["TensorFlow", "NLTK"],
          },
          {
            file: "TPProducts.ipynb",
            title: "Classer des avis produits",
            type: "tp",
            desc: "Prédire la note et la catégorie d'un produit à partir du texte des commentaires.",
            libs: ["TensorFlow", "NLTK"],
            data: ["train.csv"],
          },
          {
            file: "TPClassementDeTheses.ipynb",
            title: "Classer des thèses scientifiques",
            type: "tp",
            desc: "Classer des thèses soutenues en France (archives TEL) à partir de leur texte.",
            libs: ["TensorFlow", "NLTK"],
            data: ["TPClassementTheses.ods", "Traitement des theses.ods"],
          },
          {
            file: "TPClassificationLivres.ipynb",
            title: "Classer des critiques de livres",
            type: "tp",
            desc: "Même démarche sur des commentaires de livres rédigés en français.",
            libs: ["TensorFlow", "NLTK", "Pandas"],
          },
        ],
      },
      {
        title: "Réseaux convolutifs et récurrents",
        items: [
          {
            file: "petitConvolutif.ipynb",
            title: "Un petit réseau convolutif",
            type: "demo",
            desc: "Reconnaître des chiffres manuscrits du jeu de données MNIST avec un réseau convolutif Keras.",
            libs: ["TensorFlow"],
          },
          {
            file: "memoryNN_rnn.ipynb",
            title: "RNN : prolonger une courbe",
            type: "demo",
            desc: "Un réseau récurrent simple prédit la valeur suivante d'une courbe.",
            libs: ["TensorFlow"],
          },
          {
            file: "memoryNN_lstm.ipynb",
            title: "LSTM : prolonger une courbe",
            type: "demo",
            desc: "Même tâche avec des cellules LSTM, sur des séries de 20 valeurs.",
            libs: ["TensorFlow"],
          },
          {
            file: "memoryNN_gru.ipynb",
            title: "GRU : prolonger une courbe",
            type: "demo",
            desc: "Même tâche avec des cellules GRU, plus légères.",
            libs: ["TensorFlow"],
          },
          {
            file: "gru_text.ipynb",
            title: "GRU : prédire le mot suivant",
            type: "demo",
            desc: "Construction d'un vocabulaire puis génération de texte mot à mot.",
            libs: ["TensorFlow"],
          },
        ],
      },
      {
        title: "Modèles pré-entraînés et langage",
        items: [
          {
            file: "introHuggingFace.ipynb",
            title: "Découvrir Hugging Face",
            type: "demo",
            desc: "Utiliser en quelques lignes des modèles déjà entraînés : vocabulaire, tokenisation, réseau et restitution du résultat.",
            libs: ["transformers"],
          },
          {
            file: "introHuggingFaceDatasets.ipynb",
            title: "Récupérer des jeux de données",
            type: "demo",
            desc: "Charger et explorer les datasets publiés sur Hugging Face.",
            libs: ["datasets", "Pandas"],
          },
          {
            file: "introHuggingFaceTD.ipynb",
            title: "TD Hugging Face",
            type: "td",
            desc: "Mettre en pratique les pipelines Hugging Face sur vos propres exemples.",
            libs: ["transformers"],
          },
          {
            file: "resume.ipynb",
            title: "Résumé automatique",
            type: "demo",
            desc: "Résumé par extraction des phrases les plus importantes, sur un extrait des Misérables.",
            libs: ["spaCy"],
          },
        ],
      },
    ],
  },

  /* ---------------------------------------------------------------- */
  {
    id: "floue",
    title: "Logique floue",
    tagline: "Décider avec des règles vagues",
    intro:
      "Des variables comme « proche », « chaud » ou « populaire », des règles SI… ALORS…, et une décision chiffrée en sortie. Tous les notebooks utilisent scikit-fuzzy.",
    groups: [
      {
        title: "Démonstrations",
        items: [
          {
            file: "logique_floue.ipynb",
            title: "Freiner devant un piéton",
            type: "demo",
            desc: "Urgence de freinage selon la position et la taille d'un piéton. Les règles sont incomplètes : à vous de les améliorer.",
            libs: ["skfuzzy"],
          },
          {
            file: "choixSejourLogiqueFloue.ipynb",
            title: "Durée d'un séjour",
            type: "exo",
            desc: "Choisir la durée d'une location de vacances selon la météo prévue et le prix du loyer.",
            libs: ["skfuzzy"],
            solutions: [{ file: "choixSejourLogiqueFloueSolution.ipynb", title: "Corrigé" }],
          },
        ],
      },
      {
        title: "Exercices et TP",
        items: [
          {
            file: "IntrusionLogiqueFloueToDO.ipynb",
            title: "Détecter une intrusion",
            type: "exo",
            desc: "Évaluer le niveau de menace d'après le nombre de connexions et le taux de paquets invalides.",
            libs: ["skfuzzy"],
          },
          {
            file: "choixClimLogiqueFloue.ipynb",
            title: "Régler un climatiseur",
            type: "tp",
            desc: "Choisir l'action d'un climatiseur à partir de la température ambiante et de la température souhaitée.",
            libs: ["skfuzzy"],
          },
          {
            file: "choixActiviteLogiqueFloue.ipynb",
            title: "Durée d'une activité en extérieur",
            type: "tp",
            desc: "Doser l'intensité d'une activité physique selon le ciel, la température et le vent.",
            libs: ["skfuzzy"],
          },
          {
            file: "PerformanceLogiqueFloue.ipynb",
            title: "Évaluer une compétence",
            type: "tp",
            desc: "Combiner résultats d'examen et soft skills pour estimer la performance d'une personne.",
            libs: ["skfuzzy"],
          },
          {
            file: "bienEtreFloue.ipynb",
            title: "Prévoir le bien-être physique",
            type: "tp",
            desc: "Estimer le bien-être à partir de l'alimentation, de l'exercice et du sommeil.",
            libs: ["skfuzzy"],
          },
          {
            file: "recommandationFloue.ipynb",
            title: "Recommander un film",
            type: "tp",
            desc: "Recommander un film selon la note des critiques et sa popularité.",
            libs: ["skfuzzy"],
          },
        ],
      },
    ],
  },

  /* ---------------------------------------------------------------- */
  {
    id: "optimisation",
    title: "Optimisation et évolution",
    tagline: "Recuit, essaims, génétique",
    intro:
      "Chercher une bonne solution sans tout explorer : recuit simulé, essaims particulaires, puis algorithmes génétiques qui font évoluer des contrôleurs dans les environnements Gymnasium.",
    groups: [
      {
        title: "Métaheuristiques",
        items: [
          {
            file: "recuitSimule01.ipynb",
            title: "Recuit simulé et voyageur de commerce",
            type: "demo",
            desc: "Tant que la température est haute, on accepte de moins bonnes solutions pour sortir des minima locaux.",
            libs: ["NumPy", "Matplotlib"],
          },
          {
            file: "PSO.ipynb",
            title: "Essaim particulaire (PSO)",
            type: "demo",
            desc: "Un essaim cherche le minimum de la fonction de Rastrigin, truffée de minima locaux.",
            libs: ["NumPy", "Matplotlib"],
            data: ["mylib_rastrigin.py"],
          },
        ],
      },
      {
        title: "Algorithmes génétiques sur Gymnasium",
        items: [
          {
            file: "TPMLIntroGym.ipynb",
            title: "Prise en main de Gymnasium",
            type: "demo",
            desc: "États, actions, récompenses : le fonctionnement des environnements utilisés dans la suite.",
            libs: ["Gymnasium"],
            note: "Prérequis pour les algorithmes génétiques et le Q-Learning.",
          },
          {
            file: "MLGymGA.ipynb",
            title: "Un algorithme génétique pas à pas",
            type: "demo",
            desc: "Population, sélection, croisement, mutation appliqués à un environnement Gym.",
            libs: ["Gym"],
          },
          {
            file: "TPMLGymGA-CarttPole.ipynb",
            title: "Équilibrer le CartPole",
            type: "tp",
            desc: "Faire évoluer une politique qui maintient le bâton en équilibre.",
            libs: ["Gym"],
            solutions: [{ file: "TPMLGymGA-Solution.ipynb", title: "Corrigé générique" }],
          },
          {
            file: "MLGymGAMoutainCar.ipynb",
            title: "Hisser la Mountain Car",
            type: "tp",
            desc: "Trouver la séquence d'élans qui amène la voiture au sommet.",
            libs: ["Gymnasium"],
          },
          {
            file: "MLGymGALunar.ipynb",
            title: "Poser le Lunar Lander",
            type: "tp",
            desc: "Faire évoluer un pilote capable d'alunir en douceur.",
            libs: ["Gym", "Box2D"],
            data: ["lunarsourcegym.py"],
          },
        ],
      },
      {
        title: "Plusieurs objectifs à la fois",
        items: [
          {
            file: "tutorialParetoOptimality.ipynb",
            title: "Optimalité de Pareto",
            type: "demo",
            lang: "en",
            desc: "Placer les arrêts d'une navette autonome en arbitrant entre objectifs contradictoires. Fait le lien avec la théorie des jeux.",
            libs: ["NumPy", "SciPy"],
          },
        ],
      },
    ],
  },

  /* ---------------------------------------------------------------- */
  {
    id: "renforcement",
    title: "Apprentissage par renforcement",
    tagline: "Q-Learning et variantes",
    intro:
      "Un agent apprend par essais et erreurs une table Q des meilleures actions. On commence sur le lac gelé, puis on compare les variantes sur d'autres environnements.",
    groups: [
      {
        title: "Q-Learning",
        items: [
          {
            file: "TPMLGymQLearning.ipynb",
            title: "Traverser le lac gelé",
            type: "tp",
            desc: "Implémenter le Q-Learning sur FrozenLake, un environnement où le sol glisse.",
            libs: ["Gymnasium"],
            data: ["FrozenLakeWithPenalties.py"],
            solutions: [{ file: "GymFrozenLakeQLearning.ipynb", title: "Corrigé" }],
            note: "Voir d'abord « Prise en main de Gymnasium ».",
          },
        ],
      },
      {
        title: "Variantes et autres environnements",
        intro: "Exemples de sortie attendue pour le Double Q-Learning.",
        items: [
          {
            file: "GymCLIFFDoubleQLearningTODO.ipynb",
            title: "Double Q-Learning sur CliffWalking",
            type: "exo",
            desc: "Longer la falaise sans y tomber : aucune récompense à l'arrivée, seulement des pénalités en route.",
            libs: ["Gymnasium"],
          },
          {
            file: "GymTaxiDoubleQLearningTODO.ipynb",
            title: "Double Q-Learning sur Taxi",
            type: "exo",
            desc: "Prendre et déposer des passagers : le Q-Learning construit des solutions complètes.",
            libs: ["Gymnasium"],
          },
          {
            file: "GymBlackJackDoubleQLearning.ipynb",
            title: "Double Q-Learning au Blackjack",
            type: "demo",
            desc: "Apprendre quand tirer une carte et quand s'arrêter.",
            libs: ["Gymnasium"],
          },
        ],
      },
    ],
    extras: {
      title: "Pour aller plus loin",
      steps: [
        "Implémenter le <b>Double Q-Learning</b> et comparer ses performances au Q-Learning simple.",
        "Implémenter le <b>Delayed Q-Learning</b>, puis comparer les quatre variantes : simple, double, delayed, delayed double.",
        "Appliquer ces algorithmes à <b>CliffWalking-v0</b> : coût de −1 par pas, −100 dans la falaise, rien à l'arrivée.",
        "Les appliquer à <b>Taxi-v3</b>.",
      ],
      lesson:
        "FrozenLake montre le Q-Learning dans un monde non déterministe, CliffWalking qu'il fonctionne sans récompense finale, Taxi qu'il sait construire des solutions.",
      questions: [
        "Quelle forme aurait la matrice Q pour <b>CartPole-v1</b> ? Qu'apporte le <b>Deep Q-Learning</b> ?",
        "Comment le Q-Learning combiné à une recherche MCTS est-il utilisé dans les jeux vidéo ? Donner des exemples.",
        "Citer des applications industrielles ou commerciales réelles du Q-Learning.",
      ],
    },
  },

  /* ---------------------------------------------------------------- */
  {
    id: "jeux",
    title: "Théorie des jeux et négociation",
    tagline: "Nash, Axelrod, agents négociateurs",
    lang: "en",
    intro:
      "Quatre mini-livres en anglais. Chaque chapitre alterne démonstrations et questions de 3 à 10 lignes de code, avec la solution juste en dessous.",
    books: [
      {
        folder: "gameTheory/matrix-games-book",
        title: "Matrix games with nashpy",
        desc: "Cinq jeux à deux joueurs résolus à la main par le principe d'indifférence, puis vérifiés avec nashpy.",
        libs: ["nashpy"],
        helper: "myNashTools.py",
        chapters: [
          ["01_nashflix.ipynb", "NashFlix"],
          ["02_rock_paper_scissors.ipynb", "Rock-Paper-Scissors"],
          ["03_fingers.ipynb", "Odd or even"],
          ["04_tandem.ipynb", "Tandem bike"],
          ["05_country_road.ipynb", "Country road"],
        ],
      },
      {
        folder: "gameTheory/axelrod-book",
        title: "Repeated games with axelrod",
        desc: "Le même jeu joué de nombreuses fois : matchs, tournois à la Axelrod, puis évolution d'une population de stratégies.",
        libs: ["axelrod"],
        helper: "myIGTools.py",
        chapters: [
          ["01_matches.ipynb", "Matches"],
          ["02_tournaments.ipynb", "Tournaments"],
          ["03_evolution.ipynb", "Evolution"],
        ],
      },
      {
        folder: "gameTheory/negotiation-book",
        title: "Negotiation for mobility",
        desc: "Solutions de Nash et de Kalai-Smorodinsky, bien-être social, puis offres alternées et modèle de Rubinstein.",
        libs: ["NumPy", "Matplotlib"],
        helper: "bargain.py",
        chapters: [
          ["01_sharing_a_ride.ipynb", "Sharing a ride"],
          ["02_eco_bonus.ipynb", "An eco-bonus for electric bikes"],
          ["03_loading_bay.ipynb", "A shared loading bay"],
          ["04_offers_in_turn.ipynb", "Offers in turn"],
        ],
      },
      {
        folder: "gameTheory/carpool-agents-book",
        title: "Negotiating agents: a carpool price",
        desc: "Alice conduit à Valenciennes, Bob cherche une place : deux agents négocient le prix offre après offre.",
        libs: ["NumPy", "Matplotlib"],
        helper: "carpool.py",
        chapters: [
          ["01_the_protocol.ipynb", "The protocol"],
          ["02_boulware_conceder.ipynb", "Boulware or Conceder"],
          ["03_tit_for_tat_distance.ipynb", "Tit-for-Tat and Distance"],
        ],
      },
    ],
  },

  /* ---------------------------------------------------------------- */
  {
    id: "summer",
    title: "Summer School",
    tagline: "Parcours condensé en anglais",
    lang: "en",
    intro:
      "Une version courte et en anglais des briques ci-dessus, pour une découverte en quelques séances. Les réseaux de neurones y sont écrits avec PyTorch.",
    groups: [
      {
        title: "Applications of AI",
        items: [
          { file: "summerSchool/FuzzyLogic_1_AirCond.ipynb", title: "Fuzzy control of an air conditioner", type: "demo", lang: "en", libs: ["skfuzzy"] },
          { file: "summerSchool/NN_1_learn_AND.ipynb", title: "A network learns logical AND", type: "demo", lang: "en", libs: ["PyTorch"] },
          { file: "summerSchool/NN_2_ArithmeticSignsDetection.ipynb", title: "Arithmetic signs detection", type: "demo", lang: "en", libs: ["PyTorch"], data: ["summerSchool/arithmDessins.png"] },
          { file: "summerSchool/NN_3_EmailClassification.ipynb", title: "Email classification", type: "demo", lang: "en", libs: ["PyTorch"] },
          { file: "summerSchool/NN_4_SentimentsDetector.ipynb", title: "Sentiment detection", type: "demo", lang: "en", libs: ["PyTorch", "NLTK"], data: ["summerSchool/IMDB Dataset.csv"] },
          { file: "summerSchool/NN_5_lstm.ipynb", title: "Predict the next values (LSTM)", type: "demo", lang: "en", libs: ["TensorFlow"] },
          { file: "summerSchool/NN_6_gru_text.ipynb", title: "Predict the next words (GRU)", type: "demo", lang: "en", libs: ["TensorFlow"], data: ["summerSchool/vocab.txt"] },
          { file: "summerSchool/QL_1_GymFrozenLake.ipynb", title: "Find the treasure (Q-Learning)", type: "demo", lang: "en", libs: ["Gymnasium"] },
        ],
      },
    ],
  },
];