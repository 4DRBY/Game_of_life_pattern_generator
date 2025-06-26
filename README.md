# Ultimate Game of Life

An advanced and feature-rich implementation of Conway's Game of Life, built with Pygame. This project goes beyond a simple simulation by offering an extensive, categorized library of patterns, customizable rules, an interactive UI with multiple themes, and powerful controls for exploring the fascinating world of cellular automata.

## Table of Contents

  - [About The Project](https://www.google.com/search?q=%23about-the-project)
  - [Features](https://www.google.com/search?q=%23features)
  - [Built With](https://www.google.com/search?q=%23built-with)
  - [Getting Started](https://www.google.com/search?q=%23getting-started)
      - [Prerequisites](https://www.google.com/search?q=%23prerequisites)
      - [Installation](https://www.google.com/search?q=%23installation)
  - [Usage](https://www.google.com/search?q=%23usage)
      - [Controls](https://www.google.com/search?q=%23controls)
      - [Pattern Library](https://www.google.com/search?q=%23pattern-library)
      - [Custom Rules](https://www.google.com/search?q=%23custom-rules)
      - [Themes](https://www.google.com/search?q=%23themes)
  - [Future Development](https://www.google.com/search?q=%23future-development)
  - [License](https://www.google.com/search?q=%23license)

## About The Project

This project is a sophisticated version of Conway's Game of Life, designed for both enthusiasts and newcomers. The core of the application is a highly efficient simulation engine that uses a sparse grid representation, allowing for vast and complex patterns to evolve without performance degradation.

The graphical user interface, built with Pygame, provides a rich user experience with features such as:

  * Infinite, pannable, and zoomable grid.
  * An extensive, categorized library of over 40 pre-built patterns, from simple still lifes to complex computational constructs.
  * Support for alternative cellular automata rules beyond Conway's classic $B3/S23$.
  * A polished and customizable visual experience with multiple color themes.

Whether you want to watch a simple Glider travel across the screen or build a working Prime Number Generator within the simulation, this project provides the tools to do so.

## Features

  * **Infinite Grid:** The simulation space is unbounded thanks to a sparse matrix implementation.
  * **Panning and Zooming:** Navigate the grid with ease using mouse or keyboard controls. The view dynamically adjusts to show more or less detail.
  * **Extensive Pattern Library:** Place over 40 famous and complex patterns, neatly organized into categories:
      * Still Lifes & Oscillators
      * Spaceships (including LWSS, MWSS, HWSS)
      * Guns & Puffers (Glider Guns, factories, etc.)
      * Methuselahs (long-lasting patterns like Acorn and Diehard)
      * Computational Patterns (Logic gates, memory, and even concepts for a Turing Machine)
  * **Customizable Rules:** Switch between different rulesets like Conway's Life, HighLife, Day & Night, and Maze, or define your own.
  * **Simulation Controls:** Pause, resume, and step through the simulation one generation at a time. Control the simulation speed.
  * **Interactive UI:** A clean interface with a sidebar for pattern selection, status display (generation, population), and settings.
  * **Multiple Color Themes:** Choose from several themes (Default, Light, Neon, High Contrast) to customize the look and feel. The cells change color based on their age.
  * **Undo/Redo:** Step backward and forward through the simulation's history.
  * **Pattern Placement Preview:** See a transparent preview of a pattern and its bounding box before placing it on the grid.

## Built With

This project is built using the following main libraries:

  * [Pygame](https://www.pygame.org/) - For the core graphics, event handling, and user interface.
  * [NumPy](https://numpy.org/) - For potential future numerical operations.
  * [Tkinter](https://docs.python.org/3/library/tkinter.html) - For native file dialogs and message boxes.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

You need to have Python 3 and pip installed on your system.

  * **Python 3:** [Download Python](https://www.python.org/downloads/)
  * **pip** (usually comes with Python)

### Installation

1.  **Clone the repository:**

    ```sh
    git clone https://github.com/your_username/Game_of_life_pattern_generator.git
    cd ultimate-game-of-life
    ```

2.  **Create a virtual environment (recommended):**

    ```sh
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

## Usage

To run the application, execute the main Python script:

```sh
python main.py
```

*(Assuming your script is named `main.py`)*

### Controls

| Action                  | Control                               | Description                                                      |
| ----------------------- | ------------------------------------- | ---------------------------------------------------------------- |
| **Grid Interaction** |                                       |                                                                  |
| Add Cells               | `Left Mouse Click + Drag`             | Draw new live cells onto the grid.                               |
| Remove Cells            | `Right Mouse Click + Drag`            | Erase live cells.                                                |
| Pan View                | `Middle Mouse Click + Drag`           | Move the camera around the grid.                                 |
| Pan View (Keyboard)     | `Arrow Keys`                          | Pan the view up, down, left, or right.                           |
| Zoom In/Out             | `Mouse Wheel Scroll`                  | Zoom the view in and out, centered on the mouse cursor.          |
| **Simulation** |                                       |                                                                  |
| Pause / Resume          | `Spacebar` or `Pause/Resume` button   | Toggle the simulation's running state.                           |
| Step Forward            | `S` key or `Step` button              | Advance the simulation by a single generation.                   |
| Change Speed            | `+` / `-` buttons                     | Increase or decrease the simulation speed (generations per second).|
| Clear Grid              | `Clear` button                        | Remove all cells from the grid.                                  |
| **History** |                                       |                                                                  |
| Undo                    | `Ctrl + Z`                            | Revert to the previous generation state.                         |
| Redo                    | `Ctrl + Y`                            | Go forward to the next generation state in history.              |
| **Pattern Placement** |                                       |                                                                  |
| Select Pattern          | Click on a pattern in the library.    | Enter pattern placement mode.                                    |
| Place Pattern           | `Left Mouse Click`                    | Place the selected pattern on the grid, centered at the cursor.  |
| Cancel Placement        | `Right Mouse Click` or `Escape` key   | Exit pattern placement mode.                                     |

### Pattern Library

The Pattern Library is located in the sidebar on the left.

1.  **Select a Category:** Click on a category tab (e.g., "Spaceships", "Guns & Puffers") to view the patterns within it.
2.  **Scroll:** Use the mouse wheel or scroll buttons to navigate the list of patterns.
3.  **Select a Pattern:** Click a pattern's name to select it for placement. Information about the pattern and instructions will appear at the bottom of the sidebar.
4.  **Place:** Move your mouse over the grid and left-click to place the pattern. You can place multiple copies.

### Custom Rules

The simulation defaults to Conway's classic rule ($B3/S23$), but you can switch to other presets using the buttons on the right-hand side of the screen.

The rule notation is **B/S**, where:

  * **B** (Birth): A list of numbers of live neighbors that will cause a dead cell to become alive.
  * **S** (Survival): A list of numbers of live neighbors that will allow a live cell to survive to the next generation.

### Themes

You can change the application's appearance at any time:

1.  Click the **Settings** button.
2.  In the settings panel, select a new **Color Theme**.
3.  The theme will change with a smooth transition.

## Future Development

This project has a solid foundation with many planned features to make it even more powerful:

  - [ ] **File Operations:** Save and load patterns and entire simulation states to and from files (e.g., `.rle`, `.lif`, `.cells` formats).
  - [ ] **Pattern Manager:** An interface to create, edit, and save your own custom patterns to the library.
  - [ ] **Statistics Tracker:** A module to track and visualize data like population trends, pattern density, and other interesting metrics.
  - [ ] **Advanced Rule Manager:** A UI for creating and saving custom cellular automata rules without editing code.

## License

Distributed under the MIT License. See `LICENSE` for more information.

# Ultimate Game of Life

An advanced and feature-rich implementation of Conway's Game of Life, built with Pygame. This project goes beyond a simple simulation by offering an extensive, categorized library of patterns, customizable rules, an interactive UI with multiple themes, and powerful controls for exploring the fascinating world of cellular automata.

## Table of Contents

  - [About The Project](https://www.google.com/search?q=%23about-the-project)
  - [Features](https://www.google.com/search?q=%23features)
  - [Built With](https://www.google.com/search?q=%23built-with)
  - [Getting Started](https://www.google.com/search?q=%23getting-started)
      - [Prerequisites](https://www.google.com/search?q=%23prerequisites)
      - [Installation](https://www.google.com/search?q=%23installation)
  - [Usage](https://www.google.com/search?q=%23usage)
      - [Controls](https://www.google.com/search?q=%23controls)
      - [Pattern Library](https://www.google.com/search?q=%23pattern-library)
      - [Custom Rules](https://www.google.com/search?q=%23custom-rules)
      - [Themes](https://www.google.com/search?q=%23themes)
  - [Future Development](https://www.google.com/search?q=%23future-development)
  - [License](https://www.google.com/search?q=%23license)

## About The Project

This project is a sophisticated version of Conway's Game of Life, designed for both enthusiasts and newcomers. The core of the application is a highly efficient simulation engine that uses a sparse grid representation, allowing for vast and complex patterns to evolve without performance degradation.

The graphical user interface, built with Pygame, provides a rich user experience with features such as:

  * Infinite, pannable, and zoomable grid.
  * An extensive, categorized library of over 40 pre-built patterns, from simple still lifes to complex computational constructs.
  * Support for alternative cellular automata rules beyond Conway's classic $B3/S23$.
  * A polished and customizable visual experience with multiple color themes.

Whether you want to watch a simple Glider travel across the screen or build a working Prime Number Generator within the simulation, this project provides the tools to do so.

## Features

  * **Infinite Grid:** The simulation space is unbounded thanks to a sparse matrix implementation.
  * **Panning and Zooming:** Navigate the grid with ease using mouse or keyboard controls. The view dynamically adjusts to show more or less detail.
  * **Extensive Pattern Library:** Place over 40 famous and complex patterns, neatly organized into categories:
      * Still Lifes & Oscillators
      * Spaceships (including LWSS, MWSS, HWSS)
      * Guns & Puffers (Glider Guns, factories, etc.)
      * Methuselahs (long-lasting patterns like Acorn and Diehard)
      * Computational Patterns (Logic gates, memory, and even concepts for a Turing Machine)
  * **Customizable Rules:** Switch between different rulesets like Conway's Life, HighLife, Day & Night, and Maze, or define your own.
  * **Simulation Controls:** Pause, resume, and step through the simulation one generation at a time. Control the simulation speed.
  * **Interactive UI:** A clean interface with a sidebar for pattern selection, status display (generation, population), and settings.
  * **Multiple Color Themes:** Choose from several themes (Default, Light, Neon, High Contrast) to customize the look and feel. The cells change color based on their age.
  * **Undo/Redo:** Step backward and forward through the simulation's history.
  * **Pattern Placement Preview:** See a transparent preview of a pattern and its bounding box before placing it on the grid.

## Built With

This project is built using the following main libraries:

  * [Pygame](https://www.pygame.org/) - For the core graphics, event handling, and user interface.
  * [NumPy](https://numpy.org/) - For potential future numerical operations.
  * [Tkinter](https://docs.python.org/3/library/tkinter.html) - For native file dialogs and message boxes.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

You need to have Python 3 and pip installed on your system.

  * **Python 3:** [Download Python](https://www.python.org/downloads/)
  * **pip** (usually comes with Python)

### Installation

1.  **Clone the repository:**

    ```sh
    git clone https://github.com/your_username/ultimate-game-of-life.git
    cd ultimate-game-of-life
    ```

2.  **Create a virtual environment (recommended):**

    ```sh
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

## Usage

To run the application, execute the main Python script:

```sh
python main.py
```

*(Assuming your script is named `main.py`)*

### Controls

| Action                  | Control                               | Description                                                      |
| ----------------------- | ------------------------------------- | ---------------------------------------------------------------- |
| **Grid Interaction** |                                       |                                                                  |
| Add Cells               | `Left Mouse Click + Drag`             | Draw new live cells onto the grid.                               |
| Remove Cells            | `Right Mouse Click + Drag`            | Erase live cells.                                                |
| Pan View                | `Middle Mouse Click + Drag`           | Move the camera around the grid.                                 |
| Pan View (Keyboard)     | `Arrow Keys`                          | Pan the view up, down, left, or right.                           |
| Zoom In/Out             | `Mouse Wheel Scroll`                  | Zoom the view in and out, centered on the mouse cursor.          |
| **Simulation** |                                       |                                                                  |
| Pause / Resume          | `Spacebar` or `Pause/Resume` button   | Toggle the simulation's running state.                           |
| Step Forward            | `S` key or `Step` button              | Advance the simulation by a single generation.                   |
| Change Speed            | `+` / `-` buttons                     | Increase or decrease the simulation speed (generations per second).|
| Clear Grid              | `Clear` button                        | Remove all cells from the grid.                                  |
| **History** |                                       |                                                                  |
| Undo                    | `Ctrl + Z`                            | Revert to the previous generation state.                         |
| Redo                    | `Ctrl + Y`                            | Go forward to the next generation state in history.              |
| **Pattern Placement** |                                       |                                                                  |
| Select Pattern          | Click on a pattern in the library.    | Enter pattern placement mode.                                    |
| Place Pattern           | `Left Mouse Click`                    | Place the selected pattern on the grid, centered at the cursor.  |
| Cancel Placement        | `Right Mouse Click` or `Escape` key   | Exit pattern placement mode.                                     |

### Pattern Library

The Pattern Library is located in the sidebar on the left.

1.  **Select a Category:** Click on a category tab (e.g., "Spaceships", "Guns & Puffers") to view the patterns within it.
2.  **Scroll:** Use the mouse wheel or scroll buttons to navigate the list of patterns.
3.  **Select a Pattern:** Click a pattern's name to select it for placement. Information about the pattern and instructions will appear at the bottom of the sidebar.
4.  **Place:** Move your mouse over the grid and left-click to place the pattern. You can place multiple copies.

### Custom Rules

The simulation defaults to Conway's classic rule ($B3/S23$), but you can switch to other presets using the buttons on the right-hand side of the screen.

The rule notation is **B/S**, where:

  * **B** (Birth): A list of numbers of live neighbors that will cause a dead cell to become alive.
  * **S** (Survival): A list of numbers of live neighbors that will allow a live cell to survive to the next generation.

### Themes

You can change the application's appearance at any time:

1.  Click the **Settings** button.
2.  In the settings panel, select a new **Color Theme**.
3.  The theme will change with a smooth transition.

## Future Development

This project has a solid foundation with many planned features to make it even more powerful:

  - [ ] **File Operations:** Save and load patterns and entire simulation states to and from files (e.g., `.rle`, `.lif`, `.cells` formats).
  - [ ] **Pattern Manager:** An interface to create, edit, and save your own custom patterns to the library.
  - [ ] **Statistics Tracker:** A module to track and visualize data like population trends, pattern density, and other interesting metrics.
  - [ ] **Advanced Rule Manager:** A UI for creating and saving custom cellular automata rules without editing code.

## License

Distributed under the MIT License. See `LICENSE` for more information.
