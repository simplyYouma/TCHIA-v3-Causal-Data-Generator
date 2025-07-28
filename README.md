# TCHIA v3 - Générateur de Données Causales Cohérentes

## 🎯 Objectif

Ce projet génère des données agricoles synthétiques avec **cohérence causale parfaite** pour l'entraînement de modèles d'intelligence artificielle. Chaque ligne de données raconte une histoire agricole complète et réaliste basée sur les conditions agro-climatiques du Mali.

## 🌾 Contexte Scientifique

Le générateur TCHIA v3 s'appuie sur :
- **Données empiriques** du Mali (IER, ICRISAT, CMDT, AGRHYMET)
- **Modèles agronomiques** validés pour l'Afrique de l'Ouest
- **Cohérence causale temporelle** : chaque événement influence la suite du cycle cultural
- **Réalisme décisionnel** : intégration des stratégies adaptatives des producteurs

## 📁 Structure du Projet

```
TCHIA_Data_Causal_Generator/
├── README.md                           # Ce fichier
├── Notebook_causal_generator.ipynb     # Notebook principal de génération
├── tchia_v3_generator.py               # Générateur principal avec cohérence causale
├── tchia_v3_validator.py               # Validateur de cohérence des données
├── tchia_validation_analysis.py        # Analyses de validation
├── enhanced_crop_profiles_v2.py        # Profils agronomiques des cultures
├── hyper_realistic_generator_v2.py     # Générateurs climat/sol/capteurs
├── climate_cleaned.csv                 # Données climatiques de référence
├── checkpoint_batch_*.pkl              # Sauvegardes de génération par batch
├── validation_tchia_v3.html            # Rapport de validation (visualisation)
├── validation_tchia_v3.json            # Rapport de validation (données)
└── validation_tchia_v3.png             # Graphiques de validation
```

## 🚀 Fonctionnalités Principales

### 1. **Générateur Cohérent (`tchia_v3_generator.py`)**

#### Scénarios Agricoles Réalistes
- **Exceptionnel** (5%) : Conditions optimales, rendements maximaux
- **Bon** (20%) : Conditions favorables, stress mineurs
- **Moyen** (40%) : Conditions variables, adaptations nécessaires
- **Difficile** (25%) : Stress multiples, changements de stratégie
- **Catastrophique** (10%) : Échecs majeurs, survie minimale

#### Cohérence Causale Temporelle
- **Mémoire des événements** : Un stress précoce impacte tout le cycle
- **Stades phénologiques** : Impact différencié selon le timing
- **Décisions adaptatives** : Changement de culture, ajustement des intrants
- **Effets cumulatifs** : Accumulation et propagation des stress

#### Variables Générées (50+ features)
```python
# Variables temporelles
'Year', 'SowingDate', 'SowingDelay_days', 'HarvestDate'

# Variables décisionnelles
'InitialCrop', 'FinalCrop', 'CropChange', 'ManagementStrategy'

# Variables climatiques cohérentes
'SeasonRainfall_mm', 'EffectiveRainfall_mm', 'RainfallDistribution'
'Temperature_avg', 'Humidity_avg', 'SunshineHours'

# Variables de stress causales
'AccumulatedStress', 'StressHistory', 'GrowthReduction'
'DroughtStress', 'HeatStress', 'WaterlogStress'

# Variables agronomiques
'ActualYield_kg_ha', 'YieldLoss_percent', 'YieldGap'
'FertilizerApplied_kg_ha', 'SeedDensity_plants_m2'

# Variables de télédétection
'NDVI_peak', 'NDVI_timeline', 'VegetationIndex'

# Variables économiques
'BC_Ratio', 'ProfitLoss_FCFA', 'MarketPrice_FCFA_kg'
```

### 2. **Validateur de Cohérence (`tchia_v3_validator.py`)**

#### Tests de Cohérence Causale
1. **Test Stress-Rendement** : Vérifie la relation inverse stress/productivité
2. **Test Efficacité Pluviométrique** : Valide le ruissellement (30-70%)
3. **Test Cohérence Temporelle** : Vérifie la propagation des effets
4. **Test Décisions Paysannes** : Valide la logique des adaptations
5. **Test NDVI-Biomasse** : Vérifie les relations empiriques
6. **Test Cohérence Scénario** : Valide la cohérence globale

