# N-bit Toffoli Gate Decomposition

This repository contains a Python program to generate a decomposition of an n-bit Toffoli gate with O(log(n)) gate depth using floor(n/2)+1 ancillas qubits.

### Prerequisites

```Python 3.11.5```

*Other versions of Python may work as well.

### Setup

Run ```pip install -r requirements.txt```

### Run example

Run the file ```example.py``` to print a decomposed circuit to your terminal. Adjust the variable ```control_qubit_count``` to use a different number of control qubits. View and edit thh file ```toffoli_decomposer.py``` to modify the behavior of the decomposer.