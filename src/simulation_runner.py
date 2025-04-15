"""
SimulationRunner: Core simulation engine for Bangladesh Disaster Risk Simulation Framework
"""

import os
import sys
import time
import numpy as np
import pandas as pd
from datetime import datetime
import logging
from pathlib import Path

# Import all models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.models.hazard_model import HazardModel
from src.models.exposure_model import ExposureModel
from src.models.vulnerability_model import VulnerabilityModel
from src.models.climate_change_model import ClimateChangeModel
from src.models.early_warning_model import EarlyWarningModel
from src.models.emergency_response_model import EmergencyResponseModel
from src.models.recovery_model import RecoveryModel
from src.models.transboundary_model import TransboundaryModel
from src.models.resilience_model import ResilienceModel
from src.models.governance_model import GovernanceModel
from src.models.socioeconomic_model import SocioeconomicModel
from src.models.technology_model import TechnologyModel

class SimulationRunner:
    """Core simulation engine for Bangladesh Disaster Risk Simulation Framework"""
    
    def __init__(self, config=None):
        """Initialize the simulation framework
        
        Args:
            config: Configuration dictionary or path to config file
        """
        # Setup logging
        self._setup_logging()
        
        # Load configuration
        self.config = self._load_configuration(config)
        
        # Initialize simulation parameters
        self.start_year = self.config.get('simulation', {}).get('start_year', 2025)
        self.end_year = self.config.get('simulation', {}).get('end_year', 2050)
        self.time_step = self.config.get('simulation', {}).get('time_step', 1)  # Years
        self.scenarios = self.config.get('simulation', {}).get('scenarios', ['baseline', 'rcp45', 'rcp85'])
        
        # Initialize spatial parameters
        self.regions = self.config.get('spatial', {}).get('regions', ['national'])
        self.admin_level = self.config.get('spatial', {}).get('admin_level', 'division')
        
        # Initialize model components
        self._initialize_models()
        
        # Initialize results storage
        self.results = {}
        for scenario in self.scenarios:
            self.results[scenario] = {}
            for region in self.regions:
                self.results[scenario][region] = {
                    'hazards': {},
                    'exposures': {},
                    'impacts': {},
                    'response': {},
                    'recovery': {},
                    'adaptation': {},
                    'metrics': {}
                }
                
        self.logger.info(f"Simulation initialized: {self.start_year}-{self.end_year}, {len(self.scenarios)} scenarios")
        
    def _setup_logging(self):
        """Setup logging for the simulation"""
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = log_dir / f'simulation_{timestamp}.log'
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger('bd_disaster_simulation')
    
    def _load_configuration(self, config):
        """Load configuration from file or dictionary"""
        default_config = {
            'simulation': {
                'start_year': 2025,
                'end_year': 2050,
                'time_step': 1,
                'scenarios': ['baseline', 'rcp45', 'rcp85'],
                'random_seed': 42,
                'monte_carlo_runs': 1
            },
            'spatial': {
                'regions': ['national'],
                'admin_level': 'division',
                'resolution': 'medium'
            },
            'hazards': {
                'types': ['flood', 'cyclone', 'drought'],
                'thresholds': {
                    'flood': 0.5,
                    'cyclone': 0.4,
                    'drought': 0.6
                }
            },
            'climate': {
                'baseline_period': '1986-2015',
                'projection_method': 'delta',
                'scenarios': {
                    'baseline': {'temp_change': 0, 'precip_change': 0},
                    'rcp45': {'temp_change': 1.5, 'precip_change': 0.05},
                    'rcp85': {'temp_change': 3.0, 'precip_change': 0.1}
                }
            },
            'models': {
                'hazard': {'enabled': True, 'parameters': {}},
                'exposure': {'enabled': True, 'parameters': {}},
                'vulnerability': {'enabled': True, 'parameters': {}},
                'climate_change': {'enabled': True, 'parameters': {}},
                'early_warning': {'enabled': True, 'parameters': {}},
                'emergency_response': {'enabled': True, 'parameters': {}},
                'recovery': {'enabled': True, 'parameters': {}},
                'transboundary': {'enabled': True, 'parameters': {}},
                'resilience': {'enabled': True, 'parameters': {}},
                'governance': {'enabled': True, 'parameters': {}},
                'socioeconomic': {'enabled': True, 'parameters': {}},
                'technology': {'enabled': True, 'parameters': {}}
            },
            'output': {
                'formats': ['csv', 'json'],
                'metrics': ['aal', 'vulnerability_index', 'resilience_score'],
                'visualization': True
            }
        }
        
        if config is None:
            return default_config
        
        if isinstance(config, str):
            # Load from file
            import json
            try:
                with open(config, 'r') as f:
                    user_config = json.load(f)
            except Exception as e:
                self.logger.error(f"Error loading configuration file: {e}")
                return default_config
        else:
            # Use provided dictionary
            user_config = config
            
        # Merge configurations (simple update, not deep merge)
        for key, value in user_config.items():
            if key in default_config:
                if isinstance(value, dict) and isinstance(default_config[key], dict):
                    default_config[key].update(value)
                else:
                    default_config[key] = value
            else:
                default_config[key] = value
                
        return default_config
        
    def _initialize_models(self):
        """Initialize all model components"""
        self.models = {}
        
        # Initialize models based on configuration
        try:
            # Try creating models that have _initialize_parameters methods
            if self.config['models']['hazard']['enabled']:
                # Check if the model has _initialize_parameters method
                model = HazardModel()
                self.models['hazard'] = model
                self.logger.info("Initialized HazardModel")
                
            if self.config['models']['exposure']['enabled']:
                model = ExposureModel()
                self.models['exposure'] = model
                self.logger.info("Initialized ExposureModel")
                
            if self.config['models']['vulnerability']['enabled']:
                model = VulnerabilityModel()
                self.models['vulnerability'] = model
                self.logger.info("Initialized VulnerabilityModel")
                
            if self.config['models']['climate_change']['enabled']:
                model = ClimateChangeModel()
                self.models['climate_change'] = model
                self.logger.info("Initialized ClimateChangeModel")
                
            if self.config['models']['early_warning']['enabled']:
                model = EarlyWarningModel()
                self.models['early_warning'] = model
                self.logger.info("Initialized EarlyWarningModel")
                
            if self.config['models']['emergency_response']['enabled']:
                model = EmergencyResponseModel()
                self.models['emergency_response'] = model
                self.logger.info("Initialized EmergencyResponseModel")
                
            if self.config['models']['recovery']['enabled']:
                model = RecoveryModel()
                self.models['recovery'] = model
                self.logger.info("Initialized RecoveryModel")
                
            if self.config['models']['transboundary']['enabled']:
                model = TransboundaryModel()
                self.models['transboundary'] = model
                self.logger.info("Initialized TransboundaryModel")
                
            if self.config['models']['resilience']['enabled']:
                model = ResilienceModel()
                self.models['resilience'] = model
                self.logger.info("Initialized ResilienceModel")
                
            if self.config['models']['governance']['enabled']:
                model = GovernanceModel()
                self.models['governance'] = model
                self.logger.info("Initialized GovernanceModel")
                
            if self.config['models']['socioeconomic']['enabled']:
                model = SocioeconomicModel()
                self.models['socioeconomic'] = model
                self.logger.info("Initialized SocioeconomicModel")
                
            if self.config['models']['technology']['enabled']:
                model = TechnologyModel()
                self.models['technology'] = model
                self.logger.info("Initialized TechnologyModel")
                
        except TypeError as e:
            self.logger.error(f"Error initializing models: {e}")
            self.logger.info("Creating simplified model stubs for demonstration purposes")
            
            # Create simplified versions of the models for demonstration
            self.models = {
                'hazard': self._create_hazard_model_stub(),
                'exposure': self._create_exposure_model_stub(),
                'vulnerability': self._create_vulnerability_model_stub(),
                'climate_change': self._create_climate_change_model_stub(),
                'early_warning': self._create_early_warning_model_stub(),
                'emergency_response': self._create_emergency_response_model_stub(),
                'recovery': self._create_recovery_model_stub(),
                'resilience': self._create_resilience_model_stub(),
                'governance': self._create_governance_model_stub(),
                'socioeconomic': self._create_socioeconomic_model_stub(),
                'technology': self._create_technology_model_stub(),
                'transboundary': self._create_transboundary_model_stub()
            }
            
            self.logger.info("Created model stubs for simulation demonstration")
            
    def _create_hazard_model_stub(self):
        """Create a simplified HazardModel stub"""
        return type('HazardModelStub', (), {
            'generate_events': lambda self, region, year, climate_factors, region_params, upstream_conditions=None: {
                'flood': {'magnitude': np.random.random() * climate_factors['precipitation_factor'], 'affected_area_sqkm': region_params['area_sqkm'] * 0.2},
                'cyclone': {'magnitude': np.random.random() * climate_factors['temperature_factor'], 'affected_area_sqkm': region_params['area_sqkm'] * 0.1},
                'drought': {'magnitude': np.random.random() * climate_factors['temperature_factor'], 'affected_area_sqkm': region_params['area_sqkm'] * 0.3}
            },
            'initialize_scenario': lambda self, scenario_name, temp_change, precip_change, baseline_period: {
                'temperature_factor': 1.0 + temp_change / 10,
                'precipitation_factor': 1.0 + precip_change,
                'sea_level_rise_m': temp_change * 0.1,
                'scenario_name': scenario_name
            }
        })()
        
    def _create_exposure_model_stub(self):
        """Create a simplified ExposureModel stub"""
        return type('ExposureModelStub', (), {
            'get_exposed_elements': lambda self, hazards, region, region_type, population, socioeconomic_factors: {
                hazard_type: {
                    'population_exposed': int(population * hazard['magnitude'] * hazard['affected_area_sqkm'] / 1000),
                    'buildings_exposed': int(population * 0.25 * hazard['magnitude']),
                    'infrastructure_exposed': {
                        'roads_km': 100 * hazard['magnitude'],
                        'bridges': int(10 * hazard['magnitude']),
                        'critical_facilities': int(5 * hazard['magnitude'])
                    },
                    'economic_exposed': population * 0.002 * hazard['magnitude'] * 1000000  # USD
                } for hazard_type, hazard in hazards.items()
            }
        })()
        
    def _create_vulnerability_model_stub(self):
        """Create a simplified VulnerabilityModel stub"""
        return type('VulnerabilityModelStub', (), {
            'calculate_damages': lambda self, hazards, exposures, region_type, socioeconomic_factors, resilience_scores: {
                hazard_type: {
                    'casualties': int(exposure['population_exposed'] * hazards[hazard_type]['magnitude'] * 0.01),
                    'displaced': int(exposure['population_exposed'] * hazards[hazard_type]['magnitude'] * 0.2),
                    'buildings_damaged': int(exposure['buildings_exposed'] * hazards[hazard_type]['magnitude']),
                    'infrastructure_damaged': {
                        'roads_km': exposure['infrastructure_exposed']['roads_km'] * hazards[hazard_type]['magnitude'],
                        'bridges': int(exposure['infrastructure_exposed']['bridges'] * hazards[hazard_type]['magnitude']),
                        'critical_facilities': int(exposure['infrastructure_exposed']['critical_facilities'] * hazards[hazard_type]['magnitude'])
                    },
                    'economic_losses': exposure['economic_exposed'] * hazards[hazard_type]['magnitude'] * (1 - resilience_scores.get('overall_resilience', 0.5))
                } for hazard_type, exposure in exposures.items() if hazard_type in hazards
            }
        })()
        
    def _create_climate_change_model_stub(self):
        """Create a simplified ClimateChangeModel stub"""
        return type('ClimateChangeModelStub', (), {
            'initialize_scenario': lambda self, scenario_name, temp_change, precip_change, baseline_period: {
                'temperature_factor': 1.0 + temp_change / 10,
                'precipitation_factor': 1.0 + precip_change,
                'sea_level_rise_m': temp_change * 0.1,
                'scenario_name': scenario_name
            },
            'project_climate_factors': lambda self, base_factors, time_period: {
                'temperature_factor': base_factors['temperature_factor'] * (1 + 0.002 * time_period),
                'precipitation_factor': base_factors['precipitation_factor'] * (1 + 0.003 * time_period),
                'sea_level_rise_m': base_factors.get('sea_level_rise_m', 0) + 0.004 * time_period,
                'scenario_name': base_factors.get('scenario_name', 'baseline')
            }
        })()
        
    def _create_early_warning_model_stub(self):
        """Create a simplified EarlyWarningModel stub"""
        return type('EarlyWarningModelStub', (), {
            'simulate_warning_process': lambda self, hazards, region, region_type, governance_effectiveness: {
                'warning_lead_time': 24 * governance_effectiveness,  # hours
                'warning_coverage': 0.7 * governance_effectiveness,
                'warning_response_rate': 0.5 * governance_effectiveness,
                'lives_saved': sum([
                    int(hazard.get('magnitude', 0.5) * 100 * governance_effectiveness)
                    for hazard in hazards.values()
                ])
            }
        })()
        
    def _create_emergency_response_model_stub(self):
        """Create a simplified EmergencyResponseModel stub"""
        return type('EmergencyResponseModelStub', (), {
            'simulate_response': lambda self, hazards, exposures, governance_effectiveness, region, region_type: {
                'search_rescue_effectiveness': 0.6 * governance_effectiveness,
                'relief_effectiveness': 0.5 * governance_effectiveness,
                'evacuation_effectiveness': 0.6 * governance_effectiveness,
                'additional_lives_saved': int(sum([
                    exposure.get('population_exposed', 0) * 0.01 * governance_effectiveness
                    for exposure in exposures.values()
                ]))
            }
        })()
        
    def _create_recovery_model_stub(self):
        """Create a simplified RecoveryModel stub"""
        return type('RecoveryModelStub', (), {
            'simulate_recovery': lambda self, disaster_impacts, governance_quality, funding_availability: {
                'recovery_horizon_months': {
                    'housing': 24,
                    'infrastructure': 36,
                    'livelihoods': 18,
                    'social': 30
                },
                'recovery_quality': {
                    'housing': 0.7 * float(governance_quality.get('coordination', 0.5)),
                    'infrastructure': 0.6 * float(governance_quality.get('coordination', 0.5)),
                    'livelihoods': 0.8 * float(governance_quality.get('coordination', 0.5)),
                    'social': 0.7 * float(governance_quality.get('coordination', 0.5))
                },
                'bbb_improvement': 0.1 * (1 - float(governance_quality.get('corruption_level', 0.5))),
                'funding_ratio': float(funding_availability.get('total_funding', 0)) / (float(disaster_impacts.get('economic', {}).get('direct_losses', 1000000)) + 1)
            }
        })()
        
    def _create_resilience_model_stub(self):
        """Create a simplified ResilienceModel stub"""
        return type('ResilienceModelStub', (), {
            'calculate_resilience': lambda self, region_type, socioeconomic_profile, governance_quality, hazard_type: {
                'infrastructure_resilience': 0.4 + (socioeconomic_profile.get('development_level', 0.5) * 0.2),
                'social_resilience': 0.5 - (socioeconomic_profile.get('poverty_rate', 0.3) * 0.5),
                'economic_resilience': 0.4 + (socioeconomic_profile.get('education_level', 0.6) * 0.2),
                'ecosystem_resilience': 0.3 + (governance_quality.get('policy_implementation', 0.5) * 0.2),
                'institutional_resilience': 0.4 + (governance_quality.get('coordination', 0.5) * 0.2),
                'overall_resilience': 0.45 + ((1 - governance_quality.get('corruption_level', 0.5)) * 0.1),
                'hazard_specific_resilience': 0.4 if hazard_type == 'flood' else (0.5 if hazard_type == 'cyclone' else 0.3)
            }
        })()
        
    def _create_governance_model_stub(self):
        """Create a simplified GovernanceModel stub"""
        return type('GovernanceModelStub', (), {
            'simulate_governance': lambda self, region, time_period, disaster_phase, external_factors=None: {
                'coordination_effectiveness': 0.5 + (0.01 * time_period),
                'policy_effectiveness': 0.45 + (0.005 * time_period),
                'resource_effectiveness': 0.5 + (0.01 * time_period),
                'governance_quality': {
                    'transparency': 0.4 + (0.005 * time_period),
                    'accountability': 0.4 + (0.005 * time_period),
                    'participation': 0.5 + (0.005 * time_period),
                    'corruption_level': max(0.2, 0.6 - (0.005 * time_period))
                },
                'overall_effectiveness': 0.45 + (0.01 * time_period),
                'phase_effectiveness': 0.6 if disaster_phase == 'response' else 0.5
            }
        })()
        
    def _create_socioeconomic_model_stub(self):
        """Create a simplified SocioeconomicModel stub"""
        return type('SocioeconomicModelStub', (), {
            'simulate_socioeconomic_vulnerability': lambda self, region_type, time_period, hazard_type: {
                'economic_vulnerability': 0.6 - (0.005 * time_period),
                'social_vulnerability': 0.7 - (0.005 * time_period),
                'physical_vulnerability': 0.65 - (0.01 * time_period),
                'final_vulnerability_score': max(0.3, 0.65 - (0.008 * time_period)),
                'evolved_profile': {
                    'poverty_rate': max(0.05, 0.25 - (0.005 * time_period)),
                    'service_access': min(0.95, 0.6 + (0.01 * time_period)),
                    'education_level': min(0.9, 0.65 + (0.01 * time_period)),
                    'health_access': min(0.9, 0.6 + (0.01 * time_period)),
                    'employment_stability': min(0.9, 0.55 + (0.01 * time_period))
                }
            }
        })()
        
    def _create_technology_model_stub(self):
        """Create a simplified TechnologyModel stub"""
        return type('TechnologyModelStub', (), {
            'simulate_technology_adoption': lambda self, region_type, time_period, hazard_type, socioeconomic_profile: {
                'early_warning': {
                    'adoption': min(0.9, 0.5 + (0.02 * time_period)),
                    'effectiveness': min(0.9, 0.6 + (0.01 * time_period)),
                    'effective_adoption': min(0.8, 0.4 + (0.015 * time_period))
                },
                'resilient_infrastructure': {
                    'adoption': min(0.8, 0.3 + (0.02 * time_period)),
                    'effectiveness': min(0.85, 0.55 + (0.015 * time_period)),
                    'effective_adoption': min(0.7, 0.25 + (0.015 * time_period))
                },
                'overall_effectiveness': min(0.8, 0.4 + (0.02 * time_period))
            }
        })()
        
    def _create_transboundary_model_stub(self):
        """Create a simplified TransboundaryModel stub"""
        return type('TransboundaryModelStub', (), {
            'simulate_transboundary_effects': lambda self, upstream_conditions, cooperation_level: {
                'river_flow_modification': {
                    'ganges': {'dry_season': -0.2, 'wet_season': 0.1},
                    'brahmaputra': {'dry_season': -0.1, 'wet_season': 0.2}
                },
                'flood_risk_modification': {
                    'ganges': {'peak_flow_change': 0.1, 'flood_frequency_change': 0.2},
                    'brahmaputra': {'peak_flow_change': 0.2, 'flood_frequency_change': 0.15}
                },
                'overall_impacts': {
                    'flood_hazard_modification': 0.15,
                    'water_security_impact': -0.1,
                    'environmental_impact': -0.05
                }
            }
        })()
        
    def run_simulation(self, scenarios=None, regions=None):
        """Run the full simulation across scenarios and regions
        
        Args:
            scenarios (list): List of climate scenarios to simulate
            regions (list): List of regions to simulate
            
        Returns:
            dict: Simulation results organized by scenario and region
        """
        self.logger.info(f"Starting simulation run from {self.start_year} to {self.end_year}")
        
        # Use default scenarios if none provided
        if scenarios is None:
            scenarios = self.config['simulation']['scenarios']
        
        # Use default regions if none provided
        if regions is None:
            regions = self.config['simulation']['regions']
            
        # Initialize results structure
        self.results = {}
        
        # Run simulation for each scenario
        for scenario in scenarios:
            self.results[scenario] = {}
            
            # Initialize climate scenario
            climate_baseline = self._initialize_climate_scenario(scenario)
            
            # Simulate for each region
            for region in regions:
                self.logger.info(f"Running simulation for scenario {scenario}, region {region}")
                
                # Initialize region parameters
                region_params = self._initialize_region_parameters(region)
                
                # Run time-series simulation
                region_results = self._run_time_series(scenario, region, climate_baseline, region_params)
                
                # Store results
                self.results[scenario][region] = region_results
        
        self.logger.info("Simulation completed successfully")
        return self.results
        
    def _initialize_climate_scenario(self, scenario):
        """Initialize climate factors for a specific scenario"""
        # Get climate scenario parameters
        if scenario in self.config['climate']['scenarios']:
            climate_config = self.config['climate']['scenarios'][scenario]
        else:
            # Default to baseline if scenario not found
            climate_config = self.config['climate']['scenarios']['baseline']
            
        # Simple default climate factors
        climate_factors = {
            'temperature_factor': 1.0 + climate_config.get('temp_change', 0) / 10,
            'precipitation_factor': 1.0 + climate_config.get('precip_change', 0),
            'sea_level_rise_m': climate_config.get('slr', 0),
            'scenario_name': scenario
        }
            
        return climate_factors

    def _initialize_region_parameters(self, region):
        """Initialize parameters specific to a region"""
        # Default regional parameters
        region_params = {
            'name': region,
            'population': 1000000,
            'area_sqkm': 1000,
            'region_type': 'rural',
            'hazard_exposure': {
                'flood': 0.7,
                'cyclone': 0.5,
                'drought': 0.3
            }
        }
        
        return region_params
    
    def _run_time_series(self, scenario, region, climate_baseline, region_params):
        """Run time-series simulation for a region"""
        # Initialize results tracking
        region_results = {}
        region_results['metrics'] = {}
        
        # Run for each year in the simulation
        for year in range(self.start_year, self.end_year + 1):
            self.logger.info(f"Simulating {scenario} - {region} - Year {year}")
            
            # Generate sample data for demonstration
            year_data = self._generate_sample_data(scenario, region, year)
            
            # Store results for this year
            metrics = region_results['metrics']
            metrics['resilience_improvement'] = metrics.get('resilience_improvement', 0) + year_data.get('adaptation', {}).get('resilience_improvement', 0)
            region_results[year] = year_data
        
        # Calculate summary metrics for the region
        region_results['metrics'] = self._calculate_metrics(scenario, region)
        
        return region_results
    
    def _calculate_metrics(self, scenario, region):
        """Calculate summary metrics for scenario and region"""
        import random
        
        # Get yearly data
        yearly_data = {}
        for year in range(self.start_year, self.end_year + 1):
            if year in self.results[scenario][region]:
                yearly_data[year] = self.results[scenario][region][year]
        
        if not yearly_data:
            return {}
            
        # Calculate metrics from yearly data
        total_casualties = sum(data.get('impacts', {}).get('casualties', 0) for data in yearly_data.values())
        total_displaced = sum(data.get('impacts', {}).get('displaced', 0) for data in yearly_data.values())
        total_economic_loss = sum(data.get('impacts', {}).get('economic_loss', 0) for data in yearly_data.values())
        total_adaptation_investment = sum(data.get('adaptation', {}).get('adaptation_investment', 0) for data in yearly_data.values())
            avoided_losses = metrics['vulnerability_reduction'] * metrics['average_annual_loss'] * years * 0.2
            metrics['benefit_cost_ratio'] = avoided_losses / total_adaptation_investment
        
        # Store metrics
        self.results[scenario][region]['metrics'] = metrics

    def export_results(self, output_dir=None, formats=None):
        """Export simulation results to files
        
        Args:
            output_dir: Directory to save results (default: results/)
            formats: List of formats to export (default: config formats)
        """
        if output_dir is None:
            output_dir = 'results'
        
        if formats is None:
            formats = self.config['output'].get('formats', ['csv'])
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True, parents=True)
        
        # Timestamp for filenames
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Use the Report Generator for exporting results
        from report_generator import ReportGenerator
        report_gen = ReportGenerator()
        
        # Export results based on requested formats
        for format_type in formats:
            if format_type.lower() == 'csv':
                report_gen.generate_csv_report(self.results, output_path, timestamp)
            elif format_type.lower() == 'json':
                report_gen.generate_json_reports(self.results, output_path, timestamp)
            elif format_type.lower() == 'html':
                report_gen.generate_html_report(self.results, output_path, timestamp)
        
        # Always generate HTML report for better visualization
        if 'html' not in [f.lower() for f in formats]:
            report_gen.generate_html_report(self.results, output_path, timestamp)
            
        self.logger.info(f"Results exported to {output_path}")

    def _export_csv(self, output_path, timestamp):
        """Export results to CSV files"""
        # Create a metrics DataFrame
        metrics_data = []
        
        for scenario in self.results:
            for region in self.results[scenario]:
                if 'metrics' in self.results[scenario][region]:
                    metrics = self.results[scenario][region]['metrics']
                    row = {
                        'scenario': scenario,
                        'region': region
                    }
                    row.update(metrics)
                    metrics_data.append(row)
        
        # Export metrics to CSV
        if metrics_data:
            metrics_df = pd.DataFrame(metrics_data)
            metrics_file = output_path / f'metrics_{timestamp}.csv'
            metrics_df.to_csv(metrics_file, index=False)
            self.logger.info(f"Exported metrics to {metrics_file}")
        
        # Export yearly data for each scenario and region
        for scenario in self.results:
            for region in self.results[scenario]:
                yearly_data = {}
                
                # Collect yearly data
                for year, data in self.results[scenario][region].items():
                    if isinstance(year, int):  # Only process year entries
                        # Extract key data points
                        impacts = {}
                        for hazard_type, impact in data.get('impacts', {}).items():
                            impacts[f'{hazard_type}_economic_losses'] = impact.get('economic_losses', 0)
                            impacts[f'{hazard_type}_casualties'] = impact.get('casualties', 0)
                            impacts[f'{hazard_type}_displaced'] = impact.get('displaced', 0)
                        
                        # Create yearly row
                        row = {
                            'year': year,
                            'vulnerability': data.get('state', {}).get('vulnerability', {}).get('overall_vulnerability', 0),
                            'resilience': data.get('state', {}).get('resilience', {}).get('overall_resilience', 0),
                            'adaptation_investment': data.get('adaptation', {}).get('adaptation_investment', 0)
                        }
                        row.update(impacts)
                        yearly_data[year] = row
                
                # Create DataFrame and export
                if yearly_data:
                    yearly_df = pd.DataFrame(list(yearly_data.values()))
                    yearly_file = output_path / f'{scenario}_{region}_yearly_{timestamp}.csv'
                    yearly_df.to_csv(yearly_file, index=False)
                    self.logger.info(f"Exported yearly data for {scenario}-{region} to {yearly_file}")

    def _export_json(self, output_path, timestamp):
        """Export results to JSON files"""
        import json
        
        # Export summary metrics
        metrics_data = {}
        for scenario in self.results:
            metrics_data[scenario] = {}
            for region in self.results[scenario]:
                if 'metrics' in self.results[scenario][region]:
                    metrics_data[scenario][region] = self.results[scenario][region]['metrics']
        
        if metrics_data:
            metrics_file = output_path / f'metrics_{timestamp}.json'
            with open(metrics_file, 'w') as f:
                json.dump(metrics_data, f, indent=2)
            self.logger.info(f"Exported metrics to {metrics_file}")
        
        # Export full results (excluding large data structures)
        full_results = {}
        for scenario in self.results:
            full_results[scenario] = {}
            for region in self.results[scenario]:
                full_results[scenario][region] = {}
                
                # Add metrics
                if 'metrics' in self.results[scenario][region]:
                    full_results[scenario][region]['metrics'] = self.results[scenario][region]['metrics']
                
                # Add yearly summary data
                yearly_summary = {}
                for year, data in self.results[scenario][region].items():
                    if isinstance(year, int):  # Only process year entries
                        # Create a simplified summary
                        yearly_summary[year] = {
                            'vulnerability': data.get('state', {}).get('vulnerability', {}).get('overall_vulnerability', 0),
                            'resilience': data.get('state', {}).get('resilience', {}).get('overall_resilience', 0),
                            'adaptation_investment': data.get('adaptation', {}).get('adaptation_investment', 0),
                            'accumulated_impacts': data.get('state', {}).get('accumulated_impacts', {})
                        }
                
                if yearly_summary:
                    full_results[scenario][region]['yearly_summary'] = yearly_summary
        
        full_results_file = output_path / f'simulation_results_{timestamp}.json'
        with open(full_results_file, 'w') as f:
            json.dump(full_results, f, indent=2)
        self.logger.info(f"Exported full results to {full_results_file}")
        
        return full_results
        
    def _export_html(self, output_path, timestamp):
        """Export results to an interactive HTML report"""
        # Get full results in JSON format
        full_results = self._export_json(output_path, timestamp)
        
        # Create HTML report filename
        report_file = output_path / f'report_{timestamp}.html'
        
        # Create a simple HTML report for now (avoiding JavaScript template conflicts)
        import json
        
        # Convert results to a pretty JSON string
        results_json = json.dumps(full_results, indent=4)
        
        # Create a simple HTML report with the results embedded
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Bangladesh Disaster Risk Simulation Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
                h1 {{ color: #3498db; }}
                pre {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto; }}
                .header {{ background-color: #3498db; color: white; padding: 20px; text-align: center; margin-bottom: 20px; }}
                .footer {{ text-align: center; margin-top: 30px; padding: 20px; background: #f8f9fa; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Bangladesh Disaster Risk Simulation Report</h1>
                <p>Generated on {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}</p>
            </div>
            
            <h2>Simulation Results</h2>
            <p>Below are the results of the Bangladesh Disaster Risk Simulation:</p>
            
            <pre>{results_json}</pre>
            
            <div class="footer">
                <p>Bangladesh Disaster Risk Simulation Framework</p>
                <p>© 2025 University of Tennessee</p>
            </div>
        </body>
        </html>
        """
        
        # Write the HTML file
        with open(report_file, 'w') as f:
            f.write(html)
            
        self.logger.info(f"Exported HTML report to {report_file}")
        
    def _generate_html_report(self, results, timestamp):
        """Generate HTML report content"""
        # Convert results to JSON string for JavaScript
        import json
        results_json = json.dumps(results)
        
        # Create HTML template
        html = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Bangladesh Disaster Risk Simulation Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; line-height: 1.6; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                h1, h2, h3, h4 {{ color: #2c3e50; }}
                .header {{ background-color: #3498db; color: white; padding: 20px; text-align: center; margin-bottom: 20px; }}
                .section {{ margin-bottom: 30px; background: #f9f9f9; padding: 20px; border-radius: 5px; }}
                .footer {{ text-align: center; margin-top: 30px; padding: 20px; background: #f9f9f9; }}
                table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #f2f2f2; }}
                tr:hover {{ background-color: #f5f5f5; }}
                .dashboard {{ display: flex; flex-wrap: wrap; gap: 20px; margin-bottom: 20px; }}
                .metric-card {{ background: white; padding: 15px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); flex: 1; min-width: 200px; }}
                .metric-value {{ font-size: 24px; font-weight: bold; margin: 10px 0; }}
                .chart-container {{ background: white; padding: 15px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 20px; }}
                .tabs {{ display: flex; margin-bottom: 20px; }}
                .tab {{ padding: 10px 20px; cursor: pointer; background: #f1f1f1; border: none; }}
                .tab.active {{ background: #3498db; color: white; }}
                .tab-content {{ display: none; }}
                .tab-content.active {{ display: block; }}
                .scenario-selector, .region-selector {{ margin-bottom: 20px; }}
                select {{ padding: 8px; width: 200px; }}
            </style>
            <!-- Include Chart.js -->
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body>
            <div class="header">
                <h1>Bangladesh Disaster Risk Simulation Report</h1>
                <p>Generated on {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}</p>
            </div>
            
            <div class="container">
                <div class="section">
                    <h2>Simulation Overview</h2>
                    <p>This report presents the results of a multi-dimensional disaster risk simulation for Bangladesh from 2025-2050.</p>
                    <p>The simulation integrates hydrometeorological hazards, climate change impacts, and infrastructure vulnerabilities to provide insights for disaster risk management and resilience planning.</p>
                    
                    <div class="scenario-selector">
                        <label for="scenario-select">Select Climate Scenario:</label>
                        <select id="scenario-select" onchange="updateView()"></select>
                    </div>
                    
                    <div class="region-selector">
                        <label for="region-select">Select Region:</label>
                        <select id="region-select" onchange="updateView()"></select>
                    </div>
                </div>
                
                <div class="tabs">
                    <button class="tab active" onclick="openTab(event, 'dashboard')">Dashboard</button>
                    <button class="tab" onclick="openTab(event, 'trends')">Trends</button>
                    <button class="tab" onclick="openTab(event, 'metrics')">Detailed Metrics</button>
                    <button class="tab" onclick="openTab(event, 'data')">Raw Data</button>
                </div>
                
                <div id="dashboard" class="tab-content active">
                    <div class="section">
                        <h2>Key Performance Indicators</h2>
                        <div class="dashboard" id="kpi-dashboard">
                            <!-- KPIs will be inserted here -->
                        </div>
                    </div>
                    
                    <div class="section">
                        <h2>Vulnerability & Resilience</h2>
                        <div class="chart-container">
                            <canvas id="vuln-resilience-chart"></canvas>
                        </div>
                    </div>
                </div>
                
                <div id="trends" class="tab-content">
                    <div class="section">
                        <h2>Vulnerability Trends</h2>
                        <div class="chart-container">
                            <canvas id="vulnerability-chart"></canvas>
                        </div>
                    </div>
                    
                    <div class="section">
                        <h2>Resilience Trends</h2>
                        <div class="chart-container">
                            <canvas id="resilience-chart"></canvas>
                        </div>
                    </div>
                    
                    <div class="section">
                        <h2>Adaptation Investment Trends</h2>
                        <div class="chart-container">
                            <canvas id="adaptation-chart"></canvas>
                        </div>
                    </div>
                </div>
                
                <div id="metrics" class="tab-content">
                    <div class="section">
                        <h2>Detailed Metrics</h2>
                        <table id="metrics-table">
                            <thead>
                                <tr>
                                    <th>Metric</th>
                                    <th>Value</th>
                                </tr>
                            </thead>
                            <tbody>
                                <!-- Metrics will be inserted here -->
                            </tbody>
                        </table>
                    </div>
                </div>
                
                <div id="data" class="tab-content">
                    <div class="section">
                        <h2>Raw Simulation Data</h2>
                        <pre id="raw-data"></pre>
                    </div>
                </div>
            </div>
            
            <div class="footer">
                <p>Bangladesh Disaster Risk Simulation Framework</p>
                <p>© 2025 University of Tennessee</p>
            </div>
            
            <script>
                // Store the simulation results
                const simulationResults = {results_json};
                
                // Initialize the page
                document.addEventListener('DOMContentLoaded', function() {{                    
                    // Set up scenario selector
                    const scenarioSelect = document.getElementById('scenario-select');
                    for (const scenario in simulationResults) {{                        
                        const option = document.createElement('option');
                        option.value = scenario;
                        option.textContent = scenario.charAt(0).toUpperCase() + scenario.slice(1);
                        scenarioSelect.appendChild(option);
                    }}
                    
                    // Get first scenario
                    const firstScenario = Object.keys(simulationResults)[0];
                    
                    // Set up region selector
                    const regionSelect = document.getElementById('region-select');
                    if (firstScenario) {{                        
                        for (const region in simulationResults[firstScenario]) {{                            
                            const option = document.createElement('option');
                            option.value = region;
                            option.textContent = region.charAt(0).toUpperCase() + region.slice(1);
                            regionSelect.appendChild(option);
                        }}
                    }}
                    
                    // Update the view
                    updateView();
                }});
                
                // Function to open tabs
                function openTab(evt, tabName) {{                    
                    // Hide all tab content
                    const tabcontent = document.getElementsByClassName("tab-content");
                    for (let i = 0; i < tabcontent.length; i++) {{                        
                        tabcontent[i].classList.remove("active");
                    }}
                    
                    // Remove active class from all tabs
                    const tabs = document.getElementsByClassName("tab");
                    for (let i = 0; i < tabs.length; i++) {{                        
                        tabs[i].classList.remove("active");
                    }}
                    
                    // Show the selected tab content
                    document.getElementById(tabName).classList.add("active");
                    
                    // Add active class to the clicked tab
                    evt.currentTarget.classList.add("active");
                }}
                
                // Function to update the view based on selected scenario and region
                function updateView() {{                    
                    const scenario = document.getElementById('scenario-select').value;
                    const region = document.getElementById('region-select').value;
                    
                    if (!scenario || !region || !simulationResults[scenario] || !simulationResults[scenario][region]) {{                        
                        return;
                    }}
                    
                    // Get the data for selected scenario and region
                    const data = simulationResults[scenario][region];
                    
                    // Update KPI dashboard
                    updateKPIDashboard(data);
                    
                    // Update charts
                    updateCharts(data);
                    
                    // Update metrics table
                    updateMetricsTable(data);
                    
                    // Update raw data
                    document.getElementById('raw-data').textContent = JSON.stringify(data, null, 2);
                }}
                
                // Function to update KPI dashboard
                function updateKPIDashboard(data) {{                    
                    const kpiDashboard = document.getElementById('kpi-dashboard');
                    kpiDashboard.innerHTML = '';
                    
                    // Create KPI cards
                    if (data.metrics) {{                        
                        const metrics = data.metrics;
                        
                        // Average Annual Loss
                        const aalCard = document.createElement('div');
                        aalCard.className = 'metric-card';
                        aalCard.innerHTML = `
                            <h3>Average Annual Loss</h3>
                            <div class="metric-value">${'$'}{Math.round(metrics.average_annual_loss / 1000000).toLocaleString()}M</div>
                            <p>USD per year</p>
                        `;
                        kpiDashboard.appendChild(aalCard);
                        
                        // Total Casualties
                        const casualtiesCard = document.createElement('div');
                        casualtiesCard.className = 'metric-card';
                        casualtiesCard.innerHTML = `
                            <h3>Total Casualties</h3>
                            <div class="metric-value">{'$'}{Math.round(metrics.total_casualties).toLocaleString()}</div>
                            <p>Persons</p>
                        `;
                        kpiDashboard.appendChild(casualtiesCard);
                        
                        // Total Displaced
                        const displacedCard = document.createElement('div');
                        displacedCard.className = 'metric-card';
                        displacedCard.innerHTML = `
                            <h3>Total Displaced</h3>
                            <div class="metric-value">{'$'}{Math.round(metrics.total_displaced).toLocaleString()}</div>
                            <p>Persons</p>
                        `;
                        kpiDashboard.appendChild(displacedCard);
                        
                        // Vulnerability Reduction
                        const vulnCard = document.createElement('div');
                        vulnCard.className = 'metric-card';
                        vulnCard.innerHTML = `
                            <h3>Vulnerability Reduction</h3>
                            <div class="metric-value">{'$'}{(metrics.vulnerability_reduction * 100).toFixed(1)}%</div>
                            <p>Over simulation period</p>
                        `;
                        kpiDashboard.appendChild(vulnCard);
                        
                        // Benefit-Cost Ratio
                        const bcrCard = document.createElement('div');
                        bcrCard.className = 'metric-card';
                        bcrCard.innerHTML = `
                            <h3>Benefit-Cost Ratio</h3>
                            <div class="metric-value">{'$'}{metrics.benefit_cost_ratio.toFixed(2)}</div>
                            <p>Return on adaptation investment</p>
                        `;
                        kpiDashboard.appendChild(bcrCard);
                    }}
                }}
                
                // Function to update charts
                function updateCharts(data) {{                    
                    // Get yearly data
                    const yearlyData = data.yearly_summary || {{}};
                    const years = Object.keys(yearlyData).sort();
                    
                    // Prepare datasets
                    const vulnerabilityData = [];
                    const resilienceData = [];
                    const adaptationData = [];
                    
                    years.forEach(year => {{                        
                        vulnerabilityData.push(yearlyData[year].vulnerability);
                        resilienceData.push(yearlyData[year].resilience);
                        adaptationData.push(yearlyData[year].adaptation_investment / 1000000); // Convert to millions
                    }});
                    
                    // Create vulnerability and resilience chart
                    const vulnResChart = document.getElementById('vuln-resilience-chart');
                    if (vulnResChart.chart) {{                        
                        vulnResChart.chart.destroy();
                    }}
                    
                    vulnResChart.chart = new Chart(vulnResChart, {{                        
                        type: 'line',
                        data: {{                            
                            labels: years,
                            datasets: [
                                {{                                    
                                    label: 'Vulnerability',
                                    data: vulnerabilityData,
                                    borderColor: 'rgba(255, 99, 132, 1)',
                                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                                    tension: 0.1
                                }},
                                {{                                    
                                    label: 'Resilience',
                                    data: resilienceData,
                                    borderColor: 'rgba(54, 162, 235, 1)',
                                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                                    tension: 0.1
                                }}
                            ]
                        }},
                        options: {{                            
                            responsive: true,
                            scales: {{                                
                                y: {{                                    
                                    min: 0,
                                    max: 1,
                                    title: {{                                        
                                        display: true,
                                        text: 'Score (0-1)'
                                    }}
                                }}
                            }},
                            plugins: {{                                
                                title: {{                                    
                                    display: true,
                                    text: 'Vulnerability and Resilience Over Time'
                                }}
                            }}
                        }}
                    }});
                    
                    // Create vulnerability chart
                    const vulnChart = document.getElementById('vulnerability-chart');
                    if (vulnChart.chart) {{                        
                        vulnChart.chart.destroy();
                    }}
                    
                    vulnChart.chart = new Chart(vulnChart, {{                        
                        type: 'line',
                        data: {{                            
                            labels: years,
                            datasets: [{{                                
                                label: 'Vulnerability',
                                data: vulnerabilityData,
                                borderColor: 'rgba(255, 99, 132, 1)',
                                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                                tension: 0.1
                            }}]
                        }},
                        options: {{                            
                            responsive: true,
                            scales: {{                                
                                y: {{                                    
                                    min: 0,
                                    max: 1,
                                    title: {{                                        
                                        display: true,
                                        text: 'Vulnerability Score (0-1)'
                                    }}
                                }}
                            }},
                            plugins: {{                                
                                title: {{                                    
                                    display: true,
                                    text: 'Vulnerability Trend'
                                }}
                            }}
                        }}
                    }});
                    
                    // Create resilience chart
                    const resChart = document.getElementById('resilience-chart');
                    if (resChart.chart) {{                        
                        resChart.chart.destroy();
                    }}
                    
                    resChart.chart = new Chart(resChart, {{                        
                        type: 'line',
                        data: {{                            
                            labels: years,
                            datasets: [{{                                
                                label: 'Resilience',
                                data: resilienceData,
                                borderColor: 'rgba(54, 162, 235, 1)',
                                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                                tension: 0.1
                            }}]
                        }},
                        options: {{                            
                            responsive: true,
                            scales: {{                                
                                y: {{                                    
                                    min: 0,
                                    max: 1,
                                    title: {{                                        
                                        display: true,
                                        text: 'Resilience Score (0-1)'
                                    }}
                                }}
                            }},
                            plugins: {{                                
                                title: {{                                    
                                    display: true,
                                    text: 'Resilience Trend'
                                }}
                            }}
                        }}
                    }});
                    
                    // Create adaptation chart
                    const adaptChart = document.getElementById('adaptation-chart');
                    if (adaptChart.chart) {{                        
                        adaptChart.chart.destroy();
                    }}
                    
                    adaptChart.chart = new Chart(adaptChart, {{                        
                        type: 'bar',
                        data: {{                            
                            labels: years,
                            datasets: [{{                                
                                label: 'Adaptation Investment',
                                data: adaptationData,
                                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                                borderColor: 'rgba(75, 192, 192, 1)',
                                borderWidth: 1
                            }}]
                        }},
                        options: {{                            
                            responsive: true,
                            scales: {{                                
                                y: {{                                    
                                    title: {{                                        
                                        display: true,
                                        text: 'Investment (Million USD)'
                                    }}
                                }}
                            }},
                            plugins: {{                                
                                title: {{                                    
                                    display: true,
                                    text: 'Adaptation Investment by Year'
                                }}
                            }}
                        }}
                    }});
                }}
                
                // Function to update metrics table
                function updateMetricsTable(data) {{                    
                    const metricsTable = document.getElementById('metrics-table').getElementsByTagName('tbody')[0];
                    metricsTable.innerHTML = '';
                    
                    if (data.metrics) {{                        
                        const metrics = data.metrics;
                        
                        for (const [key, value] of Object.entries(metrics)) {{                            
                            const row = metricsTable.insertRow();
                            
                            // Format metric name
                            const metricName = key.replace(/_/g, ' ').replace(/\b[a-z]/g, l => l.toUpperCase());
                            
                            // Format metric value
                            let formattedValue = value;
                            if (key.includes('cost') || key.includes('loss')) {{                                
                                formattedValue = `$${Math.round(value / 1000000).toLocaleString()}M USD`;
                            }} else if (key.includes('ratio') || key.includes('reduction')) {{                                
                                formattedValue = value.toFixed(2);
                            }} else if (Number.isInteger(value)) {{                                
                                formattedValue = value.toLocaleString();
                            }} else if (typeof value === 'number') {{                                
                                formattedValue = value.toFixed(2);
                            }}
                            
                            row.insertCell(0).textContent = metricName;
                            row.insertCell(1).textContent = formattedValue;
                        }}
                    }}
                }}
            </script>
        </body>
        </html>
        '''
        
        return html


# Main execution when run directly
if __name__ == "__main__":
    import argparse
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Bangladesh Disaster Risk Simulation Framework')
    parser.add_argument('--config', type=str, help='Path to configuration file')
    parser.add_argument('--years', type=int, default=25, help='Number of years to simulate')
    parser.add_argument('--scenarios', type=str, nargs='+', default=['baseline', 'rcp45', 'rcp85'], 
                     help='Climate scenarios to simulate')
    parser.add_argument('--regions', type=str, nargs='+', default=['national'], 
                     help='Regions to simulate')
    parser.add_argument('--output', default='results', help='Output directory for results')
    parser.add_argument('--formats', default='json', help='Comma-separated list of output formats (json,csv,html)')
    
    args = parser.parse_args()
    
    # Initialize simulation
    config = None
    if args.config:
        config = args.config
    
    # Create and run simulation
    simulation = SimulationRunner(config=args.config)
    
    # Override configuration with command-line arguments if provided
    simulation.end_year = simulation.start_year + args.years - 1
    
    # Run simulation
    print(f"Running Bangladesh Disaster Risk Simulation for {args.years} years")
    print(f"Climate scenarios: {args.scenarios}")
    print(f"Regions: {args.regions}")
    print(f"Output directory: {args.output}")
    # Run simulation
    results = simulation.run_simulation(scenarios=args.scenarios, regions=args.regions)
    
    # Parse formats
    formats = args.formats.split(',')
    
    # Export results
    simulation.export_results(output_dir=args.output, formats=formats)
    
    print("\nSimulation completed successfully!")
    print(f"Results exported to: {args.output}/")