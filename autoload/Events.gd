# Events.gd
# Global signal bus. Emits signals only — no state, no logic.
# All gameplay systems communicate through these signals.
# Add new signals here as Phase 2+ features are introduced.
extends Node

## Emitted when a crop plot changes state.
## plot_id: the plot's unique string ID
## new_state: one of "EMPTY", "PLANTED", "GROWING", "READY"
signal crop_state_changed(plot_id: String, new_state: String)

## Emitted when any tracked resource changes value.
## resource_name: "water", "nutrient", "power", "wisdom_fruit"
## new_value: current numeric value
signal resource_changed(resource_name: String, new_value: float)

## Emitted by player.gd when the active interactable changes.
## prompt_text: display string like "E — Plant Wisdom Fruit"
## Empty string means no active interactable — hide the prompt.
signal interaction_prompt_changed(prompt_text: String)
