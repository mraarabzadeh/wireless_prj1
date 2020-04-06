import numpy as np
import matplotlib.pyplot as plt
from QPSK import signal

class Hamming(signal):
    def __init__(self,seq):
        self.hamming_code = []
        for item in range(0,len(seq),4):
            self.hamming_code+= ''.join([i for i in self.hamming(seq[item:item+4])])
        self.hamming_code = ''.join(self.hamming_code)
        super().__init__(self.hamming_code)

    def hamming(self,seq):
        t1 = self.parity(seq, [0,1,3])
        t2 = self.parity(seq, [0,2,3])
        t3 = self.parity(seq, [1,2,3])
        return seq + t1 + t2 + t3

    def parity(self,seq, indices):
        s = ""
        for i in indices:
            s += str(seq[i])
        return str(str.count(s, "1") % 2)

    def ERR_parity(self,seq):
        t1 = (seq[0] + seq[1] + seq[3] +seq[4])%2
        t2 = (seq[0] + seq[2] + seq[3] +seq[5])%2
        t3 = (seq[1] + seq[2] + seq[3] +seq[6])%2
        if t1 * t2 * t3:
            seq[3] = 0 if seq[3] else 1
        elif t1 *t2:
            seq[0] = 0 if seq[0] else 1
        elif t1 * t3:
            seq[1] = 0 if seq[1] else 1
        elif t2*t3:
            seq[2] = 0 if seq[2] else 1
        return seq

    def analyse_data(self,seq):
        result = ''
        for item in seq:
            item = self.ERR_parity(item)
            result += ''.join([str(item[i]) for i in range(4)])
        return result

    def get_data(self, seq):
        result = super().get_data(seq)
        rewResult = [int(i) for i in result]
        return [rewResult[i:i+7] for i in range(0,len(rewResult),7)]

if __name__ == "__main__":
    snrItem = [10,1,.1]
    for snr in snrItem:
        random_seq = ''.join([str(i) for i in np.random.randint(0,2,1000)])
        ham = Hamming(random_seq)
        ham.set_SNR(snr)
        result = ham.transfer()
        plt.scatter([item[0] for item in result], [item[1] for item in result])
        plt.scatter(ham.gray_code_list_I,ham.gray_code_list_Q)
        plt.show()
        result = ham.get_data(result)
        result = ham.analyse_data(result)
        ham.calc_acc(random_seq, result)