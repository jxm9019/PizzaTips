'''
Created on Feb 11, 2020
**PIZZA TIPS**
App to collect tip data for analysis
 
@author: Jake from State Farm
'''

class Employee():
    """Employee constructor
    
    Takes in first and last name and sets pay to minimum wage
    """
    
    SHIFTS = []
    # TODO from db
    
    def __init__(self, first, last):
        self.first = first
        self.last = last
        self.emp_map = self.create_map()
        self.pay = 11.10
    
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
        self.SHIFTS[len(self.SHIFTS)-1].add_tip_shift(new_tip)
    
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
    @property
    def shifts(self):
        return self.SHIFTS

    def __str__(self):
        return "Employee {}, {}".format(self.fullname, self.wage)
    def __repr__(self):
        return "Employee({}, {})".format(self.first, self.last)
        
class Shift():
    """Shift constructor
    
    Takes schedule time and creates Shift Object
    """
    def __init__(self, start, end, date):
        self.start = start
        self.end = end
        self.date = date
        self.tips = []
        self.total = 0.0
        
    def add_tip_shift(self, tip_obj):
        """Adds Tip object to list of tips for the shift"""
        self.tips.append(tip_obj)
        self.total += tip_obj.tip_amt
        
    @property
    def tip_total(self):
        """Returns total tips from shift"""
        return '${}'.format(self.total)
    
    
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
    
    gross_tips = 0.0
    #TODO from db
    
    def __init__(self, sector, tip_amt, tip_type):
        """Tip Constructor
        
        Takes sector as string "D13", "L10";
              tip_amt as float 5.0, 9.43;
              tip_type as string "$", "cc", "cc/$"
              
        Adds to total amount of tips
        """
        self.sector = sector
        self.tip_amt = tip_amt
        self.tip_type = tip_type 
        Tip.gross_tips += tip_amt

        
         
    def __str__(self):
        return '${}, {}, from sec {}'.format(self.tip_amt, self.tip_type, self.sector)
        
    def __repr__(self):
        return "Tip({}, {}, {})".format(self.tip_amt, self.tip_type, self.sector)
        
    def __add__(self, other):
        """Overrides add function to access variables"""
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
    jake.new_shift(10, 13, "2/19/20" )
    jake.add_tip_emp("D10",5.00,"$")
    jake.add_tip_emp("D10",10.00,"cc")
    
    jake.new_shift(17,24,"2/21/20")
    jake.add_tip_emp("D12", 12.00,"cc")
    shift1 = jake.shifts[0]
    shift2 = jake.shifts[1]
    print(shift1.tips)
    print(shift2.tips)
    print(shift1.tip_total)
    print(shift2.tip_total)
    
    print('derp')
    