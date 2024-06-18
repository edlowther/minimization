from yaml import safe_load, dump

with open('./initialize-project.yaml') as f: 
    new_project_data = safe_load(f)

default_participant_data = {
    'participant_id': 0
}

csv_column_names = ['participant_id']

for category, values in new_project_data.items():
    default_participant_data[category] = {}
    for value in values:
        default_participant_data[category][value] = 0
        csv_column_names.append(value)

csv_column_names.append('allocation')

with open('./new-participant-data.yaml', 'w') as f:
    dump(default_participant_data, f, sort_keys=False)

with open('./demo/new-participant-data.yaml', 'w') as f:
    dump(default_participant_data, f, sort_keys=False)

with open('./allocations.csv', 'w') as f:
    f.write(','.join(csv_column_names))

for proportion in ['0.0', '0.2', '0.4', '0.6', '0.8', '1.0']:
    with open(f'./demo/allocations-{proportion}.csv', 'w') as f:
        f.write(','.join(csv_column_names))
