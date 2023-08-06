import math
import numpy as np
import scipy.stats

# Confidence interval (CI) for mean
 
def ci_mean(alpha, sample=[], sample_mean=False, n=False, true_sigma=False, sample_sigma=False, verbose=False):
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
        margin_error = z * true_sigma / math.sqrt(n)
        if verbose == True:
            print(f'{round((1-alpha) * 100)}% Confidence Interval (CI) for mean is between {round(lower_bound, 2)} and\
    {round(upper_bound, 2)}')
            print(f'Z statistics with n={n} and alpha={alpha} is equal to {round(z, 2)}')
            print(f'CI width is {round(upper_bound - lower_bound, 2)}')
            print(f'Margin of Error is {round(margin_error, 2)}')
            print(f'Point estimate {round((lower_bound + upper_bound) / 2, 2)}')
        return lower_bound, upper_bound
    # unknown true sigma but known sig
    elif sample_sigma != False:
        t = scipy.stats.t.ppf(1 - alpha / 2, n - 1)
        lower_bound = sample_mean - t * sample_sigma / math.sqrt(n)
        upper_bound = sample_mean + t * sample_sigma / math.sqrt(n)
        margin_error = t * sample_sigma / math.sqrt(n)
        if verbose == True:
            print(f'{round((1-alpha) * 100)}% Confidence Interval for mean is between {round(lower_bound, 2)} and\
    {round(upper_bound, 2)}')
            print(f't (student) statistics with n={n} and alpha={alpha} is equal to {round(t, 2)}')
            print(f'CI width is {round(upper_bound - lower_bound, 2)}')
            print(f'Margin of Error is {round(margin_error, 2)}')
            print(f'Point estimate {round((lower_bound + upper_bound) / 2, 2)}')
        return lower_bound, upper_bound
    else:
        print('Some data is missing. Check input parameters')

# CI for variance

def ci_variance(n, alpha, sample=[], sample_var=False, true_mean=False, verbose=False):
    # when there is a vector of values i.e. sample itself
    if len(sample) != 0:
        sample = np.array(sample)
        n = len(sample)
        sample_var = np.var(sample)

    # known true variance and there is a sample itself
    if (true_mean != False) and (len(sample) != 0):
        chi_squared_right = scipy.stats.chi2.ppf(1 - alpha / 2, n) # bigger number
        chi_squared_left = scipy.stats.chi2.ppf(alpha / 2, n) # smaller number
        numerator = sum((np.array(sample) - true_mean) ** 2)
        lower_bound = numerator / chi_squared_right 
        upper_bound = numerator / chi_squared_left
        if verbose == True:
            print(f'{round((1-alpha) * 100)}% Confidence Interval (CI) for variance is between {round(lower_bound, 2)} and\
    {round(upper_bound, 2)}')
            print(f'Chi-square statistics with n={n} and alpha/2={alpha / 2} is equal to {round(chi_squared_right, 2)}')
            print(f'Chi-square statistics with n={n} and 1-alpha/2={1 - alpha / 2} is equal to {round(chi_squared_left, 2)}')
            print(f'CI width is {round(upper_bound - lower_bound, 2)}')
            print(f'Point estimate {round((upper_bound + lower_bound) / 2, 2)}')
        return lower_bound, upper_bound 
    # unknown true variance but known sample variance
    elif (sample_var != False) and (true_mean == False):
        chi_squared_right = scipy.stats.chi2.ppf(1 - alpha / 2, n - 1) # bigger number
        chi_squared_left = scipy.stats.chi2.ppf(alpha / 2, n - 1) # smaller number
        lower_bound = (n - 1) * sample_var / chi_squared_right
        upper_bound = (n - 1) * sample_var / chi_squared_left
        if verbose == True:
            print(f'{round((1-alpha) * 100)}% Confidence Interval (CI) for variance is between {round(lower_bound, 2)} and\
    {round(upper_bound, 2)}')
            print(f'Chi-square statistics with n={n} and alpha/2={alpha / 2} is equal to {round(chi_squared_right, 2)}')
            print(f'Chi-square statistics with n={n} and 1-alpha/2={1 - alpha / 2} is equal to {round(chi_squared_left, 2)}')
            print(f'CI width is {round(upper_bound - lower_bound, 2)}')
            print(f'Point estimate {round((upper_bound + lower_bound) / 2, 2)}')
        return (n - 1) * sample_var / chi_squared_right, (n - 1) * sample_var / chi_squared_left    
    else:
        print('Some data is missing. Check input parameters')

