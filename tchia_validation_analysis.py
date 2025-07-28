"""
=============================================================================
ANALYSE EXHAUSTIVE DATASET TCHIA - VALIDATION GÉNÉRATEUR V2
=============================================================================

🎯 OBJECTIFS :
- Valider la cohérence scientifique du générateur TCHIA
- Vérifier la variabilité climatique et scénarios multiples  
- Détecter problèmes potentiels (overfitting, biais, incohérences)
- Garantir qualité 100% des données pour modèles ML

🔬 MÉTHODOLOGIE :
- Validation structurelle et scientifique rigoureuse
- Analyses statistiques avancées et visualisations
- Tests de cohérence physique et agronomique
- Métriques de diversité et variabilité

Auteur : Fatoumata Youma Sokona - Projet TCHIA Mali
Date : Décembre 2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import pearsonr, spearmanr, normaltest, kstest
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Configuration graphiques haute qualité
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 11
plt.rcParams['figure.figsize'] = [14, 10]
sns.set_style("whitegrid")
sns.set_palette("Set2")

class TCHIADatasetValidator:
    """
    Validateur exhaustif pour dataset TCHIA
    
    Validation multi-niveaux :
    1. Validation structurelle
    2. Validation scientifique  
    3. Validation variabilité
    4. Validation relations physiques
    5. Détection anomalies et biais
    """
    
    def __init__(self, dataset_path):
        """Initialisation avec chargement dataset"""
        print("🔄 Chargement dataset TCHIA...")
        self.df = pd.read_csv(dataset_path)
        print(f"✅ Dataset chargé : {self.df.shape[0]:,} lignes × {self.df.shape[1]} variables")
        
        # Dictionnaires de validation scientifique
        self.expected_ranges = self._define_expected_ranges()
        self.scientific_correlations = self._define_scientific_correlations()
        self.crop_specific_ranges = self._define_crop_ranges()
        
        # Résultats validation
        self.validation_results = {}
        self.critical_issues = []
        self.warnings_list = []
        
    def _define_expected_ranges(self):
        """Définition des gammes scientifiquement valides pour chaque variable"""
        return {
            # Variables climatiques Mali
            'SeasonRainfall_mm': (150, 1500),       # Sahel-Soudanien
            'MeanTemp_C': (22, 38),                 # Températures Mali
            'MaxTemp_C': (25, 48),                  # Maximales extrêmes
            'MinTemp_C': (12, 30),                  # Minimales
            'Humidity_percent': (10, 95),           # Humidité relative
            'WindSpeed_ms': (0.5, 15),              # Vitesse vent
            'SoilTemp_C': (18, 45),                 # Température sol
            'AtmPressure_kPa': (98, 104),           # Pression atmosphérique
            
            # Variables sol Mali
            'Soil_pH': (4.2, 7.0),                 # Source YieldGap Mali validée
            'Soil_OM_percent': (0.1, 3.0),         # Matière organique
            'Soil_N_kg_ha': (5, 80),               # Azote sol
            'Soil_P_kg_ha': (2, 50),               # Phosphore sol
            'Soil_K_kg_ha': (20, 200),             # Potassium sol
            'Soil_EC_dS_m': (0.05, 2.0),           # Conductivité électrique
            'SoilMoisture_percent': (5, 90),        # Humidité sol
            
            # Fertilisation réaliste Mali
            'FertN_kg_ha': (0, 150),               # Azote appliqué
            'FertP_kg_ha': (0, 50),                # Phosphore appliqué
            'FertK_kg_ha': (0, 80),                # Potassium appliqué
            
            # Stress (graduées 0-1)
            'Stress_Water_graded': (0, 1),
            'Stress_Temp_graded': (0, 1),
            'Stress_Nitrogen_graded': (0, 1),
            
            # Variables IoT
            'CO2_ppm': (350, 450),                 # CO2 atmosphérique
            'Light_lux': (5000, 120000),           # Luminosité jour
            
            # Sorties critiques
            'Yield_kg_ha': (50, 8000),             # Rendements réalistes Mali
            'NDVI_peak': (0.1, 0.95)               # NDVI satellite
        }
    
    def _define_scientific_correlations(self):
        """Corrélations scientifiques attendues (littérature validée)"""
        return {
            # Corrélations positives attendues
            'positive_strong': [
                ('SeasonRainfall_mm', 'Yield_kg_ha'),      # r > 0.6
                ('NDVI_peak', 'Yield_kg_ha'),              # r > 0.7
                ('Soil_OM_percent', 'Soil_N_kg_ha'),       # r > 0.8
                ('FertN_kg_ha', 'Yield_kg_ha'),            # r > 0.4
                ('SoilMoisture_percent', 'SeasonRainfall_mm')  # r > 0.5
            ],
            
            # Corrélations négatives attendues
            'negative_moderate': [
                ('Stress_Water_graded', 'Yield_kg_ha'),    # r < -0.4
                ('Stress_Temp_graded', 'Yield_kg_ha'),     # r < -0.3
                ('Stress_Nitrogen_graded', 'Yield_kg_ha'), # r < -0.4
                ('MeanTemp_C', 'Humidity_percent')         # r < -0.3
            ],
            
            # Cohérence température
            'temperature_coherence': [
                ('MeanTemp_C', 'SoilTemp_C'),              # r > 0.7
                ('MaxTemp_C', 'MinTemp_C'),                # r > 0.6
                ('MeanTemp_C', 'MaxTemp_C')                # r > 0.8
            ]
        }
    
    def _define_crop_ranges(self):
        """Gammes de rendement spécifiques par culture (données IER/FAOSTAT)"""
        return {
            'mil': {'min': 200, 'max': 2500, 'mean_expected': 800},
            'sorgho': {'min': 300, 'max': 3000, 'mean_expected': 1000},
            'maïs': {'min': 500, 'max': 6000, 'mean_expected': 1800},
            'coton': {'min': 400, 'max': 2800, 'mean_expected': 1300},
            'riz': {'min': 1000, 'max': 7000, 'mean_expected': 3500}
        }

    def run_complete_validation(self):
        """Exécution validation complète avec rapport détaillé"""
        print("\n" + "="*80)
        print("🔬 DÉMARRAGE VALIDATION EXHAUSTIVE DATASET TCHIA")
        print("="*80)
        
        # Étape 1 : Validation structurelle
        print("\n📋 ÉTAPE 1 : VALIDATION STRUCTURELLE")
        self.validate_structure()
        
        # Étape 2 : Validation gammes scientifiques
        print("\n🔬 ÉTAPE 2 : VALIDATION GAMMES SCIENTIFIQUES")
        self.validate_scientific_ranges()
        
        # Étape 3 : Validation variabilité et diversité
        print("\n📊 ÉTAPE 3 : VALIDATION VARIABILITÉ ET DIVERSITÉ")
        self.validate_variability()
        
        # Étape 4 : Validation relations physiques
        print("\n⚗️ ÉTAPE 4 : VALIDATION RELATIONS PHYSIQUES")
        self.validate_scientific_relationships()
        
        # Étape 5 : Validation par culture
        print("\n🌾 ÉTAPE 5 : VALIDATION SPÉCIFIQUE PAR CULTURE")
        self.validate_crop_specific()
        
        # Étape 6 : Validation zonage géographique
        print("\n🗺️ ÉTAPE 6 : VALIDATION ZONAGE GÉOGRAPHIQUE")
        self.validate_geographic_coherence()
        
        # Étape 7 : Détection anomalies
        print("\n🚨 ÉTAPE 7 : DÉTECTION ANOMALIES ET OUTLIERS")
        self.detect_anomalies()
        
        # Étape 8 : Visualisations avancées
        print("\n📊 ÉTAPE 8 : GÉNÉRATION VISUALISATIONS")
        self.create_advanced_visualizations()
        
        # Rapport final
        print("\n📋 ÉTAPE 9 : RAPPORT FINAL VALIDATION")
        self.generate_final_report()

    def validate_structure(self):
        """Validation structurelle basique"""
        print("  🔍 Analyse structure générale...")
        
        # Informations générales
        n_rows, n_cols = self.df.shape
        memory_mb = self.df.memory_usage(deep=True).sum() / (1024**2)
        
        print(f"    • Dimensions : {n_rows:,} lignes × {n_cols} variables")
        print(f"    • Mémoire : {memory_mb:.1f} MB")
        print(f"    • Période : {self.df['Year'].min()} - {self.df['Year'].max()}")
        
        # Valeurs manquantes
        missing_data = self.df.isnull().sum()
        if missing_data.sum() > 0:
            self.critical_issues.append(f"Valeurs manquantes détectées : {missing_data.sum()}")
            print(f"    ⚠️ Valeurs manquantes : {missing_data.sum()}")
        else:
            print("    ✅ Aucune valeur manquante")
        
        # Doublons
        duplicates = self.df.duplicated().sum()
        if duplicates > 0:
            self.critical_issues.append(f"Lignes dupliquées : {duplicates}")
            print(f"    ⚠️ Doublons : {duplicates}")
        else:
            print("    ✅ Aucun doublon")
        
        # Types de données
        print("    📊 Types de variables :")
        type_counts = self.df.dtypes.value_counts()
        for dtype, count in type_counts.items():
            print(f"      - {dtype} : {count} variables")
        
        # Variables redondantes (problème identifié)
        redundant_vars = []
        if 'FertN_kg_ha' in self.df.columns:
            redundant_vars.append('FertN_kg_ha')
        if 'FertP_kg_ha' in self.df.columns:
            redundant_vars.append('FertP_kg_ha')
        if 'FertK_kg_ha' in self.df.columns:
            redundant_vars.append('FertK_kg_ha')
        
        if redundant_vars:
            self.critical_issues.append(f"Variables redondantes : {redundant_vars}")
            print(f"    🚨 Variables redondantes détectées : {redundant_vars}")
        
        self.validation_results['structure'] = {
            'dimensions': (n_rows, n_cols),
            'missing_data': missing_data.sum(),
            'duplicates': duplicates,
            'redundant_variables': redundant_vars
        }

    def validate_scientific_ranges(self):
        """Validation des gammes scientifiquement acceptables"""
        print("  🔬 Validation gammes scientifiques...")
        
        range_violations = {}
        
        for variable, (min_val, max_val) in self.expected_ranges.items():
            if variable in self.df.columns:
                data = self.df[variable]
                violations_low = (data < min_val).sum()
                violations_high = (data > max_val).sum()
                total_violations = violations_low + violations_high
                
                if total_violations > 0:
                    violation_pct = (total_violations / len(data)) * 100
                    range_violations[variable] = {
                        'below_min': violations_low,
                        'above_max': violations_high,
                        'total': total_violations,
                        'percentage': violation_pct,
                        'actual_range': (data.min(), data.max()),
                        'expected_range': (min_val, max_val)
                    }
                    
                    if violation_pct > 5:  # Plus de 5% hors gamme = problème critique
                        self.critical_issues.append(
                            f"{variable}: {violation_pct:.1f}% valeurs hors gamme scientifique"
                        )
                        print(f"    🚨 {variable}: {violation_pct:.1f}% hors gamme")
                    else:
                        print(f"    ⚠️ {variable}: {violation_pct:.1f}% hors gamme (tolérable)")
                else:
                    print(f"    ✅ {variable}: toutes valeurs dans gamme attendue")
        
        # Statistiques descriptives variables critiques
        critical_vars = ['Yield_kg_ha', 'NDVI_peak', 'SeasonRainfall_mm', 'MeanTemp_C']
        print("\n    📊 Statistiques variables critiques :")
        for var in critical_vars:
            if var in self.df.columns:
                stats_data = self.df[var].describe()
                print(f"      {var}: μ={stats_data['mean']:.1f}, σ={stats_data['std']:.1f}, "
                      f"range=[{stats_data['min']:.1f}, {stats_data['max']:.1f}]")
        
        self.validation_results['ranges'] = range_violations

    def validate_variability(self):
        """Validation variabilité et diversité pour éviter overfitting"""
        print("  📊 Analyse variabilité et diversité...")
        
        variability_metrics = {}
        
        # 1. Variabilité temporelle
        yearly_counts = self.df['Year'].value_counts().sort_index()
        year_balance = yearly_counts.std() / yearly_counts.mean()
        print(f"    📅 Équilibre temporel (CV): {year_balance:.3f}")
        if year_balance > 0.3:
            self.warnings_list.append("Déséquilibre temporel élevé")
        
        # 2. Diversité géographique
        locality_counts = self.df['Locality'].value_counts()
        geo_balance = locality_counts.std() / locality_counts.mean()
        print(f"    🗺️ Équilibre géographique (CV): {geo_balance:.3f}")
        print(f"      Localités représentées: {len(locality_counts)}")
        
        # 3. Diversité culturale
        crop_counts = self.df['Crop'].value_counts()
        crop_balance = crop_counts.std() / crop_counts.mean()
        print(f"    🌾 Équilibre cultural (CV): {crop_balance:.3f}")
        for crop, count in crop_counts.items():
            print(f"      {crop}: {count:,} observations ({count/len(self.df)*100:.1f}%)")
        
        # 4. Variabilité climatique (essentiel anti-overfitting)
        climate_vars = ['SeasonRainfall_mm', 'MeanTemp_C', 'Humidity_percent']
        print("    🌡️ Variabilité climatique:")
        for var in climate_vars:
            if var in self.df.columns:
                cv = self.df[var].std() / self.df[var].mean()
                print(f"      {var}: CV = {cv:.3f}")
                if cv < 0.15:  # Faible variabilité = risque overfitting
                    self.warnings_list.append(f"Faible variabilité climatique: {var}")
        
        # 5. Distribution des stress (crucial pour scénarios multiples)
        stress_vars = ['Stress_Water_graded', 'Stress_Temp_graded', 'Stress_Nitrogen_graded']
        print("    🚨 Distribution des stress:")
        for stress_var in stress_vars:
            if stress_var in self.df.columns:
                # Catégorisation stress
                stress_categories = pd.cut(self.df[stress_var], 
                                         bins=[0, 0.2, 0.5, 0.8, 1.0], 
                                         labels=['Faible', 'Modéré', 'Élevé', 'Sévère'])
                stress_dist = stress_categories.value_counts(normalize=True)
                print(f"      {stress_var}:")
                for category, pct in stress_dist.items():
                    print(f"        {category}: {pct*100:.1f}%")
        
        # 6. Diversité des rendements par culture
        print("    📈 Diversité rendements par culture:")
        for crop in self.df['Crop'].unique():
            crop_data = self.df[self.df['Crop'] == crop]['Yield_kg_ha']
            cv_yield = crop_data.std() / crop_data.mean()
            print(f"      {crop}: CV rendement = {cv_yield:.3f}")
            if cv_yield < 0.25:  # Faible variabilité rendements
                self.warnings_list.append(f"Faible variabilité rendement: {crop}")
        
        variability_metrics = {
            'temporal_balance': year_balance,
            'geographic_balance': geo_balance,
            'crop_balance': crop_balance,
            'climate_variability': {var: self.df[var].std()/self.df[var].mean() 
                                  for var in climate_vars if var in self.df.columns}
        }
        
        self.validation_results['variability'] = variability_metrics

    def validate_scientific_relationships(self):
        """Validation relations physiques et agronomiques attendues"""
        print("  ⚗️ Validation relations scientifiques...")
        
        correlation_results = {}
        
        # Fonction helper pour calcul corrélations
        def calculate_correlation(var1, var2):
            if var1 in self.df.columns and var2 in self.df.columns:
                # Suppression valeurs manquantes
                data = self.df[[var1, var2]].dropna()
                if len(data) > 100:  # Minimum observations
                    corr_pearson, p_val = pearsonr(data[var1], data[var2])
                    return corr_pearson, p_val
            return None, None
        
        # 1. Corrélations positives attendues
        print("    ➕ Corrélations positives attendues:")
        for var1, var2 in self.scientific_correlations['positive_strong']:
            corr, p_val = calculate_correlation(var1, var2)
            if corr is not None:
                print(f"      {var1} ↔ {var2}: r = {corr:.3f} (p = {p_val:.3f})")
                if corr < 0.3:  # Corrélation plus faible qu'attendue
                    self.warnings_list.append(f"Corrélation faible: {var1}-{var2} (r={corr:.3f})")
                correlation_results[f"{var1}_vs_{var2}"] = {'correlation': corr, 'p_value': p_val}
        
        # 2. Corrélations négatives attendues
        print("    ➖ Corrélations négatives attendues:")
        for var1, var2 in self.scientific_correlations['negative_moderate']:
            corr, p_val = calculate_correlation(var1, var2)
            if corr is not None:
                print(f"      {var1} ↔ {var2}: r = {corr:.3f} (p = {p_val:.3f})")
                if corr > -0.2:  # Corrélation négative trop faible
                    self.warnings_list.append(f"Corrélation négative faible: {var1}-{var2} (r={corr:.3f})")
                correlation_results[f"{var1}_vs_{var2}"] = {'correlation': corr, 'p_value': p_val}
        
        # 3. Cohérence température
        print("    🌡️ Cohérence températures:")
        for var1, var2 in self.scientific_correlations['temperature_coherence']:
            corr, p_val = calculate_correlation(var1, var2)
            if corr is not None:
                print(f"      {var1} ↔ {var2}: r = {corr:.3f}")
                if corr < 0.6:  # Cohérence température insuffisante
                    self.critical_issues.append(f"Incohérence température: {var1}-{var2} (r={corr:.3f})")
        
        # 4. Test spécifique NDVI-Rendement (critique)
        if 'NDVI_peak' in self.df.columns and 'Yield_kg_ha' in self.df.columns:
            # Par culture (plus précis)
            print("    📡 Corrélations NDVI-Rendement par culture:")
            for crop in self.df['Crop'].unique():
                crop_data = self.df[self.df['Crop'] == crop]
                if len(crop_data) > 50:
                    corr_ndvi, p_ndvi = pearsonr(crop_data['NDVI_peak'], crop_data['Yield_kg_ha'])
                    print(f"      {crop}: r = {corr_ndvi:.3f} (p = {p_ndvi:.3f})")
                    
                    # Validation littérature: r² = 0.58-0.89 documenté
                    r_squared = corr_ndvi ** 2
                    if r_squared < 0.4:  # r² < 0.4 problématique
                        self.critical_issues.append(
                            f"Corrélation NDVI-rendement faible pour {crop}: r²={r_squared:.3f}"
                        )
        
        self.validation_results['correlations'] = correlation_results

    def validate_crop_specific(self):
        """Validation spécifique par culture"""
        print("  🌾 Validation paramètres spécifiques par culture...")
        
        crop_validation = {}
        
        for crop in self.df['Crop'].unique():
            print(f"    📊 Analyse {crop}:")
            crop_data = self.df[self.df['Crop'] == crop]
            
            # Rendements vs attentes
            if crop in self.crop_specific_ranges:
                expected = self.crop_specific_ranges[crop]
                actual_mean = crop_data['Yield_kg_ha'].mean()
                actual_range = (crop_data['Yield_kg_ha'].min(), crop_data['Yield_kg_ha'].max())
                
                print(f"      Rendement moyen: {actual_mean:.0f} kg/ha "
                      f"(attendu: {expected['mean_expected']} kg/ha)")
                print(f"      Gamme: [{actual_range[0]:.0f}, {actual_range[1]:.0f}] kg/ha "
                      f"(attendu: [{expected['min']}, {expected['max']}])")
                
                # Écart à l'attendu
                deviation = abs(actual_mean - expected['mean_expected']) / expected['mean_expected']
                if deviation > 0.3:  # Écart > 30%
                    self.critical_issues.append(
                        f"Rendement {crop} dévie de {deviation*100:.1f}% de l'attendu"
                    )
                
                # Valeurs hors gamme
                out_of_range = ((crop_data['Yield_kg_ha'] < expected['min']) | 
                               (crop_data['Yield_kg_ha'] > expected['max'])).sum()
                out_of_range_pct = (out_of_range / len(crop_data)) * 100
                
                if out_of_range_pct > 5:
                    self.warnings_list.append(
                        f"{crop}: {out_of_range_pct:.1f}% rendements hors gamme réaliste"
                    )
            
            # Adaptation zones agro-climatiques
            zone_adaptation = crop_data['AgroZone'].value_counts()
            print(f"      Zones de culture: {dict(zone_adaptation)}")
            
            # Vérification adaptations non réalistes
            if crop == 'mil' and 'sud_tropical' in zone_adaptation.index:
                self.critical_issues.append("Mil cultivé en zone sud-tropicale (non réaliste)")
            if crop == 'riz' and zone_adaptation.get('sahelien', 0) > len(crop_data) * 0.1:
                self.warnings_list.append("Riz sur-représenté en zone sahélienne")
            
            crop_validation[crop] = {
                'n_observations': len(crop_data),
                'mean_yield': actual_mean,
                'yield_range': actual_range,
                'zone_distribution': dict(zone_adaptation)
            }
        
        self.validation_results['crop_specific'] = crop_validation

    def validate_geographic_coherence(self):
        """Validation cohérence géographique et zonage"""
        print("  🗺️ Validation cohérence géographique...")
        
        # Correspondance localité-zone attendue (selon générateur)
        expected_zones = {
            'SIKASSO': 'sud_tropical',
            'BAMAKO': 'soudanien', 
            'BOUGOUNI': 'soudanien',
            'SAMANKO': 'soudanien',
            'BAGUINEDA': 'soudanien',
            'KASSELA': 'soudanien',
            'SEGOU': 'sahelien',
            'MOPTI': 'sahelien'
        }
        
        geographic_issues = []
        
        for locality in self.df['Locality'].unique():
            locality_data = self.df[self.df['Locality'] == locality.upper()]
            zones_observed = locality_data['AgroZone'].unique()
            
            if locality.upper() in expected_zones:
                expected_zone = expected_zones[locality.upper()]
                if len(zones_observed) > 1:
                    geographic_issues.append(f"{locality}: multiple zones détectées {zones_observed}")
                elif zones_observed[0] != expected_zone:
                    geographic_issues.append(
                        f"{locality}: zone {zones_observed[0]} vs attendue {expected_zone}"
                    )
                else:
                    print(f"    ✅ {locality}: zone {expected_zone} cohérente")
            else:
                geographic_issues.append(f"{locality}: localité non reconnue")
        
        if geographic_issues:
            self.critical_issues.extend(geographic_issues)
            print("    🚨 Problèmes géographiques détectés:")
            for issue in geographic_issues:
                print(f"      - {issue}")
        
        # Validation gradients climatiques par zone
        print("    🌡️ Gradients climatiques par zone:")
        climate_by_zone = self.df.groupby('AgroZone')[['SeasonRainfall_mm', 'MeanTemp_C']].mean()
        print(climate_by_zone)
        
        # Vérification gradient attendu (sahélien < soudanien < sud_tropical pour pluie)
        if len(climate_by_zone) >= 2:
            if 'sahelien' in climate_by_zone.index and 'soudanien' in climate_by_zone.index:
                if climate_by_zone.loc['sahelien', 'SeasonRainfall_mm'] > \
                   climate_by_zone.loc['soudanien', 'SeasonRainfall_mm']:
                    self.critical_issues.append("Gradient pluviométrique inversé sahélien-soudanien")
        
        self.validation_results['geographic'] = {
            'zone_coherence': geographic_issues,
            'climate_gradients': climate_by_zone.to_dict()
        }

    def detect_anomalies(self):
        """Détection anomalies et outliers potentiellement problématiques"""
        print("  🚨 Détection anomalies et outliers...")
        
        anomalies_detected = {}
        
        # Variables critiques à analyser
        critical_variables = [
            'Yield_kg_ha', 'NDVI_peak', 'SeasonRainfall_mm', 'MeanTemp_C',
            'Soil_pH', 'FertN_kg_ha', 'Stress_Water_graded'
        ]
        
        for variable in critical_variables:
            if variable in self.df.columns:
                data = self.df[variable].dropna()
                
                # Méthode IQR pour outliers
                Q1 = data.quantile(0.25)
                Q3 = data.quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = data[(data < lower_bound) | (data > upper_bound)]
                outlier_percentage = (len(outliers) / len(data)) * 100
                
                # Test normalité
                stat_normal, p_normal = normaltest(data)
                is_normal = p_normal > 0.05
                
                anomalies_detected[variable] = {
                    'outliers_count': len(outliers),
                    'outliers_percentage': outlier_percentage,
                    'is_normal_distribution': is_normal,
                    'normality_p_value': p_normal,
                    'extreme_values': {
                        'min': data.min(),
                        'max': data.max(),
                        'q01': data.quantile(0.01),
                        'q99': data.quantile(0.99)
                    }
                }
                
                print(f"    📊 {variable}:")
                print(f"      Outliers: {len(outliers)} ({outlier_percentage:.1f}%)")
                print(f"      Distribution normale: {'Oui' if is_normal else 'Non'} (p={p_normal:.3f})")
                
                if outlier_percentage > 10:
                    self.warnings_list.append(f"{variable}: {outlier_percentage:.1f}% outliers")
        
        # Détection combinaisons impossibles
        print("    🔍 Détection combinaisons impossibles:")
        impossible_combinations = 0
        
        # Exemples de combinaisons physiquement impossibles
        if 'Stress_Water_graded' in self.df.columns and 'Yield_kg_ha' in self.df.columns:
            # Stress hydrique sévère (>0.8) avec rendements très élevés
            severe_stress_high_yield = self.df[
                (self.df['Stress_Water_graded'] > 0.8) & 
                (self.df['Yield_kg_ha'] > self.df.groupby('Crop')['Yield_kg_ha'].transform('quantile', 0.9))
            ]
            if len(severe_stress_high_yield) > 0:
                impossible_combinations += len(severe_stress_high_yield)
                print(f"      ⚠️ {len(severe_stress_high_yield)} cas: stress hydrique sévère + rendement élevé")
        
        # NDVI très faible avec rendements élevés
        if 'NDVI_peak' in self.df.columns and 'Yield_kg_ha' in self.df.columns:
            low_ndvi_high_yield = self.df[
                (self.df['NDVI_peak'] < 0.3) & 
                (self.df['Yield_kg_ha'] > self.df['Yield_kg_ha'].quantile(0.8))
            ]
            if len(low_ndvi_high_yield) > 0:
                impossible_combinations += len(low_ndvi_high_yield)
                print(f"      ⚠️ {len(low_ndvi_high_yield)} cas: NDVI faible + rendement élevé")
        
        if impossible_combinations > len(self.df) * 0.01:  # Plus de 1%
            self.critical_issues.append(f"{impossible_combinations} combinaisons physiquement douteuses")
        
        self.validation_results['anomalies'] = anomalies_detected

    def create_advanced_visualizations(self):
        """Génération visualisations avancées pour validation"""
        print("  📊 Génération visualisations avancées...")
        
        # Configuration subplots
        fig = plt.figure(figsize=(20, 24))
        
        # 1. Distribution des rendements par culture
        plt.subplot(4, 3, 1)
        sns.boxplot(data=self.df, x='Crop', y='Yield_kg_ha')
        plt.title('Distribution Rendements par Culture', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45)
        plt.ylabel('Rendement (kg/ha)')
        
        # 2. Corrélation NDVI-Rendement par culture
        plt.subplot(4, 3, 2)
        for crop in self.df['Crop'].unique():
            crop_data = self.df[self.df['Crop'] == crop]
            plt.scatter(crop_data['NDVI_peak'], crop_data['Yield_kg_ha'], 
                       alpha=0.6, label=crop, s=20)
        plt.xlabel('NDVI Peak')
        plt.ylabel('Rendement (kg/ha)')
        plt.title('Relation NDVI-Rendement', fontsize=14, fontweight='bold')
        plt.legend()
        
        # 3. Distribution stress hydrique
        plt.subplot(4, 3, 3)
        sns.histplot(data=self.df, x='Stress_Water_graded', bins=50, alpha=0.7)
        plt.title('Distribution Stress Hydrique', fontsize=14, fontweight='bold')
        plt.xlabel('Stress Hydrique (0-1)')
        
        # 4. Variabilité climatique temporelle
        plt.subplot(4, 3, 4)
        yearly_climate = self.df.groupby('Year')[['SeasonRainfall_mm', 'MeanTemp_C']].mean()
        plt.plot(yearly_climate.index, yearly_climate['SeasonRainfall_mm'], 'b-', label='Pluie (mm)')
        plt.ylabel('Pluviométrie (mm)', color='b')
        plt.tick_params(axis='y', labelcolor='b')
        
        ax2 = plt.gca().twinx()
        ax2.plot(yearly_climate.index, yearly_climate['MeanTemp_C'], 'r-', label='Température (°C)')
        ax2.set_ylabel('Température (°C)', color='r')
        ax2.tick_params(axis='y', labelcolor='r')
        
        plt.title('Variabilité Climatique Temporelle', fontsize=14, fontweight='bold')
        plt.xlabel('Année')
        
        # 5. Distribution géographique
        plt.subplot(4, 3, 5)
        locality_counts = self.df['Locality'].value_counts()
        plt.pie(locality_counts.values, labels=locality_counts.index, autopct='%1.1f%%')
        plt.title('Répartition Géographique', fontsize=14, fontweight='bold')
        
        # 6. Heatmap corrélations variables numériques
        plt.subplot(4, 3, 6)
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns[:15]  # Limiter pour lisibilité
        corr_matrix = self.df[numeric_cols].corr()
        sns.heatmap(corr_matrix, annot=True, cmap='RdBu_r', center=0, 
                   square=True, fmt='.2f', cbar_kws={'shrink': 0.8})
        plt.title('Corrélations Variables Numériques', fontsize=14, fontweight='bold')
        
        # 7. Distribution stress par zone
        plt.subplot(4, 3, 7)
        stress_by_zone = self.df.groupby('AgroZone')[['Stress_Water_graded', 'Stress_Temp_graded', 'Stress_Nitrogen_graded']].mean()
        stress_by_zone.plot(kind='bar', ax=plt.gca())
        plt.title('Stress Moyen par Zone', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45)
        plt.ylabel('Niveau Stress (0-1)')
        plt.legend()
        
        # 8. Rendement vs Pluviométrie
        plt.subplot(4, 3, 8)
        plt.scatter(self.df['SeasonRainfall_mm'], self.df['Yield_kg_ha'], alpha=0.5, s=15)
        plt.xlabel('Pluviométrie Saisonnière (mm)')
        plt.ylabel('Rendement (kg/ha)')
        plt.title('Rendement vs Pluviométrie', fontsize=14, fontweight='bold')
        
        # Ligne de tendance
        z = np.polyfit(self.df['SeasonRainfall_mm'], self.df['Yield_kg_ha'], 1)
        p = np.poly1d(z)
        plt.plot(self.df['SeasonRainfall_mm'], p(self.df['SeasonRainfall_mm']), "r--", alpha=0.8)
        
        # 9. Distribution fertilisation NPK
        plt.subplot(4, 3, 9)
        fert_data = self.df[['FertN_kg_ha', 'FertP_kg_ha', 'FertK_kg_ha']]
        fert_data.boxplot(ax=plt.gca())
        plt.title('Distribution Fertilisation NPK', fontsize=14, fontweight='bold')
        plt.ylabel('Dose (kg/ha)')
        plt.xticks(rotation=45)
        
        # 10. Évolution NDVI par culture
        plt.subplot(4, 3, 10)
        for crop in self.df['Crop'].unique():
            crop_ndvi = self.df[self.df['Crop'] == crop]['NDVI_peak']
            plt.hist(crop_ndvi, alpha=0.6, label=crop, bins=30)
        plt.xlabel('NDVI Peak')
        plt.ylabel('Fréquence')
        plt.title('Distribution NDVI par Culture', fontsize=14, fontweight='bold')
        plt.legend()
        
        # 11. Matrice stress combinés
        plt.subplot(4, 3, 11)
        stress_combinations = self.df[['Stress_Water_graded', 'Stress_Temp_graded']].copy()
        stress_combinations['Stress_Combined'] = stress_combinations.mean(axis=1)
        plt.hexbin(stress_combinations['Stress_Water_graded'], 
                  stress_combinations['Stress_Temp_graded'], 
                  gridsize=20, cmap='YlOrRd')
        plt.xlabel('Stress Hydrique')
        plt.ylabel('Stress Thermique')
        plt.title('Stress Combinés', fontsize=14, fontweight='bold')
        plt.colorbar(label='Densité')
        
        # 12. Qualité sols par zone
        plt.subplot(4, 3, 12)
        soil_by_zone = self.df.groupby('AgroZone')[['Soil_pH', 'Soil_OM_percent', 'Soil_N_kg_ha']].mean()
        soil_by_zone.plot(kind='bar', ax=plt.gca())
        plt.title('Qualité Sols par Zone', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45)
        plt.ylabel('Valeurs Moyennes')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig('tchia_dataset_validation_complete.png', dpi=300, bbox_inches='tight')
        print("    ✅ Visualisations sauvegardées: tchia_dataset_validation_complete.png")
        plt.show()

    def generate_final_report(self):
        """Génération rapport final de validation"""
        print("\n" + "="*80)
        print("📋 RAPPORT FINAL VALIDATION DATASET TCHIA")
        print("="*80)
        
        # Score global de qualité
        total_checks = 20  # Nombre total de vérifications
        critical_score = max(0, 10 - len(self.critical_issues))
        warning_score = max(0, 10 - len(self.warnings_list) // 2)
        quality_score = ((critical_score + warning_score) / total_checks) * 100
        
        print(f"\n🎯 SCORE QUALITÉ GLOBALE: {quality_score:.1f}/100")
        
        # Classification qualité
        if quality_score >= 90:
            quality_level = "EXCELLENT ✨"
            color = "🟢"
        elif quality_score >= 75:
            quality_level = "BON ✅"
            color = "🟡"
        elif quality_score >= 60:
            quality_level = "ACCEPTABLE ⚠️"
            color = "🟠"
        else:
            quality_level = "PROBLÉMATIQUE ❌"
            color = "🔴"
        
        print(f"{color} NIVEAU QUALITÉ: {quality_level}")
        
        # Problèmes critiques
        if self.critical_issues:
            print(f"\n🚨 PROBLÈMES CRITIQUES ({len(self.critical_issues)}):")
            for i, issue in enumerate(self.critical_issues, 1):
                print(f"  {i}. {issue}")
        else:
            print("\n✅ Aucun problème critique détecté")
        
        # Avertissements
        if self.warnings_list:
            print(f"\n⚠️ AVERTISSEMENTS ({len(self.warnings_list)}):")
            for i, warning in enumerate(self.warnings_list, 1):
                print(f"  {i}. {warning}")
        else:
            print("\n✅ Aucun avertissement")
        
        # Recommandations spécifiques
        print(f"\n📋 RECOMMANDATIONS:")
        
        if 'N' in self.df.columns and 'FertN_kg_ha' in self.df.columns:
            print("  1. 🔧 URGENT: Supprimer variables redondantes N, P, K")
            print("     Code: df = df.drop(['N', 'P', 'K'], axis=1)")
        
        if len(self.critical_issues) > 0:
            print("  2. 🚨 Corriger problèmes critiques avant utilisation production")
        
        if quality_score < 75:
            print("  3. ⚡ Recalibrer générateur selon problèmes identifiés")
        
        # Métriques anti-overfitting
        print(f"\n🧠 MÉTRIQUES ANTI-OVERFITTING:")
        
        # Diversité temporelle
        year_range = self.df['Year'].max() - self.df['Year'].min()
        print(f"  • Couverture temporelle: {year_range + 1} années ({'✅' if year_range >= 5 else '⚠️'})")
        
        # Diversité géographique
        n_localities = self.df['Locality'].nunique()
        print(f"  • Diversité géographique: {n_localities} localités ({'✅' if n_localities >= 6 else '⚠️'})")
        
        # Diversité culturale
        n_crops = self.df['Crop'].nunique()
        print(f"  • Diversité culturale: {n_crops} cultures ({'✅' if n_crops >= 4 else '⚠️'})")
        
        # Variabilité climatique
        cv_rain = self.df['SeasonRainfall_mm'].std() / self.df['SeasonRainfall_mm'].mean()
        print(f"  • Variabilité pluviométrique: CV = {cv_rain:.3f} ({'✅' if cv_rain > 0.3 else '⚠️'})")
        
        # Distribution des stress
        stress_diversity = (
            (self.df['Stress_Water_graded'] > 0.5).mean() > 0.2 and
            (self.df['Stress_Temp_graded'] > 0.5).mean() > 0.15 and
            (self.df['Stress_Nitrogen_graded'] > 0.5).mean() > 0.2
        )
        print(f"  • Diversité scénarios stress: {'✅' if stress_diversity else '⚠️'}")
        
        # Conclusion et prochaines étapes
        print(f"\n🎯 CONCLUSION:")
        if quality_score >= 75:
            print("  ✅ Dataset TCHIA validé pour entraînement modèles ML")
            print("  ✅ Variabilité suffisante pour éviter overfitting")
            print("  ✅ Cohérence scientifique confirmée")
        else:
            print("  ❌ Dataset nécessite corrections avant utilisation")
            print("  ⚡ Recalibration générateur recommandée")
        
        print(f"\n📊 STATISTIQUES FINALES:")
        print(f"  • Observations analysées: {len(self.df):,}")
        print(f"  • Variables validées: {len(self.df.columns)}")
        print(f"  • Problèmes critiques: {len(self.critical_issues)}")
        print(f"  • Avertissements: {len(self.warnings_list)}")
        print(f"  • Score qualité: {quality_score:.1f}/100")
        
        # Sauvegarde rapport
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        report_data = {
            'timestamp': timestamp,
            'quality_score': quality_score,
            'critical_issues': self.critical_issues,
            'warnings': self.warnings_list,
            'validation_results': self.validation_results
        }
        
        import json
        with open(f'tchia_validation_report_{timestamp}.json', 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        print(f"\n💾 Rapport détaillé sauvegardé: tchia_validation_report_{timestamp}.json")
        
        return {
            'quality_score': quality_score,
            'quality_level': quality_level,
            'critical_issues': self.critical_issues,
            'warnings': self.warnings_list,
            'recommendations': []
        }


# =============================================================================
# 🚀 EXÉCUTION VALIDATION COMPLÈTE
# =============================================================================

def main():
    """Fonction principale d'exécution"""
    print("🚀 DÉMARRAGE VALIDATION EXHAUSTIVE DATASET TCHIA")
    print("="*60)
    
    # Chemin dataset (à adapter selon votre configuration)
    dataset_path = 'dataset_mali_realistic_20250621_132403.csv'  # Votre fichier 1M observations
    
    try:
        # Initialisation validateur
        validator = TCHIADatasetValidator(dataset_path)
        
        # Exécution validation complète
        results = validator.run_complete_validation()
        
        print("\n🎉 VALIDATION TERMINÉE AVEC SUCCÈS!")
        print(f"Score qualité final: {results['quality_score']:.1f}/100")
        
        return results
        
    except FileNotFoundError:
        print(f"❌ ERREUR: Fichier {dataset_path} non trouvé")
        print("Vérifiez le chemin du dataset")
        return None
    except Exception as e:
        print(f"❌ ERREUR VALIDATION: {e}")
        return None

if __name__ == "__main__":
    validation_results = main()
