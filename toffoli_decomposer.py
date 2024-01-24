from qiskit import QuantumCircuit, QuantumRegister

class ToffoliDecomposer:

    def toffoli_gate(self, c1, c2, target):
        # This method can be changed to use a custom ccx decomposition
        self.qc.ccx(c1, c2, target)

    def __block_1(self, c):
        return c[0] # target

    def __block_2(self, c, a):
        ccx = self.toffoli_gate
        ccx(c[0], c[1], a[0])
        return a[0] # target
    
    def __block_3(self, c, a):
        ccx = self.toffoli_gate
        ccx(c[0], c[1], a[0])
        ccx(c[2], a[0], a[1])
        return a[1] # target
    
    def __block_4(self, c, a):
        ccx = self.toffoli_gate
        ccx(c[0], c[1], a[0])
        ccx(c[2], c[3], a[1])
        ccx(a[0], a[1], a[2])
        return a[2] # target
    
    def __block_5(self, c, a):
        ccx = self.toffoli_gate
        ccx(c[0], c[1], a[0])
        ccx(c[2], c[3], a[1])
        ccx(a[0], a[1], a[2])
        ccx(c[0], c[1], a[0])
        ccx(c[4], a[2], a[0])
        return a[0]
    
    def __block_6(self, c, a):
        ccx = self.toffoli_gate
        ccx(c[0], c[1], a[0])
        ccx(c[2], c[3], a[1])
        ccx(c[4], c[5], a[2])
        ccx(a[0], a[1], a[3])
        ccx(c[0], c[1], a[0])
        ccx(a[2], a[3], a[0])
        return a[0] # target
    
    def __block_7(self, c, a):
        ccx = self.toffoli_gate
        ccx(c[0], c[1], a[0])
        ccx(c[2], c[3], a[1])
        ccx(c[4], c[5], a[2])
        ccx(a[0], a[1], a[3])
        ccx(c[0], c[1], a[0])
        ccx(c[2], c[3], a[1])
        ccx(a[2], a[3], a[1])
        ccx(c[6], a[1], a[0])
        return a[0] # target

    def __block_8(self, c, a):
        ccx = self.toffoli_gate
        ccx(c[0], c[1], a[0])
        ccx(c[2], c[3], a[1])
        ccx(a[0], a[1], a[2])
        ccx(c[2], c[3], a[1])
        ccx(c[0], c[1], a[0])
        ccx(c[4], c[5], a[0])
        ccx(c[6], c[7], a[1])
        ccx(a[0], a[1], a[3])
        ccx(c[6], c[7], a[1])
        ccx(c[4], c[5], a[0])
        ccx(a[2], a[3], a[1])
        return a[1], a[0] # target, free ancilla

    def __create_qc(self):
        # This creates the QuantumRegisters and QuantumCircuit based on provided control qubit count
        # An elaborate scheme is used to layer targets and controls to ease visualization (avoid gate overlapping at same time moment)
        self.control = []
        self.ancilla = []
        self.target = QuantumRegister(1, 'target')
        registers = []
        for i in range(self.ancilla_count):
            if 2*i < self.n:
                qr1 = QuantumRegister(1, 'control_' + str(2*i))
                self.control.append(qr1)
                registers.append(qr1)
            if 2*i+1 < self.n:
                qr2 = QuantumRegister(1, 'control_' + str(2*i+1))
                self.control.append(qr2)
                registers.append(qr2)
            qa = QuantumRegister(1, 'ancilla_' + str(i))
            self.ancilla.extend(qa)
            registers.append(qa)
        registers.append(self.target)
        self.qc = QuantumCircuit(*registers)
    
    def __create_first_layer(self):
        next_controls = []
        next_ancilla = []
        for i in range(0, self.n-7, 8): # Create floor(n/8) Block_8's
            j = i // 2
            c, a = self.__block_8(self.control[i:i+8], self.ancilla[j:j+4])
            next_controls.append(c)
            next_ancilla.append(a)
        tail = self.n % 8 # Number of control qubits in final block, use this info to create on more block if needed
        i = self.n - tail
        j = (self.n // 8) * 4
        c = None
        if tail == 1:
            c = self.__block_1(self.control[i:i+1])
        elif tail == 2:
            c = self.__block_2(self.control[i:i+2], self.ancilla[j:j+1])
        elif tail == 3:
            c = self.__block_3(self.control[i:i+3], self.ancilla[j:j+2])
        elif tail == 4:
            c = self.__block_4(self.control[i:i+4], self.ancilla[j:j+3])
        elif tail == 5:
            c = self.__block_5(self.control[i:i+5], self.ancilla[j:j+3])
        elif tail == 6:
            c = self.__block_6(self.control[i:i+6], self.ancilla[j:j+4])
        elif tail == 7:
            c = self.__block_7(self.control[i:i+7], self.ancilla[j:j+4])
        if c is not None:
            next_controls.append(c)
        if self.show_barrier:
            self.qc.barrier(label="End of layer 1")
        return next_controls, next_ancilla
    
    def __create_final_layers(self, control, ancilla):
        t = self.n // 8
        next_control = []
        ancilla_idx = 0
        barrier_idx = 2
        ccx = self.toffoli_gate
        while len(control) > 1: # While at least two controls remain, create a new layer
            for i in range(0, len(control), 2): # Create as many Block_2's as possible
                if i+1 == len(control): # If the number of controls was odd, pass one onto the next layer
                    next_control.append(control[-1])
                    break
                ccx(control[i], control[i+1], ancilla[ancilla_idx])
                next_control.append(ancilla[ancilla_idx])
                ancilla_idx += 1
            control = next_control # Use output of this layer's Block_2's as next layer's input
            next_control = []
            if self.show_barrier:
                self.qc.barrier(label="End of layer " + str(barrier_idx))
                barrier_idx += 1
        self.qc.cx(control[0], self.target[0]) # Create final CX gate onto target

    def decompose(self, n, show_barrier):
        self.n = n
        self.ancilla_count = n // 2 + 1
        self.show_barrier = show_barrier

        self.__create_qc()
        nc, na = self.__create_first_layer()
        self.__create_final_layers(nc, na)

        return self.qc
