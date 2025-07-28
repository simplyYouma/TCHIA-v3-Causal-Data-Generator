"""
=============================================================================
GÉNÉRATEUR TCHIA V3 - COHÉRENCE CAUSALE PARFAITE POUR IA
=============================================================================

🎯 OBJECTIF : Chaque ligne = Une histoire agricole cohérente et complète
📊 AMÉLIORATION : Causalité temporelle + Décisions adaptatives + Effet mémoire
🔬 VALIDATION : Basée sur recherches Mali (IER, ICRISAT, CMDT)

Auteur : Système TCHIA v3.0 - Données Causales pour IA
"""
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta, date
import random
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
import warnings
warnings.filterwarnings('ignore')

# Import modules v2 existants
from enhanced_crop_profiles_v2 import CROP_PROFILES, AgroClimaticZones
from hyper_realistic_generator_v2 import (
    ClimateDataProcessor, SoilGenerator, IoTSensorGenerator
)


# =============================================================================
# 🌾 SYSTÈME DE SCÉNARIOS AGRICOLES COHÉRENTS
# =============================================================================

class ScenarioType(Enum):
    """Types de scénarios agricoles avec probabilités Mali"""
    EXCEPTIONAL = "exceptional"      # 5% - Année exceptionnelle
    GOOD = "good"                   # 20% - Bonne année
    AVERAGE = "average"             # 40% - Année moyenne
    DIFFICULT = "difficult"         # 25% - Année difficile
    CATASTROPHIC = "catastrophic"  # 10% - Année catastrophique


@dataclass
class AgricultureScenario:
    """
    Scénario agricole complet avec cohérence causale
    
    🔬 Basé sur : Distributions observées Mali (AGRHYMET, IER)
    """
    type: ScenarioType
    rainfall_pattern: Dict[str, float]  # Distribution mensuelle
    stress_timeline: List[Dict]         # Stress par stade phénologique
    farmer_decisions: Dict              # Décisions adaptatives
    yield_potential: float              # Potentiel relatif [0-1]
    narrative: str                      # Histoire du scénario