#### Métriques de Qualité
- **Score de cohérence** : Pourcentage de lignes causalement correctes
- **Détection d'anomalies** : Identification des incohérences
- **Validation distributionnelle** : Comparaison aux données réelles
- **Rapports visuels** : Graphiques de validation automatiques

### 3. **Génération Haute Performance**

#### Génération d'1 Million de Lignes
```python
# Exemple d'utilisation
from tchia_v3_generator import CausalCoherentGenerator

generator = CausalCoherentGenerator()

# Génération par batch avec sauvegarde
df = generate_1_million_advanced(
    total_rows=1_000_000,
    batch_size=50_000,
    save_checkpoints=True
)
```

#### Performances
- **Vitesse** : 100-1000 lignes/seconde selon la configuration
- **Parallélisation** : Support multi-core pour génération rapide
- **Gestion mémoire** : Génération par batch pour gros volumes
- **Sauvegarde incrémentale** : Checkpoints pour reprendre en cas d'interruption

## 📊 Utilisation

### Installation des Dépendances
```bash
pip install pandas numpy matplotlib seaborn jupyter
```

### Génération Simple
```python
from tchia_v3_generator import CausalCoherentGenerator, ScenarioType

# Initialiser le générateur
generator = CausalCoherentGenerator()

# Générer une ligne cohérente
row = generator.generate_coherent_row(
    year=2023,
    locality="SIKASSO",
    initial_crop="maïs",
    scenario_type=ScenarioType.AVERAGE
)

# Génération de dataset complet
data = []
for i in range(10000):
    row = generator.generate_coherent_row(
        year=2020 + (i % 4),
        locality=["SIKASSO", "BAMAKO", "SEGOU"][i % 3],
        initial_crop=["mil", "sorgho", "maïs"][i % 3]
    )
    data.append(row)

df = pd.DataFrame(data)
```

### Validation des Données
```python
from tchia_v3_validator import QualityReportGenerator

# Valider le dataset
validator = QualityReportGenerator()
report = validator.validate_dataset(df, verbose=True)

# Afficher le score de cohérence
print(f"Score de cohérence : {report['summary']['coherence_score']}%")

# Générer rapport visuel
validator.generate_visual_report(df, "validation_report.html")
```

### Génération Haute Performance
```python
# Utiliser le notebook pour génération optimisée
# Voir : Notebook_causal_generator.ipynb

# Ou utiliser la fonction avancée
df = generate_1_million_advanced(
    total_rows=1_000_000,
    use_parallel=True,
    n_cores=8,
    batch_size=50_000
)
```

## 🔬 Validation Scientifique

### Base Empirique
- **Données climatiques** : Stations météorologiques Mali (2018-2023)
- **Rendements** : Enquêtes EAGRRI, statistiques CMDT
- **Comportements** : Études sociologiques des adaptations paysannes
- **Modèles agronomiques** : DSSAT, APSIM, CropSyst adaptés Sahel

### Tests de Cohérence
- **Relation pluie-rendement** : R² > 0.65 pour cultures pluviales
- **Stress temporel** : Stress floraison 2x plus impactant que végétatif
- **Efficacité hydrique** : 30-70% de ruissellement selon intensité
- **Seuils décisionnels** : Ratio bénéfice/coût > 1.8 pour maintien culture

## 📈 Applications

### Entraînement IA
- **Prédiction de rendements** : Modèles ML avec features causales
- **Systèmes d'alerte précoce** : Détection de stress en temps réel
- **Optimisation agricole** : Recommandations adaptatives
- **Assurance agricole** : Modélisation des risques

### Recherche Agronomique
- **Analyse de sensibilité** : Impact des stress par culture/zone
- **Scénarios climatiques** : Simulation changement climatique
- **Politiques agricoles** : Évaluation d'interventions
- **Formation** : Jeux de données pédagogiques

## 🛠 Configuration Avancée

