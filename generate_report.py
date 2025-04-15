#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Bangladesh Disaster Risk Simulation - Report Generator Script
Generate HTML reports from simulation results or sample data
"""

import json
import argparse
import logging
from pathlib import Path
from datetime import datetime
from src.report_generator import ReportGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('bd_disaster_simulation')

def generate_sample_data():
    """Generate sample data for demonstration"""
    import random
    import math
    
    # Sample data structure
    results = {'baseline': {'national': {}}}
    region_data = results['baseline']['national']
    
    # Generate yearly data
    start_year = 2025
    num_years = 6
    
    # Initialize metrics
    total_casualties = 0
    total_displaced = 0
    total_economic_loss = 0
    total_adaptation_investment = 0
    
    for year_idx in range(num_years):
        year = start_year + year_idx
        
        # Generate evolving vulnerability and resilience scores
        vulnerability = max(0.1, 0.65 - year_idx * 0.04)
        resilience = min(0.9, 0.35 + year_idx * 0.04)
        
        # Generate hazard intensities
        flood_intensity = random.uniform(0.3, 0.8) * (1 - year_idx * 0.03)
        cyclone_intensity = max(0, random.gauss(0.4, 0.2)) * (1 - year_idx * 0.02)
        drought_intensity = max(0, 0.3 + math.sin(year_idx) * 0.2)
        
        # Calculate impacts
        casualties = int(random.uniform(30, 80) * vulnerability * max(flood_intensity, cyclone_intensity))
        displaced = int(random.uniform(1000, 5000) * vulnerability * max(flood_intensity, cyclone_intensity, drought_intensity))
        economic_loss = random.uniform(15, 65) * vulnerability * (flood_intensity + cyclone_intensity + drought_intensity) * 1000000
        
        # Calculate adaptation investment (increases over time)
        adaptation_investment = random.uniform(10, 25) * (1 + year_idx * 0.1) * 1000000
        
        # Update totals
        total_casualties += casualties
        total_displaced += displaced
        total_economic_loss += economic_loss
        total_adaptation_investment += adaptation_investment
        
        # Store yearly data
        region_data[year] = {
            'state': {
                'vulnerability': {
                    'overall_vulnerability': vulnerability,
                    'social_vulnerability': vulnerability * random.uniform(0.9, 1.1),
                    'economic_vulnerability': vulnerability * random.uniform(0.9, 1.1),
                    'infrastructure_vulnerability': vulnerability * random.uniform(0.9, 1.1)
                },
                'resilience': {
                    'overall_resilience': resilience,
                    'social_resilience': resilience * random.uniform(0.9, 1.1),
                    'economic_resilience': resilience * random.uniform(0.9, 1.1),
                    'infrastructure_resilience': resilience * random.uniform(0.9, 1.1)
                }
            },
            'events': {
                'flood': {
                    'intensity': flood_intensity,
                    'affected_area': flood_intensity * random.uniform(1000, 5000)
                },
                'cyclone': {
                    'intensity': cyclone_intensity,
                    'affected_area': cyclone_intensity * random.uniform(500, 2000)
                },
                'drought': {
                    'intensity': drought_intensity,
                    'affected_area': drought_intensity * random.uniform(2000, 8000)
                }
            },
            'impacts': {
                'casualties': casualties,
                'displaced': displaced,
                'economic_loss': economic_loss,
                'infrastructure_damage': economic_loss * random.uniform(0.3, 0.5),
                'agricultural_loss': economic_loss * random.uniform(0.2, 0.4)
            },
            'adaptation': {
                'adaptation_investment': adaptation_investment,
                'early_warning_systems': adaptation_investment * random.uniform(0.1, 0.3),
                'infrastructure_improvement': adaptation_investment * random.uniform(0.3, 0.5),
                'capacity_building': adaptation_investment * random.uniform(0.2, 0.4)
            }
        }
    
    # Calculate summary metrics
    first_year = start_year
    last_year = start_year + num_years - 1
    initial_vulnerability = region_data[first_year]['state']['vulnerability']['overall_vulnerability']
    final_vulnerability = region_data[last_year]['state']['vulnerability']['overall_vulnerability']
    vulnerability_reduction = (initial_vulnerability - final_vulnerability) / initial_vulnerability
    
    initial_resilience = region_data[first_year]['state']['resilience']['overall_resilience']
    final_resilience = region_data[last_year]['state']['resilience']['overall_resilience']
    resilience_improvement = (final_resilience - initial_resilience) / initial_resilience
    
    # Compute benefit-cost ratio
    average_annual_loss = total_economic_loss / num_years
    avoided_losses = average_annual_loss * vulnerability_reduction * 5  # 5-year horizon
    benefit_cost_ratio = avoided_losses / total_adaptation_investment if total_adaptation_investment > 0 else 1.0
    
    # Add metrics to results
    region_data['metrics'] = {
        'total_casualties': total_casualties,
        'total_displaced': total_displaced,
        'total_economic_loss': total_economic_loss,
        'average_annual_loss': average_annual_loss,
        'total_adaptation_investment': total_adaptation_investment,
        'vulnerability_reduction': vulnerability_reduction,
        'resilience_improvement': resilience_improvement,
        'benefit_cost_ratio': benefit_cost_ratio,
        'simulation_years': num_years,
        'infrastructure_damage_reduction': random.uniform(0.2, 0.4)
    }
    
    # Add additional scenarios for comparison
    for scenario_name in ['rcp4.5', 'rcp8.5']:
        results[scenario_name] = {'national': {}}
        scenario_metrics = {}
        
        # RCP4.5: moderate climate change (+20% impacts)
        # RCP8.5: severe climate change (+50% impacts)
        factor = 1.2 if scenario_name == 'rcp4.5' else 1.5
        
        scenario_metrics['total_casualties'] = int(total_casualties * factor)
        scenario_metrics['total_displaced'] = int(total_displaced * factor)
        scenario_metrics['total_economic_loss'] = total_economic_loss * factor
        scenario_metrics['average_annual_loss'] = average_annual_loss * factor
        scenario_metrics['total_adaptation_investment'] = total_adaptation_investment * factor
        scenario_metrics['vulnerability_reduction'] = vulnerability_reduction * 0.9  # harder to reduce vulnerability
        scenario_metrics['resilience_improvement'] = resilience_improvement * 0.9  # harder to improve resilience
        scenario_metrics['benefit_cost_ratio'] = benefit_cost_ratio * 0.9  # lower BCR with higher impacts
        scenario_metrics['simulation_years'] = num_years
        scenario_metrics['infrastructure_damage_reduction'] = random.uniform(0.15, 0.35)  # harder to reduce damage
        
        results[scenario_name]['national']['metrics'] = scenario_metrics
    
    return results

def main():
    """Main execution function"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Generate Bangladesh Disaster Risk Simulation Report')
    parser.add_argument('--input', type=str, help='Input JSON file with simulation results')
    parser.add_argument('--output', type=str, default='reports', help='Output directory for reports')
    parser.add_argument('--format', type=str, default='html', choices=['html', 'json'], help='Report format')
    parser.add_argument('--sample', action='store_true', help='Generate sample data for demonstration')
    args = parser.parse_args()
    
    # Create output directory
    output_path = Path(args.output)
    output_path.mkdir(exist_ok=True, parents=True)
    
    # Generate timestamp for filenames
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Initialize the report generator
    report_generator = ReportGenerator()
    
    # Load or generate data
    if args.sample:
        logger.info("Generating sample data for demonstration")
        results = generate_sample_data()
    elif args.input:
        logger.info(f"Loading simulation results from {args.input}")
        with open(args.input, 'r') as f:
            results = json.load(f)
    else:
        logger.error("Either --input or --sample must be specified")
        return
    
    # Generate reports
    if args.format == 'html':
        report_file = report_generator.generate_html_report(results, output_path, timestamp)
        logger.info(f"HTML report generated: {report_file}")
    elif args.format == 'json':
        json_files = report_generator.generate_json_reports(results, output_path, timestamp)
        for report_type, file_path in json_files.items():
            logger.info(f"{report_type.capitalize()} JSON report generated: {file_path}")
    
    print(f"\nReports generated successfully in {output_path}/")

if __name__ == "__main__":
    main()
