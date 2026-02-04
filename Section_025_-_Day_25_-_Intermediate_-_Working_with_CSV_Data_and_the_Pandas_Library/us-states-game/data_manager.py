import pandas as pd

class DataManager:

    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file)
        self.all_states = self.data.state.to_list()
        self.guessed_states = []

        # simple lookup dictionary
        self.state_positions = {}
        for _, row in self.data.iterrows():
            self.state_positions[row.state] = (row.x, row.y)

    def is_valid_state(self, state_name):
        return state_name in self.all_states

    def add_guess(self, state_name):
        if state_name not in self.guessed_states:
            self.guessed_states.append(state_name)

    def get_position(self, state_name):
        return self.state_positions[state_name]

    def get_missing_states(self):
        missing = []
        for state in self.all_states:
            if state not in self.guessed_states:
                missing.append(state)
        return missing

    def save_missing_to_csv(self, filename):
        missing = self.get_missing_states()
        df = pd.DataFrame(missing, columns=["state"])
        df.to_csv(filename, index=False)
