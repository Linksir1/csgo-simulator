# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A single-file, browser-based CS2 (Counter-Strike 2) first-person shooter simulator. The entire application lives in `index.html` (~1500 lines) with zero external dependencies. It uses 2D raycasting (Wolfenstein 3D-style) to render a 3D perspective on a `<canvas>` element. UI text is in Chinese (zh-CN).

## Running

Open `index.html` directly in a browser. No build step, no server required.

## Architecture (all within index.html)

**Rendering**: Raycasting engine casts one ray per screen column (960×600 canvas) using DDA through a 128×96 tile map (`MAP` is a `Uint8Array` of size 12288). Walls are vertical strips with distance-based shading and a dark fog at far distances. Column merging optimizes consecutive same-type walls. Enemies are billboard sprites with depth-buffer testing. Smoke clouds use animated multi-puff radial gradients for a volumetric look. Fire zones flicker via animated radial gradients.

**Maps**: All three CS2 classics are 1:1 reproductions of the topology — `buildDust2()`, `buildInferno()`, `buildMirage()` carve the level by calling primitives (`fillAll`, `rect`, `clr`, `frame`, `hLine`, `vLine`) on the `Uint8Array`. Each map preserves the actual callouts and connectivity:
- **Dust II**: T spawn (S), Long Doors → Long A → A site (Goose, Pit, Big box), B Tunnels → B site, Mid + Mid Doors, Catwalk → Short A, CT spawn (N).
- **Inferno**: T spawn (E), Banana → B site (NW), Mid → Apps → Pit/Library → A site (SW), Boiler/CT spawn.
- **Mirage**: T spawn (S), Mid → Window/Connector → A, A Ramp → Palace → A site (NE), Underpass → B Apps → B site (NW), Bench/Market.

Wall types (1-5): concrete, brick, crate/wood, metal pillar, sandstone — each with its own procedurally generated noise texture.

**Map metadata**: `MAP_DEFS` array holds per-map `{build, pSpawn, eSpawns, sites, callouts}`. Callouts are name+coord pairs rendered on the rotating radar.

**Wall Textures**: Procedurally generated on offscreen canvases. Noise + per-type surface detail (concrete grid lines, brick pattern, wood grain, metal stripes, sandstone speckle).

**Weapons**: 9 weapons — Glock-18, USP-S, Desert Eagle, MP9, P90, AK-47, M4A4, M4A1-S, AWP. CS2 economy.

**Spray Patterns**: `SPRAY` table holds per-weapon recoil arrays of `[pitchOffset, yawOffset]` in radians (30 entries for rifles, 20 for SMGs). Each shot increments `P.sprayIdx`; the index resets to 0 after 0.4s without firing. AK climbs straight then S-curves right; M4 is tighter; M4A1-S is the tightest.

**Tagging**: `P.tagT` is set to 0.4s when the player is hit, multiplying movement velocity by 0.4 — matches CS2 tagging slowdown.

**Grenades**: Flashbang (blinds proportional to facing angle), Smoke (volumetric multi-puff occlusion that blocks sight for both sides), HE (radius damage to player + enemies), Molotov (fire zone DoT).

**Player state**: `P` object — position/dir vectors, hp/armor/helmet, money, inventory, ammo per weapon, recoil/recoilYaw, spray index, tag timer, scope state, bomb mode state, grenade counts, counter-strafe velocity.

**Enemy AI**: 4 types (rusher, soldier, heavy, sniper) with state machine: patrol (A* pathfinding), combat (type-specific tactics, cover-seeking, flanking), search (last known position), alert (investigate gunfire), stunned (from flashbang). Smoke occludes both LoS and shots. Difficulty scales with `roundNum`.

**A* Pathfinding**: `findPath` uses a binary min-heap; `findCover()` scores nearby tiles by wall-coverage from a threat direction.

**Bomb Mode**: Plant at any of the two bomb sites (E key, 3.2s), 40s fuse, 5s defuse with kit / 10s without. Beep accelerates as fuse runs down.

**Round System / MR12**: 24-round match, halftime side switch at round 12 (`halfSwitched`), first to 13 wins. Money resets on side switch. CS2-style loss bonus progression ($1400 + lossStreak × $500, capped).

**Game Modes**: Bomb Defusal (MR12), Deathmatch (infinite respawn, 5min), Arms Race (auto-weapon-upgrade on kill).

**Audio**: Procedural via Web Audio API. Per-weapon-class shoot sounds (pistol, rifle, AWP), layered explosion (white noise + low-frequency oscillator), bomb beeping that accelerates near zero.

**Bullet Tracers**: `tracers` array — short-lived line segments with fade.

**Counter-Strafe + Tagging**: Velocity has momentum (instant-stop on direction change → improved accuracy); `P.tagT` reduces speed when hit.

**HUD**: CS2-styled.
- Top: round score bar (`CT 0 : 0 T`), round number, buy / round timer (color-coded).
- Bottom-left: HP/armor bars, money, side indicator, weapon slots, grenade inventory.
- Bottom-right: ammo + weapon name.
- Top-right: kill feed, map name.
- Top-left: rotating radar with callout labels, bomb-site outlines, smoke / fire / planted-bomb markers.
- Center: dynamic crosshair that spreads with movement & spray index.
- Tab: scoreboard overlay.

**Rotating Radar**: Top-left circular minimap. Rotates so the player always faces up; bomb sites, smokes, fires, callouts, and visible enemies (LoS-checked, range 22) are drawn on it. Site letters and callout text counter-rotate to stay upright.

**Game loop**: `requestAnimationFrame` with delta-time capped at 0.05s.

## Controls

- WASD: move (counter-strafe for accuracy, slowed when tagged)
- Mouse: aim (Pointer Lock) — slowed when scoped
- Left-click: shoot
- Right-click: AWP scope
- R: reload
- B: buy menu (only during 15s buy phase)
- Shift: walk (reduced speed/spread)
- 1: melee/knife slot, 2: rifle/SMG, 3: pistol — quick CS-style switch by category
- 4: flashbang (max 2)
- 5: smoke
- 6: HE grenade
- 7: molotov
- E: plant/defuse bomb
- M (start screen): pick map
- Tab: hold to view scoreboard
