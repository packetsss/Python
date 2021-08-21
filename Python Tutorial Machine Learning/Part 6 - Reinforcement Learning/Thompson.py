import random
import pandas as pd

class Thompson:
    def __init__(self, dataset, rounds, sample_size):
        self.dataset = dataset
        self.N = rounds
        self.d = sample_size
    
    def fit(self):
        ads_selected = [0] * self.N
        reward_0, reward_1 = [0] * self.d, [0] * self.d
        total_reward = 0

        for n in range(self.N):
            ad = 0
            max_rand = 0
            for i in range(self.d):
                random_beta_distro = random.betavariate(reward_1[i] + 1, reward_0[i] + 1)  # random from beta distro from 0 to 1
                if random_beta_distro > max_rand:
                    max_rand = random_beta_distro
                    ad = i
            reward = dataset.values[n, ad]
            if reward == 1:
                reward_1[ad] += 1
            else:
                reward_0[ad] += 1
            total_reward += reward
            ads_selected[n] = ad
        return ads_selected

                


if __name__ == '__main__':
    dataset = pd.read_csv('C:\\Users\\pyjpa\\Desktop\\Programming\\Machine Learning A-Z (Codes and Datasets)\\Part 6 - Reinforcement Learning\\Section 32 - Upper Confidence Bound (UCB)\\Python\\Ads_CTR_Optimisation.csv')
    model = Thompson(dataset, 500, 10)

    import matplotlib.pyplot as plt
    rst = model.fit()
    plt.hist(rst)
    plt.title('Histogram of ads selections')
    plt.xlabel('Ads')
    plt.ylabel('Number of times each ad was selected')
    plt.show()