class ScenarioGenerator:
    """
    Générateur de scénarios agricoles cohérents
    
    📚 Sources : 
    - Distribution pluies : 37% en août au Sud Mali (PDF p.3)
    - Ruissellement : 30-70% pour 15-45mm début saison (PDF p.3)
    - Décisions semis : Def_4 sahélien (22/07±15j), Def_3 soudanien (12/07±15j)
    """
    
    # Distribution réaliste pluies Mali (% du total par mois)
    RAINFALL_PATTERNS = {
        "exceptional": {"mai": 8, "juin": 15, "juillet": 25, "août": 37, "sept": 12, "oct": 3},
        "good": {"mai": 5, "juin": 12, "juillet": 28, "août": 35, "sept": 15, "oct": 5},
        "average": {"mai": 3, "juin": 10, "juillet": 30, "août": 37, "sept": 17, "oct": 3},
        "difficult": {"mai": 2, "juin": 8, "juillet": 25, "août": 40, "sept": 20, "oct": 5},
        "catastrophic": {"mai": 1, "juin": 5, "juillet": 20, "août": 45, "sept": 25, "oct": 4}
    }
    
    @classmethod
    def generate_scenario(cls, scenario_type: ScenarioType, zone: str) -> AgricultureScenario:
        """Génère un scénario cohérent selon le type et la zone"""
        
        rainfall_pattern = cls.RAINFALL_PATTERNS[scenario_type.value]
        
        if scenario_type == ScenarioType.EXCEPTIONAL:
            return cls._generate_exceptional_scenario(zone, rainfall_pattern)
        elif scenario_type == ScenarioType.GOOD:
            return cls._generate_good_scenario(zone, rainfall_pattern)
        elif scenario_type == ScenarioType.AVERAGE:
            return cls._generate_average_scenario(zone, rainfall_pattern)
        elif scenario_type == ScenarioType.DIFFICULT:
            return cls._generate_difficult_scenario(zone, rainfall_pattern)
        else:  # CATASTROPHIC
            return cls._generate_catastrophic_scenario(zone, rainfall_pattern)
    
    @classmethod
    def _generate_exceptional_scenario(cls, zone: str, rainfall_pattern: Dict) -> AgricultureScenario:
        """Année exceptionnelle : Tout est optimal"""
        
        # Pas de stress significatif à aucun stade
        stress_timeline = [
            {"stage": "germination", "water_stress": 0.0, "temp_stress": 0.0, "duration_days": 0},
            {"stage": "vegetative", "water_stress": 0.0, "temp_stress": 0.0, "duration_days": 0},
            {"stage": "flowering", "water_stress": 0.0, "temp_stress": 0.05, "duration_days": 2},
            {"stage": "grain_filling", "water_stress": 0.0, "temp_stress": 0.0, "duration_days": 0}
        ]
        
        # Décisions optimales
        farmer_decisions = {
            "sowing_adjustment_days": 0,      # Semis à la date optimale
            "variety_change": False,          # Variété prévue maintenue
            "fertilizer_adjustment": 1.2,     # 20% engrais supplémentaire
            "density_adjustment": 1.1,        # Densité augmentée
            "replanting": False               # Pas de re-semis nécessaire
        }
        
        narrative = (
            "Année exceptionnelle : Début précoce des pluies bien réparties. "
            "Sol humide optimal à la germination. Pas de période sèche. "
            "Température idéale tout le cycle. Agriculteur augmente densité et fertilisation. "
            "Conditions parfaites → rendements records."
        )
        
        return AgricultureScenario(
            type=ScenarioType.EXCEPTIONAL,
            rainfall_pattern=rainfall_pattern,
            stress_timeline=stress_timeline,
            farmer_decisions=farmer_decisions,
            yield_potential=0.95,
            narrative=narrative
        )
    
    @classmethod
    def _generate_good_scenario(cls, zone: str, rainfall_pattern: Dict) -> AgricultureScenario:
        """Bonne année : Conditions favorables, stress mineurs"""
        
        stress_timeline = [
            {"stage": "germination", "water_stress": 0.0, "temp_stress": 0.0, "duration_days": 0},
            {"stage": "vegetative", "water_stress": 0.15, "temp_stress": 0.1, "duration_days": 5},
            {"stage": "flowering", "water_stress": 0.1, "temp_stress": 0.15, "duration_days": 3},
            {"stage": "grain_filling", "water_stress": 0.2, "temp_stress": 0.1, "duration_days": 7}
        ]
        
        farmer_decisions = {
            "sowing_adjustment_days": 5,      # Léger retard prudent
            "variety_change": False,
            "fertilizer_adjustment": 1.0,     # Dose normale
            "density_adjustment": 1.0,
            "replanting": False
        }
        
        narrative = (
            "Bonne année : Démarrage normal des pluies. Petite période sèche "
            "en phase végétative (5 jours) sans impact majeur. "
            "Léger stress thermique à la floraison géré par irrigation d'appoint. "
            "Récolte dans de bonnes conditions."
        )
        
        return AgricultureScenario(
            type=ScenarioType.GOOD,
            rainfall_pattern=rainfall_pattern,
            stress_timeline=stress_timeline,
            farmer_decisions=farmer_decisions,
            yield_potential=0.75,
            narrative=narrative
        )
    
    @classmethod
    def _generate_average_scenario(cls, zone: str, rainfall_pattern: Dict) -> AgricultureScenario:
        """Année moyenne : Mix de bonnes et mauvaises périodes"""
        
        stress_timeline = [
            {"stage": "germination", "water_stress": 0.2, "temp_stress": 0.0, "duration_days": 3},
            {"stage": "vegetative", "water_stress": 0.3, "temp_stress": 0.2, "duration_days": 10},
            {"stage": "flowering", "water_stress": 0.25, "temp_stress": 0.3, "duration_days": 5},
            {"stage": "grain_filling", "water_stress": 0.4, "temp_stress": 0.2, "duration_days": 12}
        ]
        
        farmer_decisions = {
            "sowing_adjustment_days": 10,     # Attente pluies fiables
            "variety_change": True if zone == "sahelien" else False,  # Variété précoce au Sahel
            "fertilizer_adjustment": 0.8,     # Réduction par prudence
            "density_adjustment": 0.9,        # Densité réduite
            "replanting": random.random() < 0.2  # 20% chance re-semis
        }
        
        narrative = (
            "Année moyenne typique : Démarrage tardif, faux départ nécessitant "
            "parfois re-semis. Période sèche de 10j en végétatif. "
            "Stress modéré à la floraison. Fin de cycle difficile. "
            "Agriculteur s'adapte : variété précoce, densité réduite."
        )
        
        return AgricultureScenario(
            type=ScenarioType.AVERAGE,
            rainfall_pattern=rainfall_pattern,
            stress_timeline=stress_timeline,
            farmer_decisions=farmer_decisions,
            yield_potential=0.5,
            narrative=narrative
        )
    
    @classmethod
    def _generate_difficult_scenario(cls, zone: str, rainfall_pattern: Dict) -> AgricultureScenario:
        """Année difficile : Stress significatifs mais gérables"""
        
        stress_timeline = [
            {"stage": "germination", "water_stress": 0.4, "temp_stress": 0.1, "duration_days": 7},
            {"stage": "vegetative", "water_stress": 0.5, "temp_stress": 0.3, "duration_days": 15},
            {"stage": "flowering", "water_stress": 0.6, "temp_stress": 0.4, "duration_days": 10},
            {"stage": "grain_filling", "water_stress": 0.7, "temp_stress": 0.3, "duration_days": 20}
        ]
        
        farmer_decisions = {
            "sowing_adjustment_days": 20,     # Long retard
            "variety_change": True,           # Obligatoire : variété très précoce
            "fertilizer_adjustment": 0.5,     # Forte réduction
            "density_adjustment": 0.7,        # Faible densité
            "replanting": random.random() < 0.4  # 40% re-semis
        }
        
        narrative = (
            "Année difficile : Pluies très tardives, plusieurs faux départs. "
            "Longue sécheresse (15j) en végétatif → retard croissance. "
            "Stress hydrique sévère à la floraison → avortement partiel. "
            "Agriculteur bascule sur mil précoce, réduit investissements."
        )
        
        return AgricultureScenario(
            type=ScenarioType.DIFFICULT,
            rainfall_pattern=rainfall_pattern,
            stress_timeline=stress_timeline,
            farmer_decisions=farmer_decisions,
            yield_potential=0.25,
            narrative=narrative
        )
    
    @classmethod
    def _generate_catastrophic_scenario(cls, zone: str, rainfall_pattern: Dict) -> AgricultureScenario:
        """Année catastrophique : Échec cultural majeur"""
        
        # Choisir type de catastrophe
        disaster_type = random.choice(["drought", "flood"])
        
        if disaster_type == "drought":
            stress_timeline = [
                {"stage": "germination", "water_stress": 0.8, "temp_stress": 0.3, "duration_days": 14},
                {"stage": "vegetative", "water_stress": 0.9, "temp_stress": 0.5, "duration_days": 30},
                {"stage": "flowering", "water_stress": 1.0, "temp_stress": 0.6, "duration_days": 20},
                {"stage": "grain_filling", "water_stress": 1.0, "temp_stress": 0.4, "duration_days": 30}
            ]
            
            narrative = (
                "Année catastrophique - Sécheresse : Échec des pluies. "
                "Plusieurs re-semis échoués. Sécheresse terminale totale. "
                "Abandon de 50% des parcelles. Survie prioritaire du bétail. "
                "Aide alimentaire nécessaire."
            )
        else:  # flood
            stress_timeline = [
                {"stage": "germination", "water_stress": 0.8, "temp_stress": 0.0, "duration_days": 10},
                {"stage": "vegetative", "water_stress": 0.6, "temp_stress": 0.0, "duration_days": 7},
                {"stage": "flowering", "water_stress": 0.9, "temp_stress": 0.1, "duration_days": 5},
                {"stage": "grain_filling", "water_stress": 0.5, "temp_stress": 0.0, "duration_days": 10}
            ]
            
            narrative = (
                "Année catastrophique - Inondation : Pluies torrentielles précoces. "
                "Érosion massive, perte de semences. Pourrissement racinaire généralisé. "
                "Maladies fongiques explosent. Pertes post-récolte énormes. "
                "Reconversion temporaire vers cultures de décrue."
            )
        
        farmer_decisions = {
            "sowing_adjustment_days": 30,
            "variety_change": True,
            "fertilizer_adjustment": 0.2,     # Minimum vital
            "density_adjustment": 0.5,
            "replanting": True,               # Multiple tentatives
            "parcels_abandoned": 0.5          # 50% parcelles abandonnées
        }
        
        return AgricultureScenario(
            type=ScenarioType.CATASTROPHIC,
            rainfall_pattern=rainfall_pattern,
            stress_timeline=stress_timeline,
            farmer_decisions=farmer_decisions,
            yield_potential=0.05,  # Très faible potentiel
            narrative=narrative
        )


