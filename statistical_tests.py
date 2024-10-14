import numpy as np
from scipy import stats
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.multicomp import pairwise_tukeyhsd, MultiComparison
from statsmodels.formula.api import ols
from statsmodels.stats.anova import AnovaRM

def run_statistical_test(test, data):
    if test == "対応のないt検定":
        return t_test_independent(data)
    elif test == "対応のあるt検定":
        return t_test_paired(data)
    elif test == "一元配置分散分析（ANOVA）":
        return one_way_anova(data)
    elif test == "二元配置分散分析":
        return two_way_anova(data)
    elif test == "反復測定分散分析":
        return repeated_measures_anova(data)
    elif test == "共分散分析（ANCOVA）":
        return ancova(data)
    elif test == "Mann-Whitney U検定":
        return mann_whitney_u(data)
    elif test == "Wilcoxon符号順位検定":
        return wilcoxon_signed_rank(data)
    elif test == "Kruskal-Wallis検定":
        return kruskal_wallis(data)
    elif test == "Friedman検定":
        return friedman_test(data)
    elif test == "Spearman順位相関係数":
        return spearman_correlation(data)
    else:
        return "選択された検定はまだ実装されていません。", False

def run_post_hoc_test(test, data):
    if test == "Tukey's HSD検定":
        return tukey_hsd(data)
    elif test == "Dunnett検定":
        return dunnett(data)
    elif test == "Bonferroni法":
        return bonferroni(data)
    elif test == "Holm法":
        return holm(data)
    elif test == "Scheffe法":
        return scheffe(data)
    elif test == "Games-Howell法":
        return games_howell(data)
    else:
        return "選択されたPost Hoc検定はまだ実装されていません。"

def t_test_independent(data):
    group1 = data[data['group'] == data['group'].unique()[0]]['value']
    group2 = data[data['group'] == data['group'].unique()[1]]['value']
    t_stat, p_value = stats.ttest_ind(group1, group2)
    results = f"t統計量: {t_stat:.4f}\np値: {p_value:.4f}"
    return results, p_value < 0.05

def t_test_paired(data):
    group1 = data[data['group'] == data['group'].unique()[0]]['value']
    group2 = data[data['group'] == data['group'].unique()[1]]['value']
    t_stat, p_value = stats.ttest_rel(group1, group2)
    results = f"t統計量: {t_stat:.4f}\np値: {p_value:.4f}"
    return results, p_value < 0.05

def one_way_anova(data):
    groups = [group for name, group in data.groupby('group')['value']]
    f_value, p_value = stats.f_oneway(*groups)
    results = f"F値: {f_value:.4f}\np値: {p_value:.4f}"
    return results, p_value < 0.05

def two_way_anova(data):
    formula = 'value ~ C(factor1) + C(factor2) + C(factor1):C(factor2)'
    model = ols(formula, data).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    results = anova_table.to_string()
    return results, any(anova_table['PR(>F)'] < 0.05)

def repeated_measures_anova(data):
    aov = AnovaRM(data, 'value', 'subject', within=['time'])
    res = aov.fit()
    results = res.summary().as_text()
    return results, res.anova_table['Pr > F']['time'] < 0.05

def ancova(data):
    formula = 'value ~ C(group) + covariate'
    model = ols(formula, data).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    results = anova_table.to_string()
    return results, anova_table.loc['C(group)', 'PR(>F)'] < 0.05

def mann_whitney_u(data):
    group1 = data[data['group'] == data['group'].unique()[0]]['value']
    group2 = data[data['group'] == data['group'].unique()[1]]['value']
    statistic, p_value = stats.mannwhitneyu(group1, group2)
    results = f"U統計量: {statistic:.4f}\np値: {p_value:.4f}"
    return results, p_value < 0.05

def wilcoxon_signed_rank(data):
    group1 = data[data['group'] == data['group'].unique()[0]]['value']
    group2 = data[data['group'] == data['group'].unique()[1]]['value']
    statistic, p_value = stats.wilcoxon(group1, group2)
    results = f"W統計量: {statistic:.4f}\np値: {p_value:.4f}"
    return results, p_value < 0.05

def kruskal_wallis(data):
    groups = [group for _, group in data.groupby('group')['value']]
    statistic, p_value = stats.kruskal(*groups)
    results = f"H統計量: {statistic:.4f}\np値: {p_value:.4f}"
    return results, p_value < 0.05

def friedman_test(data):
    groups = [group for _, group in data.groupby('group')['value']]
    statistic, p_value = stats.friedmanchisquare(*groups)
    results = f"Friedman統計量: {statistic:.4f}\np値: {p_value:.4f}"
    return results, p_value < 0.05

def spearman_correlation(data):
    correlation, p_value = stats.spearmanr(data['x'], data['y'])
    results = f"Spearman相関係数: {correlation:.4f}\np値: {p_value:.4f}"
    return results, p_value < 0.05

def tukey_hsd(data):
    mc = MultiComparison(data['value'], data['group'])
    result = mc.tukeyhsd()
    return str(result)

def dunnett(data):
    from statsmodels.stats.multicomp import pairwise_tukeyhsd
    result = pairwise_tukeyhsd(data['value'], data['group'])
    return str(result)

def bonferroni(data):
    mc = MultiComparison(data['value'], data['group'])
    result = mc.allpairtest(stats.ttest_ind, method='bonf')
    return str(result[0])

def holm(data):
    mc = MultiComparison(data['value'], data['group'])
    result = mc.allpairtest(stats.ttest_ind, method='holm')
    return str(result[0])

def scheffe(data):
    mc = MultiComparison(data['value'], data['group'])
    result = mc.scheffe_test()
    return str(result)

def games_howell(data):
    from statsmodels.stats.multicomp import pairwise_gameshowell
    result = pairwise_gameshowell(data['value'], data['group'])
    return str(result)