# CI for probability (share)

def ci_probs(alpha, sample=[], p_hat=False, n=False, verbose=False):
    # when there is a vector of values i.e. sample itself
    if len(sample) != 0:
        sample = np.array(sample)
        n = len(sample)
        p_hat = np.mean(sample)
    
    if (p_hat != False) and (n != False):
        z = scipy.stats.norm.ppf(1 - alpha / 2)
        lower_bound = p_hat - z * math.sqrt(p_hat * (1 - p_hat) / n)
        upper_bound = p_hat + z * math.sqrt(p_hat * (1 - p_hat) / n)
        margin_error = z * math.sqrt(p_hat * (1 - p_hat) / n)
        if verbose == True:
            print(f'{round((1-alpha) * 100, 1)}% Confidence Interval (CI) for mean is between {round(lower_bound, 2)} and\
        {round(upper_bound, 2)}')
            print(f'Z statistics with n={n} and 1 - alpha/2 ={1 - alpha / 2} is equal to {round(z, 2)}')
            print(f'CI width is {round(upper_bound - lower_bound, 2)}')
            print(f'Margin of Error is {round(margin_error, 2)}')
            print(f'Point estimate {round((lower_bound + upper_bound) / 2, 2)}')
        return lower_bound, upper_bound
    else:
        print('Some data is missing. Check input parameters')


# CI for means difference

