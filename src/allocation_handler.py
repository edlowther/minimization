import pandas as pd
import numpy as np

class AllocationHandler(): 
    """Implement the 'biased coin' according to how the project has been configured"""
    def __init__(self, data_loader, minimisation_weight): 
        self.data_loader = data_loader
        self.minimisation_weight = minimisation_weight

    def get_score_by_allocation_group(self, allocation):
        """To determine whether an allocation would make the two groups more or less similar, we 
        calculate the total score for each of the groups that match the non-zero values of the new 
        trial participant"""
        relevant_cols = self.data_loader.participant.non_zero_subcategory_names
        filtered_df = self.data_loader.allocations_df.loc[
            self.data_loader.allocations_df['allocation'] == allocation, 
            relevant_cols
        ]
        if len(filtered_df) == 0: 
            group_score = 0 
        else: 
            group_score = filtered_df.sum(axis=1).sum()
        return group_score
    
    def get_allocation(self): 
        """Taking the scores defined above, flip the biased coin"""
        control_group_score = self.get_score_by_allocation_group('Control')
        intervention_group_score = self.get_score_by_allocation_group('Intervention')

        # Scale the minimisation_weight so that 0 -> 0.5 and 1 -> 1 to use in `np.random.choice`, 
        # so that 0 (fully random) results in a 50:50 chance of either group, and 1 results in 
        # a fully deteministic allocation of the new participant to the group with the lowest score, 
        # i.e. it will raise that score to make the two groups more equal
        scaled_minimisation_weight = self.minimisation_weight / 2.0 + 0.5

        if control_group_score == intervention_group_score: 
            new_participant_assignment = np.random.choice(['Control', 'Intervention'])
        elif control_group_score < intervention_group_score: 
            new_participant_assignment = np.random.choice(['Control', 'Intervention'], 
                                                        p=[scaled_minimisation_weight, 1-scaled_minimisation_weight])
        else: 
            new_participant_assignment = np.random.choice(['Control', 'Intervention'], 
                                                        p=[1-scaled_minimisation_weight, scaled_minimisation_weight])
        
        # For analytical purposes, but not currently in use:
        self.scores_diff = control_group_score - intervention_group_score

        return new_participant_assignment
