# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A single-file, browser-based CS2 (Counter-Strike 2) first-person shooter simulator. The entire application lives in `index.html` (~1500 lines) with zero external dependencies. It uses 2D raycasting (Wolfenstein 3D-style) to render a 3D perspective on a `<canvas>` element. UI text is in Chinese (zh-CN).

## Running

Open `index.html` directly in a browser. No build step, no server required.

## Architecture (all within index.html)

**Rendering**: Raycasting engine casts one ray per screen column (960×600 canvas) using DDA through a 32×24 tile map. Walls are vertical strips with distance-based shading. Column merging optimizes consecutive same-type walls. Enemies are billboard sprites with depth-buffer testing. Smoke clouds and fire zones are rendered as sprites with alpha blending.

**Maps**: `MAPS` array contains 3 maps (Dust II, Inferno, Mirage). `MAP` is the currently active map. `0` = open, `1-5` = wall types with colors in `WALL_CLR`.

**Wall Textures**: Procedurally generated on offscreen canvases. Each wall type has noise-based texture with surface detail lines.

**Weapons**: 9 weapons: Glock-18, USP-S, Desert Eagle, MP9, P90, AK-47, M4A4, M4A1-S, AWP. Categories: pistol, SMG, rifle, sniper. Buy menu with CS2 economy.

**Grenades**: Flashbang (blind enemies), Smoke (vision block), HE (area damage), Molotov (fire zone). Bought separately from weapons.

**Player state**: `P` object tracks position, direction vectors, HP, armor, money, inventory, ammo, visual effects, screen shake, kill streak, bomb mode state, grenade inventory, counter-strafe velocity, scope state.

**Enemy AI**: 4 types (rusher, soldier, heavy, sniper) with enhanced state machine: patrol (A* pathfinding), combat (type-specific tactics, cover-seeking, flanking), search (last known position), alert (investigate gunfire), stunned (from flashbang). Spawning scales difficulty per round.

**A* Pathfinding**: Grid-based pathfinding with diagonal movement. `findCover()` for tactical cover-seeking.

**Bomb Mode**: Plant at bomb sites (E key, 3s), 40s fuse, 5s defuse. Objective-based gameplay.

**Game Modes**: Bomb Defusal (classic), Deathmatch (infinite respawn, 5min), Arms Race (auto-weapon-upgrade on kill).

**Audio**: Procedural via Web Audio API. Noise-based sounds for explosions, footsteps, flashbangs. Oscillator-based for shoot, hit, kill, reload. Layered explosion sounds with white noise + low-frequency oscillator.

**Bullet Tracers**: Visual bullet trails with fade-out.

**Counter-Strafe**: Player velocity has momentum with deceleration. Stopping quickly improves accuracy.

**HUD**: CS2-style with HP/armor bars, ammo counter, weapon name, money, round timer, round score (CT vs T), minimap with bomb/smoke markers, grenade inventory, kill feed, kill streak display, bomb plant/defuse progress.

**Game loop**: `requestAnimationFrame` with delta-time capped at 0.05s.

## Controls

- WASD: move (counter-strafe for accuracy)
- Mouse: aim (Pointer Lock)
- Left-click: shoot
- Right-click: AWP scope
- R: reload
- B: buy menu
- Shift: walk (reduced speed/spread)
- 1-9: weapon slots
- E: plant/defuse bomb
- 4: flashbang
- 5: smoke
- 6: HE grenade
- 7: molotov
- M: select map (on start screen)