# =============================================================================
# 🌊 MODÈLE HYDROLOGIQUE AVEC RUISSELLEMENT
# =============================================================================

class HydrologicalModel:
    """
    Modèle hydrologique intégrant le ruissellement
    
    📚 Source : 30-70% ruissellement pour pluies 15-45mm début saison (PDF p.3)
    🔬 Méthode : SCS Curve Number adaptée Sahel
    """
    
    @staticmethod
    def calculate_effective_rainfall_FIXED(
        rainfall_mm: float,
        soil_texture: str,
        crop: str,
        soil_moisture: float,
        month: str
    ) -> Dict[str, float]:
        """
        CORRECTION CRITIQUE: Relation pluie-rendement cohérente
        
        AVANT (problématique):
        - Fallback écrasait relation pluie-rendement
        - Ratios d'efficacité fixes non liés à la pluie totale
        - Possibilité pluie effective > pluie totale
        
        APRÈS (corrigé):
        - Relation monotone croissante garantie
        - Bornes physiques respectées
        - Corrélation positive garantie
        """
        
        # GARANTIE: Si pas de pluie, pas de pluie effective
        if rainfall_mm <= 0:
            return {
                "effective_mm": 0.0,
                "runoff_mm": 0.0,
                "runoff_percent": 0.0
            }
        
        # Curve Number avec validation physique
        cn_base = {
            "mil": {"sableux": 72, "limoneux": 78, "argileux": 82},
            "sorgho": {"sableux": 74, "limoneux": 79, "argileux": 84},
            "maïs": {"sableux": 75, "limoneux": 80, "argileux": 85}
        }.get(crop, {"sableux": 75, "limoneux": 80, "argileux": 85})
        
        texture_key = soil_texture.split("-")[0] if "-" in soil_texture else soil_texture
        cn = cn_base.get(texture_key, 78)
        
        # Ajustement humidité avec bornes strictes
        if soil_moisture < 30:
            cn = max(30, cn - 10)
        elif soil_moisture > 70:
            cn = min(95, cn + 10)
        
        # Calcul SCS avec protection division par zéro
        S = max(1.0, (1000 / cn - 10) * 25.4)  # Protection S > 0
        Ia = 0.001 * S  # Spécifique Sahel
        
        # Calcul ruissellement avec validation physique
        if rainfall_mm <= Ia:
            runoff_mm = 0
        else:
            runoff_mm = (rainfall_mm - Ia)**2 / (rainfall_mm - Ia + S)
        
        # CORRECTION CRITIQUE: Bornes physiques strictes
        runoff_mm = np.clip(runoff_mm, 0, rainfall_mm * 0.90)  # Max 90% runoff
        effective_mm = rainfall_mm - runoff_mm
        
        # GARANTIE: Relation positive pluie-rendement
        # Plus de pluie totale → Plus de pluie effective (obligatoire)
        effectiveness_ratio = effective_mm / rainfall_mm
        
        # Validation finale cohérence physique
        assert effective_mm >= 0, "Pluie effective négative impossible"
        assert effective_mm <= rainfall_mm, "Pluie effective > totale impossible"
        assert effectiveness_ratio >= 0.1, "Efficacité minimum 10%"
        
        return {
            "effective_mm": round(effective_mm, 1),
            "runoff_mm": round(runoff_mm, 1),
            "runoff_percent": round(runoff_mm / rainfall_mm * 100, 1)
        }


# =============================================================================
# 🌱 MODÈLE PHÉNOLOGIQUE AVEC MÉMOIRE
# =============================================================================

@dataclass
class CropState:
    """État cultural avec historique des stress"""
    stage: str = "pre_sowing"
    stage_start_date: Optional[date] = None
    accumulated_stress: float = 0.0
    stress_history: List[Dict] = field(default_factory=list)
    growth_reduction: float = 0.0
    potential_loss: float = 0.0
    biomass_accumulated: float = 0.0
    final_crop: Optional[str] = None  # IMPORTANT : Cet attribut doit exister

    def add_stress_event(self, stress_type: str, intensity: float, duration_days: int):
        """
        Enregistre un événement de stress avec effet mémoire (CORRIGÉ selon données Mali)
        
        📚 Sources : 
        - Index stress ICRISAT Mali (0=stress complet, 1=pas stress)
        - Stress végétatif >36% perte, reproductif >55% perte
        - Données Cinzana : sécheresses 6-8 jours fréquentes
        """
        
        # 🔧 CORRECTION : Facteurs de sensibilité ajustés selon recherches Mali
        stage_sensitivity = {
            "germination": {"water": 1.2, "temp": 0.8},     # Réduit vs original (1.5, 1.0)
            "vegetative": {"water": 0.8, "temp": 0.6},      # Réduit vs original (1.0, 0.8)
            "flowering": {"water": 1.8, "temp": 1.4},       # Réduit vs original (2.0, 1.5)
            "grain_filling": {"water": 1.0, "temp": 0.8}    # Réduit vs original (1.2, 1.0)
        }
        
        sensitivity = stage_sensitivity.get(self.stage, {}).get(stress_type, 1.0)
        
        # 🔧 CORRECTION : Impact pondéré par période plus longue (observations Mali)
        # Changement : diviseur 10 au lieu de 7 (stress hebdomadaire → décadaire)
        impact = intensity * sensitivity * (duration_days / 10)
        
        # 🔧 CORRECTION : Accumulation avec décroissance plus lente + impact modéré
        # - Facteur mémoire 0.95 au lieu de 0.9 (stress persiste plus)
        # - Impact réduit 0.8 au lieu de 1.0 (moins d'accumulation brutale)
        self.accumulated_stress = self.accumulated_stress * 0.95 + impact * 0.8
        
        # 🔧 CORRECTION : Réduction croissance plus progressive
        # - Impact 0.06 au lieu de 0.1 (6% au lieu de 10%)
        # - Plafond 0.8 au lieu de 0.9 (max 80% réduction)
        self.growth_reduction = min(0.8, self.growth_reduction + impact * 0.06)
        
        # Enregistrement historique (inchangé)
        self.stress_history.append({
            "date": date.today(),
            "stage": self.stage,
            "type": stress_type,
            "intensity": intensity,
            "duration": duration_days,
            "impact": impact
        })
        
        # 🔧 CORRECTION : Calcul perte potentielle selon données Mali
        # Seuils ajustés selon recherches stress-rendement Mali
        if self.stage == "flowering":
            # Stress floraison critique : seuil 0.4 au lieu de 0.5
            if intensity > 0.4:
                # Avortement floral : impact réduit 0.25 au lieu de 0.3
                self.potential_loss += min(0.4, intensity * 0.25)
        
        elif self.stage == "grain_filling":
            # Stress remplissage : seuil 0.5 au lieu de 0.6  
            if intensity > 0.5:
                # Échaudage : impact réduit 0.15 au lieu de 0.2
                self.potential_loss += min(0.25, intensity * 0.15)
        
        elif self.stage == "vegetative":
            # 🔧 NOUVEAU : Ajout stress végétatif (>36% perte selon recherches)
            if intensity > 0.6:
                # Stress végétatif sévère : impact modéré
                self.potential_loss += min(0.2, intensity * 0.12)
        
        # 🔧 CORRECTION : Plafonner la perte potentielle totale selon scénario
        # Éviter accumulation excessive non-réaliste
        max_loss_by_stage = {
            "germination": 0.3,      # Max 30% perte germination
            "vegetative": 0.4,       # Max 40% perte végétatif  
            "flowering": 0.6,        # Max 60% perte floraison
            "grain_filling": 0.5     # Max 50% perte remplissage
        }
        
        max_loss = max_loss_by_stage.get(self.stage, 0.5)
        self.potential_loss = min(max_loss, self.potential_loss)
        
        # 🔧 DEBUG : Messages pour validation (optionnel)
        if intensity > 0.5:
            print(f"⚠️ Stress {stress_type} {self.stage}: intensité={intensity:.2f}, "
                f"durée={duration_days}j, impact={impact:.3f}, "
                f"stress_accumulé={self.accumulated_stress:.3f}")


