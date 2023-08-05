import math
import numpy as np
import scipy.stats

def ci_mean(alpha, sample=[], sample_mean=False, n=False, true_sigma=False, sample_sigma=False):
    # when there is a vector of values i.e. sample itself
    if len(sample) != 0:
        sample = np.array(sample)
        n = len(sample)
        sample_mean = np.mean(sample)
        sample_sigma = np.std(sample)
    # known true (theoretical) sigma
    if true_sigma != False:
        z = scipy.stats.norm.ppf(1 - alpha)
        lower_bound = sample_mean - z * true_sigma / math.sqrt(n)
        upper_bound = sample_mean + z * true_sigma / math.sqrt(n)
        print(f'{round((1-alpha) * 100)}% Confidence Interval (CI) for mean is between {round(lower_bound, 2)} and\
 {round(upper_bound, 2)}')
        print(f'Z statistics with n={n} and alpha={alpha} is equal to {round(z, 2)}')
        print(f'CI width is {round(upper_bound - lower_bound, 2)}')
        print(f'Margin of Error is {round(z * true_sigma / math.sqrt(n), 2)}')
        print(f'Point estimate {round((lower_bound + upper_bound) / 2, 2)}')
        return lower_bound, upper_bound
    # unknown true sigma but known sig
    elif sample_sigma != False:
        t = scipy.stats.t.ppf(1 - alpha / 2, n - 1)
        lower_bound = sample_mean - t * sample_sigma / math.sqrt(n)
        upper_bound = sample_mean + t * sample_sigma / math.sqrt(n)
        print(f'{round((1-alpha) * 100)}% Confidence Interval for mean is between {round(lower_bound, 2)} and\
 {round(upper_bound, 2)}')
        print(f't (student) statistics with n={n} and alpha={alpha} is equal to {round(t, 2)}')
        print(f'CI width is {round(upper_bound - lower_bound, 2)}')
        print(f'Margin of Error is {round(t * sample_sigma / math.sqrt(n), 2)}')
        print(f'Point estimate {round((lower_bound + upper_bound) / 2, 2)}')
        return lower_bound, upper_bound
    else:
        print('Some data is missing. Check input parameters')