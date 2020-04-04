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
        
    def add_tips_emp_csv(self, csv_fn):
        """Processes CSV file and returns dict of Shifts"""
        tips_from_csv = from_CSV.get_tips_from_csv(csv_fn)
        for shif in tips_from_csv:    # (date, Shift)
            # Add Shift to employee if it does not exist
            if shif.date not in self.shifts:      
                self.shifts[shif.date] = shif
            else: # Add to shift if it is already there, not sure if I'll keep this
                self.shifts[shif.date] + shif
            self.gross_tips += shif.shift_total
        
    
    @classmethod
    def from_pay(cls,first, last, pay):
        """Alternate Constructor
        
        Creates Employee with provided hourly pay
        """
        emp = cls(first, last)
        cls.set_pay(emp, pay)
        return emp
         
    def new_shift(self, date):
        """Creates and adds Shifts with tip details to Employee's list of shifts
        
        takes date
        """
#         cls.shifts.append(shift) # for use with list of shifts
        if isinstance(date, Shift):
            if date.date != self.shifts[date.date].date:
                self.shifts[date.date] = date
            else:
                return self.update_shift(date)
        elif date not in self.shifts:
            shift = Shift(date)
            self.shifts[date] = shift
            return shift
        else:
            return self.shifts[date]
    
    def add_shifts_from_csv(self, csv_fn):
        """Creates and adds Shift skeletons with no tip details from CSV"""
        shifts_from_csv = from_CSV.get_shifts_from_csv(csv_fn)
        for shift in shifts_from_csv:
            if shift.date not in self.shifts:
                self.shifts[shift.date] = shift
            else:
                self.update_shift(shift)
    
    def update_shift(self, shift_obj):
        """Compares each attribute of Shift object to be updated
        
        If the old value is < new, it gets updated
        """
        for attr, val in shift_obj:
            if getattr(self.shifts[shift_obj.date], attr) < val:
                setattr(self.shifts[shift_obj.date], attr, val)
        return self.shifts[shift_obj.date]
        
    @property
    def fullname(self):
        return '{} {}'.format(self.first, self.last)
    @property
    def wage(self):
        return '${:0,.2f}/hr'.format(self.pay)


    def __str__(self):
        return "Employee {}, {}".format(self.fullname, self.wage)
    def __repr__(self):
        return "Employee({}, {})".format(self.first, self.last)
        
class Shift():
    """Shift constructor
    
    Takes schedule time and creates Shift Object
    """
    def __init__(self, date, sched_hrs=0, actual_hrs=0.0, 
                 actual_miles=0.0, store_miles=0):
        self.date = date
        self.tips = []
        self.shift_cash = 0.0
        self.shift_cc = 0.0
        self.shift_total = 0.0
        self.sched_hrs = sched_hrs
        self.actual_hrs = actual_hrs
        self.store_miles = store_miles
        self.actual_miles = actual_miles
        self.orders = 0
        
    def add_tip_shift(self, tip_obj):
        """Adds Tip object to list of tips for the shift"""
        self.tips.append(tip_obj)
        self.shift_cash += tip_obj.tip_cash
        self.shift_cc += tip_obj.tip_cc
        self.shift_total += tip_obj.tip_amt
        self.orders += 1
        
    def add_tip_shift_list(self, tip_list):
        """Adds list of Tip objects to shift"""
        for tip in tip_list:
            self.add_tip_shift(tip)
    
       
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
        return other.__add__(self)
    
    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value
#     def __getattr__(self, attr):
        
class Sec():
    """Sector of map that holds list of Tip objects
    """
#     total_stiffs = 0
    
    def __init__(self, name):
        self.name = name
        self.sec_tips = []
        self.sec_cc = 0.0
        self.sec_cash = 0.0
        self.sector_total = 0.0
#         self.sec_stiffs = 0
        
    def add_tip_sec(self, tip_obj):
        """Adds tip to sector, updating each tip value; $/cc/tot"""
        self.sec_tips.append(tip_obj)
        self.sec_cc += tip_obj.tip_cc
        self.sec_cash += tip_obj.tip_cash
        self.sector_total += tip_obj.tip_amt
#         if tip_obj.tip_amt <= 0.5:
#             self.sec_stiffs += 1
#             Sec.total_stiffs += 1
    
    @property
    def sec_total(self):
        return '${:0,.2f}'.format(self.sector_total)
    
    
class Tip():
    """Tip Constructor
    
    Takes sector as string "D13", "L10";
          tip_amt as float 5.0, 9.43;
          tip_type as string "$", "cc", "cc/$, sz, oop"
          
    Adds to total amount of tips
    """
    def __init__(self, sector, tip_amt, tip_type):
        self.sector = sector
        self.tip_type = tip_type
        self.tip_cash = 0.0
        self.tip_cc = 0.0
        if(tip_type == "cc/$"):
            tip_amt = tip_amt.split("/")
            self.tip_cc = float(tip_amt[0])
            self.tip_cash = float(tip_amt[1])
        elif(tip_type == "$"):
            self.tip_cash = float(tip_amt)
        elif(tip_type == "cc"):
            self.tip_cc = float(tip_amt)
        else:
            self.tip_amt = float(tip_amt)
        self.tip_amt = self.tip_cc + self.tip_cash
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
        return '${:0,.2f}'.format(cls.gross_tips)
    

if __name__ == '__main__':
    print("Hello Pizza Tips\n")
    jake = Employee.from_pay("Jacob","Madlem",11.80)
    shelb = Employee("Shelby", "Harmon")
    
    print(jake.fullname)
    print(jake.wage)
#     jake.new_shift("Sat, Feb 1")
#     jake.add_tip_emp("D10",5.00,"$")
#     jake.add_tip_emp("D10",10.00,"cc")
#     tip_list = [Tip("C17", 10.00, "$"), Tip("C16", 14.00, "cc"), Tip("C8", 5.00, "cc")]
    
#     jake.new_shift("Fri, Feb 21")
#     jake.add_tip_emp("D12", 12.00,"cc")
#     jake.new_shift(Shift('Sat, Feb 1', 5.0, 6.5, 39.0, 41.0))
#     shift1.add_tip_shift_csv(tip_list)
    jake.add_shifts_from_csv('Marks Tips 2020 - Feb20.csv')
    jake.add_tips_emp_csv('Tips Breakdown 2020 - Feb20.csv')
    jake.add_shifts_from_csv('Marks Tips 2020 - Mar20.csv')
    jake.add_tips_emp_csv('Tips Breakdown 2020 - Mar20.csv')
#     print(shift1.tips)
#     print(shift2.tips)
#     print(shift1.tip_total)
#     print(shift2.tip_total)
    
    print('derp')
    