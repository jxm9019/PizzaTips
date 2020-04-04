'''
Created on Mar 28, 2020
Takes data from CSV and tries to imput as Tips
@author: Jake from State Farm
'''
import PizzaTips
import pandas as pd

def get_tips_from_csv(csv_fn):
    """Creates list of Shift objects and adds Tips to feed back to main program
    
    
    Takes 'Tips Breakdown 2020 - MMM YY.csv', must be in same format
    """
    tip_list = []
    df = pd.read_csv(csv_fn, sep= ',', header=None, skipinitialspace=True)
    for col in range(1,df.shape[1]):
        date = df.iloc[0][col]
        n_tips = int(df.iloc[1][col])
        series_tips = df.iloc[2:2+n_tips][col]
#         print(date)
        new_shift = PizzaTips.Shift(date)
        for tip in series_tips:
#             print(tip)
            new_shift.add_tip_shift(PizzaTips.Tip.from_string(tip))
#         print('\n')
        tip_list.append(new_shift)
#     print(tip_list)
    return tip_list
    # print(df)
    
def get_shifts_from_csv(csv_fn):
    """Creates list of Shift objects with Shift info to feed back to main program
    
    
    Takes 'Marks Tips 2020 - MMMYY.csv' file
    """
    shift_list = []
    df = pd.read_csv(csv_fn, sep=',', skiprows=[0,1,2], usecols = range(0,5), header=None)
    for idx, row in df.iterrows():
        shift = PizzaTips.Shift(date=row[0], sched_hrs=row[1], actual_hrs=row[2], 
                 actual_miles=row[3], store_miles=row[4])
#         print('Shift(date= \'{}\', sched_hrs= {}, actual_hrs= {}, actual_miles= {}, store_miles= {})'.format(row[0],row[1],row[2],row[3],row[4]))
        shift_list.append(shift)
    return shift_list
    
    
if __name__ == '__main__':
#     testicles = get_tips_from_csv('Tips Breakdown 2020 - Feb20.csv')
#     balls = get_shifts_from_csv('Marks Tips 2020 - Feb20.csv')
    print('derp')