import sys
import pandas as pd
import numpy as np
from yaml import safe_load
from yaml.scanner import ScannerError

from src.data_loader import DataLoader
from src.report_builder import ReportBuilder
from src.allocation_handler import AllocationHandler

# Configure the project: 
minimisation_weight = 0.8 # 0.0 for fully random allocation, 1.0 for no randomisation
source_filename = './new-participant-data.yaml'
with (open(source_filename)) as f:
    expected_yaml_file_keys = safe_load(f).keys()
allocations_filepath = './allocations.csv'

# The commit hash gets passed to this script via the GitLab runner and is useful to ensure
# that the chart to be published on the `README.md` doc is not a cached (i.e. out-of-date) version
commit_hash = sys.argv[1]
report_builder = ReportBuilder(commit_hash)

# Get both the newly entered data at `source_filename` and the previously saved data 
# at `allocations_filepath`
data_loaded = False
try:
    data_loader = DataLoader(source_filename, allocations_filepath, expected_yaml_file_keys)
    data_loaded = True
except ScannerError:
    report_builder.add_error('## Error: Poorly formatted yaml file?')


# There are some checks that the newly enetered data in the yaml file matches expectations, 
# e.g. that there is only one 1 in each category (and the rest are zeros), or that the participant_ids
# are unique. 
if data_loaded:
    # Logic to handle the allocation of the new trial participant
    allocation_handler = AllocationHandler(data_loader, minimisation_weight)
    
    if not data_loader.participant.is_valid: 
        print('not valid')
        print(data_loader.participant.error_message)
        report_builder.add_error(data_loader.participant.error_message)
        report_builder.analyse_metadata(data_loader.allocations_df)

    # The code goes ahead and generates the report if the new data is valid:
    else: 
        new_participant_allocation = allocation_handler.get_allocation()
        report_builder.add_success(data_loader.participant.participant_id, new_participant_allocation)

        output_data = {
            'participant_id': data_loader.participant.participant_id, 
            'allocation': new_participant_allocation
        }
        output_data.update(data_loader.participant.get_subcategory_values())
        updated_allocations_df = pd.concat([data_loader.allocations_df, pd.DataFrame([output_data])])

        updated_allocations_df.to_csv(allocations_filepath, index=False)

        report_builder.analyse_metadata(updated_allocations_df)
        report_builder.make_chart(updated_allocations_df, data_loader.participant.data.keys(), data_loader.subcategory_to_category_lookup)

report_builder.write_report()
