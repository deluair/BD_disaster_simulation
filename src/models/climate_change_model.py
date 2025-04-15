"""
ClimateChangeModel: Models climate change impacts on disaster profiles for Bangladesh
"""

class ClimateChangeModel:
    """Model climate change impacts on disaster profiles"""
    def __init__(self):
        # Initialize climate change scenarios and impact parameters
        self._initialize_climate_scenarios()
        
    def _initialize_climate_scenarios(self):
        """Initialize climate change scenarios based on IPCC projections"""
        # Base year for projections
        self.base_year = 2025
        
        # Define climate change scenarios (based on IPCC AR6)
        self.scenarios = {
            # Intermediate-low emissions scenario
            'RCP4.5': {
                'temperature_increase': {
                    # Yearly temperature increase in °C by decade
                    2030: 0.8,
                    2040: 1.1,
                    2050: 1.4
                },
                'precipitation_change': {
                    # Seasonal precipitation change factors by decade
                    # Values: [pre-monsoon, monsoon, post-monsoon, winter]
                    2030: [0.05, 0.08, 0.04, -0.02],
                    2040: [0.08, 0.12, 0.06, -0.03],
                    2050: [0.10, 0.15, 0.08, -0.05]
                },
                'sea_level_rise': {
                    # Sea level rise in meters by decade
                    2030: 0.12,
                    2040: 0.22,
                    2050: 0.32
                },
                'cyclone_intensity_factor': {
                    # Cyclone intensity increase factor by decade
                    2030: 0.05,
                    2040: 0.08,
                    2050: 0.12
                },
                'drought_frequency_factor': {
                    # Drought frequency increase factor by decade
                    2030: 0.10,
                    2040: 0.15,
                    2050: 0.20
                },
                'extreme_rainfall_factor': {
                    # Extreme rainfall intensity increase factor by decade
                    2030: 0.07,
                    2040: 0.12,
                    2050: 0.18
                }
            },
            # High emissions scenario
            'RCP8.5': {
                'temperature_increase': {
                    # Yearly temperature increase in °C by decade
                    2030: 1.0,
                    2040: 1.6,
                    2050: 2.2
                },
                'precipitation_change': {
                    # Seasonal precipitation change factors by decade
                    # Values: [pre-monsoon, monsoon, post-monsoon, winter]
                    2030: [0.07, 0.11, 0.06, -0.04],
                    2040: [0.12, 0.18, 0.09, -0.08],
                    2050: [0.18, 0.25, 0.12, -0.12]
                },
                'sea_level_rise': {
                    # Sea level rise in meters by decade
                    2030: 0.15,
                    2040: 0.30,
                    2050: 0.45
                },
                'cyclone_intensity_factor': {
                    # Cyclone intensity increase factor by decade
                    2030: 0.08,
                    2040: 0.15,
                    2050: 0.25
                },
                'drought_frequency_factor': {
                    # Drought frequency increase factor by decade
                    2030: 0.15,
                    2040: 0.25,
                    2050: 0.35
                },
                'extreme_rainfall_factor': {
                    # Extreme rainfall intensity increase factor by decade
                    2030: 0.10,
                    2040: 0.20,
                    2050: 0.30
                }
            },
            # Very low emissions scenario
            'RCP2.6': {
                'temperature_increase': {
                    # Yearly temperature increase in °C by decade
                    2030: 0.6,
                    2040: 0.8,
                    2050: 0.9
                },
                'precipitation_change': {
                    # Seasonal precipitation change factors by decade
                    # Values: [pre-monsoon, monsoon, post-monsoon, winter]
                    2030: [0.03, 0.05, 0.02, -0.01],
                    2040: [0.05, 0.07, 0.03, -0.02],
                    2050: [0.06, 0.08, 0.04, -0.02]
                },
                'sea_level_rise': {
                    # Sea level rise in meters by decade
                    2030: 0.10,
                    2040: 0.18,
                    2050: 0.24
                },
                'cyclone_intensity_factor': {
                    # Cyclone intensity increase factor by decade
                    2030: 0.03,
                    2040: 0.05,
                    2050: 0.07
                },
                'drought_frequency_factor': {
                    # Drought frequency increase factor by decade
                    2030: 0.05,
                    2040: 0.08,
                    2050: 0.10
                },
                'extreme_rainfall_factor': {
                    # Extreme rainfall intensity increase factor by decade
                    2030: 0.05,
                    2040: 0.07,
                    2050: 0.09
                }
            }
        }
        
        # Regional vulnerability to climate change impacts
        # Higher values indicate greater sensitivity to climate impacts
        self.regional_sensitivity = {
            'coastal': {
                'sea_level_rise': 1.0,
                'cyclone': 1.0,
                'salinity': 1.0,
                'flood': 0.7,
                'drought': 0.5
            },
            'floodplain': {
                'sea_level_rise': 0.3,
                'cyclone': 0.6,
                'salinity': 0.5,
                'flood': 1.0,
                'drought': 0.7
            },
            'haor_basin': {
                'sea_level_rise': 0.1,
                'cyclone': 0.4,
                'salinity': 0.2,
                'flood': 0.9,
                'drought': 0.5
            },
            'barind_tract': {
                'sea_level_rise': 0.0,
                'cyclone': 0.2,
                'salinity': 0.1,
                'flood': 0.3,
                'drought': 1.0
            },
            'hill_tracts': {
                'sea_level_rise': 0.0,
                'cyclone': 0.3,
                'salinity': 0.0,
                'flood': 0.4,
                'drought': 0.7
            },
            'urban': {
                'sea_level_rise': 0.5,  # For coastal cities
                'cyclone': 0.7,
                'salinity': 0.3,
                'flood': 0.8,  # Urban flooding is significant
                'drought': 0.6
            }
        }
        
    def apply_climate_scenarios(self, year, scenario, region, hazard_type):
        """Apply climate change scenarios to hazard properties
        
        Args:
            year: Simulation year
            scenario: Climate scenario (RCP2.6, RCP4.5, RCP8.5)
            region: Geographic region in Bangladesh
            hazard_type: Type of hazard to modify
            
        Returns:
            Dictionary of climate change effects to apply to hazard
        """
        # Find applicable decade for climate projections
        if year <= 2030:
            decade = 2030
        elif year <= 2040:
            decade = 2040
        else:
            decade = 2050
        
        # Climate effects based on scenario and hazard type
        effects = {}
        
        if scenario not in self.scenarios:
            # Default to RCP4.5 if scenario not recognized
            scenario = 'RCP4.5'
        
        # Get regional sensitivity factor if region is known
        region_factors = self.regional_sensitivity.get(region, self.regional_sensitivity['floodplain'])
        
        if hazard_type == 'flood':
            # Flood intensity affected by precipitation changes and sea level rise
            monsoon_change = self.scenarios[scenario]['precipitation_change'][decade][1]  # Monsoon season
            slr = self.scenarios[scenario]['sea_level_rise'][decade]
            
            # Regional sensitivity to floods
            flood_sensitivity = region_factors.get('flood', 0.5)
            
            # Combined effect on flood depth and frequency
            effects['intensity_change'] = monsoon_change * flood_sensitivity
            if region == 'coastal':
                # Sea level rise adds to coastal flood depths
                effects['intensity_change'] += slr * 0.5
            
            # Extreme rainfall affects flood frequency
            effects['frequency_change'] = self.scenarios[scenario]['extreme_rainfall_factor'][decade] * flood_sensitivity
            
            # Duration changes
            effects['duration_change'] = monsoon_change * 0.3  # Duration increases with precipitation
            
        elif hazard_type == 'cyclone':
            # Cyclone intensity affected by sea surface temperature (linked to global warming)
            temp_increase = self.scenarios[scenario]['temperature_increase'][decade]
            
            # Regional sensitivity to cyclones
            cyclone_sensitivity = region_factors.get('cyclone', 0.5)
            
            # Effect on wind speed and storm surge
            cyclone_intensity_factor = self.scenarios[scenario]['cyclone_intensity_factor'][decade]
            effects['intensity_change'] = cyclone_intensity_factor * cyclone_sensitivity
            
            # Cyclone frequency is complex - some research suggests fewer but more intense cyclones
            # Using a simplified approach here
            effects['frequency_change'] = cyclone_intensity_factor * 0.5 * cyclone_sensitivity
            
            # Storm surge amplified by sea level rise
            if region == 'coastal':
                slr = self.scenarios[scenario]['sea_level_rise'][decade]
                effects['surge_amplification'] = slr * 1.5  # Surge height increases more than SLR
            
        elif hazard_type == 'drought':
            # Drought affected by temperature and precipitation changes
            temp_increase = self.scenarios[scenario]['temperature_increase'][decade]
            winter_precip_change = self.scenarios[scenario]['precipitation_change'][decade][3]  # Winter season
            
            # Regional sensitivity to drought
            drought_sensitivity = region_factors.get('drought', 0.5)
            
            # Combined effect on drought severity and frequency
            # Temperature increases drought stress
            effects['intensity_change'] = temp_increase * 0.2 * drought_sensitivity
            
            # Decreased winter precipitation increases drought risk
            if winter_precip_change < 0:
                effects['intensity_change'] -= winter_precip_change * drought_sensitivity
                
            # Drought frequency affected by climate change
            effects['frequency_change'] = self.scenarios[scenario]['drought_frequency_factor'][decade] * drought_sensitivity
        
        elif hazard_type == 'landslide':
            # Landslides affected by extreme rainfall
            extreme_rainfall_factor = self.scenarios[scenario]['extreme_rainfall_factor'][decade]
            
            # Only significant in hill regions
            if region == 'hill_tracts':
                effects['intensity_change'] = extreme_rainfall_factor * 0.8
                effects['frequency_change'] = extreme_rainfall_factor * 1.2
            else:
                effects['intensity_change'] = 0
                effects['frequency_change'] = 0
                
        elif hazard_type == 'salinity':
            # Salinity affected by sea level rise and precipitation
            slr = self.scenarios[scenario]['sea_level_rise'][decade]
            
            # Regional sensitivity to salinity
            salinity_sensitivity = region_factors.get('salinity', 0.5)
            
            # Mainly affects coastal and some floodplain regions
            if region in ['coastal', 'floodplain']:
                effects['intensity_change'] = slr * 0.7 * salinity_sensitivity
                effects['inland_intrusion_km'] = slr * 5  # 5km additional intrusion per meter SLR
            else:
                effects['intensity_change'] = 0
                effects['inland_intrusion_km'] = 0
        
        elif hazard_type == 'erosion':
            # River erosion affected by flood intensity and precipitation
            monsoon_change = self.scenarios[scenario]['precipitation_change'][decade][1]  # Monsoon season
            extreme_rainfall_factor = self.scenarios[scenario]['extreme_rainfall_factor'][decade]
            
            # Affects floodplain and coastal regions
            if region in ['floodplain', 'coastal', 'haor_basin']:
                effects['intensity_change'] = (monsoon_change + extreme_rainfall_factor) * 0.5
                effects['frequency_change'] = extreme_rainfall_factor * 0.3
            else:
                effects['intensity_change'] = 0
                effects['frequency_change'] = 0
        
        else:
            # Generic effects for other hazards
            temp_increase = self.scenarios[scenario]['temperature_increase'][decade]
            effects['intensity_change'] = temp_increase * 0.1
            effects['frequency_change'] = temp_increase * 0.05
        
        return effects
    
    def get_annual_climate_parameters(self, year, scenario):
        """Get climate parameters for a specific year
        
        Args:
            year: Simulation year
            scenario: Climate scenario (RCP2.6, RCP4.5, RCP8.5)
            
        Returns:
            Dictionary of climate parameters for the year
        """
        # Find applicable decade for climate projections
        if year <= 2030:
            decade = 2030
            years_from_decade_start = year - 2025
            interpolation_factor = years_from_decade_start / 5  # Interpolate within 5-year period
        elif year <= 2040:
            decade = 2040
            prev_decade = 2030
            interpolation_factor = (year - 2030) / 10  # Interpolate between decades
        else:
            decade = 2050
            prev_decade = 2040
            interpolation_factor = (year - 2040) / 10  # Interpolate between decades
        
        if scenario not in self.scenarios:
            # Default to RCP4.5 if scenario not recognized
            scenario = 'RCP4.5'
        
        parameters = {}
        
        # Temperature
        if decade == 2030:
            # Interpolate from base year (2025)
            base_temp_increase = 0
            decade_temp_increase = self.scenarios[scenario]['temperature_increase'][decade]
            parameters['temperature_increase'] = base_temp_increase + (decade_temp_increase - base_temp_increase) * interpolation_factor
        else:
            # Interpolate between decades
            prev_temp_increase = self.scenarios[scenario]['temperature_increase'][prev_decade]
            decade_temp_increase = self.scenarios[scenario]['temperature_increase'][decade]
            parameters['temperature_increase'] = prev_temp_increase + (decade_temp_increase - prev_temp_increase) * interpolation_factor
        
        # Sea level rise (similar interpolation)
        if decade == 2030:
            base_slr = 0
            decade_slr = self.scenarios[scenario]['sea_level_rise'][decade]
            parameters['sea_level_rise'] = base_slr + (decade_slr - base_slr) * interpolation_factor
        else:
            prev_slr = self.scenarios[scenario]['sea_level_rise'][prev_decade]
            decade_slr = self.scenarios[scenario]['sea_level_rise'][decade]
            parameters['sea_level_rise'] = prev_slr + (decade_slr - prev_slr) * interpolation_factor
        
        # Precipitation changes - seasonal
        if decade == 2030:
            base_precip = [0, 0, 0, 0]  # No change in base year
            decade_precip = self.scenarios[scenario]['precipitation_change'][decade]
            parameters['precipitation_change'] = [base + (decade - base) * interpolation_factor 
                                                for base, decade in zip(base_precip, decade_precip)]
        else:
            prev_precip = self.scenarios[scenario]['precipitation_change'][prev_decade]
            decade_precip = self.scenarios[scenario]['precipitation_change'][decade]
            parameters['precipitation_change'] = [prev + (decade - prev) * interpolation_factor 
                                                for prev, decade in zip(prev_precip, decade_precip)]
        
        # Cyclone intensity factor
        if decade == 2030:
            base_cyclone = 0
            decade_cyclone = self.scenarios[scenario]['cyclone_intensity_factor'][decade]
            parameters['cyclone_intensity_factor'] = base_cyclone + (decade_cyclone - base_cyclone) * interpolation_factor
        else:
            prev_cyclone = self.scenarios[scenario]['cyclone_intensity_factor'][prev_decade]
            decade_cyclone = self.scenarios[scenario]['cyclone_intensity_factor'][decade]
            parameters['cyclone_intensity_factor'] = prev_cyclone + (decade_cyclone - prev_cyclone) * interpolation_factor
        
        # Drought frequency factor
        if decade == 2030:
            base_drought = 0
            decade_drought = self.scenarios[scenario]['drought_frequency_factor'][decade]
            parameters['drought_frequency_factor'] = base_drought + (decade_drought - base_drought) * interpolation_factor
        else:
            prev_drought = self.scenarios[scenario]['drought_frequency_factor'][prev_decade]
            decade_drought = self.scenarios[scenario]['drought_frequency_factor'][decade]
            parameters['drought_frequency_factor'] = prev_drought + (decade_drought - prev_drought) * interpolation_factor
        
        # Extreme rainfall factor
        if decade == 2030:
            base_extreme = 0
            decade_extreme = self.scenarios[scenario]['extreme_rainfall_factor'][decade]
            parameters['extreme_rainfall_factor'] = base_extreme + (decade_extreme - base_extreme) * interpolation_factor
        else:
            prev_extreme = self.scenarios[scenario]['extreme_rainfall_factor'][prev_decade]
            decade_extreme = self.scenarios[scenario]['extreme_rainfall_factor'][decade]
            parameters['extreme_rainfall_factor'] = prev_extreme + (decade_extreme - prev_extreme) * interpolation_factor
        
        return parameters
