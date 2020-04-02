'''
Created on Feb 11, 2020
**PIZZA TIPS**
App to collect tip data for analysis
 
@author: Jake from State Farm
'''

import re
import from_CSV

class Employee():
    """Employee constructor
    
    Takes in first and last name and sets pay to minimum wage
    """
    
    
    # TODO from db
    
    def __init__(self, first, last):
        self.first = first
        self.last = last
        self.emp_map = self.create_map()
        self.pay = 11.10
        self.shifts = {}
        self.gross_tips = 0.0
    
    def set_pay(self, pay=11.10):
        self.pay = pay
        
    def create_map(self):
        """Creates dict ,,map'' of sectors by Marks^TM
        
        
        Values range from C to P and 3-19, other sections are considered "OUT"
        """
        mapo = {}
        for a in range(ord('C'),ord('P')):
            for i in range(3,20):
                mapo[chr(a)+str(i)] = Sec(chr(a)+str(i))
                
        mapo["OUT"] = Sec("OUT")
        return mapo
    
    def add_tip_emp(self, sector, tip_amt, tip_type):
        """Creates Tip object, adds to employee's map, adds to latest shift"""
        new_tip = Tip(sector, tip_amt, tip_type)
        self.emp_map[new_tip.sector].add_tip_sec(new_tip)
        list(self.shifts.values())[-1].add_tip_shift(new_tip)
        self.gross_tips += tip_amt
#         self.shifts[len(self.shifts)-1].add_tip_shift(new_tip) # for use with list of shifts
        
    def add_tip_emp_csv(self, csv_fn):
        """Processes CSV file and returns dict of Shifts"""
        shifts_from_csv = from_CSV.get_data_from_csv(csv_fn)
        for shif in shifts_from_csv.items():    # (date, Shift)
            if shif[0] not in self.shifts:      # shif[0] is date
                self.shifts[shif[0]] = shif[1]  # shif[1] is Shift obj
            else:
                self.shifts[shif[0]] + shif[1]
            self.gross_tips += shif[1].shift_total
        
    
    @classmethod
    def from_pay(cls,first, last, pay):
        """Alternate Constructor
        
        Creates Employee with provided hourly pay
        """
        emp = cls(first, last)
        cls.set_pay(emp, pay)
        return emp
         
    def new_shift(self, date):
        """Creates and adds shift to Employee's list of shifts
        
        takes start and end times on schedule, and date
        """
        shift = Shift(date)
#         cls.shifts.append(shift) # for use with list of shifts
        self.shifts[date] = shift
        return shift
    
    @property
    def fullname(self):
        return '{} {}'.format(self.first, self.last)
    @property
    def wage(self):
        return '${}/hr'.format(self.pay)


    def __str__(self):
        return "Employee {}, {}".format(self.fullname, self.wage)
    def __repr__(self):
        return "Employee({}, {})".format(self.first, self.last)
        
class Shift():
    """Shift constructor
    
    Takes schedule time and creates Shift Object
    """
    def __init__(self, date):
        self.date = date
        self.tips = []
        self.shift_total = 0.0
        
    def add_tip_shift(self, tip_obj):
        """Adds Tip object to list of tips for the shift"""
        self.tips.append(tip_obj)
        self.shift_total += tip_obj.tip_amt
        
    def add_tip_shift_list(self, tip_list):
        """Adds list of Tip objects to shift"""
        self.tips += tip_list
#         list_tot = 0.0
        for tips in tip_list:
            self.shift_total += tips.tip_amt            
       
    @property
    def tip_total(self):
        """Returns total tips from shift"""
        return '${}'.format(self.shift_total)
    
    def __add__(self, other):
        if other.__class__.__name__ == 'Shift':
            for tips in other.tips:
                self.shift_total += tips.tip_amt
            return self.tips.extend(other.tips)
        elif(isinstance(other, list)):
            for tips in list:
                self.shift_total += tips.tip_amt
            return self.tips.extend(other)
        else:
            return 'Cannot add {} and {}'.format(type(self), type(other))
        
    def __radd__(self, other):
        return self.__add__(other)
    
class Sec():
    """Sector of map that holds list of Tip objects
    """
    def __init__(self, name):
        self.name = name
        self.sec_tips = []
        self.sector_total = 0.0
        
    def add_tip_sec(self, tip_obj):
        self.sec_tips.append(tip_obj)
        self.sector_total += tip_obj.tip_amt
    
    @property
    def sec_total(self):
        return '${}0'.format(self.sector_total)
    
    
class Tip():
    
#     gross_tips = 0.0
    #TODO from db
    
    def __init__(self, sector, tip_amt, tip_type):
        """Tip Constructor
        
        Takes sector as string "D13", "L10";
              tip_amt as float 5.0, 9.43;
              tip_type as string "$", "cc", "cc/$, sz"
              
        Adds to total amount of tips
        """
        self.sector = sector
        self.tip_type = tip_type 
        if tip_type == "cc/$":
            tip_split = tip_amt.split("/")
            tip_amt = float(tip_split[0]) + float(tip_split[1])
        self.tip_amt = float(tip_amt)
#         Tip.gross_tips += self.tip_amt

    @classmethod
    def from_string(cls, tip_str):
        tip = re.sub(r"\s+", "", tip_str).split(',')
#         print(tip)
        return cls(tip[0], tip[1], tip[2]) 
        
         
    def __str__(self):
        return '${}, {}, from sec {}'.format(self.tip_amt, self.tip_type, self.sector)
        
    def __repr__(self):
        return "Tip({}, {}, {})".format(self.sector, self.tip_amt, self.tip_type)
        
    def __add__(self, other):
        """Overrides add function to access variables"""
        if(isinstance(other,Tip)):
            return self.tip_amt + other.tip_amt
        elif(isinstance(other, float)):
            return self.tip_amt + other
        else:
            return 'Cannot add {} and {}\n'.format(type(self), type(other))
    
    @classmethod
    def gross(cls):
        return '${}'.format(cls.gross_tips)
    

if __name__ == '__main__':
    print("Hello Pizza Tips\n")
    jake = Employee.from_pay("Jacob","Madlem",11.80)
    shelb = Employee("Shelby", "Harmon")
    
    print(jake.fullname)
    print(jake.wage)
    jake.new_shift("Wed, Feb 19" )
    jake.add_tip_emp("D10",5.00,"$")
    jake.add_tip_emp("D10",10.00,"cc")
#     tip_list = [Tip("C17", 10.00, "$"), Tip("C16", 14.00, "cc"), Tip("C8", 5.00, "cc")]
    
    jake.new_shift("Fri, Feb 21")
    jake.add_tip_emp("D12", 12.00,"cc")
    shift1 = list(jake.shifts.items())[0][1]
    shift2 = list(jake.shifts.items())[1][1]
#     shift1.add_tip_shift_csv(tip_list)
    jake.add_tip_emp_csv('Tips Breakdown 2020 - Feb20.csv')
    print(shift1.tips)
    print(shift2.tips)
    print(shift1.tip_total)
    print(shift2.tip_total)
    
    print('derp')
    