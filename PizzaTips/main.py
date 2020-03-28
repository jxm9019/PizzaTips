'''
Created on Feb 11, 2020
**PIZZA TIPS**
App to collect tip data for analysis
 
@author: Jake from State Farm
'''
# from pip._internal import self_outdated_check

class Employee():
    """Employee constructor
    
    Takes in first and last name and sets pay to minimum wage
    """
    
    SHIFTS = []
    # TODO from db
    
    def __init__(self, first, last):
        self.first = first
        self.last = last
        self.map = Map()
        self.pay = 11.10
    
    def set_pay(self, pay=11.10):
        self.pay = pay
        
    @classmethod
    def from_pay(cls,first, last, pay):
        """Alternate Constructor
        
        Creates Employee with provided hourly pay
        """
        emp = cls(first, last)
        cls.set_pay(emp, pay)
        return emp
        
    @classmethod
    def new_shift(cls, start, end, date):
        """Creates and adds shift to Employee's list of shifts
        
        takes start and end times on schedule, and date
        """
        shift = Shift(start, end, date)
        cls.SHIFTS.append(shift)
        return shift
    
    @property
    def fullname(self):
        return '{} {}'.format(self.first, self.last)
    @property
    def wage(self):
        return '${}/hr'.format(self.pay)

        
class Shift(Employee):
    """Shift constructor
    
    Takes schedule time and creates Shift Object
    """
    def __init__(self, start, end, date):
        self.start = start
        self.end = end
        self.date = date
        self.tips = []
        self.total = 0.0
        
    def add_tip(self, sector, tip_amt, tip_type):
        """Creates and adds Tip object to list of tips for the shift"""
        self.tips.append(Tip(sector, tip_amt, tip_type))
        self.total += tip_amt
        
    @property
    def tip_total(self):
        """Returns total tips from shift"""
        return '${}'.format(self.total)
    
        
class Map():
    """2D Map of sectors
    
    holds total tips, 'heatmap', tips per sector
    """
    super_map = {}
    
    def __init__(self):
        for a in range(ord('C'),ord('P')):
            for i in range(3,20):
                self.super_map[chr(a)+str(i)] = Sec(chr(a)+str(i))

    
    def add_tip_map(self, tip_obj):
        print("add tip to map")
        self.super_map[tip_obj.sector].add_tip_sec(tip_obj)
        
        
class Sec():
    """Sector of map that holds list of Tip objects
    """
    sector_total = 0.0
    def __init__(self, name):
        self.name = name
        self.sec_tips = []
        
    def add_tip_sec(self, tip_obj):
        print("add tip to sector")
        self.sec_tips.append(tip_obj)
        self.sector_total += tip_obj.tip_amt
        pass
    
class Tip(Map):
    
    gross_tips = 0.0
    #TODO from db
    
    def __init__(self, sector, tip_amt, tip_type):
        self.sector = sector
        self.tip_amt = tip_amt
        self.tip_type = tip_type 
        Tip.gross_tips += tip_amt
        Map.add_tip_map(self, self)
        
         
    def __str__(self):
        return '${}, {}, from sec {}'.format(self.tip_amt, self.tip_type, self.sector)
        
    def __repr__(self):
        return "Tip({}, {}, {})".format(self.tip_amt, self.tip_type, self.sector)
        
    def __add__(self, other):
        if(isinstance(other,Tip)):
            return self.tip_amt + other.tip_amt
        elif(isinstance(other, float)):
            return self.tip_amt + other
        else:
            return 'Cannot add {} and {}\n'.format(self.type, other.type)
    
    @classmethod
    def gross(cls):
        return '${}'.format(cls.gross_tips)
    

if __name__ == '__main__':
    print("Hello Pizza Tips\n")
    jake = Employee.from_pay("Jacob","Madlem",11.80)
    shelb = Employee("Shelby", "Harmon")
    
    print(jake.fullname)
    print(jake.wage)
    shift1 = jake.new_shift(10, 13, "2/19/20" )
    shift1.add_tip("J13",5.00,"$")
    shift1.add_tip("D10",10.00,"cc")
    
    shift2 = jake.new_shift(17,24,"2/21/20")
    shift2.add_tip("D12", 12.00,"cc")
    print(shift1.tips)
    print(shift2.tips)
    print(shift1.tip_total)
    print(shift2.tip_total)
    
    print('derp')
    