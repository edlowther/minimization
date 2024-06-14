class Participant():
    def __init__(self, new_participant_data, existing_participant_ids, expected_yaml_file_keys):
        """Manage expectations about trial participant data"""
        self.data = new_participant_data.copy()
        self.participant_id = self.data.pop('participant_id')
        self.is_valid = self.validate(new_participant_data, expected_yaml_file_keys, existing_participant_ids)
        
    def validate(self, new_participant_data, expected_yaml_file_keys, existing_participant_ids):
        """Handle three ways in which the data may not be valid: are any keys missing, e.g. due to accidental 
        deletion; the participant id is not unique; and that the variables are mutually exclusive, i.e. a 
        participant cannot be treated at more than one hospital"""
        missing_keys = self.check_for_missing_keys(new_participant_data, expected_yaml_file_keys)
        if len(missing_keys) > 0:
            self.error_message = f'## Missing category or categories in new participant data: {missing_keys}'
            return False
        if self.participant_id in existing_participant_ids:
            self.error_message = '## Participant ID found in existing data. \nPlease double-check ID and re-enter data\n'
            return False
        if self.has_more_than_one_nonzero_entry_per_category():
            self.error_message = '## More than one non-zero entry found in a data category: \nThese are assumed to be \
            mutually exclusive. Please double-check input data and try again\n'
            return False
        return True

    def check_for_missing_keys(self, new_participant_data, expected_yaml_file_keys):
        missing_keys = []
        for key in expected_yaml_file_keys:
            if key not in new_participant_data.keys():
                missing_keys.append(key)
        return missing_keys

    def has_more_than_one_nonzero_entry_per_category(self):
        self.non_zero_subcategory_names = []
        for category in self.data:
            non_zero_count = 0
            for subcategory, value in self.data[category].items():
                print(category, subcategory, value, non_zero_count)
                if value > 0:
                    non_zero_count += 1
                    self.non_zero_subcategory_names.append(subcategory)
                    if non_zero_count > 1:
                        return True
        return False

    def get_subcategory_values(self):
        """This is useful for wrangling the participant's data into the right format to be stored
        in the `allocations.csv` file"""
        subcategories = {}
        for subcategory in self.data.values():
            subcategories.update(subcategory)
        return subcategories 