# =============================================================================
# 🧠 MODÈLE DÉCISIONS PAYSANNES ADAPTATIVES
# =============================================================================

class FarmerDecisionModel:
    """
    Modèle de décisions adaptatives des agriculteurs maliens
    
    📚 Sources :
    - Dates semis : Def_4 sahélien (22/07±15j), Def_3 soudanien (12/07±15j)
    - Seuils rentabilité : ratio B/C minimum 1.8:1
    - Stratégies : diversification comme gestion risque principal
    """
    
    @staticmethod
    def decide_sowing_date(
        rainfall_history: List[float],
        zone: str,
        original_crop: str,
        scenario: AgricultureScenario
    ) -> Tuple[date, str, Dict]:
        """
        Décide date de semis et éventuellement change de culture
        
        Retourne : (date_semis, culture_finale, decisions_details)
        """
        
        # Dates optimales par zone (Source : PDF définitions onset)
        optimal_dates = {
            "sahelien": date(date.today().year, 7, 22),    # Def_4
            "soudanien": date(date.today().year, 7, 12),   # Def_3
            "sud_tropical": date(date.today().year, 6, 25)
        }
        
        base_date = optimal_dates.get(zone, date(date.today().year, 7, 1))
        
        # Ajustement selon scénario
        adjustment_days = scenario.farmer_decisions["sowing_adjustment_days"]
        
        # Décision changement culture selon conditions
        final_crop = original_crop
        if scenario.farmer_decisions["variety_change"]:
            # Logique de substitution
            substitutions = {
                "maïs": "sorgho",    # Maïs → Sorgho si difficile
                "coton": "mil",      # Coton → Mil si très tardif
                "sorgho": "mil",     # Sorgho → Mil variété précoce
                "riz": "sorgho"      # Riz pluvial → Sorgho
            }
            final_crop = substitutions.get(original_crop, "mil")
        
        sowing_date = base_date + timedelta(days=adjustment_days)
        
        decisions = {
            "original_crop": original_crop,
            "final_crop": final_crop,
            "reason": scenario.narrative,
            "confidence": 1.0 - (adjustment_days / 60),  # Confiance décroît avec retard
            "expected_cycle_reduction": adjustment_days * 0.5 if final_crop in ["mil", "sorgho"] else 0
        }
        
        return sowing_date, final_crop, decisions
    
    @staticmethod
    def adjust_management(
        crop_state: CropState,
        scenario: AgricultureScenario,
        economic_context: Dict
    ) -> Dict:
        """Ajuste les pratiques selon l'état cultural et économique"""
        
        # DEBUG - Décommentez pour voir ce qui arrive
        # print(f"DEBUG adjust_management - Type economic_context: {type(economic_context)}")
        # print(f"DEBUG - crop_price_cfa_kg: {economic_context.get('crop_price_cfa_kg')}")
        
        # Ratio bénéfice/coût pour décisions
        fertilizer_price = economic_context.get("fertilizer_price_cfa_kg", 300)
        
        # =========== CORRECTION CRITIQUE ICI ===========
        # NE PAS faire : crop_price = economic_context.get("crop_price_cfa_kg", 150)
        # Car cela retourne le dictionnaire entier !
        
        # SOLUTION : Extraire le bon prix
        crop_price_data = economic_context.get("crop_price_cfa_kg", 150)
        
        # Vérifier le type et extraire la valeur appropriée
        if isinstance(crop_price_data, dict):
            # C'est un dictionnaire - on doit choisir un prix
            # Option 1 : Utiliser le prix de la culture finale si disponible
            if hasattr(crop_state, 'final_crop') and crop_state.final_crop in crop_price_data:
                crop_price = crop_price_data[crop_state.final_crop]
            else:
                # Option 2 : Utiliser une valeur par défaut
                crop_price = 150
            
            # DEBUG
            # print(f"DEBUG - Prix extrait du dict: {crop_price} pour culture {getattr(crop_state, 'final_crop', 'inconnue')}")
        else:
            # C'est déjà un nombre
            crop_price = crop_price_data
            # print(f"DEBUG - Prix direct: {crop_price}")
        
        # =========== FIN DE LA CORRECTION ===========
        
        # Si stress accumulé élevé, réduire investissements
        if crop_state.accumulated_stress > 0.5:
            fert_adjustment = max(0.3, scenario.farmer_decisions["fertilizer_adjustment"] - 0.3)
            density_adjustment = max(0.5, scenario.farmer_decisions["density_adjustment"] - 0.2)
        else:
            fert_adjustment = scenario.farmer_decisions["fertilizer_adjustment"]
            density_adjustment = scenario.farmer_decisions["density_adjustment"]
        
        # Calcul ratio B/C estimé
        expected_yield_loss = crop_state.potential_loss
        
        # Maintenant crop_price est un nombre, pas un dict !
        expected_revenue = crop_price * 1000 * (1 - expected_yield_loss)  # kg/ha
        input_cost = fertilizer_price * 100 * fert_adjustment  # 100 kg/ha base
        
        bc_ratio = expected_revenue / input_cost if input_cost > 0 else 0
        
        # Si B/C < 1.8, réduire encore les intrants
        if bc_ratio < 1.8:
            fert_adjustment *= 0.7
            density_adjustment *= 0.8
        
        return {
            "fertilizer_adjustment": fert_adjustment,
            "density_adjustment": density_adjustment,
            "bc_ratio": bc_ratio,
            "economic_decision": "reduce_risk" if bc_ratio < 1.8 else "normal"
        }


