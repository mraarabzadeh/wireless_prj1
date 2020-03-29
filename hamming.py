import numpy as np
import matplotlib.pyplot as plt

class Hamming():
    def __init__(self,seq):
        self.hamming_code = []
        for item in range(0,len(seq),4):
            self.hamming_code.append(np.array([int(i) for i in self.hamming(seq[item:item+4])]))
        self.H = [[np.random.normal(0,1) for _ in range(7)] for i in range(len(self.hamming_code))]
        
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

    def set_SNR(self, x):
        x = 1/x
        self.AWGN = [[np.random.normal(0,x) for _ in range(7)] for i in range(len(self.hamming_code))]

    def transfer(self):
        result_i = []
        for i in range(len(self.hamming_code)):
            result_i.append(self.hamming_code[i] * self.H[i] + self.AWGN[i]) 
        return result_i

    def get_data(self,seq):
        digit_get_data = []
        for item in seq:
            digit_get_data.append(list(map(lambda x: 1 if x >.5 else 0,item)))
        return digit_get_data

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
    def calc_acc(self, transfered, recived):
        numb = 0
        for i, data in enumerate(transfered):
            if recived[i] == data:
                numb+=1
        print(numb / len(transfered))
if __name__ == "__main__":
    snr = float(input())
    random_seq = ''.join([str(i) for i in np.random.randint(0,2,1000)])
    # print(random_seq)
    ham = Hamming(random_seq)
    # print(ham.hamming_code)
    ham.set_SNR(snr)
    result = ham.transfer()
    result = ham.get_data(result)
    result = ham.analyse_data(result)
    ham.calc_acc(random_seq, result)