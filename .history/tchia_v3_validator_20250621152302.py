"""
=============================================================================
VALIDATEUR COHÉRENCE CAUSALE TCHIA V3
=============================================================================

🎯 OBJECTIF : Valider que chaque ligne raconte une histoire cohérente
📊 MÉTHODE : Tests causaux multi-niveaux + comparaison distributions réelles
🔬 VALIDATION : Basée sur connaissances agronomiques Mali

Auteur : Système TCHIA v3.0 - Validation Causale
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


# =============================================================================
# 📊 DISTRIBUTIONS RÉELLES MALI (RÉFÉRENCE)
# =============================================================================

@dataclass
class RealDistributions:
    """
    Distributions réelles observées au Mali pour validation
    
    📚 Sources : FAOSTAT, IER Mali, CMDT, enquêtes LSMS-ISA
    """
    
    # Rendements moyens par culture (kg/ha) - Source : IER 2010-2024
    YIELD_DISTRIBUTIONS = {
        "mil": {"mean": 865, "std": 250, "min": 200, "max": 1500},
        "sorgho": {"mean": 1000, "std": 300, "min": 300, "max": 1800},
        "maïs": {"mean": 1800, "std": 600, "min": 500, "max": 4000},
        "coton": {"mean": 1100, "std": 300, "min": 400, "max": 2200},
        "riz": {"mean": 2500, "std": 800, "min": 800, "max": 5500}
    }
    
    # Coefficients de variation par zone
    CV_BY_ZONE = {
        "sahelien": 0.35,      # Plus variable
        "soudanien": 0.25,     # Modérément variable
        "sud_tropical": 0.20   # Moins variable
    }
    
    # Corrélations connues
    KNOWN_CORRELATIONS = {
        "rainfall_yield": {"mil": 0.72, "sorgho": 0.68, "maïs": 0.85},
        "ndvi_yield": {"range": (0.65, 0.88)},  # Selon culture et stade
        "stress_yield": {"water": -0.76, "temp": -0.54, "combined": -0.82}
    }
    
    # Fréquences stress observées
    STRESS_FREQUENCIES = {
        "water_stress": {"none": 0.15, "mild": 0.35, "moderate": 0.35, "severe": 0.15},
        "temp_stress": {"none": 0.30, "mild": 0.40, "moderate": 0.25, "severe": 0.05}
    }


# =============================================================================
# 🔍 TESTS DE COHÉRENCE CAUSALE
# =============================================================================

class CausalCoherenceTests:
    """
    Batterie de tests pour valider la cohérence causale
    
    🔬 Chaque test vérifie une relation causale spécifique
    📊 Retourne : (passed: bool, message: str, severity: str)
    """
    
    @staticmethod
    def test_stress_yield_coherence(row: pd.Series) -> Tuple[bool, str, str]:
        """
        Test 1 : Cohérence stress-rendement
        
        📚 Règle : Stress sévère → Rendement faible obligatoire
        """
        accumulated_stress = row['AccumulatedStress']
        yield_loss = row['YieldLoss_percent']
        scenario = row['Scenario']
        
        # Règles de cohérence
        if accumulated_stress > 0.7 and yield_loss < 40:
            return False, f"Stress élevé ({accumulated_stress:.2f}) mais perte faible ({yield_loss:.1f}%)", "CRITICAL"
        
        if accumulated_stress < 0.2 and yield_loss > 60:
            return False, f"Stress faible ({accumulated_stress:.2f}) mais perte élevée ({yield_loss:.1f}%)", "CRITICAL"
        
        # Cohérence avec scénario
        if scenario == "exceptional" and yield_loss > 20:
            return False, f"Scénario exceptionnel mais perte >20% ({yield_loss:.1f}%)", "HIGH"
        
        if scenario == "catastrophic" and yield_loss < 50:
            return False, f"Scénario catastrophique mais perte <50% ({yield_loss:.1f}%)", "HIGH"
        
        return True, "Cohérence stress-rendement validée", "OK"
    
    @staticmethod
    def test_rainfall_effectiveness(row: pd.Series) -> Tuple[bool, str, str]:
        """
        Test 2 : Cohérence pluie-ruissellement
        
        📚 Règle : 30-70% ruissellement pour 15-45mm début saison
        """
        total_rain = row['SeasonRainfall_mm']
        effective_rain = row['EffectiveRainfall_mm']
        runoff = row['Runoff_mm']
        
        if total_rain > 0:
            runoff_percent = (runoff / total_rain) * 100
            
            # Validation bornes physiques
            if effective_rain > total_rain:
                return False, f"Pluie effective ({effective_rain}mm) > pluie totale ({total_rain}mm)", "CRITICAL"
            
            # Validation ruissellement début saison
            rainfall_dist = row['RainfallDistribution']
            early_rain = rainfall_dist['mai'] + rainfall_dist['juin']
            
            if 15 <= early_rain <= 45 and not (30 <= runoff_percent <= 70):
                return False, f"Ruissellement hors bornes pour début saison ({runoff_percent:.1f}%)", "MEDIUM"
        
        return True, "Cohérence hydrologique validée", "OK"
    
    @staticmethod
    def test_temporal_consistency(row: pd.Series) -> Tuple[bool, str, str]:
        """
        Test 3 : Cohérence temporelle des événements
        
        📚 Règle : Stress précoce → Impact sur tout le cycle
        """
        stress_history = row['StressHistory']
        growth_reduction = row['GrowthReduction']
        
        if not stress_history:
            if growth_reduction > 0.1:
                return False, "Réduction croissance sans stress enregistré", "HIGH"
            return True, "Pas de stress, pas de réduction", "OK"
        
        # Vérifier propagation temporelle
        early_stress = any(s['stage'] in ['germination', 'vegetative'] 
                          and s['intensity'] > 0.5 for s in stress_history)
        
        if early_stress and growth_reduction < 0.2:
            return False, "Stress précoce sévère mais faible impact croissance", "MEDIUM"
        
        # Vérifier cohérence intensité-durée
        max_intensity = max(s['intensity'] for s in stress_history)
        total_days = sum(s['duration'] for s in stress_history)
        
        if max_intensity > 0.8 and total_days > 20 and growth_reduction < 0.4:
            return False, f"Stress intense et long ({total_days}j) mais impact limité", "HIGH"
        
        return True, "Cohérence temporelle validée", "OK"
    
    @staticmethod
    def test_farmer_decisions_logic(row: pd.Series) -> Tuple[bool, str, str]:
        """
        Test 4 : Logique des décisions paysannes
        
        📚 Règle : Décisions cohérentes avec conditions et économie
        """
        initial_crop = row['InitialCrop']
        final_crop = row['FinalCrop']
        scenario = row['Scenario']
        bc_ratio = row['BC_Ratio']
        management = row['ManagementStrategy']
        
        # Changement culture cohérent
        if initial_crop != final_crop:
            if scenario in ["exceptional", "good"]:
                return False, f"Changement culture en {scenario} année", "MEDIUM"
            
            # Logique substitution
            valid_substitutions = {
                "maïs": ["sorgho", "mil"],
                "coton": ["mil", "sorgho"],
                "riz": ["sorgho"],
                "sorgho": ["mil"]
            }
            
            if final_crop not in valid_substitutions.get(initial_crop, []):
                return False, f"Substitution illogique {initial_crop}→{final_crop}", "HIGH"
        
        # Cohérence économique
        if bc_ratio < 1.8 and management != "reduce_risk":
            return False, f"B/C faible ({bc_ratio:.2f}) mais stratégie non adaptée", "MEDIUM"
        
        return True, "Décisions paysannes cohérentes", "OK"
    
    @staticmethod
    def test_ndvi_biomass_consistency(row: pd.Series) -> Tuple[bool, str, str]:
        """
        Test 5 : Cohérence NDVI-biomasse-rendement
        
        📚 Règle : Relations empiriques validées Mali
        """
        ndvi_peak = row['NDVI_peak']
        biomass = row['BiomassTotal_kg_ha']
        grain_yield = row['ActualYield_kg_ha']
        crop = row['FinalCrop']
        
        # Harvest Index réaliste
        expected_hi = {
            "mil": (0.20, 0.35),
            "sorgho": (0.25, 0.45),
            "maïs": (0.40, 0.55),
            "coton": (0.15, 0.25),
            "riz": (0.45, 0.55)
        }
        
        if biomass > 0:
            actual_hi = grain_yield / biomass
            hi_range = expected_hi.get(crop, (0.2, 0.5))
            
            if not (hi_range[0] <= actual_hi <= hi_range[1]):
                return False, f"Harvest Index irréaliste ({actual_hi:.2f}) pour {crop}", "HIGH"
        
        # Cohérence NDVI-rendement
        if ndvi_peak > 0.8 and grain_yield < 1000:
            return False, f"NDVI élevé ({ndvi_peak:.2f}) mais faible rendement", "HIGH"
        
        if ndvi_peak < 0.3 and grain_yield > 2000:
            return False, f"NDVI faible ({ndvi_peak:.2f}) mais rendement élevé", "HIGH"
        
        return True, "Cohérence NDVI-biomasse validée", "OK"
    
    @staticmethod
    def test_scenario_consistency(row: pd.Series) -> Tuple[bool, str, str]:
        """
        Test 6 : Cohérence globale du scénario
        
        📚 Règle : Toutes les variables racontent la même histoire
        """
        scenario = row['Scenario']
        narrative = row['ScenarioNarrative']
        stress = row['AccumulatedStress']
        yield_loss = row['YieldLoss_percent']
        
        # Bornes attendues par scénario
        expected_ranges = {
            "exceptional": {"stress": (0, 0.2), "loss": (0, 20)},
            "good": {"stress": (0.1, 0.4), "loss": (10, 30)},
            "average": {"stress": (0.3, 0.6), "loss": (25, 50)},
            "difficult": {"stress": (0.5, 0.8), "loss": (40, 70)},
            "catastrophic": {"stress": (0.7, 1.0), "loss": (60, 95)}
        }
        
        ranges = expected_ranges.get(scenario)
        if ranges:
            stress_ok = ranges["stress"][0] <= stress <= ranges["stress"][1]
            loss_ok = ranges["loss"][0] <= yield_loss <= ranges["loss"][1]
            
            if not stress_ok:
                return False, f"Stress hors bornes pour scénario {scenario}", "HIGH"
            
            if not loss_ok:
                return False, f"Perte rendement hors bornes pour scénario {scenario}", "HIGH"
        
        return True, "Cohérence scénario validée", "OK"


# =============================================================================
# 📈 ANALYSEUR DE DISTRIBUTIONS
# =============================================================================

class DistributionAnalyzer:
    """
    Analyse et compare les distributions avec les références réelles
    
    📊 Génère statistiques et graphiques de validation
    """
    
    def __init__(self, reference: RealDistributions = RealDistributions()):
        self.reference = reference
    
    def analyze_yield_distributions(self, df: pd.DataFrame) -> Dict:
        """Analyse distributions rendements par culture"""
        
        results = {}
        
        for crop in df['FinalCrop'].unique():
            crop_data = df[df['FinalCrop'] == crop]['ActualYield_kg_ha']
            
            if len(crop_data) > 0:
                # Statistiques observées
                obs_mean = crop_data.mean()
                obs_std = crop_data.std()
                obs_cv = obs_std / obs_mean if obs_mean > 0 else 0
                
                # Référence
                ref = self.reference.YIELD_DISTRIBUTIONS.get(crop, {})
                ref_mean = ref.get('mean', obs_mean)
                ref_std = ref.get('std', obs_std)
                
                # Tests statistiques
                mean_diff_pct = abs(obs_mean - ref_mean) / ref_mean * 100
                cv_diff = abs(obs_cv - ref_std/ref_mean)
                
                # Validation
                mean_ok = mean_diff_pct < 20  # Tolérance 20%
                cv_ok = cv_diff < 0.1          # Tolérance 0.1
                
                results[crop] = {
                    "observed_mean": round(obs_mean, 1),
                    "reference_mean": ref_mean,
                    "mean_diff_percent": round(mean_diff_pct, 1),
                    "observed_cv": round(obs_cv, 3),
                    "reference_cv": round(ref_std/ref_mean, 3),
                    "mean_validated": mean_ok,
                    "cv_validated": cv_ok,
                    "overall_valid": mean_ok and cv_ok
                }
        
        return results
    
    def analyze_correlations(self, df: pd.DataFrame) -> Dict:
        """Analyse corrélations clés"""
        
        correlations = {}
        
        # Corrélation pluie-rendement
        for crop in df['FinalCrop'].unique():
            crop_df = df[df['FinalCrop'] == crop]
            if len(crop_df) > 10:
                corr = crop_df['EffectiveRainfall_mm'].corr(crop_df['ActualYield_kg_ha'])
                expected = self.reference.KNOWN_CORRELATIONS["rainfall_yield"].get(crop, 0.7)
                
                correlations[f"rainfall_yield_{crop}"] = {
                    "observed": round(corr, 3),
                    "expected": expected,
                    "validated": abs(corr - expected) < 0.15
                }
        
        # Corrélation NDVI-rendement
        corr_ndvi = df['NDVI_peak'].corr(df['ActualYield_kg_ha'])
        ndvi_range = self.reference.KNOWN_CORRELATIONS["ndvi_yield"]["range"]
        
        correlations["ndvi_yield"] = {
            "observed": round(corr_ndvi, 3),
            "expected_range": ndvi_range,
            "validated": ndvi_range[0] <= corr_ndvi <= ndvi_range[1]
        }
        
        # Corrélation stress-rendement (négative attendue)
        corr_stress = df['AccumulatedStress'].corr(df['YieldLoss_percent'])
        
        correlations["stress_loss"] = {
            "observed": round(corr_stress, 3),
            "expected": ">0.7",
            "validated": corr_stress > 0.7
        }
        
        return correlations
    
    def analyze_stress_frequencies(self, df: pd.DataFrame) -> Dict:
        """Analyse fréquences des stress"""
        
        # Extraction niveaux de stress depuis l'historique
        stress_levels = {"water": [], "temp": []}
        
        for _, row in df.iterrows():
            history = row['StressHistory']
            if history:
                max_water = max([s['intensity'] for s in history 
                               if s['type'] == 'water'], default=0)
                max_temp = max([s['intensity'] for s in history 
                              if s['type'] == 'temp'], default=0)
                
                # Classification
                for stress_val, stress_list in [(max_water, stress_levels["water"]), 
                                               (max_temp, stress_levels["temp"])]:
                    if stress_val < 0.15:
                        stress_list.append("none")
                    elif stress_val < 0.4:
                        stress_list.append("mild")
                    elif stress_val < 0.7:
                        stress_list.append("moderate")
                    else:
                        stress_list.append("severe")
        
        # Calcul fréquences
        results = {}
        
        for stress_type in ["water", "temp"]:
            if stress_levels[stress_type]:
                obs_freq = pd.Series(stress_levels[stress_type]).value_counts(normalize=True)
                ref_freq = self.reference.STRESS_FREQUENCIES[f"{stress_type}_stress"]
                
                # Comparaison
                freq_diff = 0
                for level in ["none", "mild", "moderate", "severe"]:
                    obs = obs_freq.get(level, 0)
                    ref = ref_freq.get(level, 0.25)
                    freq_diff += abs(obs - ref)
                
                results[stress_type] = {
                    "observed": {k: round(v, 3) for k, v in obs_freq.to_dict().items()},
                    "reference": ref_freq,
                    "total_deviation": round(freq_diff, 3),
                    "validated": freq_diff < 0.3  # Tolérance 30% déviation totale
                }
        
        return results


# =============================================================================
# 📊 GÉNÉRATEUR DE RAPPORTS
# =============================================================================

class QualityReportGenerator:
    """
    Génère rapports de qualité détaillés
    
    📈 Formats : Console, JSON, HTML, PDF
    """
    
    def __init__(self):
        self.tests = CausalCoherenceTests()
        self.analyzer = DistributionAnalyzer()
    
    def validate_dataset(self, df: pd.DataFrame, verbose: bool = True) -> Dict:
        """
        Validation complète du dataset
        
        Retourne rapport structuré avec tous les résultats
        """
        
        report = {
            "metadata": {
                "date": datetime.now().isoformat(),
                "n_rows": len(df),
                "n_columns": len(df.columns),
                "crops": df['FinalCrop'].unique().tolist(),
                "scenarios": df['Scenario'].value_counts().to_dict()
            },
            "coherence_tests": {},
            "distribution_analysis": {},
            "summary": {}
        }
        
        # 1️⃣ TESTS DE COHÉRENCE
        if verbose:
            print("\n🔍 TESTS DE COHÉRENCE CAUSALE")
            print("=" * 60)
        
        test_methods = [
            ("stress_yield", self.tests.test_stress_yield_coherence),
            ("rainfall_effectiveness", self.tests.test_rainfall_effectiveness),
            ("temporal_consistency", self.tests.test_temporal_consistency),
            ("farmer_decisions", self.tests.test_farmer_decisions_logic),
            ("ndvi_biomass", self.tests.test_ndvi_biomass_consistency),
            ("scenario_consistency", self.tests.test_scenario_consistency)
        ]
        
        for test_name, test_method in test_methods:
            results = []
            failures = []
            
            for idx, row in df.iterrows():
                passed, message, severity = test_method(row)
                results.append(passed)
                
                if not passed:
                    failures.append({
                        "row": idx,
                        "message": message,
                        "severity": severity
                    })
            
            pass_rate = sum(results) / len(results) * 100
            
            report["coherence_tests"][test_name] = {
                "pass_rate": round(pass_rate, 1),
                "n_failures": len(failures),
                "failures": failures[:5]  # Top 5 pour le rapport
            }
            
            if verbose:
                status = "✅" if pass_rate > 95 else "⚠️" if pass_rate > 80 else "❌"
                print(f"{status} {test_name}: {pass_rate:.1f}% réussite")
                if failures and verbose:
                    print(f"   Exemple échec: {failures[0]['message']}")
        
        # 2️⃣ ANALYSE DISTRIBUTIONS
        if verbose:
            print("\n📊 ANALYSE DES DISTRIBUTIONS")
            print("=" * 60)
        
        # Rendements
        yield_analysis = self.analyzer.analyze_yield_distributions(df)
        report["distribution_analysis"]["yields"] = yield_analysis
        
        if verbose:
            print("\n📈 Rendements moyens (kg/ha):")
            for crop, stats in yield_analysis.items():
                status = "✅" if stats["overall_valid"] else "❌"
                print(f"{status} {crop}: {stats['observed_mean']} "
                      f"(ref: {stats['reference_mean']}, diff: {stats['mean_diff_percent']}%)")
        
        # Corrélations
        correlations = self.analyzer.analyze_correlations(df)
        report["distribution_analysis"]["correlations"] = correlations
        
        if verbose:
            print("\n🔗 Corrélations clés:")
            for corr_name, stats in correlations.items():
                status = "✅" if stats["validated"] else "❌"
                print(f"{status} {corr_name}: {stats['observed']}")
        
        # Fréquences stress
        stress_freq = self.analyzer.analyze_stress_frequencies(df)
        report["distribution_analysis"]["stress_frequencies"] = stress_freq
        
        # 3️⃣ RÉSUMÉ GLOBAL
        all_coherence_rates = [t["pass_rate"] for t in report["coherence_tests"].values()]
        all_distribution_valid = [
            stats["overall_valid"] 
            for stats in report["distribution_analysis"]["yields"].values()
        ]
        
        report["summary"] = {
            "coherence_score": round(np.mean(all_coherence_rates), 1),
            "distribution_score": round(sum(all_distribution_valid) / len(all_distribution_valid) * 100, 1)
                if all_distribution_valid else 0,
            "overall_quality": "EXCELLENT" if np.mean(all_coherence_rates) > 95 else
                              "GOOD" if np.mean(all_coherence_rates) > 85 else
                              "ACCEPTABLE" if np.mean(all_coherence_rates) > 75 else
                              "POOR",
            "recommendation": self._generate_recommendation(report)
        }
        
        if verbose:
            print("\n📋 RÉSUMÉ QUALITÉ")
            print("=" * 60)
            print(f"Score cohérence: {report['summary']['coherence_score']}%")
            print(f"Score distributions: {report['summary']['distribution_score']}%")
            print(f"Qualité globale: {report['summary']['overall_quality']}")
            print(f"\n💡 Recommandation: {report['summary']['recommendation']}")
        
        return report
    
    def _generate_recommendation(self, report: Dict) -> str:
        """Génère recommandation basée sur l'analyse"""
        
        coherence_score = report["summary"]["coherence_score"]
        
        if coherence_score > 95:
            return "Dataset prêt pour entraînement IA. Excellente cohérence causale."
        elif coherence_score > 85:
            return "Dataset utilisable. Quelques incohérences mineures à surveiller."
        elif coherence_score > 75:
            return "Dataset acceptable mais perfectible. Revoir les cas d'échec critiques."
        else:
            return "Dataset nécessite corrections. Trop d'incohérences causales."
    
    def generate_visual_report(self, df: pd.DataFrame, output_path: str = "validation_report.png"):
        """Génère rapport visuel avec graphiques"""
        
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle("Rapport Validation Cohérence Causale TCHIA V3", fontsize=16)
        
        # 1. Distribution rendements par culture
        ax = axes[0, 0]
        df.boxplot(column='ActualYield_kg_ha', by='FinalCrop', ax=ax)
        ax.set_title("Rendements par culture")
        ax.set_xlabel("Culture")
        ax.set_ylabel("Rendement (kg/ha)")
        
        # 2. Relation stress-perte
        ax = axes[0, 1]
        ax.scatter(df['AccumulatedStress'], df['YieldLoss_percent'], alpha=0.6)
        ax.set_xlabel("Stress accumulé")
        ax.set_ylabel("Perte rendement (%)")
        ax.set_title("Cohérence stress-perte")
        
        # 3. Distribution scénarios
        ax = axes[0, 2]
        scenario_counts = df['Scenario'].value_counts()
        ax.pie(scenario_counts.values, labels=scenario_counts.index, autopct='%1.1f%%')
        ax.set_title("Répartition scénarios")
        
        # 4. NDVI vs Rendement
        ax = axes[1, 0]
        ax.scatter(df['NDVI_peak'], df['ActualYield_kg_ha'], alpha=0.6)
        ax.set_xlabel("NDVI max")
        ax.set_ylabel("Rendement (kg/ha)")
        ax.set_title("Cohérence NDVI-rendement")
        
        # 5. Efficacité pluie
        ax = axes[1, 1]
        runoff_pct = (df['Runoff_mm'] / df['SeasonRainfall_mm'] * 100).dropna()
        ax.hist(runoff_pct, bins=20, edgecolor='black')
        ax.axvline(30, color='red', linestyle='--', label='Min attendu')
        ax.axvline(70, color='red', linestyle='--', label='Max attendu')
        ax.set_xlabel("Ruissellement (%)")
        ax.set_ylabel("Fréquence")
        ax.set_title("Distribution ruissellement")
        ax.legend()
        
        # 6. Score cohérence par test
        ax = axes[1, 2]
        report = self.validate_dataset(df, verbose=False)
        test_scores = [v["pass_rate"] for v in report["coherence_tests"].values()]
        test_names = list(report["coherence_tests"].keys())
        
        colors = ['green' if s > 95 else 'orange' if s > 80 else 'red' for s in test_scores]
        ax.barh(test_names, test_scores, color=colors)
        ax.set_xlabel("Taux de réussite (%)")
        ax.set_title("Scores tests cohérence")
        ax.axvline(95, color='green', linestyle='--', alpha=0.5)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"\n📊 Rapport visuel sauvegardé : {output_path}")
    
    def export_detailed_report(self, report: Dict, format: str = "json", filename: str = "report"):
        """Exporte rapport détaillé dans différents formats"""
        
        if format == "json":
            with open(f"{filename}.json", 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"📄 Rapport JSON exporté : {filename}.json")
        
        elif format == "html":
            html_content = self._generate_html_report(report)
            with open(f"{filename}.html", 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"🌐 Rapport HTML exporté : {filename}.html")
    
    def _generate_html_report(self, report: Dict) -> str:
        """Génère rapport HTML formaté"""
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Rapport Validation TCHIA V3</title>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h1 {{ color: #2c3e50; }}
                h2 {{ color: #34495e; }}
                .score-excellent {{ color: green; font-weight: bold; }}
                .score-good {{ color: orange; font-weight: bold; }}
                .score-poor {{ color: red; font-weight: bold; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .summary-box {{ 
                    background-color: #ecf0f1; 
                    padding: 20px; 
                    border-radius: 10px;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <h1>Rapport de Validation - Cohérence Causale TCHIA V3</h1>
            <p>Date : {report['metadata']['date']}</p>
            <p>Nombre de lignes : {report['metadata']['n_rows']}</p>
            
            <div class="summary-box">
                <h2>Résumé Exécutif</h2>
                <p>Score de cohérence : <span class="{self._get_score_class(report['summary']['coherence_score'])}">{report['summary']['coherence_score']}%</span></p>
                <p>Qualité globale : <strong>{report['summary']['overall_quality']}</strong></p>
                <p>Recommandation : {report['summary']['recommendation']}</p>
            </div>
            
            <h2>Tests de Cohérence Causale</h2>
            <table>
                <tr>
                    <th>Test</th>
                    <th>Taux de réussite</th>
                    <th>Échecs</th>
                </tr>
        """
        
        for test_name, results in report['coherence_tests'].items():
            score_class = self._get_score_class(results['pass_rate'])
            html += f"""
                <tr>
                    <td>{test_name.replace('_', ' ').title()}</td>
                    <td class="{score_class}">{results['pass_rate']}%</td>
                    <td>{results['n_failures']}</td>
                </tr>
            """
        
        html += """
            </table>
            
            <h2>Analyse des Distributions</h2>
            <h3>Rendements par culture</h3>
            <table>
                <tr>
                    <th>Culture</th>
                    <th>Moyenne observée</th>
                    <th>Moyenne référence</th>
                    <th>Écart</th>
                    <th>Validation</th>
                </tr>
        """
        
        for crop, stats in report['distribution_analysis']['yields'].items():
            validation = "✅" if stats['overall_valid'] else "❌"
            html += f"""
                <tr>
                    <td>{crop}</td>
                    <td>{stats['observed_mean']} kg/ha</td>
                    <td>{stats['reference_mean']} kg/ha</td>
                    <td>{stats['mean_diff_percent']}%</td>
                    <td>{validation}</td>
                </tr>
            """
        
        html += """
            </table>
        </body>
        </html>
        """
        
        return html
    
    def _get_score_class(self, score: float) -> str:
        """Retourne classe CSS selon score"""
        if score > 95:
            return "score-excellent"
        elif score > 80:
            return "score-good"
        else:
            return "score-poor"


# =============================================================================
# 🧪 TESTS ET DÉMONSTRATION
# =============================================================================

if __name__ == "__main__":
    print("🔍 VALIDATEUR DE COHÉRENCE CAUSALE TCHIA V3")
    print("=" * 60)
    
    # Import du générateur V3
    try:
        from tchia_v3_generator import CausalCoherentGenerator, ScenarioType
    except ImportError:
        print("❌ Erreur : Le générateur V3 doit être dans le même dossier")
        exit(1)
    
    # 1️⃣ GÉNÉRATION DONNÉES TEST
    print("\n📊 Génération dataset test...")
    generator = CausalCoherentGenerator()
    
    # Générer 100 lignes avec mix de scénarios
    test_data = []
    scenarios = list(ScenarioType)
    localities = ["SIKASSO", "BAMAKO", "SEGOU", "BOUGOUNI", "MOPTI"]
    crops = ["mil", "sorgho", "maïs", "coton", "riz"]
    
    for i in range(100):
        scenario = scenarios[i % len(scenarios)]
        locality = localities[i % len(localities)]
        crop = crops[i % len(crops)]
        
        row = generator.generate_coherent_row(
            year=2023,
            locality=locality,
            initial_crop=crop,
            scenario_type=scenario
        )
        test_data.append(row)
    
    df_test = pd.DataFrame(test_data)
    print(f"✅ Dataset généré : {len(df_test)} lignes")
    
    # 2️⃣ VALIDATION COMPLÈTE
    print("\n🔬 Lancement validation complète...")
    validator = QualityReportGenerator()
    
    # Rapport détaillé
    report = validator.validate_dataset(df_test, verbose=True)
    
    # 3️⃣ GÉNÉRATION RAPPORTS
    print("\n📈 Génération des rapports...")
    
    # Rapport visuel
    validator.generate_visual_report(df_test, "validation_tchia_v3.png")
    
    # Export JSON
    validator.export_detailed_report(report, format="json", filename="validation_tchia_v3")
    
    # Export HTML
    validator.export_detailed_report(report, format="html", filename="validation_tchia_v3")
    
    # 4️⃣ EXEMPLES D'INCOHÉRENCES DÉTECTÉES
    print("\n⚠️ EXEMPLES D'INCOHÉRENCES DÉTECTÉES :")
    print("-" * 60)
    
    for test_name, results in report["coherence_tests"].items():
        if results["n_failures"] > 0:
            print(f"\n{test_name}:")
            for failure in results["failures"][:2]:  # Top 2
                print(f"  - Ligne {failure['row']}: {failure['message']} [{failure['severity']}]")
    
    print("\n✅ VALIDATION TERMINÉE !")
    print(f"📊 Qualité globale : {report['summary']['overall_quality']}")
    print(f"💡 {report['summary']['recommendation']}")


# =============================================================================
# 📚 DOCUMENTATION VALIDATEUR
# =============================================================================

"""
🌟 VALIDATEUR COHÉRENCE CAUSALE V3

🎯 OBJECTIFS :
1. Garantir que chaque ligne raconte une histoire cohérente
2. Détecter les incohérences causales
3. Valider les distributions vs références réelles
4. Générer rapports qualité exploitables

🔍 TESTS IMPLÉMENTÉS :
1. Cohérence stress-rendement
2. Cohérence pluie-ruissellement (30-70% règle)
3. Cohérence temporelle (effet mémoire)
4. Logique décisions paysannes
5. Cohérence NDVI-biomasse-rendement
6. Cohérence globale scénario

📊 ANALYSES STATISTIQUES :
- Distributions rendements vs références IER/FAOSTAT
- Corrélations clés (pluie-rendement, NDVI-rendement)
- Fréquences stress vs observations terrain
- Coefficients variation par zone

📈 FORMATS DE RAPPORT :
- Console : Résumé temps réel
- JSON : Données structurées complètes
- HTML : Rapport formaté web
- PNG : Graphiques validation

✅ UTILISATION :
```python
# Validation simple
validator = QualityReportGenerator()
report = validator.validate_dataset(df)

# Rapport visuel
validator.generate_visual_report(df, "rapport.png")

# Export détaillé
validator.export_detailed_report(report, format="html")
```

🏆 CRITÈRES QUALITÉ :
- EXCELLENT : >95% cohérence, distributions validées
- GOOD : >85% cohérence, écarts mineurs
- ACCEPTABLE : >75% cohérence, corrections conseillées
- POOR : <75% cohérence, dataset à revoir
"""
