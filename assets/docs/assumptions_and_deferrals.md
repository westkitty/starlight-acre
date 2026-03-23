# Assumptions & Deferred Assets

This document records the design decisions and assumptions made during the generation of the Starlight Acre startup asset pack.

## Key Assumptions

### 1. Visual Scale & Resolution
- **Target Resolution**: 1920x1080 (16:9).
- **Pixel Density**: Assets are designed with a "GBA/SNES" vibe in mind, meaning a 1:1 pixel scale on a 1920x1080 canvas would look very small. It is assumed the game will be rendered at a lower internal resolution (e.g., 480x270 or 640x360) and scaled up with "Nearest" filtering to maintain the pixel art look.
- **Tile Size**: All environment tiles are designed to fit a 16x16 or 32x32 grid.

### 2. Player Mechanics
- **Side-View**: The game is strictly 2D side-view. No top-down or 3/4 view assets were generated.
- **Interactions**: Animation for "Interact" is a simple 2-frame reach, assuming the object being interacted with provides the secondary visual feedback (e.g., terminal glowing).

### 3. Resource Management
- **UI Icons**: It is assumed the HUD will display Water, Nutrient, and Power as simple bars or counters next to the generated icons.
- **Terminal Distinction**: The Repair terminal uses "Copper/Orange" hues to denote hardware, while the Replenish terminal uses "Teal/Blue" to denote fluids.

## Intentionally Deferred Assets

The following items were deferred to keep the startup pack focused and cohesive:

- **Liquid/Particle Source Files**: While effects like "growth_glow" were provided, complex liquid simulations for the Replenish terminal should be handled via Godot's `GPUParticles2D`.
- **Background Parallax Layers**: The background is provided as a single composite image. For true parallax, the "Nebula" and "Station Interior" would need to be separated into distinct layers.
- **Normal Maps**: No lighting/normal maps were generated, assuming the 16-bit aesthetic relies primarily on baked-in shading.
- **Additional Character Variants**: Only the primary "Caretaker" technician was created.
- **Alternate Crops**: Only "Wisdom Fruit" was generated to satisfy the bootstrap requirement.
