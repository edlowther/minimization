import pandas as pd
import numpy as np
from yaml import safe_load

from .participant import Participant

class DataLoader():
    """Handle loading the new data and the existing data, and create handy lookup to understand
    which category a subcategory is in, e.g. that `leeds` is a `hospital_site`"""
    def __init__(self, source_filename, allocations_filepath, expected_yaml_file_keys):
        self.source_filename = source_filename
        self.allocations_df = pd.read_csv(allocations_filepath)
        self.participant = self.create_new_participant(expected_yaml_file_keys)
        self.subcategory_to_category_lookup = self.get_lookup()

    def create_new_participant(self, expected_yaml_file_keys):
        new_participant_data = self.load_new_participant_data()
        existing_participant_ids = self.allocations_df['participant_id'].values
        return Participant(new_participant_data, existing_participant_ids, expected_yaml_file_keys)

    def load_new_participant_data(self): 
        with open(self.source_filename) as f: 
            return safe_load(f)

    def get_lookup(self): 
        lookup = {}
        for category in self.participant.data: 
            for subcategory in self.participant.data[category]:
                lookup[subcategory] = category 
        return lookup