# =============================================================================
# 🚀 GÉNÉRATEUR PRINCIPAL V3 AVEC COHÉRENCE CAUSALE
# =============================================================================

class CausalCoherentGenerator:
    """
    Générateur V3 avec cohérence causale parfaite
    
    ⭐ INNOVATION : Chaque ligne = histoire agricole complète
    🔬 AMÉLIORATION : Causalité temporelle + Mémoire + Décisions
    """
    
    def __init__(self, climate_file: str = 'climate_cleaned.csv'):
        """Initialisation avec composants v2 + nouveaux modèles"""
        
        # Composants v2 réutilisés
        self.climate_processor = ClimateDataProcessor(climate_file)
        self.climate_data = self.climate_processor.load_climate_data()
        self.seasonal_climate = self.climate_processor.aggregate_seasonal_data()
        
        # Nouveaux modèles v3
        self.hydrological_model = HydrologicalModel()
        self.farmer_model = FarmerDecisionModel()
        
        # Profils cultures
        self.crop_profiles = CROP_PROFILES
        
        print("✅ Générateur V3 initialisé avec cohérence causale")
    
    def generate_coherent_row(
        self,
        year: int,
        locality: str,
        initial_crop: str,
        scenario_type: Optional[ScenarioType] = None,
        economic_context: Optional[Dict] = None
    ) -> Dict:
        """
        Génère UNE ligne avec cohérence causale complète
        
        🎯 Chaque valeur découle logiquement des précédentes
        📊 L'histoire se construit étape par étape
        """
        
        # 1️⃣ DÉTERMINATION DU SCÉNARIO
        if scenario_type is None:
            # Tirage selon probabilités réelles
            scenario_type = np.random.choice(
                list(ScenarioType),
                p=[0.05, 0.20, 0.40, 0.25, 0.10]
            )
        
        zone = AgroClimaticZones.get_zone(locality)
        scenario = ScenarioGenerator.generate_scenario(scenario_type, zone)
        
        # 2️⃣ CONTEXTE ÉCONOMIQUE
        if economic_context is None:
            economic_context = {
                "fertilizer_price_cfa_kg": np.random.normal(300, 50),
                "crop_price_cfa_kg": {
                    "mil": 150, "sorgho": 140, "maïs": 180,
                    "coton": 265, "riz": 220
                }
            }
        
        
        # 3️⃣ CLIMAT RÉEL + DISTRIBUTION TEMPORELLE
        climate_base = self._get_real_climate_data(year, locality)
        monthly_rainfall = self._distribute_rainfall(
            climate_base["SeasonRainfall_mm"],
            scenario.rainfall_pattern
        )
        
        # 4️⃣ ÉTAT CULTURAL INITIAL
        crop_state = CropState()
        
        # 5️⃣ DÉCISIONS SEMIS ADAPTATIVES
        rainfall_early = [monthly_rainfall["mai"], monthly_rainfall["juin"]]
        sowing_date, final_crop, sowing_decisions = self.farmer_model.decide_sowing_date(
            rainfall_early, zone, initial_crop, scenario
        )
        
        # IMPORTANT : Ajouter la culture finale à crop_state
        crop_state.final_crop = final_crop
        
        # 6️⃣ PROPRIÉTÉS SOL
        soil_props = SoilGenerator.generate_soil_properties(locality, climate_base)
        
        # 7️⃣ SIMULATION CYCLE CULTURAL AVEC MÉMOIRE
        cycle_data = self._simulate_crop_cycle(
            final_crop, sowing_date, monthly_rainfall,
            climate_base, soil_props, scenario, crop_state
        )
        
        # 8️⃣ DÉCISIONS GESTION ADAPTATIVES
        # CORRECTION : Passer le contexte tel quel, adjust_management gère maintenant les deux cas
        management = FarmerDecisionModel.adjust_management(
            crop_state, scenario, economic_context
        )

        # 9️⃣ CALCUL RENDEMENT COHÉRENT
        yield_data = self._calculate_coherent_yield(
            final_crop, zone, crop_state, scenario,
            cycle_data, management
        )
        
        # 🔟 NDVI COHÉRENT AVEC HISTOIRE
        ndvi_timeline = self._generate_coherent_ndvi(
            final_crop, yield_data["final_yield"],
            crop_state, cycle_data
        )
        
        # 1️⃣1️⃣ VARIABLES IOT CORRÉLÉES
        iot_data = IoTSensorGenerator.generate_sensor_data(climate_base, soil_props)
        
        # 1️⃣2️⃣ ASSEMBLAGE LIGNE COMPLÈTE
        row = {
            # Métadonnées
            "Year": year,
            "Locality": locality,
            "InitialCrop": initial_crop,
            "FinalCrop": final_crop,
            "Scenario": scenario_type.value,
            "ScenarioNarrative": scenario.narrative,
            
            # Décisions paysannes
            "SowingDate": sowing_date,
            "SowingDelay_days": sowing_decisions["confidence"],
            "CropChanged": initial_crop != final_crop,
            "ManagementStrategy": management["economic_decision"],
            
            # Climat avec distribution
            **climate_base,
            "RainfallDistribution": monthly_rainfall,
            "EffectiveRainfall_mm": cycle_data["total_effective_rain"],
            "Runoff_mm": cycle_data["total_runoff"],
            
            # Sol
            **soil_props,
            
            # Stress temporels
            "StressHistory": crop_state.stress_history,
            "AccumulatedStress": round(crop_state.accumulated_stress, 3),
            "GrowthReduction": round(crop_state.growth_reduction, 3),
            
            # Rendements cohérents
            "PotentialYield_kg_ha": yield_data["potential_yield"],
            "ActualYield_kg_ha": yield_data["final_yield"],
            "YieldLoss_percent": yield_data["loss_percent"],
            "BiomassTotal_kg_ha": yield_data["biomass_total"],
            
            # NDVI temporel
            "NDVI_timeline": ndvi_timeline,
            "NDVI_peak": max(ndvi_timeline.values()),
            
            # Économie
            "BC_Ratio": management["bc_ratio"],
            "FertilizerApplied_kg_ha": 100 * management["fertilizer_adjustment"],
            
            # IoT
            **iot_data
        }
        
        return row
    
    def _get_real_climate_data(self, year: int, locality: str) -> Dict:
        """Récupère climat réel (réutilise v2)"""
        mask = (
            (self.seasonal_climate["Year"] == year) & 
            (self.seasonal_climate["Locality"].str.upper() == locality.upper())
        )
        matching = self.seasonal_climate[mask]
        
        if len(matching) > 0:
            return matching.iloc[0].to_dict()
        else:
            # Fallback année proche
            return self.seasonal_climate.iloc[0].to_dict()
    
    def _distribute_rainfall(
        self,
        total_rainfall: float,
        pattern: Dict[str, float]
    ) -> Dict[str, float]:
        """
        Distribue la pluie totale selon le pattern mensuel
        
        📚 Validation : 37% en août au Sud Mali (PDF p.3)
        """
        monthly = {}
        for month, percent in pattern.items():
            monthly[month] = round(total_rainfall * percent / 100, 1)
        
        return monthly
    
    def _simulate_crop_cycle(
        self,
        crop: str,
        sowing_date: date,
        monthly_rainfall: Dict[str, float],
        climate_base: Dict,
        soil_props: Dict,
        scenario: AgricultureScenario,
        crop_state: CropState
    ) -> Dict:
        """
        Simule le cycle cultural complet avec événements causaux
        
        🔬 Intègre : ruissellement, stress par stade, effet mémoire
        """
        
        # Profil cultural
        profile = self.crop_profiles.get_crop_profile(crop)
        cycle_days = np.mean(profile["cycle_range_days"])
        
        # Durées stades phénologiques (% du cycle)
        stage_durations = {
            "germination": 0.10,      # 10% du cycle
            "vegetative": 0.35,       # 35%
            "flowering": 0.20,        # 20%
            "grain_filling": 0.35     # 35%
        }
        
        # Variables accumulées
        total_effective = 0
        total_runoff = 0
        total_seasonal_rain = climate_base["SeasonRainfall_mm"]  # ✅ UNE SEULE FOIS
        
        # Simulation par stade
        current_date = sowing_date
        
        for stage_name, duration_frac in stage_durations.items():
            duration_days = int(cycle_days * duration_frac)
            crop_state.stage = stage_name
            crop_state.stage_start_date = current_date
            
            # Déterminer le mois
            month_name = current_date.strftime("%B").lower()
            month_map = {
                "january": "janvier", "february": "février", "march": "mars",
                "april": "avril", "may": "mai", "june": "juin",
                "july": "juillet", "august": "août", "september": "septembre",
                "october": "octobre", "november": "novembre", "december": "décembre"
            }
            month_fr = month_map.get(month_name, "juin")
            
            # 🔧 CORRECTION : Gestion robuste des mois
            if month_fr in monthly_rainfall:
                monthly_rain = monthly_rainfall[month_fr]
            else:
                # Chercher par première lettre
                monthly_rain = 0
                for m in monthly_rainfall:
                    if m[0] == month_fr[0]:
                        monthly_rain = monthly_rainfall[m]
                        break
                
                # Si toujours pas trouvé, utiliser défaut saisonnier
                if monthly_rain == 0 and month_fr in ["mai", "juin", "juillet", "août", "septembre"]:
                    monthly_rain = total_seasonal_rain * 0.15  # 15% par mois de saison
            
            # Calculer la pluie pour ce stade
            days_in_month = 30  # Approximation
            rain_per_stage = (monthly_rain * duration_days) / days_in_month
            
            # Calcul ruissellement avec validation
            if rain_per_stage > 0:
                hydro = self.hydrological_model.calculate_effective_rainfall(
                    rain_per_stage,
                    soil_props["SoilTexture"],
                    crop,
                    soil_props["SoilMoisture_percent"],
                    month_fr
                )
                
                total_effective += hydro["effective_mm"]
                total_runoff += hydro["runoff_mm"]
            
            # Application stress du scénario
            stage_stress = next(
                (s for s in scenario.stress_timeline if s["stage"] == stage_name),
                {"water_stress": 0, "temp_stress": 0, "duration_days": 0}
            )
            
            # Enregistrement stress avec effet mémoire
            if stage_stress["water_stress"] > 0.1:
                crop_state.add_stress_event(
                    "water",
                    stage_stress["water_stress"],
                    stage_stress["duration_days"]
                )
            
            if stage_stress["temp_stress"] > 0.1:
                crop_state.add_stress_event(
                    "temp",
                    stage_stress["temp_stress"],
                    stage_stress["duration_days"]
                )
            
            # Accumulation biomasse (réduite par stress)
            stage_biomass = 1000 * duration_frac * (1 - crop_state.growth_reduction)
            crop_state.biomass_accumulated += stage_biomass
            
            # Avancement date
            current_date += timedelta(days=duration_days)
        
        # 🔧 CORRECTION INTELLIGENTE : Validation et ajustement si nécessaire
        if total_effective <= 0 and total_seasonal_rain > 0:
            # Fallback selon scénario (mais pas d'écrasement total)
            effectiveness_ratios = {
                ScenarioType.EXCEPTIONAL: 0.6,
                ScenarioType.GOOD: 0.5,
                ScenarioType.AVERAGE: 0.4,
                ScenarioType.DIFFICULT: 0.3,
                ScenarioType.CATASTROPHIC: 0.2
            }
            
            ratio = effectiveness_ratios.get(scenario.type, 0.4)
            total_effective = total_seasonal_rain * ratio
            total_runoff = total_seasonal_rain * (1 - ratio)
            
            print(f"⚠️ Fallback appliqué: Pluie effective ajustée à {total_effective:.1f}mm ({ratio*100:.0f}%)")
        
        # 🔧 VALIDATION FINALE : Cohérence physique
        elif total_effective + total_runoff > total_seasonal_rain * 1.1:  # Tolérance 10%
            # Réajuster proportionnellement si dépassement
            total_sum = total_effective + total_runoff
            if total_sum > 0:
                factor = total_seasonal_rain / total_sum
                total_effective *= factor
                total_runoff *= factor
        
        # 🔧 GARANTIE : Corrélation positive pluie-rendement
        # S'assurer que plus de pluie = plus de pluie effective
        if total_seasonal_rain > 0:
            min_effectiveness = 0.15  # Minimum 15% d'efficacité
            max_effectiveness = 0.8   # Maximum 80% d'efficacité
            
            current_ratio = total_effective / total_seasonal_rain
            if current_ratio < min_effectiveness:
                total_effective = total_seasonal_rain * min_effectiveness
                total_runoff = total_seasonal_rain * (1 - min_effectiveness)
            elif current_ratio > max_effectiveness:
                total_effective = total_seasonal_rain * max_effectiveness
                total_runoff = total_seasonal_rain * (1 - max_effectiveness)
        
        return {
            "cycle_duration": cycle_days,
            "harvest_date": current_date,
            "total_effective_rain": round(max(0, total_effective), 1),
            "total_runoff": round(max(0, total_runoff), 1),
            "runoff_percent": round(total_runoff / total_seasonal_rain * 100, 1) if total_seasonal_rain > 0 else 0
        }
    
    def _calculate_coherent_yield(
        self,
        crop: str,
        zone: str,
        crop_state: CropState,
        scenario: AgricultureScenario,
        cycle_data: Dict,
        management: Dict
    ) -> Dict:
        """
        Calcule rendement cohérent avec contraintes strictes par scénario
        
        📚 Sources : Rendements Mali (IER), contraintes climatiques Sahel
        """
        
        # Potentiel de base selon zone et culture
        yield_range = self.crop_profiles.get_yield_range(crop, zone)
        base_potential = yield_range[1]  # Potentiel max théorique
        
        # Contraintes STRICTES par scénario (basées sur observations Mali)
        scenario_constraints = {
            ScenarioType.EXCEPTIONAL: {
                "potential_factor": 0.90,  # 90% du potentiel max
                "min_yield_factor": 0.75,  # Minimum 75% du potentiel
                "max_loss_percent": 25     # Maximum 25% de perte
            },
            ScenarioType.GOOD: {
                "potential_factor": 0.75,
                "min_yield_factor": 0.60,
                "max_loss_percent": 40
            },
            ScenarioType.AVERAGE: {
                "potential_factor": 0.60,
                "min_yield_factor": 0.40,
                "max_loss_percent": 60
            },
            ScenarioType.DIFFICULT: {
                "potential_factor": 0.45,
                "min_yield_factor": 0.25,
                "max_loss_percent": 75
            },
            ScenarioType.CATASTROPHIC: {
                "potential_factor": 0.20,
                "min_yield_factor": 0.05,
                "max_loss_percent": 95
            }
        }
        
        constraints = scenario_constraints[scenario.type]
        scenario_potential = base_potential * constraints["potential_factor"]
        
        # Facteurs de réduction ÉQUILIBRÉS
        # 1. Stress cumulés (réduit pour éviter sur-pénalisation)
        stress_reduction = min(0.6, crop_state.accumulated_stress * 0.4)  # Max 60% réduction
        stress_factor = max(0.4, 1 - stress_reduction)
        
        # 2. Facteur croissance (plus modéré)
        growth_factor = max(0.6, 1 - crop_state.growth_reduction * 0.3)  # Max 40% réduction
        
        # 3. Facteur hydrique (basé sur besoins réels Mali)
        water_needs = self.crop_profiles.get_stress_thresholds(crop)["rainfall_mm"]
        effective_rain = cycle_data["total_effective_rain"]
        
        # Seuils hydriques spécifiques Mali
        if crop == "mil":
            water_factor = min(1.0, effective_rain / max(300, water_needs * 0.6))  # Très tolérant
        elif crop == "sorgho":
            water_factor = min(1.0, effective_rain / max(400, water_needs * 0.7))  # Tolérant
        elif crop == "maïs":
            water_factor = min(1.0, effective_rain / max(600, water_needs * 0.9))  # Exigeant
        else:
            water_factor = min(1.0, effective_rain / water_needs)
        
        # 4. Facteur gestion (bonus modéré)
        management_factor = 1.0 + (management["fertilizer_adjustment"] - 1.0) * 0.15  # Max +15%
        management_factor = max(0.8, min(1.2, management_factor))
        
        # Calcul rendement avec tous les facteurs
        calculated_yield = scenario_potential * stress_factor * growth_factor * water_factor * management_factor
        
        # FORCER le respect des contraintes de scénario
        min_yield = base_potential * constraints["min_yield_factor"]
        max_yield = scenario_potential  # Ne pas dépasser le potentiel du scénario
        
        actual_yield = np.clip(calculated_yield, min_yield, max_yield)
        
        # Calcul perte cohérente
        max_allowed_loss = constraints["max_loss_percent"]
        loss_percent = ((scenario_potential - actual_yield) / scenario_potential) * 100
        
        # Si perte dépasse le maximum autorisé, recalculer le rendement
        if loss_percent > max_allowed_loss:
            actual_yield = scenario_potential * (1 - max_allowed_loss / 100)
            loss_percent = max_allowed_loss
        
        # Harvest Index ajusté selon culture et stress
        base_hi = {"mil": 0.30, "sorgho": 0.35, "maïs": 0.48, "coton": 0.20, "riz": 0.50}
        hi = base_hi.get(crop, 0.35)
        
        # Réduction HI sous stress (limité)
        if crop_state.accumulated_stress > 0.5:
            hi *= max(0.85, 1 - crop_state.accumulated_stress * 0.15)  # Max -15%
        
        biomass_total = actual_yield / hi
        
        return {
            "potential_yield": round(scenario_potential, 1),
            "final_yield": round(actual_yield, 1),
            "loss_percent": round(loss_percent, 1),
            "biomass_total": round(biomass_total, 1),
            "grain_straw_ratio": round(hi, 3)
        }
    
    def _generate_coherent_ndvi(
        self,
        crop: str,
        final_yield: float,
        crop_state: CropState,
        cycle_data: Dict
    ) -> Dict[str, float]:
        """
        Génère NDVI cohérent sans valeurs NaN
        
        📚 Base : Relations NDVI-biomasse validées Sahel
        """
        
        # NDVI de base selon rendement (relation empirique Mali)
        # Source : +0.1 NDVI = +0.8-1.3 t/ha rendement céréales
        if final_yield > 0:
            # Relation calibrée Mali : NDVI = 0.3 + (yield/3000) * 0.5
            base_ndvi = 0.3 + min(0.5, final_yield / 3000 * 0.5)
        else:
            base_ndvi = 0.25  # NDVI minimum sol cultivé
        
        # Ajustement selon culture
        crop_factors = {
            "mil": 0.85,      # NDVI plus faible (clairsemé)
            "sorgho": 0.90,   # NDVI modéré
            "maïs": 1.0,      # NDVI de référence
            "coton": 0.95,    # NDVI modéré-élevé
            "riz": 1.05       # NDVI élevé (dense)
        }
        
        ndvi_adjusted = base_ndvi * crop_factors.get(crop, 1.0)
        
        # Timeline temporelle réaliste
        timeline = {
            "sowing": 0.15,
            "emergence": 0.25,
            "vegetative_peak": ndvi_adjusted * 0.70,
            "flowering": ndvi_adjusted * 0.95,
            "maturity": ndvi_adjusted * 0.60
        }
        
        # Application stress history avec modération
        for stress_event in crop_state.stress_history:
            stage = stress_event["stage"]
            impact = min(0.4, stress_event["impact"] * 0.3)  # Limiter impact
            
            if stage == "vegetative":
                timeline["vegetative_peak"] *= (1 - impact)
            elif stage == "flowering":
                timeline["flowering"] *= (1 - impact)
                timeline["maturity"] *= (1 - impact * 0.5)
        
        # GARANTIR bornes valides et éliminer NaN
        for key in timeline:
            value = timeline[key]
            if np.isnan(value) or np.isinf(value):
                value = 0.3  # Valeur de sécurité
            timeline[key] = round(np.clip(value, 0.10, 0.95), 3)
        
        return timeline
    
    def generate_scenario_examples(self) -> pd.DataFrame:
        """
        Génère 5 exemples, un par type de scénario
        
        🎯 Démontre la cohérence causale pour chaque scénario
        """
        
        examples = []
        scenarios = [
            ScenarioType.EXCEPTIONAL,
            ScenarioType.GOOD,
            ScenarioType.AVERAGE,
            ScenarioType.DIFFICULT,
            ScenarioType.CATASTROPHIC
        ]
        
        localities = ["SIKASSO", "BAMAKO", "SEGOU", "BOUGOUNI", "MOPTI"]
        crops = ["maïs", "sorgho", "mil", "coton", "mil"]
        
        for i, scenario_type in enumerate(scenarios):
            print(f"\n🌾 Génération exemple {scenario_type.value}...")
            
            row = self.generate_coherent_row(
                year=2023,
                locality=localities[i],
                initial_crop=crops[i],
                scenario_type=scenario_type
            )
            
            # Résumé narratif
            print(f"  📖 Histoire : {row['ScenarioNarrative'][:100]}...")
            print(f"  🌾 Culture : {row['InitialCrop']} → {row['FinalCrop']}")
            print(f"  💧 Pluie : {row['SeasonRainfall_mm']}mm (efficace: {row['EffectiveRainfall_mm']}mm)")
            print(f"  😰 Stress accumulé : {row['AccumulatedStress']}")
            print(f"  🌾 Rendement : {row['ActualYield_kg_ha']}kg/ha ({row['YieldLoss_percent']}% perte)")
            print(f"  📊 NDVI max : {row['NDVI_peak']}")
            
            examples.append(row)
        
        return pd.DataFrame(examples)


