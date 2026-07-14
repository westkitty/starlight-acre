# Events.gd
# Global signal bus. Emits signals only - no state, no logic.
# All gameplay systems communicate through these signals.
extends Node

## Emitted when a crop plot changes state.
## plot_id: the plot's unique string ID
## new_state: one of "EMPTY", "PLANTED", "GROWING", "READY"
signal crop_state_changed(plot_id: String, new_state: String)

## Emitted when any tracked resource changes value.
## resource_name: "water", "nutrient", "power", "wisdom_fruit", "trickster_vine"
## new_value: current numeric value
signal resource_changed(resource_name: String, new_value: float)

## Emitted by player.gd when the active interactable changes.
## Empty string means no active interactable - hide the prompt.
signal interaction_prompt_changed(prompt_text: String)

## Emitted for short action feedback such as save/load, harvest, and trade results.
signal status_message_changed(message_text: String)
