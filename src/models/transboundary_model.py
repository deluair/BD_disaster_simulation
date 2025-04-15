"""
TransboundaryModel: Models cross-border disaster dimensions
"""

import numpy as np

class TransboundaryModel:
    """Model cross-border disaster dimensions"""
    def __init__(self):
        # Initialize transboundary parameters
        self._initialize_transboundary_parameters()
        
    def _initialize_transboundary_parameters(self):
        """Initialize parameters for transboundary effects"""
        # Upstream countries affecting Bangladesh
        self.upstream_countries = {
            'india': {
                'shared_rivers': ['brahmaputra', 'ganges', 'teesta', 'feni', 'meghna'],
                'control_factor': 0.8,  # High control over river flows
                'cooperation_history': 0.6,  # Moderate historical cooperation
                'notification_system': 0.7,  # Moderate notification system
                'dam_capacity': {  # Major dams affecting flow to Bangladesh
                    'farakka_barrage': {
                        'capacity_mcm': 570000,  # million cubic meters
                        'control_river': 'ganges',
                        'purpose': ['irrigation', 'navigation'],
                        'distance_to_border_km': 16
                    },
                    'gajoldoba_barrage': {
                        'capacity_mcm': 40000,
                        'control_river': 'teesta',
                        'purpose': ['irrigation', 'hydropower'],
                        'distance_to_border_km': 100
                    },
                    'dumbur_dam': {
                        'capacity_mcm': 5800,
                        'control_river': 'gumti',
                        'purpose': ['hydropower', 'flood_control'],
                        'distance_to_border_km': 35
                    }
                }
            },
            'nepal': {
                'shared_rivers': ['koshi', 'gandaki', 'karnali'],
                'control_factor': 0.4,  # Lower control over river flows
                'cooperation_history': 0.7,  # Good historical cooperation
                'notification_system': 0.6,  # Moderate notification system
                'dam_capacity': {
                    'koshi_barrage': {
                        'capacity_mcm': 13350,
                        'control_river': 'koshi',
                        'purpose': ['flood_control', 'irrigation'],
                        'distance_to_border_km': 20
                    }
                }
            },
            'china': {
                'shared_rivers': ['brahmaputra', 'ganges'],
                'control_factor': 0.5,  # Moderate control (upper reaches)
                'cooperation_history': 0.4,  # Lower historical cooperation
                'notification_system': 0.3,  # Limited notification system
                'dam_capacity': {
                    'zangmu_dam': {
                        'capacity_mcm': 86600,
                        'control_river': 'brahmaputra',
                        'purpose': ['hydropower'],
                        'distance_to_border_km': 550
                    }
                }
            },
            'bhutan': {
                'shared_rivers': ['manas', 'sankosh'],
                'control_factor': 0.3,  # Lower control over river flows
                'cooperation_history': 0.8,  # Good historical cooperation
                'notification_system': 0.7,  # Good notification system
                'dam_capacity': {
                    'kurichhu_dam': {
                        'capacity_mcm': 2800,
                        'control_river': 'kurichhu',
                        'purpose': ['hydropower'],
                        'distance_to_border_km': 30
                    }
                }
            }
        }
        
        # Major rivers and their transboundary characteristics
        self.river_systems = {
            'brahmaputra': {
                'upstream_countries': ['china', 'india'],
                'flow_contribution': {  # % of flow from each country
                    'china': 25,
                    'india': 40,
                    'bangladesh': 35
                },
                'flow_variability': 0.4,  # Natural flow variability
                'sediment_load': 'very_high',
                'flood_propagation_time_days': {  # Days for flood peak to reach Bangladesh
                    'china': 10,
                    'india': 4
                }
            },
            'ganges': {
                'upstream_countries': ['nepal', 'india', 'china'],
                'flow_contribution': {
                    'nepal': 40,
                    'india': 45,
                    'china': 5,
                    'bangladesh': 10
                },
                'flow_variability': 0.6,  # High variability between wet/dry seasons
                'sediment_load': 'high',
                'flood_propagation_time_days': {
                    'nepal': 7,
                    'india': 3,
                    'china': 12
                }
            },
            'meghna': {
                'upstream_countries': ['india'],
                'flow_contribution': {
                    'india': 65,
                    'bangladesh': 35
                },
                'flow_variability': 0.5,
                'sediment_load': 'medium',
                'flood_propagation_time_days': {
                    'india': 3
                }
            },
            'teesta': {
                'upstream_countries': ['india'],
                'flow_contribution': {
                    'india': 70,
                    'bangladesh': 30
                },
                'flow_variability': 0.7,  # Very high variability
                'sediment_load': 'medium',
                'flood_propagation_time_days': {
                    'india': 2
                }
            }
        }
        
        # Transboundary disaster types
        self.transboundary_disaster_types = {
            'riverine_flood': {
                'upstream_dependency': 0.9,  # High dependency on upstream conditions
                'notification_importance': 0.8,  # Importance of early notification
                'control_possible': 0.7,  # Dams/barriers can influence
                'seasonal_pattern': [0.1, 0.1, 0.2, 0.3, 0.7, 0.9, 1.0, 0.9, 0.7, 0.3, 0.2, 0.1]  # Monthly pattern
            },
            'flash_flood': {
                'upstream_dependency': 0.6,  # Moderate dependency
                'notification_importance': 0.9,  # Very important due to rapid onset
                'control_possible': 0.4,  # Limited control
                'seasonal_pattern': [0.1, 0.1, 0.3, 0.6, 0.8, 0.7, 0.6, 0.5, 0.4, 0.2, 0.1, 0.1]
            },
            'drought': {
                'upstream_dependency': 0.8,  # High dependency
                'notification_importance': 0.5,  # Less critical (slower onset)
                'control_possible': 0.8,  # High influence from water management
                'seasonal_pattern': [0.3, 0.4, 0.6, 0.8, 0.9, 0.7, 0.5, 0.3, 0.2, 0.2, 0.2, 0.3]
            },
            'water_pollution': {
                'upstream_dependency': 0.9,  # Very high dependency
                'notification_importance': 0.7,
                'control_possible': 0.6,
                'seasonal_pattern': [0.5, 0.5, 0.6, 0.7, 0.8, 0.9, 0.9, 0.9, 0.8, 0.7, 0.6, 0.5]
            },
            'sedimentation': {
                'upstream_dependency': 0.8,
                'notification_importance': 0.3,  # Less immediate impact
                'control_possible': 0.5,
                'seasonal_pattern': [0.3, 0.3, 0.4, 0.5, 0.7, 0.9, 1.0, 0.9, 0.8, 0.6, 0.4, 0.3]
            }
        }
        
        # Water treaties and cooperation agreements
        self.water_treaties = {
            'ganges_water_treaty': {
                'countries': ['india', 'bangladesh'],
                'signed_year': 1996,
                'rivers': ['ganges'],
                'effectiveness': 0.7,  # 0-1 scale
                'flow_guarantee': {
                    'dry_season': 0.6,  # Guaranteed flow in dry season
                    'wet_season': 0.3   # Less guarantee needed in wet season
                }
            },
            'india_bangladesh_mou': {
                'countries': ['india', 'bangladesh'],
                'signed_year': 2010,
                'rivers': ['teesta'],
                'effectiveness': 0.3,  # Limited effectiveness
                'flow_guarantee': {
                    'dry_season': 0.2,
                    'wet_season': 0.1
                }
            }
        }
        
        # Upstream land use change impacts
        self.upstream_land_use_impacts = {
            'deforestation': {
                'flood_impact': 0.3,  # Increased flood risk
                'erosion_impact': 0.4,  # Increased erosion
                'sedimentation_impact': 0.4,  # Increased sedimentation
                'current_trend': {
                    'india': 0.02,  # Annual rate
                    'nepal': 0.01,
                    'bhutan': 0.005,
                    'china': 0.01
                }
            },
            'urbanization': {
                'flood_impact': 0.2,  # Increased runoff
                'water_quality_impact': 0.3,  # Decreased water quality
                'current_trend': {
                    'india': 0.03,  # Annual rate
                    'nepal': 0.02,
                    'bhutan': 0.01,
                    'china': 0.04
                }
            },
            'agricultural_intensification': {
                'water_quality_impact': 0.3,  # Increased pollution
                'water_quantity_impact': 0.2,  # Increased consumption
                'current_trend': {
                    'india': 0.02,
                    'nepal': 0.01,
                    'bhutan': 0.01,
                    'china': 0.02
                }
            }
        }
    
    def simulate_transboundary_effects(self, upstream_conditions, cooperation_level):
        """Simulate the effects of upstream conditions on Bangladesh hazards
        
        Args:
            upstream_conditions: Dictionary of conditions in upstream countries
            cooperation_level: Dictionary of cooperation levels with each country
            
        Returns:
            Dictionary of transboundary effects on hazards
        """
        # Initialize effects dictionary
        transboundary_effects = {
            'river_flow_modification': {},
            'flood_risk_modification': {},
            'early_warning_effectiveness': {},
            'water_quality_impacts': {},
            'sedimentation_impacts': {}
        }
        
        # Process each major river system
        for river_name, river_data in self.river_systems.items():
            # Calculate upstream flow modification
            flow_modification = self._calculate_flow_modification(
                river_name, river_data, upstream_conditions, cooperation_level)
            
            transboundary_effects['river_flow_modification'][river_name] = flow_modification
            
            # Calculate flood risk modification
            flood_risk_mod = self._calculate_flood_risk_modification(
                river_name, river_data, upstream_conditions, flow_modification)
            
            transboundary_effects['flood_risk_modification'][river_name] = flood_risk_mod
            
            # Calculate warning system effectiveness
            warning_effectiveness = self._calculate_warning_effectiveness(
                river_name, river_data, upstream_conditions, cooperation_level)
            
            transboundary_effects['early_warning_effectiveness'][river_name] = warning_effectiveness
            
            # Calculate water quality impacts
            water_quality = self._calculate_water_quality_impacts(
                river_name, river_data, upstream_conditions)
            
            transboundary_effects['water_quality_impacts'][river_name] = water_quality
            
            # Calculate sedimentation impacts
            sedimentation = self._calculate_sedimentation_impacts(
                river_name, river_data, upstream_conditions)
            
            transboundary_effects['sedimentation_impacts'][river_name] = sedimentation
        
        # Calculate overall impact scores
        overall_impacts = self._calculate_overall_impacts(transboundary_effects)
        transboundary_effects['overall_impacts'] = overall_impacts
        
        return transboundary_effects
    
    def _calculate_flow_modification(self, river_name, river_data, upstream_conditions, cooperation_level):
        """Calculate how upstream activities modify river flow"""
        flow_modification = {
            'dry_season': 0.0,  # Negative values mean flow reduction
            'wet_season': 0.0,  # Positive values mean flow increase
            'variability_change': 0.0  # Change in flow variability
        }
        
        # Get upstream countries for this river
        upstream_countries = river_data['upstream_countries']
        
        for country in upstream_countries:
            # Get country control factor
            control_factor = self.upstream_countries[country]['control_factor']
            
            # Get country cooperation level
            country_cooperation = cooperation_level.get(country, 0.5)
            
            # Get country contribution to this river
            flow_contribution = river_data['flow_contribution'].get(country, 0)
            
            # Extract upstream conditions for this country
            country_conditions = upstream_conditions.get(country, {})
            
            # Water withdrawal factor (negative impact on flow)
            withdrawal = country_conditions.get('water_withdrawal_factor', 0.2)
            
            # Dam operation factor
            dam_operation = country_conditions.get('dam_operation', {})
            dry_season_release = dam_operation.get('dry_season_release', 0.5)
            wet_season_storage = dam_operation.get('wet_season_storage', 0.5)
            
            # Land use change impacts
            land_use = country_conditions.get('land_use_change', {})
            deforestation = land_use.get('deforestation_rate', 0.01)
            urbanization = land_use.get('urbanization_rate', 0.02)
            
            # Calculate dry season flow modification
            # Higher cooperation means better dry season releases
            dry_season_mod = (
                -withdrawal * control_factor * flow_contribution / 100 +  # Withdrawal reduces flow
                (dry_season_release - 0.5) * country_cooperation * control_factor * flow_contribution / 100  # Dam release can help
            )
            
            # Calculate wet season flow modification
            # Deforestation and urbanization increase wet season flows
            # Dam storage reduces peak flows
            wet_season_mod = (
                (deforestation * 2 + urbanization) * flow_contribution / 100 -  # Land use increases peaks
                wet_season_storage * control_factor * flow_contribution / 100  # Dams reduce peaks
            )
            
            # Calculate variability change
            # Dams generally reduce variability, deforestation increases it
            variability_mod = (
                deforestation * 0.1 * flow_contribution / 100 -  # Deforestation increases variability
                control_factor * 0.1 * flow_contribution / 100  # Dams decrease variability
            )
            
            # Add to overall modification
            flow_modification['dry_season'] += dry_season_mod
            flow_modification['wet_season'] += wet_season_mod
            flow_modification['variability_change'] += variability_mod
        
        # Cap modifications at reasonable levels
        flow_modification['dry_season'] = max(-0.8, min(0.2, flow_modification['dry_season']))
        flow_modification['wet_season'] = max(-0.3, min(0.5, flow_modification['wet_season']))
        flow_modification['variability_change'] = max(-0.3, min(0.3, flow_modification['variability_change']))
        
        return flow_modification
    
    def _calculate_flood_risk_modification(self, river_name, river_data, upstream_conditions, flow_modification):
        """Calculate how upstream activities modify flood risk"""
        # Flood risk modification depends primarily on wet season flow changes
        wet_season_change = flow_modification['wet_season']
        variability_change = flow_modification['variability_change']
        
        # Also affected by upstream land use changes
        land_use_impact = 0
        
        # Aggregate land use impacts across upstream countries
        for country in river_data['upstream_countries']:
            # Get country contribution to this river
            flow_contribution = river_data['flow_contribution'].get(country, 0)
            
            # Get upstream land use conditions
            country_conditions = upstream_conditions.get(country, {})
            land_use = country_conditions.get('land_use_change', {})
            
            deforestation = land_use.get('deforestation_rate', 0.01)
            urbanization = land_use.get('urbanization_rate', 0.02)
            
            # Calculate land use impact on flood risk
            country_land_impact = (
                deforestation * self.upstream_land_use_impacts['deforestation']['flood_impact'] +
                urbanization * self.upstream_land_use_impacts['urbanization']['flood_impact']
            ) * flow_contribution / 100
            
            land_use_impact += country_land_impact
        
        # Calculate flood risk modification
        flood_risk_mod = {
            'peak_flow_change': wet_season_change,
            'flood_frequency_change': wet_season_change * 0.7 + variability_change * 0.3 + land_use_impact,
            'flood_duration_change': wet_season_change * 0.5 + variability_change * 0.2
        }
        
        # Cap at reasonable levels
        for key in flood_risk_mod:
            flood_risk_mod[key] = max(-0.5, min(0.8, flood_risk_mod[key]))
            
        return flood_risk_mod
    
    def _calculate_warning_effectiveness(self, river_name, river_data, upstream_conditions, cooperation_level):
        """Calculate early warning effectiveness for transboundary floods"""
        warning_effectiveness = {
            'lead_time_hrs': 0,
            'accuracy': 0,
            'communication_effectiveness': 0
        }
        
        # Base lead time depends on flood propagation time from upstream
        base_lead_time = 0
        weighted_accuracy = 0
        total_weight = 0
        
        for country, prop_time in river_data.get('flood_propagation_time_days', {}).items():
            # Convert to hours
            lead_time_hrs = prop_time * 24
            
            # Weight by flow contribution
            country_weight = river_data['flow_contribution'].get(country, 0)
            
            # Apply weight to lead time
            base_lead_time += lead_time_hrs * country_weight / 100
            
            # Get country notification system quality
            notification_quality = self.upstream_countries[country].get('notification_system', 0.5)
            
            # Apply cooperation level to notification quality
            country_cooperation = cooperation_level.get(country, 0.5)
            effective_notification = notification_quality * country_cooperation
            
            # Add to weighted accuracy
            weighted_accuracy += effective_notification * country_weight
            total_weight += country_weight
        
        # Calculate final accuracy
        if total_weight > 0:
            warning_accuracy = weighted_accuracy / total_weight
        else:
            warning_accuracy = 0.5
            
        # Calculate communication effectiveness based on cooperation
        avg_cooperation = 0
        for country in river_data['upstream_countries']:
            avg_cooperation += cooperation_level.get(country, 0.5)
        
        if len(river_data['upstream_countries']) > 0:
            avg_cooperation /= len(river_data['upstream_countries'])
            communication_effectiveness = avg_cooperation * 0.8  # Max 0.8 effectiveness
        else:
            communication_effectiveness = 0.4  # Default
        
        # Set final values
        warning_effectiveness['lead_time_hrs'] = base_lead_time
        warning_effectiveness['accuracy'] = warning_accuracy
        warning_effectiveness['communication_effectiveness'] = communication_effectiveness
        
        return warning_effectiveness
    
    def _calculate_water_quality_impacts(self, river_name, river_data, upstream_conditions):
        """Calculate water quality impacts from upstream activities"""
        water_quality_impacts = {
            'pollution_level': 0,
            'nutrient_loading': 0,
            'industrial_contamination': 0,
            'overall_quality_change': 0
        }
        
        # Aggregate impacts across upstream countries
        for country in river_data['upstream_countries']:
            # Get country contribution to this river
            flow_contribution = river_data['flow_contribution'].get(country, 0)
            
            # Get upstream conditions
            country_conditions = upstream_conditions.get(country, {})
            pollution_sources = country_conditions.get('pollution_sources', {})
            
            # Extract pollution metrics
            urban_pollution = pollution_sources.get('urban_wastewater', 0.3)
            agricultural_pollution = pollution_sources.get('agricultural_runoff', 0.3)
            industrial_pollution = pollution_sources.get('industrial_discharge', 0.2)
            
            # Calculate impacts
            country_pollution = urban_pollution * 0.3 + industrial_pollution * 0.7
            country_nutrients = agricultural_pollution * 0.8 + urban_pollution * 0.2
            country_industrial = industrial_pollution
            
            # Weight by flow contribution
            water_quality_impacts['pollution_level'] += country_pollution * flow_contribution / 100
            water_quality_impacts['nutrient_loading'] += country_nutrients * flow_contribution / 100
            water_quality_impacts['industrial_contamination'] += country_industrial * flow_contribution / 100
        
        # Calculate overall quality change (negative value = deterioration)
        water_quality_impacts['overall_quality_change'] = -(
            water_quality_impacts['pollution_level'] * 0.3 +
            water_quality_impacts['nutrient_loading'] * 0.4 +
            water_quality_impacts['industrial_contamination'] * 0.3
        )
        
        # Cap at reasonable levels
        water_quality_impacts['overall_quality_change'] = max(-0.8, min(0.1, water_quality_impacts['overall_quality_change']))
        
        return water_quality_impacts
    
    def _calculate_sedimentation_impacts(self, river_name, river_data, upstream_conditions):
        """Calculate sedimentation impacts from upstream activities"""
        sedimentation_impacts = {
            'sediment_load_change': 0,
            'river_morphology_impact': 0,
            'delta_building_impact': 0
        }
        
        # Base sediment load rating
        if river_data.get('sediment_load') == 'very_high':
            base_load = 0.9
        elif river_data.get('sediment_load') == 'high':
            base_load = 0.7
        elif river_data.get('sediment_load') == 'medium':
            base_load = 0.5
        else:
            base_load = 0.3
            
        # Aggregate impacts across upstream countries
        for country in river_data['upstream_countries']:
            # Get country contribution to this river
            flow_contribution = river_data['flow_contribution'].get(country, 0)
            
            # Get upstream conditions
            country_conditions = upstream_conditions.get(country, {})
            land_use = country_conditions.get('land_use_change', {})
            
            # Extract land use changes
            deforestation = land_use.get('deforestation_rate', 0.01)
            agriculture_expansion = land_use.get('agricultural_expansion', 0.01)
            
            # Dam trapping effect (reduces sediment)
            dam_operation = country_conditions.get('dam_operation', {})
            dam_trapping = dam_operation.get('sediment_trapping', 0.3)
            
            # Calculate sediment load change
            # Deforestation and agriculture increase sediment, dams trap it
            country_sed_change = (
                deforestation * self.upstream_land_use_impacts['deforestation']['sedimentation_impact'] +
                agriculture_expansion * self.upstream_land_use_impacts['agricultural_intensification'].get('sedimentation_impact', 0.1) -
                dam_trapping * self.upstream_countries[country]['control_factor']
            ) * flow_contribution / 100
            
            sedimentation_impacts['sediment_load_change'] += country_sed_change
        
        # Calculate morphology and delta impacts based on sediment change
        sed_change = sedimentation_impacts['sediment_load_change']
        
        # River morphology impact (negative = erosion, positive = aggradation)
        sedimentation_impacts['river_morphology_impact'] = sed_change * 0.8
        
        # Delta building (negative = delta loss, positive = delta growth)
        sedimentation_impacts['delta_building_impact'] = sed_change * 1.2
        
        # Cap at reasonable levels
        for key in ['sediment_load_change', 'river_morphology_impact', 'delta_building_impact']:
            sedimentation_impacts[key] = max(-0.8, min(0.6, sedimentation_impacts[key]))
            
        return sedimentation_impacts
    
    def _calculate_overall_impacts(self, transboundary_effects):
        """Calculate overall transboundary impact scores"""
        overall_impacts = {
            'flood_hazard_modification': 0,
            'water_security_impact': 0,
            'environmental_impact': 0,
            'geomorphological_impact': 0
        }
        
        # Count number of rivers for averaging
        river_count = len(transboundary_effects['river_flow_modification'])
        if river_count == 0:
            return overall_impacts
            
        # Calculate flood hazard modification
        flood_impact = 0
        for river, flood_mod in transboundary_effects['flood_risk_modification'].items():
            flood_impact += flood_mod['flood_frequency_change']
        overall_impacts['flood_hazard_modification'] = flood_impact / river_count
        
        # Calculate water security impact
        water_security = 0
        for river, flow_mod in transboundary_effects['river_flow_modification'].items():
            # Dry season reduction affects water security
            water_security += flow_mod['dry_season'] * -2  # Negative impact
        # Also affected by water quality
        quality_impact = 0
        for river, quality_mod in transboundary_effects['water_quality_impacts'].items():
            quality_impact += quality_mod['overall_quality_change']
        water_security += quality_impact / river_count
        overall_impacts['water_security_impact'] = water_security / river_count
        
        # Calculate environmental impact
        environmental = 0
        for river, quality_mod in transboundary_effects['water_quality_impacts'].items():
            environmental += quality_mod['overall_quality_change'] * 0.7
        for river, flow_mod in transboundary_effects['river_flow_modification'].items():
            # Flow variability change affects ecosystems
            environmental += flow_mod['variability_change'] * -0.3  # Natural variability is good
        overall_impacts['environmental_impact'] = environmental / river_count
        
        # Calculate geomorphological impact
        geomorphological = 0
        for river, sed_mod in transboundary_effects['sedimentation_impacts'].items():
            geomorphological += sed_mod['delta_building_impact'] * 0.7
            geomorphological += sed_mod['river_morphology_impact'] * 0.3
        overall_impacts['geomorphological_impact'] = geomorphological / river_count
        
        return overall_impacts