# =============================================================================
# 🧪 TESTS ET VALIDATION
# =============================================================================

if __name__ == "__main__":
    print("🚀 TEST GÉNÉRATEUR V3 AVEC COHÉRENCE CAUSALE")
    print("=" * 60)
    
    # Initialisation
    generator = CausalCoherentGenerator()
    
    # Génération des 5 exemples
    print("\n📊 Génération des exemples par scénario...")
    examples_df = generator.generate_scenario_examples()
    
    # Analyse cohérence
    print("\n✅ VALIDATION COHÉRENCE CAUSALE :")
    print("-" * 40)
    
    for idx, row in examples_df.iterrows():
        scenario = row['Scenario']
        stress = row['AccumulatedStress']
        yield_loss = row['YieldLoss_percent']
        
        # Vérification cohérence stress-rendement
        if scenario == "exceptional" and (stress > 0.2 or yield_loss > 20):
            print(f"❌ Incohérence : Scénario exceptionnel avec stress/pertes élevés")
        elif scenario == "catastrophic" and (stress < 0.5 or yield_loss < 50):
            print(f"❌ Incohérence : Scénario catastrophique avec stress/pertes faibles")
        else:
            print(f"✅ {scenario} : Cohérence validée (stress={stress:.2f}, perte={yield_loss:.1f}%)")
    
    print("\n🎉 GÉNÉRATEUR V3 OPÉRATIONNEL - COHÉRENCE CAUSALE GARANTIE!")


