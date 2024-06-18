import pandas as pd
import numpy as np
import seaborn as sns 
from yaml import safe_load, safe_dump

import os
import sys
print(os.path.abspath('./src'))
sys.path.insert(0, os.path.abspath('.'))
from src.data_loader import DataLoader
from src.allocation_handler import AllocationHandler
from pprint import pprint

commit_hash = sys.argv[1]

minimisation_weights = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
new_demo = True

for participant_id in range(1, 101):
    source_filename = './demo/new-participant-data.yaml'
    with open(source_filename) as f:
        new_participant_data = safe_load(f)
    print(new_participant_data)
    new_participant_data['participant_id'] = participant_id
    stratification_classes = [key for key in new_participant_data.keys() if key != 'participant_id']
    lookup = {}
    for stratification_class in stratification_classes: 
        for value in new_participant_data[stratification_class]:
            lookup[value] = stratification_class 
    for stratification_class in stratification_classes:
        possible_values_in_class = list(new_participant_data[stratification_class].keys())
        print(possible_values_in_class)
        new_participant_data[stratification_class] = {}
        random_value = np.random.choice(possible_values_in_class)
        for x in possible_values_in_class:
            if x == random_value:
                new_participant_data[stratification_class][x] = 1
            else:
                new_participant_data[stratification_class][x] = 0
    with open(source_filename, 'w') as f:
        safe_dump(new_participant_data, f)
    for minimisation_weight in minimisation_weights:
        allocations_filepath = f'./demo/allocations-{minimisation_weight}.csv'

        if new_demo:
            allocations_df = pd.read_csv(allocations_filepath)
            allocations_df.head(0).to_csv(allocations_filepath, index=False)

        data_loader = DataLoader(source_filename, allocations_filepath, new_participant_data.keys())
        data_loaded = True

        allocation_handler = AllocationHandler(data_loader, minimisation_weight)
        new_participant_allocation = allocation_handler.get_allocation()
        output_data = {
                'participant_id': data_loader.participant.participant_id, 
                'allocation': new_participant_allocation
            }
        output_data.update(data_loader.participant.get_subcategory_values())
        updated_allocations_df = pd.concat([data_loader.allocations_df, pd.DataFrame([output_data])])

        updated_allocations_df.to_csv(allocations_filepath, index=False)
    new_demo = False

allocations_dfs = []
for minimisation_weight in minimisation_weights:
    allocations_dfs.append(pd.read_csv(f'./demo/allocations-{minimisation_weight}.csv').assign(minimisation_weight=minimisation_weight))
allocations_df = pd.concat(allocations_dfs)

chart_df = pd.melt(allocations_df.drop('participant_id', axis=1), id_vars=['allocation', 'minimisation_weight'], var_name='category', value_name='count')
chart_df['class'] = chart_df['category'].apply(lambda value: lookup[value])
chart_df['minimisation_weight'] = chart_df['minimisation_weight'].astype(str)
chart_df = chart_df.groupby(['allocation', 'class', 'category', 'minimisation_weight'])['count'].sum().reset_index()
p = sns.catplot(chart_df, x='count', y='category', col='class', hue='allocation', kind='bar', row='minimisation_weight', 
                     sharey=False, color='lightblue', margin_titles=True, height=3.6)
p.savefig(f'./demo/chart-{commit_hash}.png')

with open('./demo/sensitivity-analysis.md') as f:
    md = f.readlines()

md[-1] = f'<img src="./chart-{commit_hash}.png" width="800" />\n'

with open('./demo/sensitivity-analysis.md', 'w') as f:
    f.write(''.join(md))
