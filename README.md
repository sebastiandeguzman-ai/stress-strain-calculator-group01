# stress-strain-calculator-group01
Project Title
Stress and Strain Analysis System

Member	Primary Responsibility 

Mary Charlize Fetalcorin	Task 1 – Basic Calculations

Vennice Anne Cartera	Task 2 – Control Structures

Darylle Balbin	Task 3 – Data Structures

Sebastian Miguel De Guzman   Task 4 – Functions

Rhianne Granados Task 5 – OOP

Task 6 – Modular Integration was completed collaboratively by all members.

Project Description

The Stress and Strain Analysis System is a modular Python application designed to assist engineers, researchers, and students in evaluating the mechanical behavior of materials under tensile loads. Built using object-oriented design and standard engineering formulas, the application enables users to calculate key mechanical parameters—such as engineering stress, engineering strain, Young’s Modulus, and the Factor of Safety (FoS)—for both default and custom-defined materials.

By structuring the codebase across specialized modules (material.py, properties.py, tests.py, utils.py, database.py, and main.py), the system cleanly separates data modeling, computational logic, input validation, and user interface workflows. The system features persistent storage capabilities via standard Python libraries (json and csv), allowing test results to be logged with automatic timestamps, loaded for future review, or exported for external reporting and visualization. Additionally, robust input validation safeguards calculations against invalid parameter inputs (e.g., zero cross-sectional area or negative dimensional measurements).

Installation/Requirements

Python Version: Python 3.10 or higher is required (supports modern type hints such as list[dict] and dict | None).

Dependencies: No third-party packages are required. The project relies entirely on the Python Standard Library (json, csv, datetime, pathlib, dataclasses, math).

Operating System: Cross-platform (compatible with Windows, macOS, and Linux).

How to Run the Program

Open your command line interface and clone the group repository using git clone [https://github.com/your-org/stress-strain-calculator-groupXX.git](https://github.com/your-org/stress-strain-calculator-groupXX.git).
Change your active directory into the project folder by running cd stress-strain-calculator-groupXX.
Launch the application from your terminal by executing python main.py or python3 main.py.
Follow the interactive on-screen menu prompts to run stress-strain calculations, display saved results, or export/import data files.

Repository Structure

material.py: Defines the Material base class and its sub-classes (Metal, Polymer), establishing the object-oriented hierarchy for material behavior.

properties.py: Contains data-oriented structures using @dataclass to standardize material properties and test result schema.

tests.py: Manages test execution logic via StressStrainTest and handles reading, writing, and exporting test histories using json, csv, and pathlib.

utils.py: Holds reusable mathematical utilities for stress-strain formulas and input validation routines to handle non-numeric or negative values.

database.py: Provides pre-configured, standard material profiles (e.g., Structural Steel, Aluminum) for quick selection during testing.

main.py: Serves as the central entry point, presenting the interactive menu interface and coordinating interactions across all other modules.
