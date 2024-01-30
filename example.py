from toffoli_decomposer import ToffoliDecomposer
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler

# QiskitRuntimeService.save_account(channel="ibm_quantum", token="TOKEN")

td = ToffoliDecomposer()
n = 500
show_barrier = True
one_controls = range(n)
qc = td.decompose(n, show_barrier, one_controls)
 
service = QiskitRuntimeService()
 
backend = service.backend('ibmq_qasm_simulator')
 
sampler = Sampler(backend=backend)
 
job = sampler.run(qc, shots=100)
 
print(job.result())