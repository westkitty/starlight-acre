extends Node

signal crop_state_changed(plot_id: String, new_state: String)
signal resource_changed(resource_name: String, new_value: float)
signal interaction_prompt_changed(prompt_text: String)
signal upgrade_unlocked(upgrade_id: String)
signal station_message(text: String)
