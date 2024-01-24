from toffoli_decomposer import ToffoliDecomposer

td = ToffoliDecomposer()
control_qubit_count = 21
show_barrier = True # Should be set to False to reduce transpiled gate depth
qc = td.decompose(control_qubit_count, show_barrier)
print(qc)