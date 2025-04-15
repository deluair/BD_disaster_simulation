"""
HazardModel class: Models individual disaster hazards with specific characteristics
"""

import numpy as np
import scipy.stats as stats

class HazardModel:
    """Model individual disaster hazards with specific characteristics"""
    def __init__(self, hazard_type, return_periods, intensity_scales,
                 spatial_patterns, seasonal_profile, climate_sensitivity):
        # Initialize hazard-specific parameters
        self.hazard_type = hazard_type
        self.return_periods = return_periods
        self.intensity_scales = intensity_scales
        self.spatial_patterns = spatial_patterns
        self.seasonal_profile = seasonal_profile
        self.climate_sensitivity = climate_sensitivity
        
        # Hazard-specific model configurations
        self.configs = {
            'flood': {
                'monsoon_timing': {'start_month': 6, 'end_month': 9},
                'flash_flood_regions': ['haor_basins', 'northeastern_hills'],
                'river_systems': ['brahmaputra_jamuna', 'ganges_padma', 'meghna'],
                'urban_drainage_efficiency': 0.6,  # efficiency factor for urban drainage
                'polder_drainage_capacity': 30  # mm/day drainage capacity
            },
            'cyclone': {
                'bay_genesis_probability': {
                    # Monthly cyclogenesis probability distribution
                    1: 0.02, 2: 0.03, 3: 0.07, 4: 0.09, 5: 0.14, 
                    6: 0.05, 7: 0.01, 8: 0.01, 9: 0.03, 10: 0.10,
                    11: 0.12, 12: 0.04
                },
                'surge_amplification_factor': 1.2,  # amplification due to coastal bathymetry
                'wind_decay_rate': 0.15,  # inland decay rate per km
                'track_probability': {
                    'west': 0.40,  # probability of westward track
                    'northwest': 0.35,  # probability of northwestward track
                    'north': 0.25  # probability of northward track
                }
            },
            'geophysical': {
                'fault_systems': {
                    'dauki': {'slip_rate': 2.3, 'max_magnitude': 7.8},
                    'madhupur': {'slip_rate': 0.8, 'max_magnitude': 6.5}
                },
                'liquefaction_susceptibility': {
                    'very_high': ['delta_sediments', 'coastal_lowlands'],
                    'high': ['river_floodplains', 'reclaimed_areas'],
                    'moderate': ['alluvial_fans', 'piedmont_areas'],
                    'low': ['tertiary_hills', 'uplifted_terraces']
                },
                'landslide_thresholds': {
                    'chittagong_hills': {'rainfall_24hr': 200, 'slope_threshold': 25}
                },
                'erosion_rates': {
                    'jamuna': 70,  # meters/year max
                    'padma': 45,   # meters/year max
                    'meghna': 30   # meters/year max
                }
            }
        }
        
    def generate_events(self, year, climate_effects=None):
        """Generate hazard events based on return periods and seasonal patterns
        
        Args:
            year: Simulation year
            climate_effects: Climate change effects to apply
            
        Returns:
            List of hazard events with characteristics
        """
        events = []
        
        # Apply climate effects if provided
        intensity_multiplier = 1.0
        frequency_multiplier = 1.0
        if climate_effects:
            intensity_multiplier += climate_effects.get('intensity_change', 0)
            frequency_multiplier += climate_effects.get('frequency_change', 0)
        
        # Generate events based on return periods and random sampling
        for return_period in self.return_periods:
            # Annual exceedance probability = 1/return_period
            annual_prob = 1.0 / return_period * frequency_multiplier
            
            # Simulate occurrence based on probability
            if stats.uniform.rvs() < annual_prob:
                # Sample month based on seasonal profile
                month = self._sample_month_from_profile()
                
                # Generate intensity based on return period
                base_intensity = self._intensity_from_return_period(return_period)
                adjusted_intensity = base_intensity * intensity_multiplier
                
                # Create event with spatial footprint
                event = {
                    'type': self.hazard_type,
                    'year': year,
                    'month': month,
                    'return_period': return_period,
                    'intensity': adjusted_intensity,
                    'spatial_footprint': self._generate_spatial_footprint(adjusted_intensity)
                }
                
                # Add hazard-specific attributes
                self._add_hazard_specific_attributes(event)
                
                events.append(event)
        
        return events
    
    def _sample_month_from_profile(self):
        """Sample a month based on the seasonal profile"""
        if self.hazard_type == 'flood':
            if self.seasonal_profile == 'monsoon':
                # Higher probability during monsoon months (June-September)
                probabilities = [0.01, 0.01, 0.02, 0.05, 0.10, 0.20, 0.25, 0.20, 0.10, 0.04, 0.01, 0.01]
            else:
                # Uniform distribution for other flood types
                probabilities = [1/12] * 12
        elif self.hazard_type == 'cyclone':
            # Bi-modal distribution with peaks in pre and post monsoon
            probabilities = [0.02, 0.03, 0.07, 0.09, 0.14, 0.05, 0.01, 0.01, 0.03, 0.10, 0.12, 0.04]
        else:
            # Default uniform distribution
            probabilities = [1/12] * 12
            
        # Sample month (1-12) based on probabilities
        return stats.rv_discrete(values=(range(1, 13), probabilities)).rvs()
    
    def _intensity_from_return_period(self, return_period):
        """Calculate hazard intensity based on return period"""
        # Use logarithmic relationship between return period and intensity
        # I = a * ln(RP) + b where a,b are hazard-specific
        if self.hazard_type == 'flood':
            a, b = 0.8, 1.0  # Coefficients for flood depth
            return a * np.log(return_period) + b
        elif self.hazard_type == 'cyclone':
            a, b = 15, 120  # Coefficients for wind speed
            return a * np.log(return_period) + b
        else:
            # Default relationship
            a, b = 0.5, 1.0
            return a * np.log(return_period) + b
    
    def _generate_spatial_footprint(self, intensity):
        """Generate spatial footprint for the hazard event"""
        # Placeholder for spatial footprint generation
        # In a full implementation, this would generate a GeoDataFrame or raster
        if self.spatial_patterns == 'riverine':
            return {'type': 'riverine', 'affected_rivers': ['brahmaputra', 'ganges', 'meghna']}
        elif self.spatial_patterns == 'coastal':
            return {'type': 'coastal', 'affected_coast': ['chittagong', 'khulna', 'barisal']}
        else:
            return {'type': 'generic', 'coverage': 'national'}
    
    def _add_hazard_specific_attributes(self, event):
        """Add hazard-specific attributes to the event"""
        if self.hazard_type == 'flood':
            event['flood_type'] = 'riverine' if event['month'] in [6, 7, 8, 9] else 'flash'
            event['duration'] = stats.gamma.rvs(5, scale=3) if event['flood_type'] == 'riverine' else stats.gamma.rvs(2, scale=1)
            event['depth'] = event['intensity']  # Intensity is depth for floods
            
        elif self.hazard_type == 'cyclone':
            event['wind_speed'] = event['intensity']  # Intensity is wind speed for cyclones
            event['storm_surge'] = 0.05 * event['wind_speed'] * self.configs['cyclone']['surge_amplification_factor']
            event['track_direction'] = self._sample_from_dict(self.configs['cyclone']['track_probability'])
            event['rainfall_intensity'] = 10 * np.log(event['wind_speed']) - 40  # mm/hr
            event['duration'] = stats.gamma.rvs(2, scale=12)  # Hours
            
        elif self.hazard_type == 'geophysical':
            if event['type'] == 'earthquake':
                event['magnitude'] = event['intensity']
                event['depth'] = stats.gamma.rvs(2, scale=10)  # km
                event['fault'] = 'dauki' if stats.uniform.rvs() < 0.6 else 'madhupur'
            elif event['type'] == 'landslide':
                event['volume'] = stats.lognorm.rvs(s=1.5, scale=1000)  # cubic meters
                event['slope'] = stats.uniform.rvs(low=25, high=60)  # degrees
                
    def _sample_from_dict(self, probability_dict):
        """Sample a key from a dictionary of probabilities"""
        keys = list(probability_dict.keys())
        probabilities = list(probability_dict.values())
        return keys[stats.rv_discrete(values=(range(len(keys)), probabilities)).rvs()]