### Paramètres du Générateur
```python
config = {
    'localities_weights': {
        "SIKASSO": 0.20,    # Zone cotonnière
        "SEGOU": 0.18,      # Zone Office Niger
        "MOPTI": 0.15,      # Zone mil/sorgho
        # ...
    },
    'crops_weights': {
        "mil": 0.30,        # Culture dominante
        "sorgho": 0.25,     # 2ème céréale
        # ...
    },
    'scenarios_distribution': {
        ScenarioType.EXCEPTIONAL: 0.05,
        ScenarioType.GOOD: 0.20,
        ScenarioType.AVERAGE: 0.40,
        ScenarioType.DIFFICULT: 0.25,
        ScenarioType.CATASTROPHIC: 0.10
    }
}
```

### Personnalisation des Cultures
```python
# Modifier enhanced_crop_profiles_v2.py
CROP_PROFILES = {
    'nouvelle_culture': {
        'cycle_days': 120,
        'water_requirement': 500,
        'yield_potential': 2500,
        'stress_sensitivity': {
            'germination': 0.8,
            'flowering': 1.2,
            'grain_filling': 1.0
        }
    }
}
```

## 📋 Exemples de Données Générées

### Scénario Exceptionnel
```python
{
    "Year": 2023,
    "Locality": "SIKASSO",
    "Scenario": "exceptional",
    "InitialCrop": "maïs", "FinalCrop": "maïs",
    "SeasonRainfall_mm": 1250, "EffectiveRainfall_mm": 1087,
    "AccumulatedStress": 0.045,
    "YieldLoss_percent": 5.2,
    "ActualYield_kg_ha": 3798,
    "NDVI_peak": 0.84,
    "BC_Ratio": 3.2
}
```

### Scénario Catastrophique
```python
{
    "Year": 2023,
    "Locality": "MOPTI",
    "Scenario": "catastrophic",
    "InitialCrop": "riz", "FinalCrop": "mil",  # Changement adaptatif
    "SeasonRainfall_mm": 280, "EffectiveRainfall_mm": 145,
    "AccumulatedStress": 0.94,
    "YieldLoss_percent": 91.5,
    "ActualYield_kg_ha": 68,
    "NDVI_peak": 0.21,
    "BC_Ratio": 0.3
}
```

## 🔧 Dépannage

### Problèmes Courants
1. **Mémoire insuffisante** : Réduire `batch_size` ou utiliser génération par chunks
2. **Génération lente** : Activer parallélisation avec `use_parallel=True`
3. **Validation échoue** : Ajuster seuils de cohérence dans le validateur
4. **Données incohérentes** : Vérifier configuration des scénarios

### Support
- **Issues GitHub** : Signaler bugs et demandes de fonctionnalités
- **Documentation** : Voir commentaires détaillés dans le code
- **Exemples** : Notebook Jupyter avec cas d'usage complets

## 📜 Licence et Citation

### Auteurs
- **Fatoumata Youma Sokona** - Conception et développement
- **Claude Anthropic** - Assistance à la recherche et développement
- **ChatGPT** - Support recherche documentaire

### Citation
```bibtex
@software{tchia_v3_2024,
    title={TCHIA v3: Générateur de Données Agricoles avec Cohérence Causale},
    author={Sokona, Fatoumata Youma},
    year={2024},
    version={3.0},
    note={Générateur de données synthétiques pour IA agricole - Mali}
}
```

## 🔄 Historique des Versions

- **v3.0** (2024) : Cohérence causale complète, validation intégrée
- **v2.0** (2024) : Profils agronomiques avancés, capteurs IoT
- **v1.0** (2023) : Générateur de base TCHIA

## 🎯 Roadmap

### Prochaines Améliorations
- [ ] Support multi-pays (Burkina Faso, Sénégal)
- [ ] Intégration données satellitaires temps réel
- [ ] Module économique avancé (prix, marchés)
- [ ] Export formats ML (TensorFlow, PyTorch)
- [ ] API REST pour génération à la demande
- [ ] Interface graphique utilisateur

---

**🌾 TCHIA v3 - Des données agricoles qui racontent de vraies histoires pour une IA plus intelligente ! 🚀**