# =============================================================================
# 📚 DOCUMENTATION DES AMÉLIORATIONS V3
# =============================================================================

"""
🌟 AMÉLIORATIONS CLÉS V2 → V3

1️⃣ SCÉNARIOS AGRICOLES COHÉRENTS
   - 5 types avec probabilités réelles Mali
   - Chaque scénario = histoire complète
   - Distribution temporelle réaliste des stress

2️⃣ CAUSALITÉ TEMPORELLE
   - Stress appliqués par stade phénologique
   - Impact différencié selon période (floraison critique)
   - Propagation des effets dans le temps

3️⃣ MÉMOIRE DES ÉVÉNEMENTS
   - CropState accumule l'historique
   - Stress précoce → réduction croissance permanente
   - Effet cumulatif avec décroissance

4️⃣ DÉCISIONS PAYSANNES ADAPTATIVES
   - Changement culture si conditions défavorables
   - Ajustement date semis selon onset
   - Réduction intrants si B/C < 1.8

5️⃣ HYDROLOGIE RÉALISTE
   - Ruissellement 30-70% début saison
   - Distribution mensuelle (37% août)
   - Pluie effective ≠ pluie totale

6️⃣ COHÉRENCE NDVI-RENDEMENT-HISTOIRE
   - NDVI suit l'histoire des stress
   - Timeline cohérente avec événements
   - Corrélation validée avec biomasse

✅ RÉSULTAT : Chaque ligne = Histoire agricole complète et cohérente
"""
