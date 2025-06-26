import pygame
import numpy as np
from collections import defaultdict
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import threading
import math

class GameOfLife:
    """Core game logic handling the cellular automaton simulation."""
    
    def __init__(self, rules="B3/S23"):
        self.cells = defaultdict(int)  # Sparse representation {(x, y): age}
        self.generation = 0
        self.rules = self.parse_rules(rules)
        self.rule_string = rules
        self.history = [dict()]  # For undo/redo functionality, start with empty state
        self.history_position = 0
        self.max_history = 100
        self.patterns = self.initialize_patterns()
        self.pattern_categories = self.categorize_patterns()
        
    def initialize_patterns(self):
        """Initialize a dictionary of built-in patterns."""
        patterns = {}
        
        # Still Lifes
        patterns["Block"] = [(0, 0), (0, 1), (1, 0), (1, 1)]
        patterns["Beehive"] = [(0, 1), (0, 2), (1, 0), (1, 3), (2, 1), (2, 2)]
        patterns["Loaf"] = [(0, 1), (0, 2), (1, 0), (1, 3), (2, 1), (3, 2)]
        patterns["Boat"] = [(0, 0), (0, 1), (1, 0), (1, 2), (2, 1)]
        patterns["Tub"] = [(0, 1), (1, 0), (1, 2), (2, 1)]
        
        # Oscillators
        patterns["Blinker"] = [(0, 0), (0, 1), (0, 2)]
        patterns["Toad"] = [(0, 0), (1, 0), (2, 0), (-1, 1), (0, 1), (1, 1)]
        patterns["Beacon"] = [(0, 0), (1, 0), (0, 1), (3, 2), (2, 3), (3, 3)]
        
        # Glider
        patterns["Glider"] = [(0, 0), (1, 1), (1, 2), (0, 2), (-1, 2)]
        
        # Pulsar
        patterns["Pulsar"] = [
            # Top
            (2, 0), (3, 0), (4, 0), (8, 0), (9, 0), (10, 0),
            # Upper middle
            (0, 2), (5, 2), (7, 2), (12, 2),
            (0, 3), (5, 3), (7, 3), (12, 3),
            (0, 4), (5, 4), (7, 4), (12, 4),
            (2, 5), (3, 5), (4, 5), (8, 5), (9, 5), (10, 5),
            # Lower middle
            (2, 7), (3, 7), (4, 7), (8, 7), (9, 7), (10, 7),
            (0, 8), (5, 8), (7, 8), (12, 8),
            (0, 9), (5, 9), (7, 9), (12, 9),
            (0, 10), (5, 10), (7, 10), (12, 10),
            # Bottom
            (2, 12), (3, 12), (4, 12), (8, 12), (9, 12), (10, 12)
        ]
        
        # Pentadecathlon
        patterns["Pentadecathlon"] = [
            (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)
        ]
        patterns["Pentadecathlon"].extend([(-1, 1), (1, 1), (-1, 6), (1, 6)])
        
        # Clock
        patterns["Clock"] = [(1, 0), (0, 1), (2, 1), (1, 2)]
        
        # Figure 8
        patterns["Figure 8"] = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 3), (1, 3), (2, 3), (0, 4), (1, 4), (2, 4)]
        
        # LWSS
        patterns["LWSS"] = [(0, 0), (3, 0), (4, 1), (0, 2), (4, 2), (1, 3), (2, 3), (3, 3), (4, 3)]
        
        # MWSS
        patterns["MWSS"] = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (0, 1), (5, 1), (-1, 2), (5, 2), (5, 3), (-1, 4), (0, 4), (4, 4)]
        
        # HWSS
        patterns["HWSS"] = [(2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (1, 1), (6, 1), 
                           (0, 2), (6, 2), (0, 3), (5, 3), (0, 4), (1, 4), (2, 4), (3, 4)]
        
        # Weekender
        patterns["Weekender"] = [
            (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
            (0, 1), (7, 1),
            (2, 2), (5, 2),
            (0, 3), (3, 3), (4, 3), (7, 3),
            (0, 5), (3, 5), (4, 5), (7, 5),
            (2, 6), (5, 6),
            (0, 7), (7, 7),
            (0, 8), (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8)
        ]
        
        # Copperhead
        patterns["Copperhead"] = [
            (4, 0), (5, 0), (6, 0), (7, 0),
            (3, 1), (8, 1),
            (2, 2), (9, 2),
            (1, 3), (3, 3), (8, 3), (10, 3),
            (1, 4), (4, 4), (7, 4), (10, 4),
            (0, 5), (3, 5), (8, 5), (11, 5),
            (0, 6), (2, 6), (9, 6), (11, 6),
            (0, 7), (5, 7), (6, 7), (11, 7),
            (0, 8), (3, 8), (8, 8), (11, 8),
            (1, 9), (10, 9),
            (2, 10), (9, 10),
            (3, 11), (8, 11),
            (4, 12), (7, 12),
            (5, 13), (6, 13)
        ]
        
        # Glider Gun
        patterns["Glider Gun"] = [
            (0, 4), (0, 5), (1, 4), (1, 5),  # Block
            (10, 4), (10, 5), (10, 6), (11, 3), (11, 7), (12, 2), (12, 8),
            (13, 2), (13, 8), (14, 5), (15, 3), (15, 7), (16, 4), (16, 5), (16, 6),
            (17, 5),  # Left side
            (20, 2), (20, 3), (20, 4), (21, 2), (21, 3), (21, 4), (22, 1), (22, 5),
            (24, 0), (24, 1), (24, 5), (24, 6),  # Right side
            (34, 2), (34, 3), (35, 2), (35, 3)  # Block
        ]
        
        # Simkin Glider Gun
        patterns["Simkin Glider Gun"] = [
            (0, 0), (1, 0), (7, 0), (8, 0),
            (0, 1), (1, 1), (7, 1), (8, 1),
            (4, 2), (5, 2),
            (4, 3), (5, 3),
            (12, 5), (13, 5), (11, 6), (13, 6), (21, 6), (22, 6),
            (10, 7), (11, 7), (13, 7), (14, 7), (21, 7), (22, 7),
            (1, 8), (2, 8), (10, 8), (15, 8),
            (1, 9), (2, 9), (10, 9), (11, 9), (13, 9), (14, 9),
            (11, 10), (13, 10),
            (12, 11), (13, 11)
        ]
        
        # B-heptomino Puffer
        patterns["B-heptomino Puffer"] = [
            (1, 0), (2, 0), (3, 0), (0, 1), (3, 1), (0, 2), (2, 2)
        ]
        
        # Spacefiller
        patterns["Spacefiller"] = [
            (3, 0), (4, 0), (5, 0), (7, 0), (8, 0), (9, 0),
            (2, 1), (6, 1), (10, 1),
            (1, 2), (2, 2), (6, 2), (10, 2), (11, 2),
            (0, 3), (2, 3), (6, 3), (10, 3), (12, 3),
            (0, 4), (4, 4), (8, 4), (12, 4),
            (0, 5), (12, 5),
            (0, 6), (1, 6), (5, 6), (7, 6), (11, 6), (12, 6),
            (1, 7), (5, 7), (7, 7), (11, 7),
            (2, 8), (3, 8), (4, 8), (8, 8), (9, 8), (10, 8)
        ]
        
        # R-pentomino
        patterns["R-pentomino"] = [(0, 0), (1, 0), (-1, 1), (0, 1), (0, 2)]
        
        # Diehard
        patterns["Diehard"] = [(0, 0), (1, 0), (1, 1), (5, 1), (6, 1), (7, 1), (6, -1)]
        
        # Acorn
        patterns["Acorn"] = [(0, 0), (1, 0), (1, 2), (3, 1), (4, 0), (5, 0), (6, 0)]
        
        # Brain
        patterns["Brain"] = [
            (1, 0),
            (0, 1), (2, 1),
            (0, 2), (1, 2), (2, 2)
        ]
        
        # Pi-heptomino
        patterns["Pi-heptomino"] = [
            (0, 0), (1, 0), (2, 0),
            (0, 1), (2, 1),
            (0, 2)
        ]
        
        # Thunderbird
        patterns["Thunderbird"] = [
            (0, 0), (1, 0), (2, 0),
            (1, 1), (1, 2)
        ]
        
        # Switch Engine
        patterns["Switch Engine"] = [
            (0, 0), (2, 0),
            (1, 1), (2, 1),
            (-1, 2), (0, 2)
        ]
        
        # Garden of Eden
        patterns["Garden of Eden"] = [
            (1, 0), (2, 0), (3, 0), (5, 0), (6, 0), (7, 0), 
            (0, 1), (4, 1), (8, 1),
            (0, 2), (2, 2), (6, 2), (8, 2),
            (0, 3), (4, 3), (8, 3),
            (1, 4), (2, 4), (3, 4), (5, 4), (6, 4), (7, 4)
        ]
        
        # Cross
        patterns["Cross"] = [
            (1, 0), (2, 0), (4, 0), (5, 0),
            (0, 1), (3, 1), (6, 1),
            (0, 2), (6, 2),
            (1, 3), (2, 3), (4, 3), (5, 3)
        ]
        
        # Queen Bee Shuttle
        patterns["Queen Bee Shuttle"] = [
            # Queen Bee
            (1, 0), (2, 1), (0, 2), (4, 2), (1, 3), (2, 3), (3, 3),
            # Left Block
            (-4, 1), (-4, 2), (-3, 1), (-3, 2),
            # Right Block
            (8, 1), (8, 2), (7, 1), (7, 2)
        ]
        
        # Max
        patterns["Max"] = [
            (2, 0), (3, 0), (5, 0), (6, 0),
            (0, 1), (1, 1), (3, 1), (5, 1), (7, 1), (8, 1),
            (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2),
            (2, 3), (6, 3)
        ]
        
        # Star
        patterns["Star"] = [
            (3, 0),
            (2, 1), (4, 1),
            (1, 2), (2, 2), (4, 2), (5, 2),
            (2, 3), (4, 3),
            (3, 4)
        ]
        
        # HWSS Factory
        patterns["HWSS Factory"] = [
            # Glider Gun base
            (0, 4), (0, 5), (1, 4), (1, 5),  # Block
            (10, 4), (10, 5), (10, 6), (11, 3), (11, 7), (12, 2), (12, 8),
            (13, 2), (13, 8), (14, 5), (15, 3), (15, 7), (16, 4), (16, 5), (16, 6),
            (17, 5),  # Left side
            (20, 2), (20, 3), (20, 4), (21, 2), (21, 3), (21, 4), (22, 1), (22, 5),
            (24, 0), (24, 1), (24, 5), (24, 6),  # Right side
            (34, 2), (34, 3), (35, 2), (35, 3),  # Block
            # Eater pattern at specific offset
            (41, 7), (42, 7), (41, 8), (43, 8), (43, 9), (42, 10), (43, 10)
        ]
        
        # Glider Eater
        patterns["Glider Eater"] = [
            (0, 0), (1, 0),
            (0, 1), (2, 1),
            (2, 2), (3, 2),
            (1, 3), (2, 3)
        ]
        
        # Pufferfish
        patterns["Pufferfish"] = [
            (5, 0), (6, 0), (7, 0), (9, 0), (10, 0), (11, 0),
            (4, 1), (8, 1), (12, 1),
            (3, 2), (4, 2), (8, 2), (12, 2), (13, 2),
            (2, 3), (4, 3), (8, 3), (12, 3), (14, 3),
            (2, 4), (6, 4), (10, 4), (14, 4),
            (2, 5), (14, 5),
            (2, 6), (3, 6), (7, 6), (9, 6), (13, 6), (14, 6),
            (3, 7), (7, 7), (9, 7), (13, 7),
            (4, 8), (5, 8), (6, 8), (10, 8), (11, 8), (12, 8)
        ]
        
        # NEW ADVANCED PATTERNS
        
        # Breeder 1 - First pattern with quadratic growth (simplified version)
        patterns["Breeder 1"] = []
        # Main puffer engine
        puffer_base = [(0, 0), (1, 0), (2, 0), (0, 1), (3, 1), (0, 2), (4, 2), (0, 3), (4, 3), (1, 4), (3, 4)]
        for i in range(5):
            for x, y in puffer_base:
                patterns["Breeder 1"].append((x, y + i*20))
        
        # Add gun mechanisms along the puffer's path
        gun_base = [
            (10, 0), (11, 0), (10, 1), (11, 1),  # Block
            (20, 2), (21, 2), (19, 3), (23, 3), (18, 4), (24, 4),
            (18, 5), (24, 5), (21, 5), (19, 6), (23, 6), (20, 7), (21, 7), (22, 7)
        ]
        for i in range(3):
            for x, y in gun_base:
                patterns["Breeder 1"].append((x, y + i*25))
        
        # Multi-Engine Spaceship Factory - Complex pattern that creates multiple HWSS
        patterns["Multi-Engine Spaceship Factory"] = []
        # First gun
        gun1 = patterns["Glider Gun"]
        for x, y in gun1:
            patterns["Multi-Engine Spaceship Factory"].append((x, y))
        
        # Second gun at an offset
        gun2 = patterns["Glider Gun"]
        for x, y in gun2:
            patterns["Multi-Engine Spaceship Factory"].append((x + 50, y + 20))
        
        # Third gun at another offset
        gun3 = patterns["Glider Gun"]
        for x, y in gun3:
            patterns["Multi-Engine Spaceship Factory"].append((x + 25, y + 40))
        
        # Add reflectors and converters to turn gliders into spaceships
        reflector = [(0, 0), (1, 0), (2, 0), (0, 1), (3, 1), (0, 2), (3, 2), (1, 3), (2, 3)]
        converter = [
            (0, 0), (1, 0), (2, 0), (3, 0),
            (0, 1), (4, 1),
            (4, 2),
            (0, 3), (3, 3),
            (1, 4), (2, 4)
        ]
        
        # Add reflectors at strategic positions
        for i, pos in enumerate([(40, 10), (90, 30), (65, 50)]):
            for x, y in reflector:
                patterns["Multi-Engine Spaceship Factory"].append((x + pos[0], y + pos[1]))
            for x, y in converter:
                patterns["Multi-Engine Spaceship Factory"].append((x + pos[0] + 15, y + pos[1] + 5))
        
        # Simple Computer Memory - Sliding block memory
        patterns["Simple Computer Memory"] = []
        # Memory blocks
        memory_blocks = [
            # Main block
            (0, 0), (1, 0), (0, 1), (1, 1),
            # Control blocks
            (10, 0), (11, 0), (10, 1), (11, 1),
            (20, 0), (21, 0), (20, 1), (21, 1),
            (30, 0), (31, 0), (30, 1), (31, 1)
        ]
        for x, y in memory_blocks:
            patterns["Simple Computer Memory"].append((x, y))
        
        # Glider lanes for incrementing/decrementing
        glider_inc = [(5, 10), (6, 10), (7, 10), (7, 9), (6, 8)]
        glider_dec = [(15, 10), (16, 10), (17, 10), (15, 9), (16, 8)]
        
        for x, y in glider_inc:
            patterns["Simple Computer Memory"].append((x, y))
        for x, y in glider_dec:
            patterns["Simple Computer Memory"].append((x, y))
        
        # AND Gate - Logic gate implemented in Game of Life
        patterns["AND Gate"] = []
        # Input channel A
        input_a = [(0, 0), (1, 0), (2, 0), (0, 1), (2, 1)]
        # Input channel B
        input_b = [(10, 10), (11, 10), (12, 10), (10, 11), (12, 11)]
        # Output channel
        output = [(20, 20), (21, 20), (22, 20), (20, 21), (22, 21)]
        # Gates and reflectors
        gate = [
            (15, 15), (16, 15), (15, 16), (16, 16),  # Block
            (13, 13), (14, 13), (12, 14), (15, 14),
            (12, 15), (12, 16), (13, 17), (14, 17)
        ]
        
        for coords in [input_a, input_b, output, gate]:
            for x, y in coords:
                patterns["AND Gate"].append((x, y))
        
        # Turing Machine - Simplified representation of a Turing machine
        patterns["Turing Machine"] = []
        # Tape cells (represented as blocks)
        for i in range(10):
            patterns["Turing Machine"].append((i*5, 0))
            patterns["Turing Machine"].append((i*5 + 1, 0))
            patterns["Turing Machine"].append((i*5, 1))
            patterns["Turing Machine"].append((i*5 + 1, 1))
        
        # Head mechanism (simplified)
        head = [
            (20, 10), (21, 10), (22, 10),
            (20, 11), (22, 11),
            (20, 12), (21, 12), (22, 12)
        ]
        for x, y in head:
            patterns["Turing Machine"].append((x, y))
            
        # Glider streams representing program
        for i in range(5):
            patterns["Turing Machine"].append((30 + i, 20))
            patterns["Turing Machine"].append((31 + i, 21))
            patterns["Turing Machine"].append((30 + i, 22))
        
        # Prime Number Generator - Pattern that demonstrates computational capability
        patterns["Prime Number Generator"] = []
        
        # Counter mechanism
        for i in range(5):
            block_x = i * 10
            # Counter blocks
            patterns["Prime Number Generator"].append((block_x, 0))
            patterns["Prime Number Generator"].append((block_x + 1, 0))
            patterns["Prime Number Generator"].append((block_x, 1))
            patterns["Prime Number Generator"].append((block_x + 1, 1))
            
            # Connecting gliders
            patterns["Prime Number Generator"].append((block_x + 5, 5))
            patterns["Prime Number Generator"].append((block_x + 6, 6))
            patterns["Prime Number Generator"].append((block_x + 4, 6))
        
        # Control mechanism
        control = [
            (0, 20), (1, 20), (2, 20),
            (0, 21), (2, 21),
            (0, 22), (1, 22), (2, 22),
            # Add a glider gun to drive the computation
            (10, 25), (11, 25), (10, 26), (11, 26),
            (20, 25), (21, 25), (22, 25),
            (20, 26), (22, 26),
            (20, 27), (21, 27), (22, 27)
        ]
        for x, y in control:
            patterns["Prime Number Generator"].append((x, y))
        
        # Quad-Gun - Four glider guns firing at 90-degree angles
        patterns["Quad-Gun"] = []
        base_gun = patterns["Glider Gun"]
        
        # Original orientation
        for x, y in base_gun:
            patterns["Quad-Gun"].append((x, y))
            
        # Rotate 90 degrees
        for x, y in base_gun:
            patterns["Quad-Gun"].append((y, -x + 40))
            
        # Rotate 180 degrees
        for x, y in base_gun:
            patterns["Quad-Gun"].append((-x + 40, -y + 40))
            
        # Rotate 270 degrees
        for x, y in base_gun:
            patterns["Quad-Gun"].append((-y + 40, x))
        
        # 3D Illusion - Pattern that creates an illusion of 3D movement
        patterns["3D Illusion"] = []
        
        # Create concentric oscillators
        for i in range(5):
            radius = i * 5 + 5
            for j in range(8):  # 8 points around circle
                angle = j * 3.14159 / 4  # 45 degree increments
                x = int(radius * math.cos(angle))
                y = int(radius * math.sin(angle))
                patterns["3D Illusion"].append((x + 25, y + 25))
                patterns["3D Illusion"].append((x + 26, y + 25))
                patterns["3D Illusion"].append((x + 25, y + 26))
        
        # Replicator - A pattern that replicates itself
        patterns["Replicator"] = []
        base_replicator = [
            (0, 0), (1, 0), (0, 1), (2, 1), (2, 2), (3, 2), 
            (1, 3), (2, 3), (3, 3), (4, 3), (0, 4), (4, 4)
        ]
        for x, y in base_replicator:
            patterns["Replicator"].append((x, y))
        
        # Add a second copy starting to form
        second_copy = [(x + 10, y + 10) for x, y in base_replicator]
        for x, y in second_copy:
            patterns["Replicator"].append((x, y))
        
        # Mega Gun Array - Large array of guns creating massive glider streams
        patterns["Mega Gun Array"] = []
        
        # Create a 3x3 grid of guns
        for i in range(3):
            for j in range(3):
                gun_offset_x = i * 50
                gun_offset_y = j * 50
                for x, y in patterns["Glider Gun"]:
                    patterns["Mega Gun Array"].append((x + gun_offset_x, y + gun_offset_y))
        
        # Add eaters at various positions to create interesting patterns
        eater_positions = [
            (45, 15), (95, 15), (145, 15),
            (45, 65), (145, 65),
            (45, 115), (95, 115), (145, 115)
        ]
        
        for pos in eater_positions:
            for x, y in patterns["Glider Eater"]:
                patterns["Mega Gun Array"].append((x + pos[0], y + pos[1]))
        
        # Universal Computer - Simplified version of a universal computer design
        patterns["Universal Computer"] = []
        
        # Memory region (simplified)
        for i in range(10):
            patterns["Universal Computer"].append((i*5, 0))
            patterns["Universal Computer"].append((i*5 + 1, 0))
            patterns["Universal Computer"].append((i*5, 1))
            patterns["Universal Computer"].append((i*5 + 1, 1))
        
        # Processing unit (simplified)
        processor = [
            (20, 20), (21, 20), (22, 20),
            (20, 21), (22, 21),
            (20, 22), (21, 22), (22, 22),
            (25, 20), (26, 20), (27, 20),
            (25, 21), (27, 21),
            (25, 22), (26, 22), (27, 22)
        ]
        for x, y in processor:
            patterns["Universal Computer"].append((x, y))
        
        # Connecting pathways
        for i in range(15):
            if i % 3 != 0:  # Skip every third cell to create a dotted line
                patterns["Universal Computer"].append((i + 5, 10))
        
        # Output register
        output = [(40, 40), (41, 40), (42, 40), (40, 41), (42, 41), (40, 42), (41, 42), (42, 42)]
        for x, y in output:
            patterns["Universal Computer"].append((x, y))
        
        # Running Glider Team - Group of gliders in a circular pattern
        patterns["Running Glider Team"] = []
        # Create 8 gliders arranged in a circle, each pointing along tangent
        radius = 20
        for i in range(8):
            angle = i * 3.14159 / 4  # 45 degree increments
            center_x = int(radius * math.cos(angle)) + 25
            center_y = int(radius * math.sin(angle)) + 25
            
            # Determine orientation based on position in circle
            if i == 0:  # Right
                glider = [(center_x, center_y), (center_x+1, center_y), (center_x+2, center_y), 
                          (center_x+2, center_y-1), (center_x+1, center_y-2)]
            elif i == 1:  # Bottom right
                glider = [(center_x, center_y), (center_x+1, center_y+1), (center_x+2, center_y), 
                          (center_x, center_y+2), (center_x+2, center_y+2)]
            elif i == 2:  # Bottom
                glider = [(center_x, center_y), (center_x, center_y+1), (center_x, center_y+2), 
                          (center_x-1, center_y+2), (center_x-2, center_y+1)]
            elif i == 3:  # Bottom left
                glider = [(center_x, center_y), (center_x-1, center_y+1), (center_x-2, center_y), 
                          (center_x, center_y+2), (center_x-2, center_y+2)]
            elif i == 4:  # Left
                glider = [(center_x, center_y), (center_x-1, center_y), (center_x-2, center_y), 
                          (center_x-2, center_y+1), (center_x-1, center_y+2)]
            elif i == 5:  # Top left
                glider = [(center_x, center_y), (center_x-1, center_y-1), (center_x-2, center_y), 
                          (center_x, center_y-2), (center_x-2, center_y-2)]
            elif i == 6:  # Top
                glider = [(center_x, center_y), (center_x, center_y-1), (center_x, center_y-2), 
                          (center_x+1, center_y-2), (center_x+2, center_y-1)]
            else:  # Top right
                glider = [(center_x, center_y), (center_x+1, center_y-1), (center_x+2, center_y), 
                          (center_x, center_y-2), (center_x+2, center_y-2)]
            
            for x, y in glider:
                patterns["Running Glider Team"].append((x, y))
                
        return patterns
        
    def categorize_patterns(self):
        """Organize patterns into categories"""
        categories = {
            "Still Lifes": ["Block", "Beehive", "Loaf", "Boat", "Tub"],
            "Oscillators": ["Blinker", "Toad", "Beacon", "Pulsar", "Pentadecathlon", "Clock", "Figure 8", "Queen Bee Shuttle", "Max"],
            "Spaceships": ["Glider", "LWSS", "MWSS", "HWSS", "Weekender", "Copperhead"],
            "Guns & Puffers": ["Glider Gun", "Simkin Glider Gun", "B-heptomino Puffer", "HWSS Factory", "Pufferfish", "Spacefiller", "Quad-Gun", "Mega Gun Array"],
            "Methuselahs": ["R-pentomino", "Diehard", "Acorn", "Brain", "Pi-heptomino", "Thunderbird", "Switch Engine", "3D Illusion"],
            "Special": ["Garden of Eden", "Cross", "Star", "Glider Eater", "Running Glider Team", "Replicator"],
            "Complex Growth": ["Breeder 1", "Multi-Engine Spaceship Factory"],
            "Computational": ["Simple Computer Memory", "AND Gate", "Turing Machine", "Prime Number Generator", "Universal Computer"]
        }
        return categories
    
    def parse_rules(self, rule_string):
        """Parse rule string like B3/S23 into birth and survival conditions."""
        birth = []
        survival = []
        
        parts = rule_string.split('/')
        if len(parts) == 2:
            if parts[0].startswith('B'):
                birth = [int(c) for c in parts[0][1:] if c.isdigit()]
            if parts[1].startswith('S'):
                survival = [int(c) for c in parts[1][1:] if c.isdigit()]
        
        return {"birth": birth, "survival": survival}
    
    def step(self):
        """Advance the simulation by one generation."""
        # Save current state to history
        if len(self.history) >= self.max_history:
            self.history.pop(0)
            self.history_position -= 1
        
        if self.history_position < len(self.history) - 1:
            self.history = self.history[:self.history_position + 1]
        
        self.history.append(dict(self.cells))
        self.history_position = len(self.history) - 1
        
        # Calculate next generation
        neighbors = defaultdict(int)
        
        # Count neighbors for all cells
        for (x, y) in self.cells:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    neighbors[(x + dx, y + dy)] += 1
        
        # Apply rules
        new_cells = defaultdict(int)
        for cell, count in neighbors.items():
            if cell in self.cells:
                # Cell is alive
                if count in self.rules["survival"]:
                    new_cells[cell] = self.cells[cell] + 1  # Increment age
            else:
                # Cell is dead
                if count in self.rules["birth"]:
                    new_cells[cell] = 1  # New born cell
        
        self.cells = new_cells
        self.generation += 1
        
    def undo(self):
        """Go back one generation."""
        if self.history_position > 0:
            self.history_position -= 1
            self.cells = defaultdict(int, self.history[self.history_position])
            self.generation -= 1
            return True
        return False
    
    def redo(self):
        """Go forward one generation if available."""
        if self.history_position < len(self.history) - 1:
            self.history_position += 1
            self.cells = defaultdict(int, self.history[self.history_position])
            self.generation += 1
            return True
        return False
    
    def add_cell(self, x, y):
        """Add a live cell at the specified position."""
        self.cells[(x, y)] = 1
    
    def remove_cell(self, x, y):
        """Remove a cell at the specified position."""
        if (x, y) in self.cells:
            del self.cells[(x, y)]
    
    def clear(self):
        """Clear all cells from the grid."""
        self.cells.clear()
        self.generation = 0
        # Add a new history entry for the clear state
        self.history.append(dict())
        self.history_position = len(self.history) - 1
        
    def add_pattern(self, pattern_name, center_x, center_y):
        """Add a predefined pattern centered at the given coordinates."""
        if pattern_name in self.patterns:
            pattern = self.patterns[pattern_name]
            
            # Calculate bounding box
            min_x = min(x for x, y in pattern)
            max_x = max(x for x, y in pattern)
            min_y = min(y for x, y in pattern)
            max_y = max(y for x, y in pattern)
            
            # Calculate center offset
            offset_x = center_x - (min_x + max_x) // 2
            offset_y = center_y - (min_y + max_y) // 2
            
            # Add pattern cells
            for x, y in pattern:
                self.add_cell(x + offset_x, y + offset_y)
            
            return True
        return False
    
    def set_rules(self, rule_string):
        """Set new rules for the simulation."""
        self.rules = self.parse_rules(rule_string)
        self.rule_string = rule_string
        return True
    
    # Additional methods for pattern manipulation, etc.


class GameOfLifeUI:
    """Main UI class handling the graphical interface and user interactions."""
    
    def __init__(self):
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
        pygame.display.set_caption("Ultimate Game of Life")
        
        # Initialize game
        self.game = GameOfLife()
        
        # Add some initial cells to make the grid not empty
        self.game.add_pattern("Glider", 10, 10)
        
        # View settings
        self.cell_size = 10
        self.offset_x = 400
        self.offset_y = 300
        self.paused = True
        self.simulation_speed = 10  # FPS
        
        # Mouse tracking
        self.mouse_pos = (0, 0)
        self.drawing = False
        self.erasing = False
        self.panning = False
        self.pan_start = (0, 0)
        
        # Pattern placement mode
        self.placing_pattern = False
        self.selected_pattern = None
        
        # UI constants - use consistent spacing values
        self.UI_BUTTON_HEIGHT = 30
        self.UI_BUTTON_SPACING = 5
        self.UI_SIDEBAR_WIDTH = 180  # Increased width for better pattern names display
        
        # Pattern selection
        self.pattern_categories = list(self.game.pattern_categories.keys())
        self.selected_category = self.pattern_categories[0]  # Default to first category
        self.pattern_scroll_y = 0
        self.patterns_per_page = 8  # Number of patterns visible at once
        
        # Color themes
        self.color_themes = {
            "Default": {
                "bg": (30, 30, 30),
                "grid": (50, 50, 50),
                "button": (80, 80, 80),
                "button_highlight": (100, 100, 160),
                "button_active": (100, 160, 100),
                "text": (255, 255, 255),
                "text_highlight": (255, 255, 100),
                "sidebar_bg": (40, 40, 45),
                "cell_new": (200, 220, 255),
                "cell_young": (100, 150, 255),
                "cell_adult": (120, 100, 220),
                "cell_old_base": (80, 60, 160),
                "cell_glow": (100, 220, 120)
            },
            "Light": {
                "bg": (240, 240, 240),
                "grid": (180, 180, 180),
                "button": (200, 200, 200),
                "button_highlight": (180, 180, 220),
                "button_active": (150, 200, 150),
                "text": (20, 20, 20),
                "text_highlight": (0, 0, 100),
                "sidebar_bg": (220, 220, 225),
                "cell_new": (50, 100, 255),
                "cell_young": (80, 120, 220),
                "cell_adult": (100, 70, 200),
                "cell_old_base": (130, 90, 200),
                "cell_glow": (50, 180, 50)
            },
            "High Contrast": {
                "bg": (0, 0, 0),
                "grid": (40, 40, 40),
                "button": (60, 60, 60),
                "button_highlight": (90, 90, 160),
                "button_active": (90, 150, 90),
                "text": (255, 255, 255),
                "text_highlight": (255, 255, 0),
                "sidebar_bg": (30, 30, 35),
                "cell_new": (255, 255, 255),
                "cell_young": (200, 200, 255),
                "cell_adult": (150, 100, 255),
                "cell_old_base": (180, 120, 255),
                "cell_glow": (100, 255, 100)
            },
            "Neon": {
                "bg": (10, 10, 20),
                "grid": (30, 30, 50),
                "button": (50, 50, 70),
                "button_highlight": (80, 50, 130),
                "button_active": (50, 130, 80),
                "text": (220, 220, 255),
                "text_highlight": (255, 255, 0),
                "sidebar_bg": (20, 20, 35),
                "cell_new": (0, 255, 255),
                "cell_young": (0, 200, 255),
                "cell_adult": (0, 100, 255),
                "cell_old_base": (80, 0, 255),
                "cell_glow": (0, 255, 100)
            }
        }
        
        # Current color theme
        self.current_theme = "Default"
        
        # Settings menu state
        self.show_settings = False
        self.settings_rect = pygame.Rect(
            self.screen.get_width() // 2 - 200,
            self.screen.get_height() // 2 - 150,
            400, 300
        )
        
        # Colors - will be set from theme
        self.COLOR_BG = (30, 30, 30)
        self.COLOR_GRID = (50, 50, 50)
        self.COLOR_BUTTON = (80, 80, 80)
        self.COLOR_BUTTON_HIGHLIGHT = (100, 100, 160)
        self.COLOR_BUTTON_ACTIVE = (100, 160, 100)
        self.COLOR_TEXT = (255, 255, 255)
        self.COLOR_TEXT_HIGHLIGHT = (255, 255, 100)
        self.COLOR_SIDEBAR_BG = (40, 40, 45)
        
        # Rule presets
        self.rule_presets = {
            "Conway's Life": "B3/S23",
            "HighLife": "B36/S23",
            "Day & Night": "B3678/S34678",
            "Seeds": "B2/S",
            "Maze": "B3/S12345"
        }
        
        # UI elements
        self.font = pygame.font.SysFont('Arial', 16)
        self.font_bold = pygame.font.SysFont('Arial', 16, bold=True)
        self.font_small = pygame.font.SysFont('Arial', 14)
        self.font_title = pygame.font.SysFont('Arial', 18, bold=True)
        
        # Main buttons
        self.btn_pause = pygame.Rect(10, 10, 80, 30)
        self.btn_step = pygame.Rect(100, 10, 80, 30)
        self.btn_clear = pygame.Rect(190, 10, 80, 30)
        
        # Speed control - repositioned for better spacing
        self.btn_speed_down = pygame.Rect(320, 10, 30, 30)
        self.btn_speed_up = pygame.Rect(280, 10, 30, 30)
        
        # Settings button moved further to the right
        self.btn_settings = pygame.Rect(440, 10, 80, 30)
        
        # Pattern panel
        self.sidebar_rect = pygame.Rect(10, 50, self.UI_SIDEBAR_WIDTH, self.screen.get_height() - 100)
        
        # Category tabs
        self.category_tabs = []
        self.create_category_tabs()
        
        # Pattern list area
        self.pattern_area = pygame.Rect(
            self.sidebar_rect.x + 5, 
            self.sidebar_rect.y + 80,  # Leave space for category tabs
            self.UI_SIDEBAR_WIDTH - 10,
            self.sidebar_rect.height - 120
        )
        
        # Scroll buttons
        self.pattern_scroll_up = pygame.Rect(
            self.sidebar_rect.right - 25, 
            self.pattern_area.y, 
            20, 20
        )
        self.pattern_scroll_down = pygame.Rect(
            self.sidebar_rect.right - 25, 
            self.pattern_area.bottom - 20, 
            20, 20
        )
        
        # Rule buttons
        self.rule_buttons = {}
        self.create_rule_buttons()
        
        # Pattern information
        self.pattern_info_rect = pygame.Rect(
            self.sidebar_rect.x + 5,
            self.pattern_area.bottom + 10,
            self.UI_SIDEBAR_WIDTH - 10,
            80
        )
        
        # Help text area - positioned at bottom right instead of bottom left
        self.help_text_rect = pygame.Rect(
            self.screen.get_width() - 600,
            self.screen.get_height() - 40,
            590, 30
        )
        
        # Setup temporary surface for pattern preview
        self.preview_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        
        # Apply the current theme colors - after all UI elements are initialized
        self.apply_theme(self.current_theme)
        
        # Main loop
        self.clock = pygame.time.Clock()
        self.running = True
    
    def apply_theme(self, theme_name):
        """Apply the selected color theme with a smooth transition"""
        if theme_name in self.color_themes:
            new_theme = self.color_themes[theme_name]
            
            # During initial setup, just set the colors directly without animation
            if hasattr(self, 'running') and self.running:
                # This is a user-triggered change, not initial setup
                old_theme = self.color_themes[self.current_theme]
                
                # Create a transition animation
                start_time = pygame.time.get_ticks()
                transition_duration = 300  # milliseconds
                
                # Function to interpolate between colors
                def interpolate_color(color1, color2, progress):
                    r = int(color1[0] + (color2[0] - color1[0]) * progress)
                    g = int(color1[1] + (color2[1] - color1[1]) * progress)
                    b = int(color1[2] + (color2[2] - color1[2]) * progress)
                    return (r, g, b)
                
                # Animate the transition
                while True:
                    current_time = pygame.time.get_ticks()
                    elapsed = current_time - start_time
                    
                    if elapsed >= transition_duration:
                        # Transition complete
                        break
                    
                    # Calculate transition progress (0 to 1)
                    progress = elapsed / transition_duration
                    
                    # Interpolate colors
                    self.COLOR_BG = interpolate_color(old_theme["bg"], new_theme["bg"], progress)
                    self.COLOR_GRID = interpolate_color(old_theme["grid"], new_theme["grid"], progress)
                    self.COLOR_BUTTON = interpolate_color(old_theme["button"], new_theme["button"], progress)
                    self.COLOR_BUTTON_HIGHLIGHT = interpolate_color(old_theme["button_highlight"], new_theme["button_highlight"], progress)
                    self.COLOR_BUTTON_ACTIVE = interpolate_color(old_theme["button_active"], new_theme["button_active"], progress)
                    self.COLOR_TEXT = interpolate_color(old_theme["text"], new_theme["text"], progress)
                    self.COLOR_TEXT_HIGHLIGHT = interpolate_color(old_theme["text_highlight"], new_theme["text_highlight"], progress)
                    self.COLOR_SIDEBAR_BG = interpolate_color(old_theme["sidebar_bg"], new_theme["sidebar_bg"], progress)
                    
                    # Render a frame
                    self.render()
                    self.clock.tick(60)  # Cap at 60fps for the transition
            
            # Set final colors
            self.current_theme = theme_name
            self.COLOR_BG = new_theme["bg"]
            self.COLOR_GRID = new_theme["grid"]
            self.COLOR_BUTTON = new_theme["button"]
            self.COLOR_BUTTON_HIGHLIGHT = new_theme["button_highlight"]
            self.COLOR_BUTTON_ACTIVE = new_theme["button_active"]
            self.COLOR_TEXT = new_theme["text"]
            self.COLOR_TEXT_HIGHLIGHT = new_theme["text_highlight"]
            self.COLOR_SIDEBAR_BG = new_theme["sidebar_bg"]
    
    def create_category_tabs(self):
        """Create tabs for each pattern category"""
        tab_width = self.UI_SIDEBAR_WIDTH // 2
        tab_height = 25
        x_pos = self.sidebar_rect.x
        y_pos = self.sidebar_rect.y + 5
        
        for i, category in enumerate(self.pattern_categories):
            # Create tab in 2 columns
            col = i % 2
            row = i // 2
            
            tab_rect = pygame.Rect(
                x_pos + col * tab_width,
                y_pos + row * (tab_height + 3),
                tab_width - 3,
                tab_height
            )
            
            self.category_tabs.append({
                "name": category,
                "rect": tab_rect
            })
    
    def create_rule_buttons(self):
        """Create buttons for each rule preset."""
        x_pos = self.screen.get_width() - 130
        y_pos = 120
        btn_width = 120
        btn_height = self.UI_BUTTON_HEIGHT
        spacing = self.UI_BUTTON_SPACING
        
        for rule_name in self.rule_presets:
            self.rule_buttons[rule_name] = pygame.Rect(x_pos, y_pos, btn_width, btn_height)
            y_pos += btn_height + spacing
    
    def add_glider(self, x, y):
        """Add a glider pattern at the specified position."""
        self.game.add_pattern("Glider", x, y)
    
    def run(self):
        """Main application loop."""
        while self.running:
            self.handle_events()
            
            if not self.paused:
                self.game.step()
            
            self.render()
            self.clock.tick(self.simulation_speed)
    
    def handle_events(self):
        """Process user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_button_down(event)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_button_up(event)
            
            elif event.type == pygame.MOUSEMOTION:
                self.handle_mouse_motion(event)
            
            elif event.type == pygame.KEYDOWN:
                self.handle_key_down(event)
            
            elif event.type == pygame.MOUSEWHEEL:
                self.handle_mouse_wheel(event)
            
            elif event.type == pygame.VIDEORESIZE:
                self.handle_video_resize(event)
    
    def handle_mouse_button_down(self, event):
        """Handle mouse button press events."""
        if event.button == 1:  # Left click
            # Check if buttons were clicked
            mouse_pos = pygame.mouse.get_pos()
            
            # If settings panel is open, check for interactions with it first
            if self.show_settings:
                # Check if close button was clicked
                close_btn = pygame.Rect(self.settings_rect.right - 30, self.settings_rect.y + 10, 20, 20)
                if close_btn.collidepoint(mouse_pos):
                    self.show_settings = False
                    return
                
                # Check if a theme button was clicked
                theme_btn_y = self.settings_rect.y + 90
                btn_height = 30
                btn_spacing = 10
                btn_width = self.settings_rect.width - 40
                
                for i, theme_name in enumerate(self.color_themes.keys()):
                    btn_rect = pygame.Rect(
                        self.settings_rect.x + 20,
                        theme_btn_y + i * (btn_height + btn_spacing),
                        btn_width,
                        btn_height
                    )
                    
                    if btn_rect.collidepoint(mouse_pos):
                        self.apply_theme(theme_name)
                        return
                
                # Clicked somewhere else in the settings - don't process further
                return
            
            # Check UI buttons
            if self.btn_pause.collidepoint(mouse_pos):
                self.paused = not self.paused
            elif self.btn_step.collidepoint(mouse_pos):
                self.game.step()
            elif self.btn_clear.collidepoint(mouse_pos):
                self.game.clear()
            elif self.btn_settings.collidepoint(mouse_pos):
                self.show_settings = True
            elif self.btn_speed_up.collidepoint(mouse_pos):
                self.simulation_speed = min(60, self.simulation_speed + 5)
            elif self.btn_speed_down.collidepoint(mouse_pos):
                self.simulation_speed = max(1, self.simulation_speed - 5)
            elif self.pattern_scroll_up.collidepoint(mouse_pos):
                self.pattern_scroll_y = max(0, self.pattern_scroll_y - 1)
            elif self.pattern_scroll_down.collidepoint(mouse_pos):
                # Calculate maximum scroll based on current category
                if self.selected_category in self.game.pattern_categories:
                    patterns_in_category = len(self.game.pattern_categories[self.selected_category])
                    max_scroll = max(0, patterns_in_category - self.patterns_per_page)
                    self.pattern_scroll_y = min(max_scroll, self.pattern_scroll_y + 1)
            else:
                # Check category tabs
                category_clicked = False
                for tab in self.category_tabs:
                    if tab["rect"].collidepoint(mouse_pos):
                        self.selected_category = tab["name"]
                        self.pattern_scroll_y = 0  # Reset scroll when changing category
                        category_clicked = True
                        break
                
                if not category_clicked:
                    # Check rule buttons
                    rule_clicked = False
                    for rule_name, btn_rect in self.rule_buttons.items():
                        if btn_rect.collidepoint(mouse_pos):
                            self.game.set_rules(self.rule_presets[rule_name])
                            rule_clicked = True
                            break
                    
                    if not rule_clicked:
                        # Check if a pattern was clicked in the pattern area
                        pattern_clicked = self.check_pattern_button_click(mouse_pos)
                        
                        if not pattern_clicked:
                            if self.placing_pattern and self.selected_pattern:
                                # Place the selected pattern
                                grid_x = (mouse_pos[0] - self.offset_x) // self.cell_size
                                grid_y = (mouse_pos[1] - self.offset_y) // self.cell_size
                                self.game.add_pattern(self.selected_pattern, grid_x, grid_y)
                                # Don't cancel placement mode - allow placing multiple patterns
                            else:
                                # Start drawing cells - regardless of paused state
                                self.drawing = True
                                self.handle_cell_drawing(mouse_pos)
        
        elif event.button == 3:  # Right click
            # Cancel pattern placement or start erasing
            if self.placing_pattern:
                self.placing_pattern = False
                self.selected_pattern = None
            else:
                # Start erasing cells
                self.erasing = True
                self.handle_cell_erasing(pygame.mouse.get_pos())
        
        elif event.button == 2:  # Middle click
            # Start panning
            self.panning = True
            self.pan_start = pygame.mouse.get_pos()
        
        elif event.button == 4:  # Mouse wheel up
            if self.pattern_area.collidepoint(pygame.mouse.get_pos()):
                # Scroll pattern list
                self.pattern_scroll_y = max(0, self.pattern_scroll_y - 1)
            else:
                # Zoom in
                self.handle_zoom(True)
        
        elif event.button == 5:  # Mouse wheel down
            if self.pattern_area.collidepoint(pygame.mouse.get_pos()):
                # Scroll pattern list - calculate max scroll based on selected category
                if self.selected_category in self.game.pattern_categories:
                    patterns_in_category = len(self.game.pattern_categories[self.selected_category])
                    max_scroll = max(0, patterns_in_category - self.patterns_per_page)
                    self.pattern_scroll_y = min(max_scroll, self.pattern_scroll_y + 1)
            else:
                # Zoom out
                self.handle_zoom(False)
    
    def handle_mouse_button_up(self, event):
        """Handle mouse button release events."""
        if event.button == 1:
            self.drawing = False
        elif event.button == 3:
            self.erasing = False
        elif event.button == 2:
            self.panning = False
    
    def handle_mouse_motion(self, event):
        """Handle mouse movement events."""
        self.mouse_pos = event.pos
        if self.drawing:
            self.handle_cell_drawing(event.pos)
        elif self.erasing:
            self.handle_cell_erasing(event.pos)
        elif self.panning:
            # Handle panning the view
            current_pos = pygame.mouse.get_pos()
            dx = current_pos[0] - self.pan_start[0]
            dy = current_pos[1] - self.pan_start[1]
            self.offset_x += dx
            self.offset_y += dy
            self.pan_start = current_pos
    
    def handle_key_down(self, event):
        """Handle keyboard input events."""
        if event.key == pygame.K_ESCAPE:
            # If settings panel is open, close it
            if self.show_settings:
                self.show_settings = False
            # Otherwise cancel pattern placement
            elif self.placing_pattern:
                self.placing_pattern = False
                self.selected_pattern = None
        elif event.key == pygame.K_SPACE:
            self.paused = not self.paused
        elif event.key == pygame.K_s:
            # Use 'S' key for stepping instead of right arrow
            self.game.step()
        elif event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
            self.game.undo()
        elif event.key == pygame.K_y and pygame.key.get_mods() & pygame.KMOD_CTRL:
            self.game.redo()
        # Arrow keys for panning - always available
        elif event.key == pygame.K_UP:
            self.offset_y += 20
        elif event.key == pygame.K_DOWN:
            self.offset_y -= 20
        elif event.key == pygame.K_LEFT:
            self.offset_x += 20
        elif event.key == pygame.K_RIGHT:
            self.offset_x -= 20
    
    def handle_mouse_wheel(self, event):
        """Handle mouse wheel events."""
        if self.pattern_area.collidepoint(pygame.mouse.get_pos()):
            # Scroll pattern list
            self.pattern_scroll_y = max(0, self.pattern_scroll_y - event.y)
            # Use pattern_categories instead of non-existent pattern_names
            if self.selected_category in self.game.pattern_categories:
                patterns_in_category = len(self.game.pattern_categories[self.selected_category])
                max_scroll = max(0, patterns_in_category - self.patterns_per_page)
                self.pattern_scroll_y = min(max_scroll, self.pattern_scroll_y)
        else:
            # Handle zooming
            self.handle_zoom(event.y > 0)
    
    def handle_video_resize(self, event):
        """Handle window resize events."""
        width, height = event.size
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.preview_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Update sidebar position and size
        self.sidebar_rect.height = height - 100
        
        # Update pattern area size
        self.pattern_area.height = self.sidebar_rect.height - 120
        
        # Update scroll button positions
        self.pattern_scroll_down.y = self.pattern_area.bottom - 20
        
        # Update pattern info rect
        self.pattern_info_rect.y = self.pattern_area.bottom + 10
        
        # Update help text position
        self.help_text_rect.x = width - 600
        self.help_text_rect.y = height - 40
        
        # Update settings panel position
        self.settings_rect = pygame.Rect(
            width // 2 - 200,
            height // 2 - 150,
            400, 300
        )
        
        # Recreate rule buttons on the right side
        self.rule_buttons = {}
        self.create_rule_buttons()
    
    def handle_zoom(self, zoom_in):
        """Handle zooming in or out."""
        # Calculate zoom center point (mouse position)
        zoom_center_x = (self.mouse_pos[0] - self.offset_x) / self.cell_size
        zoom_center_y = (self.mouse_pos[1] - self.offset_y) / self.cell_size
        
        # Adjust cell size
        if zoom_in:
            # Increase cell size (zoom in)
            self.cell_size = min(50, self.cell_size + 1)
        else:
            # Decrease cell size (zoom out)
            self.cell_size = max(2, self.cell_size - 1)
        
        # Adjust offset to keep zoom centered on mouse
        self.offset_x = self.mouse_pos[0] - zoom_center_x * self.cell_size
        self.offset_y = self.mouse_pos[1] - zoom_center_y * self.cell_size
    
    def handle_cell_drawing(self, pos):
        """Add a live cell at the current mouse position."""
        grid_x = (pos[0] - self.offset_x) // self.cell_size
        grid_y = (pos[1] - self.offset_y) // self.cell_size
        self.game.add_cell(grid_x, grid_y)
    
    def handle_cell_erasing(self, pos):
        """Remove a cell at the current mouse position."""
        grid_x = (pos[0] - self.offset_x) // self.cell_size
        grid_y = (pos[1] - self.offset_y) // self.cell_size
        self.game.remove_cell(grid_x, grid_y)
    
    def render(self):
        """Render the current state of the simulation."""
        # Clear screen with background color
        self.screen.fill(self.COLOR_BG)
        
        # Draw grid
        self.render_grid()
        
        # Draw cells
        self.render_cells()
        
        # Draw UI elements
        self.render_ui()
        
        # Show pattern preview if placing a pattern
        if self.placing_pattern and self.selected_pattern:
            self.render_pattern_preview()
        # Show current cell under cursor
        elif not self.panning:  # Always show cursor when not panning, regardless of paused state
            grid_x = (self.mouse_pos[0] - self.offset_x) // self.cell_size
            grid_y = (self.mouse_pos[1] - self.offset_y) // self.cell_size
            screen_x = grid_x * self.cell_size + self.offset_x
            screen_y = grid_y * self.cell_size + self.offset_y
            pygame.draw.rect(self.screen, (70, 70, 70), 
                           (screen_x, screen_y, self.cell_size, self.cell_size), 1)
        
        # Update display
        pygame.display.flip()
    
    def render_cells(self):
        """Render all active cells in the grid."""
        # Optimize by only rendering cells in the visible area
        visible_width = self.screen.get_width()
        visible_height = self.screen.get_height()
        
        # Calculate grid bounds that are visible
        min_visible_x = (0 - self.offset_x) // self.cell_size - 1
        min_visible_y = (0 - self.offset_y) // self.cell_size - 1
        max_visible_x = (visible_width - self.offset_x) // self.cell_size + 1
        max_visible_y = (visible_height - self.offset_y) // self.cell_size + 1
        
        for (x, y), age in self.game.cells.items():
            # Skip cells outside visible area for performance
            if not (min_visible_x <= x <= max_visible_x and min_visible_y <= y <= max_visible_y):
                continue
                
            screen_x = x * self.cell_size + self.offset_x
            screen_y = y * self.cell_size + self.offset_y
            
            # Determine cell color based on age
            color = self.get_cell_color(age)
            
            # Draw the cell - with a subtle glow effect for newer cells
            if age <= 3:  # Newer cells get a glow effect
                # Draw inner cell
                pygame.draw.rect(self.screen, color, 
                               (screen_x, screen_y, self.cell_size, self.cell_size))
                
                # Draw glow if cell size is large enough
                if self.cell_size >= 6:
                    glow_color = (*color[:3], 80)  # Semi-transparent
                    glow_size = self.cell_size + 2
                    glow_pos = (screen_x - 1, screen_y - 1)
                    
                    # Create a temporary surface for the glow
                    glow_surface = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
                    pygame.draw.rect(glow_surface, glow_color, (0, 0, glow_size, glow_size))
                    
                    # Blit the glow surface
                    self.screen.blit(glow_surface, glow_pos)
            else:
                # Regular cell rendering for older cells
                pygame.draw.rect(self.screen, color, 
                               (screen_x, screen_y, self.cell_size, self.cell_size))
                
                # Add a subtle pulse effect to older cells to keep them visible
                if age > 15 and age % 20 < 10 and self.cell_size >= 4:
                    # Create a subtle border for older cells
                    border_color = (*color[:3], 150)
                    pygame.draw.rect(self.screen, border_color, 
                                   (screen_x, screen_y, self.cell_size, self.cell_size), 1)
    
    def render_grid(self):
        """Draw the grid lines."""
        if self.cell_size >= 5:  # Only draw grid when zoomed in enough
            # Calculate visible grid bounds
            start_x = int((0 - self.offset_x) // self.cell_size)
            start_y = int((0 - self.offset_y) // self.cell_size)
            end_x = int((self.screen.get_width() - self.offset_x) // self.cell_size) + 1
            end_y = int((self.screen.get_height() - self.offset_y) // self.cell_size) + 1
            
            # Make coordinate axes colors based on theme
            axes_color = (self.COLOR_GRID[0] + 30, self.COLOR_GRID[1] + 30, self.COLOR_GRID[2] + 30)
            
            # Draw vertical lines
            for x in range(start_x, end_x):
                screen_x = x * self.cell_size + self.offset_x
                # Make coordinate axes slightly brighter
                line_color = axes_color if x == 0 else self.COLOR_GRID
                pygame.draw.line(self.screen, line_color, 
                               (screen_x, 0), (screen_x, self.screen.get_height()))
                
                # Show coordinate labels when zoomed in enough
                if self.cell_size >= 20 and x % 5 == 0 and x != 0:
                    # Draw coordinate number
                    coord_text = self.font_small.render(str(x), True, self.COLOR_TEXT)
                    self.screen.blit(coord_text, (screen_x + 2, self.offset_y + 2))
            
            # Draw horizontal lines
            for y in range(start_y, end_y):
                screen_y = y * self.cell_size + self.offset_y
                # Make coordinate axes slightly brighter
                line_color = axes_color if y == 0 else self.COLOR_GRID
                pygame.draw.line(self.screen, line_color, 
                               (0, screen_y), (self.screen.get_width(), screen_y))
                
                # Show coordinate labels when zoomed in enough
                if self.cell_size >= 20 and y % 5 == 0 and y != 0:
                    # Draw coordinate number
                    coord_text = self.font_small.render(str(y), True, self.COLOR_TEXT)
                    self.screen.blit(coord_text, (self.offset_x + 2, screen_y + 2))
            
            # Draw origin point if visible
            origin_x = 0 * self.cell_size + self.offset_x
            origin_y = 0 * self.cell_size + self.offset_y
            if (0 <= origin_x < self.screen.get_width() and 
                0 <= origin_y < self.screen.get_height()):
                # Draw a small marker at the origin
                marker_size = max(3, self.cell_size // 4)
                marker_color = axes_color
                pygame.draw.rect(self.screen, marker_color, 
                               (origin_x - marker_size//2, origin_y - marker_size//2, 
                                marker_size, marker_size))
                
                # Add "0,0" label when zoomed in enough
                if self.cell_size >= 20:
                    origin_text = self.font_small.render("0,0", True, self.COLOR_TEXT)
                    self.screen.blit(origin_text, (origin_x + marker_size, origin_y + marker_size))
    
    def get_cell_color(self, age):
        """Calculate cell color based on age."""
        theme = self.color_themes[self.current_theme]
        if age <= 1:  # New cells
            return theme["cell_new"]
        elif age <= 5:  # Young cells
            return theme["cell_young"]
        elif age <= 15:  # Medium age cells
            return theme["cell_adult"]
        else:  # Old cells with improved visibility
            # Calculate a better color that doesn't get too dark
            base_color = theme["cell_old_base"]
            # Add slight pulsation based on age to make older cells more distinct
            pulse = (age % 10) / 10  # Creates a value between 0 and 0.9
            r = min(255, base_color[0] + int(pulse * 30))
            g = min(255, base_color[1] + int(pulse * 20))
            b = min(255, base_color[2] + int(pulse * 40))
            return (r, g, b)
    
    def render_pattern_preview(self):
        """Render a preview of the pattern being placed."""
        if not self.selected_pattern or self.selected_pattern not in self.game.patterns:
            return
            
        pattern = self.game.patterns[self.selected_pattern]
        theme = self.color_themes[self.current_theme]
        
        # Calculate grid position
        grid_x = (self.mouse_pos[0] - self.offset_x) // self.cell_size
        grid_y = (self.mouse_pos[1] - self.offset_y) // self.cell_size
        
        # Calculate bounding box
        min_x = min(x for x, y in pattern)
        max_x = max(x for x, y in pattern)
        min_y = min(y for x, y in pattern)
        max_y = max(y for x, y in pattern)
        
        # Calculate center offset
        offset_x = grid_x - (min_x + max_x) // 2
        offset_y = grid_y - (min_y + max_y) // 2
        
        # Clear the preview surface
        self.preview_surface.fill((0, 0, 0, 0))
        
        # Draw a bounding box for the pattern
        bounding_width = (max_x - min_x + 1) * self.cell_size
        bounding_height = (max_y - min_y + 1) * self.cell_size
        bounding_x = (min_x + offset_x) * self.cell_size + self.offset_x
        bounding_y = (min_y + offset_y) * self.cell_size + self.offset_y
        
        # Draw the bounding box with a nice gradient effect
        for i in range(2):
            # Gradient from theme color to transparent
            alpha = 120 - i * 40
            glow_color = theme["cell_glow"]
            color = (glow_color[0], glow_color[1], glow_color[2], alpha)
            border_rect = pygame.Rect(
                bounding_x - i, 
                bounding_y - i,
                bounding_width + i*2,
                bounding_height + i*2
            )
            pygame.draw.rect(self.preview_surface, color, border_rect, 1)
        
        # Draw pattern preview cells with semi-transparency
        for x, y in pattern:
            screen_x = (x + offset_x) * self.cell_size + self.offset_x
            screen_y = (y + offset_y) * self.cell_size + self.offset_y
            
            # Skip rendering cells outside view
            if (screen_x + self.cell_size < 0 or screen_x > self.screen.get_width() or
                screen_y + self.cell_size < 0 or screen_y > self.screen.get_height()):
                continue
            
            # Draw preview cells - using theme glow color with transparency
            glow_color = theme["cell_glow"]
            cell_color = (glow_color[0], glow_color[1], glow_color[2], 180)
            border_color = (glow_color[0] * 0.7, glow_color[1] * 0.7, glow_color[2] * 0.7, 255)
            
            pygame.draw.rect(self.preview_surface, cell_color, 
                           (screen_x, screen_y, self.cell_size, self.cell_size))
            pygame.draw.rect(self.preview_surface, border_color, 
                           (screen_x, screen_y, self.cell_size, self.cell_size), 1)
        
        # Blit the preview surface onto the main screen
        self.screen.blit(self.preview_surface, (0, 0))
    
    def render_ui(self):
        """Render UI elements."""
        # Draw main buttons
        pygame.draw.rect(self.screen, self.COLOR_BUTTON, self.btn_pause)
        pygame.draw.rect(self.screen, self.COLOR_BUTTON, self.btn_step)
        pygame.draw.rect(self.screen, self.COLOR_BUTTON, self.btn_clear)
        pygame.draw.rect(self.screen, self.COLOR_BUTTON, self.btn_settings)
        
        # Draw button text
        pause_text = "Resume" if self.paused else "Pause"
        self.screen.blit(self.font.render(pause_text, True, self.COLOR_TEXT), (self.btn_pause.x + 10, self.btn_pause.y + 5))
        self.screen.blit(self.font.render("Step", True, self.COLOR_TEXT), (self.btn_step.x + 10, self.btn_step.y + 5))
        self.screen.blit(self.font.render("Clear", True, self.COLOR_TEXT), (self.btn_clear.x + 10, self.btn_clear.y + 5))
        self.screen.blit(self.font.render("Settings", True, self.COLOR_TEXT), (self.btn_settings.x + 10, self.btn_settings.y + 5))
        
        # Draw speed control buttons
        pygame.draw.rect(self.screen, self.COLOR_BUTTON, self.btn_speed_up)
        pygame.draw.rect(self.screen, self.COLOR_BUTTON, self.btn_speed_down)
        self.screen.blit(self.font.render("+", True, self.COLOR_TEXT), (self.btn_speed_up.x + 10, self.btn_speed_up.y + 5))
        self.screen.blit(self.font.render("-", True, self.COLOR_TEXT), (self.btn_speed_down.x + 10, self.btn_speed_down.y + 5))
        self.screen.blit(self.font.render(f"Speed: {self.simulation_speed}", True, self.COLOR_TEXT), 
                       (self.btn_speed_up.x + 80, self.btn_speed_up.y +5))
        
        # Draw status info
        generation_text = f"Generation: {self.game.generation}"
        population_text = f"Population: {len(self.game.cells)}"
        rule_text = f"Rule: {self.game.rule_string}"
        
        # Calculate cursor position in grid coordinates
        grid_x = (self.mouse_pos[0] - self.offset_x) // self.cell_size
        grid_y = (self.mouse_pos[1] - self.offset_y) // self.cell_size
        cursor_text = f"Cursor: ({grid_x}, {grid_y})"
        theme_text = f"Theme: {self.current_theme}"
        
        # Create status info panel
        status_x = self.screen.get_width() - 300
        status_y = 50
        status_spacing = 20
        
        self.screen.blit(self.font.render(generation_text, True, self.COLOR_TEXT), (status_x, status_y))
        self.screen.blit(self.font.render(population_text, True, self.COLOR_TEXT), (status_x, status_y + status_spacing))
        self.screen.blit(self.font.render(rule_text, True, self.COLOR_TEXT), (status_x, status_y + status_spacing * 2))
        self.screen.blit(self.font.render(cursor_text, True, self.COLOR_TEXT), (status_x, status_y + status_spacing * 3))
        self.screen.blit(self.font.render(theme_text, True, self.COLOR_TEXT), (status_x, status_y + status_spacing * 4))
        
        # Draw pattern selection panel background
        pygame.draw.rect(self.screen, self.COLOR_SIDEBAR_BG, self.sidebar_rect)
        pygame.draw.rect(self.screen, (60, 60, 65), self.sidebar_rect, 1)  # Border
        
        # Draw the title for the sidebar
        title_surface = self.font_title.render("Pattern Library", True, self.COLOR_TEXT_HIGHLIGHT)
        self.screen.blit(title_surface, (self.sidebar_rect.x + 10, self.sidebar_rect.y + 10))
        
        # Draw category tabs
        for tab in self.category_tabs:
            # Highlight the selected category
            if tab["name"] == self.selected_category:
                pygame.draw.rect(self.screen, self.COLOR_BUTTON_ACTIVE, tab["rect"])
            else:
                pygame.draw.rect(self.screen, self.COLOR_BUTTON, tab["rect"])
            
            # Draw tab text - truncate if needed
            tab_text = tab["name"]
            if len(tab_text) > 12:  # Truncate long category names
                tab_text = tab_text[:10] + ".."
                
            text = self.font_small.render(tab_text, True, self.COLOR_TEXT)
            text_rect = text.get_rect(center=tab["rect"].center)
            self.screen.blit(text, text_rect)
        
        # Draw pattern area
        pygame.draw.rect(self.screen, (50, 50, 55), self.pattern_area)
        pygame.draw.rect(self.screen, (60, 60, 65), self.pattern_area, 1)  # Border
        
        # Draw scroll buttons
        pygame.draw.rect(self.screen, (60, 60, 60), self.pattern_scroll_up)
        pygame.draw.rect(self.screen, (60, 60, 60), self.pattern_scroll_down)
        self.screen.blit(self.font.render("▲", True, self.COLOR_TEXT), (self.pattern_scroll_up.x + 5, self.pattern_scroll_up.y))
        self.screen.blit(self.font.render("▼", True, self.COLOR_TEXT), (self.pattern_scroll_down.x + 5, self.pattern_scroll_down.y))
        
        # Draw pattern buttons for the selected category
        if self.selected_category in self.game.pattern_categories:
            patterns_in_category = self.game.pattern_categories[self.selected_category]
            
            btn_height = self.UI_BUTTON_HEIGHT
            btn_spacing = self.UI_BUTTON_SPACING
            btn_width = self.pattern_area.width - 25  # Leave room for scrollbar
            visible_count = min(self.patterns_per_page, len(patterns_in_category) - self.pattern_scroll_y)
            
            for i in range(visible_count):
                pattern_index = self.pattern_scroll_y + i
                if pattern_index >= len(patterns_in_category):
                    break
                    
                pattern_name = patterns_in_category[pattern_index]
                
                # Create button rectangle
                btn_rect = pygame.Rect(
                    self.pattern_area.x + 5,
                    self.pattern_area.y + 5 + i * (btn_height + btn_spacing),
                    btn_width,
                    btn_height
                )
                
                # Highlight selected pattern
                if self.selected_pattern == pattern_name:
                    pygame.draw.rect(self.screen, self.COLOR_BUTTON_HIGHLIGHT, btn_rect)
                else:
                    pygame.draw.rect(self.screen, self.COLOR_BUTTON, btn_rect)
                
                # Draw button text
                text = self.font.render(pattern_name, True, self.COLOR_TEXT)
                text_rect = text.get_rect(centery=btn_rect.centery, x=btn_rect.x + 10)
                self.screen.blit(text, text_rect)
        
        # Draw pattern information box
        if self.selected_pattern:
            pygame.draw.rect(self.screen, (45, 45, 50), self.pattern_info_rect)
            pygame.draw.rect(self.screen, (60, 60, 65), self.pattern_info_rect, 1)
            
            # Pattern name
            name_text = self.font_bold.render(self.selected_pattern, True, self.COLOR_TEXT_HIGHLIGHT)
            self.screen.blit(name_text, (self.pattern_info_rect.x + 10, self.pattern_info_rect.y + 10))
            
            # Pattern category
            for category, patterns in self.game.pattern_categories.items():
                if self.selected_pattern in patterns:
                    category_text = self.font_small.render(f"Category: {category}", True, self.COLOR_TEXT)
                    self.screen.blit(category_text, (self.pattern_info_rect.x + 10, self.pattern_info_rect.y + 30))
                    break
            
            # Pattern instructions
            if self.placing_pattern:
                inst_text = self.font_small.render("Click to place, ESC/Right-click to cancel", True, self.COLOR_TEXT)
                self.screen.blit(inst_text, (self.pattern_info_rect.x + 10, self.pattern_info_rect.y + 50))
        
        # Draw rule selection label
        self.screen.blit(self.font.render("Rules:", True, self.COLOR_TEXT), 
                       (self.screen.get_width() - 130, 100))
        
        # Draw rule buttons
        for rule_name, btn_rect in self.rule_buttons.items():
            # Highlight active rule
            if self.rule_presets[rule_name] == self.game.rule_string:
                pygame.draw.rect(self.screen, self.COLOR_BUTTON_HIGHLIGHT, btn_rect)
            else:
                pygame.draw.rect(self.screen, self.COLOR_BUTTON, btn_rect)
            
            # Draw button text
            text = self.font.render(rule_name, True, self.COLOR_TEXT)
            text_rect = text.get_rect(center=btn_rect.center)
            self.screen.blit(text, text_rect)
        
        # Draw help text and pattern placement mode indicator at bottom right
        self.help_text_rect.x = self.screen.get_width() - 600  # Update position in case of resize
        self.help_text_rect.y = self.screen.get_height() - 40  # Update position in case of resize
        
        if self.placing_pattern:
            mode_text = f"PLACING: {self.selected_pattern}"
            self.screen.blit(self.font_bold.render(mode_text, True, (100, 255, 100)), 
                           (self.screen.get_width() // 2 - 100, 15))
            help_text = "Left-click: Place pattern | Right-click or ESC: Cancel | Arrow keys: Pan"
        else:
            help_text = "Left-click: Add cells | Right-click: Remove cells | Space: Pause/Resume | S: Step | Arrow: Pan"
        
        # Render help text in the dedicated area
        self.screen.blit(self.font.render(help_text, True, (200, 200, 200)), 
                       (self.help_text_rect.x, self.help_text_rect.y))
        
        # If settings menu is open, draw it on top
        if self.show_settings:
            self.render_settings_panel()
    
    def render_settings_panel(self):
        """Render the settings panel"""
        # Update settings position in case window has been resized
        self.settings_rect = pygame.Rect(
            self.screen.get_width() // 2 - 200,
            self.screen.get_height() // 2 - 150,
            400, 300
        )
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))
        
        # Draw settings panel
        pygame.draw.rect(self.screen, self.COLOR_SIDEBAR_BG, self.settings_rect)
        pygame.draw.rect(self.screen, (100, 100, 120), self.settings_rect, 2)  # Border
        
        # Draw title
        title_text = self.font_title.render("Settings", True, self.COLOR_TEXT_HIGHLIGHT)
        self.screen.blit(title_text, (self.settings_rect.x + 20, self.settings_rect.y + 20))
        
        # Draw close button
        close_btn = pygame.Rect(self.settings_rect.right - 30, self.settings_rect.y + 10, 20, 20)
        pygame.draw.rect(self.screen, self.COLOR_BUTTON, close_btn)
        self.screen.blit(self.font.render("X", True, self.COLOR_TEXT), (close_btn.x + 5, close_btn.y + 2))
        
        # Draw color theme settings
        theme_label = self.font_bold.render("Color Theme:", True, self.COLOR_TEXT)
        self.screen.blit(theme_label, (self.settings_rect.x + 20, self.settings_rect.y + 60))
        
        # Create theme buttons
        theme_btn_y = self.settings_rect.y + 90
        btn_height = 30
        btn_spacing = 10
        btn_width = self.settings_rect.width - 40
        
        for i, theme_name in enumerate(self.color_themes.keys()):
            btn_rect = pygame.Rect(
                self.settings_rect.x + 20,
                theme_btn_y + i * (btn_height + btn_spacing),
                btn_width,
                btn_height
            )
            
            # Highlight current theme
            if theme_name == self.current_theme:
                pygame.draw.rect(self.screen, self.COLOR_BUTTON_HIGHLIGHT, btn_rect)
            else:
                pygame.draw.rect(self.screen, self.COLOR_BUTTON, btn_rect)
            
            # Draw theme name
            theme_text = self.font.render(theme_name, True, self.COLOR_TEXT)
            self.screen.blit(theme_text, (btn_rect.x + 15, btn_rect.y + 5))
    
    def check_pattern_button_click(self, mouse_pos):
        """Check if a pattern button was clicked and handle selection.
        Returns True if a pattern was clicked, False otherwise."""
        if not self.pattern_area.collidepoint(mouse_pos):
            return False
            
        # Calculate which pattern was clicked based on y position
        y_rel = mouse_pos[1] - self.pattern_area.y - 5  # Adjust for padding
        btn_height = self.UI_BUTTON_HEIGHT + self.UI_BUTTON_SPACING
        
        pattern_index = self.pattern_scroll_y + int(y_rel // btn_height)
        
        # Check if valid pattern index in the selected category
        if self.selected_category in self.game.pattern_categories:
            category_patterns = self.game.pattern_categories[self.selected_category]
            if 0 <= pattern_index < len(category_patterns):
                self.selected_pattern = category_patterns[pattern_index]
                self.placing_pattern = True
                return True
            
        return False


# Additional classes would be defined here:
# - PatternManager: For handling pattern library and operations
# - RuleManager: For managing and creating custom rules
# - FileHandler: For loading/saving patterns, settings, etc.
# - StatisticsTracker: For tracking and visualizing simulation statistics

if __name__ == "__main__":
    app = GameOfLifeUI()
    app.run()