def ci_mean_dif(alpha, sample_x=[], sample_y=[], sample_mean_x=False, sample_mean_y=False, n_x=False, n_y=False,
                true_var_both=False, true_var_x=False, true_var_y=False, 
               sample_var_x=False, sample_var_y=False, verbose=False):
    
    if (len(sample_x) != 0) and (len(sample_y) != 0):
        sample_x = np.array(sample_x)
        sample_y = np.array(sample_y)
        sample_mean_x = np.mean(sample_x)
        sample_mean_y = np.mean(sample_y)
        n_x = len(sample_x)
        n_y = len(sample_y)
        sample_var_x = np.var(sample_x)
        sample_var_y = np.var(sample_y)
    
    # both true variances are known and equal
    if true_var_both !=False:
        z = scipy.stats.norm.ppf(1 - alpha / 2)
        print('both true variances are known and equal')
        lower_bound = sample_mean_x - sample_mean_y - z * true_var_both / math.sqrt(n_x + n_y)
        upper_bound = sample_mean_x - sample_mean_y + z * true_var_both / math.sqrt(n_x + n_y)
        margin_error = z * true_var_both / math.sqrt(n_x + n_y)
        if verbose == True:
            print(f'{round((1-alpha) * 100, 1)}% Confidence Interval (CI) for difference of means is between\
    {round(lower_bound, 2)} and {round(upper_bound, 2)}')
            print(f'Z statistics with 1 - alpha/2 ={1 - alpha / 2} is equal to {round(z, 2)}')
            print(f'CI width is {round(upper_bound - lower_bound, 2)}')
            print(f'Margin of Error is {round(margin_error, 2)}')
            print(f'Point estimate {round((lower_bound + upper_bound) / 2, 2)}')
        return lower_bound, upper_bound
    
    # both true variances are known and not equal
    elif (true_var_x != False) and (true_var_y != False):
        z = scipy.stats.norm.ppf(1 - alpha / 2)
        print('both true variances are known and not equal')
        lower_bound = sample_mean_x - sample_mean_y - z * math.sqrt(true_var_x/n_x + true_var_y/n_y)
        upper_bound = sample_mean_x - sample_mean_y + z * math.sqrt(true_var_x/n_x + true_var_y/n_y)
        margin_error = z * math.sqrt(true_var_x/n_x + true_var_y/n_y)
        if verbose == True:
            print(f'{round((1-alpha) * 100, 1)}% Confidence Interval (CI) for difference of means is between\
    {round(lower_bound, 2)} and {round(upper_bound, 2)}')
            print(f'Z statistics with 1 - alpha/2 ={1 - alpha / 2} is equal to {round(z, 2)}')
            print(f'CI width is {round(upper_bound - lower_bound, 2)}')
            print(f'Margin of Error is {round(margin_error, 2)}')
            print(f'Point estimate {round((lower_bound + upper_bound) / 2, 2)}')
        
        return lower_bound, upper_bound    
    # both variances are unknown but equal   
    elif (sample_var_x == sample_var_y) and (sample_var_x != False):
        t = scipy.stats.t.ppf(1 - alpha / 2, n_x + n_y - 2)
        print('both variances are unknown but equal')
        lower_bound = sample_mean_x - sample_mean_y - t * (math.sqrt((n_x - 1)*sample_var_x + (n_y - 1)*sample_var_y)) /\
    math.sqrt((n_x * n_y * (n_x + n_y - 2)) / (n_x + n_y))
        upper_bound = sample_mean_x - sample_mean_y + t * (math.sqrt((n_x - 1)*sample_var_x + (n_y - 1)*sample_var_y)) /\
    math.sqrt((n_x * n_y * (n_x + n_y - 2)) / (n_x + n_y))
        margin_error = t * (math.sqrt((n_x - 1)*sample_var_x + (n_y - 1)*sample_var_y)) /\
    math.sqrt((n_x * n_y * (n_x + n_y - 2)) / (n_x + n_y))

        if verbose == True:
            print(f'{round((1-alpha) * 100, 1)}% Confidence Interval (CI) for difference of means is between\
    {round(lower_bound, 2)} and {round(upper_bound, 2)}')
            print(f't statistics with 1 - alpha/2 ={1 - alpha / 2} is equal to {round(t, 2)}')
            print(f'CI width is {round(upper_bound - lower_bound, 2)}')
            print(f'Margin of Error is {round(margin_error, 2)}')
            print(f'Point estimate {round((lower_bound + upper_bound) / 2, 2)}')

        return sample_mean_x - sample_mean_y - t * (math.sqrt((n_x - 1)*sample_var_x + (n_y - 1)*sample_var_y)) /\
    math.sqrt((n_x * n_y * (n_x + n_y - 2)) / (n_x + n_y)),\
    sample_mean_x - sample_mean_y + t * (math.sqrt((n_x - 1)*sample_var_x + (n_y - 1)*sample_var_y)) /\
    math.sqrt((n_x * n_y * (n_x + n_y - 2)) / (n_x + n_y))
    
    # both variances are unknown and unequal
    elif (sample_var_x != False) and (sample_var_y != False) and (sample_var_x != sample_var_y):
        t = scipy.stats.t.ppf(1 - alpha / 2, n_x + n_y - 2)
        print('both variances are unknown and unequal')
        upper_bound = sample_mean_x - sample_mean_y - t * math.sqrt(sample_var_x/n_x + sample_var_x/n_y)
        lower_bound = sample_mean_x - sample_mean_y + t * math.sqrt(sample_var_x/n_x + sample_var_x/n_y)
        margin_error = t * math.sqrt(sample_var_x/n_x + sample_var_x/n_y)
        
        if verbose == True:
            print(f'{round((1-alpha) * 100, 1)}% Confidence Interval (CI) for difference of means is between\
    {round(lower_bound, 2)} and {round(upper_bound, 2)}')
            print(f't statistics with 1 - alpha/2 ={1 - alpha / 2} is equal to {round(t, 2)}')
            print(f'CI width is {round(upper_bound - lower_bound, 2)}')
            print(f'Margin of Error is {round(margin_error, 2)}')
            print(f'Point estimate {round((lower_bound + upper_bound) / 2, 2)}')
        return sample_mean_x - sample_mean_y - t * math.sqrt(sample_var_x/n_x + sample_var_x/n_y),\
    sample_mean_x - sample_mean_y + t * math.sqrt(sample_var_x/n_x + sample_var_x/n_y)
    else:
        print('Some data is missing. Check input parameters')

