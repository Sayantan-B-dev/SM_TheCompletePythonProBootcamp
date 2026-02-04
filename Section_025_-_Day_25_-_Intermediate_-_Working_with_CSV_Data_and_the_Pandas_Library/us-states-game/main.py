from data_manager import DataManager
from map_manager import MapManager

# ---------------- SETUP ----------------
data = DataManager("50_states.csv")

map_ui = MapManager(
    image="blank_states_img.gif",
    width=725,
    height=491,
    title="U.S. States Game"
)

# ---------------- GAME LOOP ----------------
while len(data.guessed_states) < len(data.all_states):

    answer = map_ui.ask_state(
        score=len(data.guessed_states),
        total=len(data.all_states)
    )

    if answer is None:
        continue

    answer = answer.title()

    if answer == "Exit":
        # reveal missing states
        missing = data.get_missing_states()
        for state in missing:
            x, y = data.get_position(state)
            map_ui.write_state(state, x, y)

        # save to csv
        data.save_missing_to_csv("states_to_learn.csv")
        break

    if data.is_valid_state(answer):
        if answer not in data.guessed_states:
            data.add_guess(answer)
            x, y = data.get_position(answer)
            map_ui.write_state(answer, x, y)

map_ui.close_on_click()
