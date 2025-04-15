"""
EarlyWarningModel: Simulates early warning systems and population response
"""

import numpy as np

class EarlyWarningModel:
    """Model early warning systems and population response to warnings"""
    def __init__(self):
        # Initialize early warning parameters and response models
        self._initialize_warning_parameters()
    
    def _initialize_warning_parameters(self):
        """Initialize early warning system parameters and response behavior"""
        # Forecast skill levels by hazard type and lead time
        self.forecast_skill = {
            'flood': {
                # Lead time in days
                1: 0.85,  # 1-day ahead forecast skill
                3: 0.75,  # 3-day ahead forecast skill
                5: 0.65,  # 5-day ahead forecast skill
                7: 0.55,  # 7-day ahead forecast skill
                10: 0.45  # 10-day ahead forecast skill
            },
            'flash_flood': {
                # Lead time in hours
                1: 0.60,  # 1-hour ahead forecast skill
                3: 0.55,  # 3-hour ahead forecast skill
                6: 0.50,  # 6-hour ahead forecast skill
                12: 0.40,  # 12-hour ahead forecast skill
                24: 0.30   # 24-hour ahead forecast skill
            },
            'cyclone': {
                # Lead time in hours
                24: 0.75,  # 24-hour ahead forecast skill
                48: 0.65,  # 48-hour ahead forecast skill
                72: 0.55,  # 72-hour ahead forecast skill
                96: 0.45,  # 96-hour ahead forecast skill
                120: 0.35  # 120-hour ahead forecast skill
            },
            'storm_surge': {
                # Lead time in hours
                6: 0.70,  # 6-hour ahead forecast skill
                12: 0.65,  # 12-hour ahead forecast skill
                24: 0.50,  # 24-hour ahead forecast skill
                36: 0.35,  # 36-hour ahead forecast skill
                48: 0.25   # 48-hour ahead forecast skill
            },
            'drought': {
                # Lead time in months
                0.5: 0.65,  # 2-week ahead forecast skill
                1: 0.55,    # 1-month ahead forecast skill
                2: 0.45,    # 2-month ahead forecast skill
                3: 0.35,    # 3-month ahead forecast skill
                6: 0.25     # 6-month ahead forecast skill
            }
        }
        
        # Warning dissemination systems and coverage
        self.dissemination_systems = {
            'sirens': {
                'coverage': 0.15,  # % of population covered
                'reliability': 0.80,  # % of time system works as intended
                'comprehension': 0.95,  # % of people who understand meaning
                'lead_time': 0.1,  # hours required to activate
                'urban_bias': 0.7,  # higher coverage in urban areas
                'placement': ['coastal', 'flood_prone']
            },
            'sms': {
                'coverage': 0.70,  # % of population with mobile phones
                'reliability': 0.85,  # % of time system works as intended
                'comprehension': 0.80,  # % of people who understand meaning
                'lead_time': 0.2,  # hours required to activate
                'urban_bias': 0.6,  # higher coverage in urban areas
                'literacy_dependent': True
            },
            'radio': {
                'coverage': 0.85,  # % of population with access
                'reliability': 0.90,  # % of time system works as intended
                'comprehension': 0.85,  # % of people who understand meaning
                'lead_time': 0.5,  # hours required to activate
                'urban_bias': 0.2,  # small urban bias
                'literacy_dependent': False
            },
            'television': {
                'coverage': 0.60,  # % of population with access
                'reliability': 0.85,  # % of time system works as intended
                'comprehension': 0.90,  # % of people who understand meaning
                'lead_time': 0.5,  # hours required to activate
                'urban_bias': 0.5,  # moderate urban bias
                'electricity_dependent': True
            },
            'volunteer_network': {
                'coverage': 0.55,  # % of population covered
                'reliability': 0.75,  # % of time system works as intended
                'comprehension': 0.95,  # % of people who understand meaning
                'lead_time': 1.0,  # hours required to activate
                'urban_bias': -0.3,  # better in rural areas
                'training_dependent': True
            },
            'mosque_announcements': {
                'coverage': 0.90,  # % of population covered
                'reliability': 0.70,  # % of time system works as intended
                'comprehension': 0.95,  # % of people who understand meaning
                'lead_time': 1.0,  # hours required to activate
                'urban_bias': -0.1,  # slightly better in rural areas
                'time_of_day_dependent': True
            }
        }
        
        # Evacuation behavior parameters by demographic
        self.evacuation_behavior = {
            'compliance_base_rate': 0.65,  # Base compliance rate
            'gender_factor': {
                'male': 1.0,
                'female': 0.85  # Lower due to care responsibilities and mobility constraints
            },
            'age_factor': {
                'child': 1.1,  # Higher as part of family units
                'adult': 1.0,
                'elderly': 0.75  # Lower due to mobility and attachment to property
            },
            'income_factor': {
                'low': 0.85,  # Lower due to livelihood concerns and lack of transport
                'medium': 1.0,
                'high': 1.1  # Higher due to better resources and transportation
            },
            'previous_experience': {
                'none': 0.9,  # Lower without prior experience
                'false_alarm': 0.7,  # Much lower after false alarms
                'minor_impact': 1.1,  # Higher after experiencing minor impacts
                'major_impact': 1.3  # Much higher after experiencing major impacts
            },
            'warning_specificity_factor': {
                'generic': 0.8,
                'location_specific': 1.0,
                'impact_based': 1.2  # Higher for impact-based forecasts
            },
            'warning_lead_time_factor': {
                'very_short': 0.8,  # Less than 3 hours
                'short': 0.9,  # 3-12 hours
                'adequate': 1.1,  # 12-48 hours
                'long': 1.0  # More than 48 hours (decreases due to uncertainty)
            },
            'livelihood_factor': {
                'agriculture': 0.8,  # Lower due to crop/livestock concerns
                'fishing': 0.85,  # Lower due to boat/equipment concerns
                'business': 0.9,  # Lower due to property protection
                'service': 1.0,
                'government': 1.1  # Higher due to awareness
            }
        }
        
        # Regional early warning system development level (0.0-1.0 scale)
        self.regional_ews_capacity = {
            'coastal': 0.8,  # High capacity due to cyclone preparedness program
            'urban': 0.7,  # Good capacity in urban centers
            'flood_plain': 0.6,  # Moderate capacity in major flood plains
            'haor_basin': 0.5,  # Lower capacity in flash flood prone areas
            'char_lands': 0.4,  # Low capacity in river islands
            'hill_tracts': 0.4,  # Low capacity in remote hill areas
            'barind_tract': 0.5   # Moderate capacity in drought prone areas
        }
        
        # Impact of false alarms on future compliance
        self.false_alarm_effect = {
            'decay_rate': 0.15,  # Compliance reduction per false alarm
            'recovery_time': 3,   # Years to recover from false alarm
            'minimum_compliance': 0.3  # Floor on compliance even after many false alarms
        }
    
    def simulate_warning_process(self, hazard_event, system_capabilities):
        """Simulate the early warning process for a hazard event
        
        Args:
            hazard_event: Dictionary with hazard properties
            system_capabilities: Dictionary with EWS capabilities and resources
            
        Returns:
            Dictionary with warning process results
        """
        # Extract relevant hazard information
        hazard_type = hazard_event['type']
        hazard_intensity = hazard_event['intensity']
        region_type = hazard_event['spatial_footprint'].get('type', 'generic')
        
        # Determine whether warning is possible based on hazard type
        if hazard_type not in self.forecast_skill:
            # No warning system for this hazard type
            warning_possible = False
            forecast_lead_time = 0
            forecast_accuracy = 0
        else:
            # Warning is possible
            warning_possible = True
            
            # Determine available lead time (hazard-specific)
            if hazard_type == 'flood':
                # Riverine floods have longer lead times
                available_lead_times = [1, 3, 5, 7, 10]  # days
                if 'duration' in hazard_event and hazard_event['duration'] > 2:
                    # For longer-duration floods, we have more lead time
                    forecast_lead_time = np.random.choice([5, 7, 10], p=[0.3, 0.4, 0.3])
                else:
                    forecast_lead_time = np.random.choice([1, 3, 5], p=[0.3, 0.4, 0.3])
                    
            elif hazard_type == 'flash_flood':
                # Flash floods have very short lead times
                available_lead_times = [1, 3, 6, 12, 24]  # hours
                forecast_lead_time = np.random.choice([1, 3, 6], p=[0.5, 0.3, 0.2])
                
            elif hazard_type == 'cyclone':
                # Cyclones typically have days of lead time
                available_lead_times = [24, 48, 72, 96, 120]  # hours
                forecast_lead_time = np.random.choice([48, 72, 96], p=[0.3, 0.4, 0.3])
                
            elif hazard_type == 'storm_surge':
                # Storm surge follows cyclone but with less lead time
                available_lead_times = [6, 12, 24, 36, 48]  # hours
                forecast_lead_time = np.random.choice([12, 24, 36], p=[0.3, 0.4, 0.3])
                
            elif hazard_type == 'drought':
                # Droughts have longest lead times but highest uncertainty
                available_lead_times = [0.5, 1, 2, 3, 6]  # months
                forecast_lead_time = np.random.choice([0.5, 1, 2], p=[0.3, 0.4, 0.3])
            
            else:
                # Generic hazard
                forecast_lead_time = 1  # Default 1 day lead time
                available_lead_times = [1]
            
            # Determine forecast accuracy based on lead time and hazard type
            # Find the closest available lead time
            closest_lead_time = min(available_lead_times, key=lambda x: abs(x - forecast_lead_time))
            base_forecast_skill = self.forecast_skill[hazard_type][closest_lead_time]
            
            # Adjust forecast skill based on system capabilities
            technology_factor = system_capabilities.get('technology_level', 0.5)
            training_factor = system_capabilities.get('staff_training', 0.5)
            data_factor = system_capabilities.get('observation_network', 0.5)
            
            # Calculate modified forecast accuracy
            forecast_accuracy = base_forecast_skill * (
                0.7 + 0.1 * technology_factor + 0.1 * training_factor + 0.1 * data_factor)
            forecast_accuracy = min(0.95, max(0.1, forecast_accuracy))  # Bounded between 0.1 and 0.95
        
        # Determine if forecast correctly predicts hazard (add some randomness)
        forecast_correct = np.random.random() < forecast_accuracy
        
        # If forecast is correct, proceed with warning dissemination
        if warning_possible and forecast_correct:
            warning_issued = True
            
            # Calculate overall warning dissemination effectiveness
            dissemination_effectiveness = self._calculate_dissemination_effectiveness(
                system_capabilities, region_type, hazard_type)
            
            # Adjust effectiveness based on regional capacity
            region_capacity = self.regional_ews_capacity.get(region_type, 0.5)
            dissemination_effectiveness *= (0.5 + 0.5 * region_capacity)
            
            # Calculate population response rate based on warning and demographics
            response_rate = self._calculate_population_response(
                hazard_type, hazard_intensity, forecast_lead_time, 
                dissemination_effectiveness, region_type, system_capabilities)
            
        elif warning_possible and not forecast_correct:
            # False negative (missed warning) or false positive (false alarm)
            if hazard_intensity > 0.5:  # Significant hazard missed
                warning_issued = False
                dissemination_effectiveness = 0
                response_rate = 0
            else:  # False alarm
                warning_issued = True
                dissemination_effectiveness = self._calculate_dissemination_effectiveness(
                    system_capabilities, region_type, hazard_type)
                response_rate = self._calculate_population_response(
                    hazard_type, 0.1, forecast_lead_time, 
                    dissemination_effectiveness, region_type, system_capabilities)
                # Record false alarm for future compliance adjustment
                # (In full implementation, would store this state)
        else:
            # No warning possible
            warning_issued = False
            dissemination_effectiveness = 0
            response_rate = 0
        
        # Calculate lives saved through early warning
        lives_saved = 0
        if warning_issued and hazard_intensity > 0.3:  # Only significant hazards cause casualties
            # Estimate potential casualties without warning
            potential_casualties = self._estimate_potential_casualties(
                hazard_type, hazard_intensity, region_type)
            
            # Calculate casualties prevented through early warning
            prevention_effectiveness = response_rate * 0.8  # 80% of responders avoid casualty
            lives_saved = potential_casualties * prevention_effectiveness
        
        # Return warning process results
        return {
            'warning_possible': warning_possible,
            'forecast_lead_time': forecast_lead_time,
            'forecast_accuracy': forecast_accuracy,
            'warning_issued': warning_issued,
            'dissemination_effectiveness': dissemination_effectiveness,
            'population_response_rate': response_rate,
            'lives_saved': int(lives_saved),
            'forecast_correct': forecast_correct
        }
    
    def _calculate_dissemination_effectiveness(self, system_capabilities, region_type, hazard_type):
        """Calculate effectiveness of warning dissemination"""
        # Calculate weighted effectiveness across all available dissemination channels
        total_effectiveness = 0
        total_weight = 0
        
        # Get available systems based on capabilities
        available_systems = system_capabilities.get('available_systems', ['radio', 'volunteer_network'])
        
        for system_name in available_systems:
            if system_name in self.dissemination_systems:
                system = self.dissemination_systems[system_name]
                
                # Calculate basic effectiveness for this system
                base_effectiveness = system['coverage'] * system['reliability'] * system['comprehension']
                
                # Adjust for region type (urban vs rural)
                if region_type == 'urban':
                    if 'urban_bias' in system:
                        base_effectiveness *= (1 + system['urban_bias'])
                elif 'urban_bias' in system and system['urban_bias'] < 0:
                    # Rural areas benefit from negative urban bias
                    base_effectiveness *= (1 - system['urban_bias'])
                
                # Adjust for special requirements
                if 'literacy_dependent' in system and system['literacy_dependent']:
                    # Reduce effectiveness in areas with low literacy
                    literacy_rate = system_capabilities.get('literacy_rate', 0.6)  # Default to 60%
                    base_effectiveness *= 0.5 + 0.5 * literacy_rate
                
                if 'electricity_dependent' in system and system['electricity_dependent']:
                    # Reduce effectiveness in areas with unreliable electricity
                    electricity_reliability = system_capabilities.get('electricity_reliability', 0.7)  # Default to 70%
                    base_effectiveness *= electricity_reliability
                
                if 'time_of_day_dependent' in system and system['time_of_day_dependent']:
                    # Average out time of day effect - in real implementation would consider actual time
                    base_effectiveness *= 0.8  # 20% reduction due to time dependency
                
                # Weight by system importance for this hazard type
                system_weight = 1.0
                if hazard_type == 'cyclone' and system_name in ['sirens', 'radio', 'volunteer_network']:
                    system_weight = 1.5  # More important for cyclones
                elif hazard_type == 'flood' and system_name in ['radio', 'television', 'mosque_announcements']:
                    system_weight = 1.3  # More important for floods
                
                total_effectiveness += base_effectiveness * system_weight
                total_weight += system_weight
        
        # Calculate normalized effectiveness
        if total_weight > 0:
            overall_effectiveness = total_effectiveness / total_weight
        else:
            overall_effectiveness = 0
        
        # Cap at reasonable bounds
        return min(0.95, max(0.05, overall_effectiveness))
    
    def _calculate_population_response(self, hazard_type, hazard_intensity, lead_time, 
                                      dissemination_effectiveness, region_type, system_capabilities):
        """Calculate population response rate to the warning"""
        # Start with base compliance rate
        base_response_rate = self.evacuation_behavior['compliance_base_rate']
        
        # Adjust for hazard intensity (people respond more to severe hazards)
        intensity_factor = 0.7 + 0.6 * hazard_intensity  # Ranges from 0.7 to 1.3
        
        # Adjust for warning lead time
        lead_time_category = self._categorize_lead_time(hazard_type, lead_time)
        lead_time_factor = self.evacuation_behavior['warning_lead_time_factor'][lead_time_category]
        
        # Adjust for warning specificity - impact-based warnings are more effective
        warning_specificity = system_capabilities.get('warning_specificity', 'generic')
        if warning_specificity in self.evacuation_behavior['warning_specificity_factor']:
            specificity_factor = self.evacuation_behavior['warning_specificity_factor'][warning_specificity]
        else:
            specificity_factor = 1.0
        
        # Adjust for previous experience (simplified - would need event history in full implementation)
        experience_category = system_capabilities.get('previous_experience', 'none')
        if experience_category in self.evacuation_behavior['previous_experience']:
            experience_factor = self.evacuation_behavior['previous_experience'][experience_category]
        else:
            experience_factor = 1.0
        
        # Adjust for regional characteristics
        region_factor = 1.0
        if region_type == 'coastal' and hazard_type == 'cyclone':
            region_factor = 1.2  # Higher compliance in coastal areas for cyclones
        elif region_type == 'flood_plain' and hazard_type == 'flood':
            region_factor = 1.1  # Higher compliance in flood plains for floods
        
        # Calculate combined response rate
        response_rate = base_response_rate * intensity_factor * lead_time_factor * \
                       specificity_factor * experience_factor * region_factor * \
                       dissemination_effectiveness
        
        # Demographic adjustments (simplified - would use population demographics in full implementation)
        # Using national averages:
        # - Gender distribution: ~50% female
        # - Age distribution: ~30% children, ~60% adults, ~10% elderly
        # - Income distribution: ~40% low, ~50% medium, ~10% high
        # - Livelihood distribution: ~40% agriculture, ~10% fishing, ~30% business, ~15% service, ~5% government
        
        gender_adjustment = 0.5 * self.evacuation_behavior['gender_factor']['male'] + \
                           0.5 * self.evacuation_behavior['gender_factor']['female']
        
        age_adjustment = 0.3 * self.evacuation_behavior['age_factor']['child'] + \
                        0.6 * self.evacuation_behavior['age_factor']['adult'] + \
                        0.1 * self.evacuation_behavior['age_factor']['elderly']
        
        income_adjustment = 0.4 * self.evacuation_behavior['income_factor']['low'] + \
                          0.5 * self.evacuation_behavior['income_factor']['medium'] + \
                          0.1 * self.evacuation_behavior['income_factor']['high']
        
        livelihood_adjustment = 0.4 * self.evacuation_behavior['livelihood_factor']['agriculture'] + \
                               0.1 * self.evacuation_behavior['livelihood_factor']['fishing'] + \
                               0.3 * self.evacuation_behavior['livelihood_factor']['business'] + \
                               0.15 * self.evacuation_behavior['livelihood_factor']['service'] + \
                               0.05 * self.evacuation_behavior['livelihood_factor']['government']
        
        # Apply demographic adjustments
        response_rate *= gender_adjustment * age_adjustment * income_adjustment * livelihood_adjustment
        
        # Cap at reasonable bounds
        return min(0.95, max(0.05, response_rate))
    
    def _categorize_lead_time(self, hazard_type, lead_time):
        """Categorize lead time as very_short, short, adequate, or long"""
        if hazard_type in ['cyclone', 'storm_surge']:
            # Hours
            if lead_time < 6:
                return 'very_short'
            elif lead_time < 24:
                return 'short'
            elif lead_time < 72:
                return 'adequate'
            else:
                return 'long'
        elif hazard_type == 'flood':
            # Days
            if lead_time < 1:
                return 'very_short'
            elif lead_time < 3:
                return 'short'
            elif lead_time < 7:
                return 'adequate'
            else:
                return 'long'
        elif hazard_type == 'flash_flood':
            # Hours
            if lead_time < 3:
                return 'very_short'
            elif lead_time < 6:
                return 'short'
            elif lead_time < 12:
                return 'adequate'
            else:
                return 'long'
        elif hazard_type == 'drought':
            # Months
            if lead_time < 0.5:
                return 'very_short'
            elif lead_time < 1:
                return 'short'
            elif lead_time < 3:
                return 'adequate'
            else:
                return 'long'
        else:
            # Default categorization
            return 'adequate'
    
    def _estimate_potential_casualties(self, hazard_type, hazard_intensity, region_type):
        """Estimate potential casualties without early warning"""
        # Baseline casualty rates per 100,000 population by hazard type
        baseline_rates = {
            'cyclone': 50,
            'flood': 20,
            'flash_flood': 30,
            'storm_surge': 40,
            'drought': 5,
            'landslide': 60,
            'earthquake': 100
        }
        
        # Get baseline rate for this hazard type (default to 10 if not defined)
        base_rate = baseline_rates.get(hazard_type, 10)
        
        # Adjust by hazard intensity (non-linear relationship)
        # For severe events (intensity > 0.7), casualty rates increase dramatically
        if hazard_intensity > 0.7:
            intensity_factor = 1 + 10 * (hazard_intensity - 0.7) ** 2
        else:
            intensity_factor = hazard_intensity / 0.7
        
        # Regional adjustments
        region_factor = 1.0
        if region_type == 'coastal' and hazard_type in ['cyclone', 'storm_surge']:
            region_factor = 1.3  # Higher risk in coastal areas
        elif region_type == 'hill_tracts' and hazard_type == 'landslide':
            region_factor = 1.5  # Higher risk in hill areas
        elif region_type == 'urban' and hazard_type in ['flood', 'earthquake']:
            region_factor = 1.4  # Higher risk in urban areas due to population density
        
        # Simplified population exposure (would use actual exposure in full implementation)
        # Assuming 100,000 people exposed on average
        exposed_population = 100000
        
        # Calculate potential casualties
        potential_casualties = base_rate * intensity_factor * region_factor * exposed_population / 100000
        
        return int(potential_casualties)
