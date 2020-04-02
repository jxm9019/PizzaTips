'''
Created on Mar 28, 2020
Takes data from CSV and tries to imput as Tips
@author: Jake from State Farm
'''
import PizzaTips
import pandas as pd

def get_data_from_csv(csv_fn):
    tip_dic = {}
    df = pd.read_csv(csv_fn, sep= ',', header=None, skipinitialspace=True)
    for row in range(1,df.shape[1]):
        date = df.iloc[0][row]
        n_tips = int(df.iloc[1][row])
        series_tips = df.iloc[2:2+n_tips][row]
        print(date)
        new_shift = PizzaTips.Shift(date)
        for tip in series_tips:
            print(tip)
            new_shift.add_tip_shift(PizzaTips.Tip.from_string(tip))
        print('\n')
        tip_dic[date] = new_shift
    print(tip_dic)
    return tip_dic
    # print(df)
if __name__ == '__main__':
    testicles = get_data_from_csv('Tips Breakdown 2020 - Feb20.csv')
    print('derp')