# CI for probabilities difference

def ci_probs_dif(alpha, sample_x=[], sample_y=[], p_hat_x=False, p_hat_y=False, n_x=False, n_y=False,
verbose=False):
    if (len(sample_x) != 0) and (len(sample_y) != 0):
        sample_x = np.array(sample_x)
        sample_y = np.array(sample_y)
        p_hat_x = np.mean(sample_x)
        p_hat_y = np.mean(sample_y)
        n_x = len(sample_x)
        n_y = len(sample_y)
        
        
    if (p_hat_x != False) and (p_hat_y != False) and (n_x != False) and (n_y != False):
        p_hat = (p_hat_x * n_x + p_hat_y * n_y) / (n_x + n_y)
        z = scipy.stats.norm.ppf(1 - alpha / 2)
        lower_bound = p_hat_x - p_hat_y - z * math.sqrt(p_hat * (1 - p_hat) * (1/n_x + 1/n_y))
        upper_bound = p_hat_x - p_hat_y + z * math.sqrt(p_hat * (1 - p_hat) * (1/n_x + 1/n_y))
        margin_error = z * math.sqrt(p_hat * (1 - p_hat) * (1/n_x + 1/n_y))
        if verbose == True:
            print(f'{round((1-alpha) * 100, 1)}% Confidence Interval (CI) for difference of probabilities is between\
    {round(lower_bound, 2)} and {round(upper_bound, 2)}')
            print(f'Z statistics with 1 - alpha/2 ={1 - alpha / 2} is equal to {round(z, 2)}')
            print(f'CI width is {round(upper_bound - lower_bound, 2)}')
            print(f'Margin of Error is {round(margin_error, 2)}')
            print(f'Point estimate {round((lower_bound + upper_bound) / 2, 2)}')
        return lower_bound, upper_bound
    
    else:
        print('Some data is missing. Check input parameters')

# CI for ratio of variances

def ci_vars_ratio(alpha, sample_x=[], sample_y=[], sample_var_x=False, sample_var_y=False, verbose=False):
    if (len(sample_x) != 0) and (len(sample_y) != 0):
        sample_x = np.array(sample_x)
        sample_y = np.array(sample_y)
        sample_var_x = np.var(sample_x)
        sample_var_y = np.var(sample_y)
        n_x = len(sample_x)
        n_y = len(sample_y)

    if (sample_var_x != False) and (sample_var_y != False):
        F_left = scipy.stats.f.ppf(alpha / 2, n_x - 1, n_y - 1) # smaller number
        F_right = scipy.stats.f.ppf(1 - alpha / 2, n_x - 1, n_y - 1) # bigger number
        lower_bound = (1 / F_left) * (sample_var_x / sample_var_y) 
        upper_bound = (1 / F_right) * (sample_var_x / sample_var_y)
        if verbose == True:
            print(f'{round((1-alpha) * 100, 1)}% Confidence Interval (CI) for ratio of variances is between\
    {round(lower_bound, 2)} and {round(upper_bound, 2)}')
            print(f'F statistics with alpha/2 ={alpha / 2} is equal to {round(F_left, 2)}')
            print(f'F statistics with 1 - alpha/2 ={1 - alpha / 2} is equal to {round(F_right, 2)}')
            print(f'CI width is {round(upper_bound - lower_bound, 2)}')
            print(f'Point estimate {round((lower_bound + upper_bound) / 2, 2)}')
        return lower_bound, upper_bound
    else:
        print('Some data is missing. Check input parameters')



