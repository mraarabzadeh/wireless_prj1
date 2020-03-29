import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class signal():
    def __init__(self,seq):
        self.gray_code_list_I = []
        self.gray_code_list_Q = []

        for i in range(0,len(seq),2):
            if seq[i:i+2] == '00':
                self.gray_code_list_I.append(1)
                self.gray_code_list_Q.append(1)

            elif seq[i:i+2] == '01':
                self.gray_code_list_I.append(-1)
                self.gray_code_list_Q.append(1)

            elif seq[i:i+2] == '11':
                self.gray_code_list_I.append(-1)
                self.gray_code_list_Q.append(-1)

            elif seq[i:i+2] == '10':
                self.gray_code_list_I.append(1)
                self.gray_code_list_Q.append(-1)

        self.HI = np.random.normal(0,1,len(self.gray_code_list_I))
        self.HQ = np.random.normal(0,1,len(self.gray_code_list_I))

    def set_SNR(self, x):
        x = 1/x
        self.AWGN_i = np.random.normal(0,x,len(self.gray_code_list_I))
        self.AWGN_q = np.random.normal(0,x,len(self.gray_code_list_I))

    def transfer(self):
        result_i = np.array(self.gray_code_list_I) * self.HI + self.AWGN_i
        result_j = np.array(self.gray_code_list_Q) * self.HQ + self.AWGN_q
        return np.stack((result_i, result_j),axis=1)

    def get_data(self,seq):
        result = ''
        for item in seq:
            if item[0] < 0:
                if item[1] < 0:
                    result+= '11'
                else:
                    result+= '01'
            else:
                if item[1] < 0:
                    result+= '10'
                else:
                    result += '00'
        return result
    
    def calc_acc(self, transfered, recived):
        numb = 0
        for i, data in enumerate(transfered):
            if recived[i] == data:
                numb+=1
        print(numb / len(transfered))
if __name__ == "__main__":
    snr = float(input())
    random_seq = np.random.randint(0,2,1000)
    random_seq = ''.join([str(i) for i in random_seq])
    # print(random_seq)
    tr = signal(random_seq)

    plt.scatter(range(1000),[int(i) for i in random_seq])
    plt.show()
    tr.set_SNR(snr)
    result = tr.transfer()
    result = tr.get_data(result)
    # print(result)
    plt.scatter(range(1000), [item for item in result])
    plt.show()
    # print(result)
    tr.calc_acc(random_seq,result)