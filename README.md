
# Project Folder Structure

The project is organized into separate folders based on their responsibilities. This makes the code easier to understand, maintain, debug, and develop collaboratively. Each module has its own purpose, but all modules work together to form one complete application.

```text
university-enrollment-system/
│
├── main.py
├── requirements.txt
├── README.md
│
├── storage/
├── data/
├── data_structures/
├── algorithms/
├── services/
├── ui/
├── utils/
├── exports/
├── tests/
└── docs/
```

## Folder and File Descriptions

| Folder / File | Purpose |
|---|---|
| `main.py` | Main entry point of the application. Runs the system. |
| `requirements.txt` | Lists the external Python packages needed by the project. |
| `README.md` | Contains project information, setup instructions, and documentation. |
| `storage/` | Handles reading, writing, and updating JSON files. |
| `data/` | Stores permanent records such as students, courses, and enrollments in JSON format. |
| `data_structures/` | Contains implementations of Dictionary, Set, and List used to organize records. |
| `algorithms/` | Contains searching, sorting, Graph, DFS, BFS, and Topological Sort implementations. |
| `services/` | Handles the system's main operations, such as student management, course management, enrollment, and reports. |
| `ui/` | Contains the Tkinter graphical user interface, including windows, pages, buttons, and other components. |
| `utils/` | Contains reusable helper functions, such as input validation. |
| `exports/` | Stores generated files and exported enrollment reports. |
| `tests/` | Contains test scripts used to check whether the system and its functions work correctly. |
| `docs/` | Stores project documentation, pseudocode, flowcharts, and algorithm complexity analysis. |

## Important Notes for Contributors

- Each member should work primarily on their assigned folder or files.
- Avoid placing unrelated code in a single file.
- Use Python imports to connect functions and modules from different folders.
- Follow the agreed data formats and function names to avoid integration problems.
- Do not create duplicate files or modify another member's module without coordination.
- Test your changes before pushing them to the shared repository.

**Remember:** These folders are not separate applications. They are individual parts of one system that work together through imports and function calls.
