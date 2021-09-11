# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

import math
import pandas as pd

class UCB:
    def __init__(self, dataset, rounds, sample_size):
        self.dataset = dataset
        self.N = rounds
        self.d = sample_size      

    def fit(self):
        # N --> total rounds, d --> number of ads
        times_selected, sum_reward = [0] * self.d, [0] * self.d
        ads_selected = []
        tot_reward = 0

        for n in range(self.N):
            ad = 0
            max_ucb = 0
            for i in range(self.d):
                if times_selected[i] > 0:
                    avg_reward = sum_reward[i] / times_selected[i]
                    delta_i = math.sqrt((3 / 2) * math.log(n + 1) / times_selected[i])
                    upper_bound = avg_reward + delta_i
                else:
                    upper_bound = float("Inf")
                if upper_bound > max_ucb:
                    max_ucb = upper_bound
                    ad = i

            ads_selected.append(ad)
            times_selected[ad] += 1
            sum_reward[ad] += dataset.values[n, ad]
            tot_reward += dataset.values[n, ad]
        
        return ads_selected
    
    def plot_predict(self):
        import matplotlib.pyplot as plt
        times_selected, sum_reward = [0] * self.d, [0] * self.d
        ads_selected = []
        tot_reward = 0

        ct = 0
        plt.ion()  # interactive mode on
        plt.show()

        for n in range(self.N):
            ad = 0
            max_ucb = 0
            for i in range(self.d):
                if times_selected[i] > 0:
                    avg_reward = sum_reward[i] / times_selected[i]
                    delta_i = math.sqrt((3 / 2) * math.log(n + 1) / times_selected[i])
                    upper_bound = avg_reward + delta_i
                else:
                    upper_bound = float("Inf")
                if upper_bound > max_ucb:
                    max_ucb = upper_bound
                    ad = i

            ads_selected.append(ad)
            times_selected[ad] += 1
            sum_reward[ad] += dataset.values[n, ad]
            tot_reward += dataset.values[n, ad]

            ct += 1
            if ct > 150:
                plt.hist(ads_selected)
                plt.title('Histogram of ads selections')
                plt.xlabel('Ads')
                plt.ylabel('Number of times each ad was selected')
                plt.pause(0.001)
                plt.clf()
                ct = 0
        return ads_selected
                

if __name__ == '__main__':
    dataset = pd.read_csv('C:\\Users\\pyjpa\\Desktop\\Programming\\Machine Learning A-Z (Codes and Datasets)\\Part 6 - Reinforcement Learning\\Section 32 - Upper Confidence Bound (UCB)\\Python\\Ads_CTR_Optimisation.csv')
    model = UCB(dataset, 1500, 10)
    model.plot_predict()