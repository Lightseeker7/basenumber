"""Library for integers of arbitrary base system. Any positive integer above 2 for a base, any length of integer. 
Has built in operations of adding, subtracting, multiplication using different algorithms, division and modulus, and exponentiation"""

from baseconvert import base
from copy import deepcopy

KARATSUBA_THRESHOLD = 30 # amount of base-10 digits a value can be below without using karatsuba algorithm

class BaseNumber:

    def __init__(self,value:tuple|int,b_base:int,negative:bool=False):
        """
        >>> i0 = BaseNumber(7,2)
        >>> str(i0)
        "(1, 1, 1) b2 negative:False"
        >>> i1 = BaseNumber((1,11),14,negative=True)
        >>> str(i1)
        "(1, 11) b14 negative:True"
        """
        assert isinstance(negative,bool), "negative must be bool"
        assert isinstance(b_base,int) and b_base >= 2, "base must be integer 2 or above"
        self.negative = negative
        self.base = b_base
        if isinstance(value,tuple):
            for val in value:
                assert isinstance(val,int) and val >= 0 and val < b_base, "all tuple values must be positive integers below the base value"
            if len(value) > 0:
                while value[0] == 0 and len(value) > 1:
                    value = value[1:]
                self.value = value
            else:
                self.value = (0,)
        elif isinstance(value,int):
            self.value = BaseNumber.try_convert(value,10,b_base)
            self.negative = value < 0
        else:
            raise ValueError("value must be tuple or int") 
        if self.value == (0,):
            self.negative = False

    def __str__(self):
        """
        If the value throws an error, shows only the first value and last value

        >>> a = BaseNumber((14,8,7),19)
        >>> str(a)
        "(14, 8, 7) b19 negative:False"
        >>> b = BaseNumber(7,2,negative=True)
        >>> str(b)
        "(1, 1, 1) b2 negative:True"
        """
        try:
            return f"{self.value} b{self.base} negative:{self.negative}"
        except:
            return f"({self.value[0]} . . . {self.value[-1]}) b{self.base} negative:{self.negative}"

    def __int__(self):
        """
        >>> i = BaseNumber((1,1,1),2,negative=True)
        >>> int(i)
        -7
        """
        return {False:1,True:-1}[self.negative] * sum((self.base ** digit) * self.value[-1*(digit+1)] for digit in range(len(self.value)))

    def __float__(self):
        """
        >>> i = BaseNumber((1,1,1),2,negative=True)
        >>> int(i)
        -7
        """
        return float({False:1,True:-1}[self.negative] * sum((self.base ** digit) * self.value[-1*(digit+1)] for digit in range(len(self.value))))

    def __abs__(self):
        """
        >>> a = BaseNumber((23,7),39,negative=True)
        >>> str(abs(a))
        "(23, 7) b39 negative:False"
        """
        new = deepcopy(self)
        new.negative = False
        return new

    def __neg__(self):
        """
        >>> a = BaseNumber((23,7),39,negative=False)
        >>> str(-a)
        "(23, 7) b39 negative:True"
        """
        new = deepcopy(self)
        new.negative = not new.negative
        return new

    def __eq__(self, other):
        """
        Returns True if the other object has an equivalent value in the same base. Returns False if not, or if other object is not a tuple, int, or BaseNumber. Considers negative values for int and BaseNumber but ignores for tuple

        >>> e0 = BaseNumber((1,1,1),2)
        >>> e0 == 7
        True
        >>> e0 == -7
        False
        >>> e1 = BaseNumber((7,),13)
        >>> e0 == e1
        True
        >>> e1.negative = True
        >>> e0 == e1
        False
        >>> e1 == (7,)
        True
        >>> e0 == "string"
        False
        """
        
        if isinstance(other, BaseNumber):
            return BaseNumber.compare(self,other.deep_convert(self.base)) == "="
        elif isinstance(other, BaseRational):
            return BaseRational.compare(BaseRational.create_rational(self,self.base),other.deep_convert(self.base)) == "="
        elif isinstance(other,(int,tuple)):
            return BaseNumber.compare(self,BaseNumber(other,self.base)) == "="
        else:
            return False

    def __lt__(self, other):
        if isinstance(other, BaseNumber):
            return BaseNumber.compare(self,other.deep_convert(self.base)) == "<"
        elif isinstance(other, BaseRational):
            return BaseRational.compare(BaseRational.create_rational(self,self.base),other.deep_convert(self.base)) == "<"
        elif isinstance(other,(int,tuple)):
            return BaseNumber.compare(self,BaseNumber(other,self.base)) == "<"
        else:
            return False

    def __gt__(self, other):
        if isinstance(other, BaseNumber):
            return BaseNumber.compare(self,other.deep_convert(self.base)) == ">"
        elif isinstance(other, BaseRational):
            return BaseRational.compare(BaseRational.create_rational(self,self.base),other.deep_convert(self.base)) == ">"
        elif isinstance(other,(int,tuple)):
            return BaseNumber.compare(self,BaseNumber(other,self.base)) == ">"
        else:
            return False

    def __le__(self, other):
        if isinstance(other, BaseNumber):
            return BaseNumber.compare(self,other.deep_convert(self.base)) in ["=","<"]
        elif isinstance(other, BaseRational):
            return BaseRational.compare(BaseRational.create_rational(self,self.base),other.deep_convert(self.base)) in ["=","<"]
        elif isinstance(other,(int,tuple)):
            return BaseNumber.compare(self,BaseNumber(other,self.base)) in ["=","<"]
        else:
            return False

    def __ge__(self, other):
        if isinstance(other, BaseNumber):
            return BaseNumber.compare(self,other.deep_convert(self.base)) in ["=",">"]
        elif isinstance(other, BaseRational):
            return BaseRational.compare(BaseRational.create_rational(self,self.base),other.deep_convert(self.base)) in ["=",">"]
        elif isinstance(other,(int,tuple)):
            return BaseNumber.compare(self,BaseNumber(other,self.base)) in ["=",">"]
        else:
            return False

    def __add__(self, other):
        if isinstance(other, BaseNumber):
            return BaseNumber.add(self,other.deep_convert(self.base))
        if isinstance(other, BaseRational):
            return BaseRational.add(BaseRational.create_rational(self,self.base),other.deep_convert(self.base))
        elif isinstance(other,(int,tuple)):
            return BaseNumber.add(self,BaseNumber(other,self.base))
        else:
            raise ValueError("BaseNumber object can only be added with BaseNumber, BaseRational, int, or tuple")

    def __sub__(self, other):
        if isinstance(other, BaseNumber):
            return BaseNumber.subtract(self,other.deep_convert(self.base))
        if isinstance(other, BaseRational):
            return BaseRational.subtract(BaseRational.create_rational(self,self.base),other.deep_convert(self.base))
        elif isinstance(other,(int,tuple)):
            return BaseNumber.subtract(self,BaseNumber(other,self.base))
        else:
            raise ValueError("BaseNumber object can only be subtracted with BaseNumber, BaseRational, int, or tuple")

    def __mul__(self, other):
        if isinstance(other, BaseNumber):
            return BaseNumber.multiply(self,other.deep_convert(self.base))
        if isinstance(other, BaseRational):
            return BaseRational.multiply(BaseRational.create_rational(self,self.base),other.deep_convert(self.base))
        elif isinstance(other,(int,tuple)):
            return BaseNumber.multiply(self,BaseNumber(other,self.base))
        else:
            raise ValueError("BaseNumber object can only be multiplied with BaseNumber, BaseRational, int, or tuple of integers")

    def __truediv__(self, other):
        if isinstance(other, BaseNumber):
            return BaseRational(self,other.deep_convert(self.base),self.base,negative=self.negative ^ other.negative)
        if isinstance(other, BaseRational):
            return BaseRational.divide(BaseRational.create_rational(self,self.base),other.deep_convert(self.base))
        elif isinstance(other,(int,tuple)):
            return BaseRational(self,BaseNumber(other,self.base),self.base,negative=self.negative ^ (other < 0))
        else:
            raise ValueError("BaseNumber object can only be divided with BaseNumber, BaseRational, int, or tuple")

    def __floordiv__(self, other):
        if isinstance(other, BaseNumber):
            return BaseNumber.divmod(self,other.deep_convert(self.base))[0]
        elif isinstance(other,(int,tuple)):
            return BaseNumber.divmod(self,BaseNumber(other,self.base))[0]
        else:
            raise ValueError("BaseNumber object can only be floor divided with BaseNumber, int, or tuple")
    
    def __mod__(self, other):
        if isinstance(other, BaseNumber):
            return BaseNumber.divmod(self,other.deep_convert(self.base))[1]
        elif isinstance(other,(int,tuple)):
            return BaseNumber.divmod(self,BaseNumber(other,self.base))[1]
        else:
            raise ValueError("BaseNumber object can only use modulo with BaseNumber, int, or tuple")

    def __divmod__(self, other):
        if isinstance(other, BaseNumber):
            return BaseNumber.divmod(self,other.deep_convert(self.base))
        elif isinstance(other,(int,tuple)):
            return BaseNumber.divmod(self,BaseNumber(other,self.base))
        else:
            raise ValueError("BaseNumber object can only use divmod with BaseNumber, int, or tuple")

    def __pow__(self, other):
        if isinstance(other, BaseNumber):
            return BaseNumber.exponent(self,other.deep_convert(self.base))
        elif isinstance(other,(int,tuple)):
            return BaseNumber.exponent(self,BaseNumber(other,self.base))
        else:
            raise ValueError("BaseNumber object can only use exponentiation with BaseNumber, int, or tuple")

    def __len__(self):
        return len(self.value)

    def convert(self,new_base:int) -> BaseNumber:
        """
        Converts this number to a new base, returns itself

        :param new_base: new base
        :type new_base: int
        :return: self
        :rtype: BaseNumber

        >>> c = BaseNumber((1,1,1,1),2)
        >>> c.convert(10)
        >>> str(c)
        "(1, 5) b10 negative:False"
        """

        self.value = BaseNumber.try_convert(self.value,self.base,new_base)
        self.base = new_base

        return self

    def deep_convert(self,new_base:int) -> BaseNumber:
        """
        Returns a copy of this number with a new base

        :param new_base: new base
        :type new_base: int
        :return: copied object with new base
        :rtype: BaseNumber

        >>> c0 = BaseNumber((1,1,1,1),2)
        >>> c1 = c0.deep_convert(10)
        >>> str(c0)
        "(1, 1, 1, 1) b2 negative:False"
        >>> str(c1)
        "(1, 5) b10 negative:False"
        """

        converted = deepcopy(self)

        converted.convert(new_base)

        return converted

    def rational(self) -> BaseRational:
        """
        Returns a copy of this number as a BaseRational object
        """

        return BaseRational.create_rational(self,self.base)

    @staticmethod
    def try_convert(num:int|tuple[int],i_base:int,b_base:int) -> tuple[int]:
        """
        Converts a number or BaseNumber value to any base, uses a recursive method if baseconvert fails

        :param num: integer to be converted
        :type num: int|tuple[int]
        :param i_base: initial base of number
        :type i_base: int
        :param b_base: base of new number
        :type b_base: int
        :return: converted value
        :rtype: tuple[int]

        >>> try_convert(13,10,2)
        (1, 1, 0, 1)
        >>> try_convert((1,1,0,1),2,10)
        (1, 3)
        """

        try:
            if isinstance(num, tuple):
                return base(num,i_base,b_base)
            elif isinstance(num,int):
                return base(abs(num),i_base,b_base)
            else:
                raise ValueError("invalid type for base")
        except:
            if isinstance(num,int):
                count = 0
                counter = deepcopy(num)
                while counter != 0:
                    counter = count // 10
                    count += 1
                count = count // 2
                nl = num // (10 ** count)
                nr = num % (10 ** count)
                return BaseNumber.try_convert(nl,i_base,b_base) + BaseNumber.try_convert(nr,i_base,b_base)
            elif isinstance(num,tuple):
                m = len(num) // 2
                nl = num[:m]
                nr = num[m:]
                return BaseNumber.try_convert(nl,i_base,b_base) + BaseNumber.try_convert(nr,i_base,b_base)
            else:
                raise ValueError("invalid type for base")

    @staticmethod
    def validate_bases(num1:BaseNumber,num2:BaseNumber):
        """
        Raises an error if the bases of the two numbers are not the same or if one of the objects is not a BaseNumber object
        
        :param num1: number to validate
        :type num1: BaseNumber
        :param num2: number to validate
        :type num2: BaseNumber
        """

        num1 = deepcopy(num1)
        num2 = deepcopy(num2)

        assert isinstance(num1,BaseNumber) and isinstance(num2,BaseNumber), "object(s) not a BaseNumber"

        if num1.base != num2.base:
            raise ValueError("function requires BaseNumber objects of equivalent bases")

    @staticmethod
    def compare(num1:BaseNumber,num2:BaseNumber,ignore_negative:bool=False) -> str:
        """
        Compares two BaseNumber objects and returns either "<" "=" ">"

        :param num1: number to compare
        :type num1: BaseNumber
        :param num2: number to compare
        :type num2: BaseNumber
        :param ignore_negative: whether or not to consider the negative
        :type ignore_negative: bool
        :return: representation of comparison
        :rtype: str

        >>> c0 = BaseNumber((4,2,3),5)
        >>> c1 = BaseNumber((4,0,4),5)
        >>> BaseNumber.compare(c0,c1)
        ">"
        >>> c0, c1 = c1, c0
        >>> BaseNumber.compare(c0,c1)
        "<"
        >>> c1.value = (4,0,4)
        >>> BaseNumber.compare(c0,c1)
        "="
        """

        BaseNumber.validate_bases(num1,num2)
        
        num1 = deepcopy(num1)
        num2 = deepcopy(num2)        

        if not ignore_negative and num1.negative ^ num2.negative:
            if num1.negative:
                return "<"
            elif num2.negative:
                return ">"
            
        if not ignore_negative and num1.negative and num2.negative:
            num1, num2 = num2, num1

        ln1 = len(num1.value)
        ln2 = len(num2.value)

        if ln1 == ln2:
            for digit in range(ln1):
                try:
                    if num1.value[digit] < num2.value[digit]:
                        return "<"
                    elif num1.value[digit] > num2.value[digit]:
                        return ">"
                except:
                    print(num1.value)
                    print(num2.value)
                    raise ValueError("What the freaking heck")
            return "="
        elif ln1 < ln2:
            return "<"
        else:
            return ">"
        

    @staticmethod
    def add(num1:BaseNumber,num2:BaseNumber) -> BaseNumber:
        """
        Adds two numbers of equivalent base

        :param num1: number to be added
        :type num1: BaseNumber
        :param num2: number to be added
        :type num2: BaseNumber
        :return: sum of numbers
        :rtype: BaseNumber

        >>> a0 = BaseNumber((3,4),5)
        >>> a1 = BaseNumber((1,0,4),5)
        >>> str(BaseNumber.add(a0,a1))
        "(1, 4, 3) b5 negative:False
        """

        BaseNumber.validate_bases(num1,num2)

        num1 = deepcopy(num1)
        num2 = deepcopy(num2)

        b_base = num1.base

        if not num1.negative ^ num2.negative:
            m = max(len(num1.value),len(num2.value)) + 1

            n1d = [digit for digit in num1.value]
            n2d = [digit for digit in num2.value]

            while len(n1d) < m:
                n1d.insert(0,0)
            while len(n2d) < m:
                n2d.insert(0,0)

            carry = 0
            s_digits = []

            for digit in range(-1,-1*m-1,-1):
                cur_sum = sum([n1d[digit],n2d[digit],carry])
                s_digits.insert(0,cur_sum % b_base)
                carry = cur_sum // b_base

            while len(s_digits) > 1 and s_digits[0] == 0:
                s_digits = s_digits[1:]

            return BaseNumber(tuple(i for i in s_digits),b_base,num1.negative)
        else:
            comp = BaseNumber.compare(num1,num2,ignore_negative=True)

            if comp == "=":
                return BaseNumber((0,),b_base)

            if comp == ">":
                top = [i for i in num1.value]
                top_negative = num1.negative
                bottom = [i for i in num2.value]
            else:
                top = [i for i in num2.value]
                top_negative = num2.negative
                bottom = [i for i in num1.value]

            while len(bottom) < len(top):
                bottom.insert(0,0)

            s_digits = []

            for i in range(-1,-1*len(top)-1,-1):
                if top[i] < bottom[i]:
                    top[i-1] -= 1
                    top[i] = top[i] + b_base
                s_digits.insert(0,top[i] - bottom[i])

            while len(s_digits) > 1 and s_digits[0] == 0:
                s_digits = s_digits[1:]

            return BaseNumber(tuple(i for i in s_digits),b_base,top_negative)

    @staticmethod
    def subtract(num1:BaseNumber,num2:BaseNumber) -> BaseNumber:
        """
        Subtracts two numbers of equivalent base

        :param num1: number to be subtracted from
        :type num1: BaseNumber
        :param num2: number to be subtracted
        :type num2: BaseNumber
        :return: sum of numbers
        :rtype: BaseNumber

        >>> s0 = BaseNumber((1,3),10)
        >>> s1 = BaseNumber((8,),10)
        >>> str(BaseNumber.subtract(s0,s1))
        "(5,) b10 negative:False
        >>> str(BaseNumber.subtract(s1,s0))
        "(5,) b10 negative:True
        """

        num1 = deepcopy(num1)
        num2 = deepcopy(num2)

        num2.negative = not num2.negative

        return BaseNumber.add(num1,num2)

    @staticmethod
    def multiply(num1:BaseNumber,num2:BaseNumber,allow_karatsuba:bool=True):
        """
        Multiplies two numbers of equivalent base
        Will use karatsuba algorithm if the number in base 10 has more digits than the threshold (default 30)
        Converts them to integers, multiplying them, and reconverting them back
        If this or karatsuba fails, it will use the raw_multiply function

        :param num1: number to be multiplied
        :type num1: BaseNumber
        :param num2: number to be multiplied
        :type num2: BaseNumber
        :param allow_karatsuba: whether or not to permit calling karatsuba
        :type allow_karatsuba: bool
        :return: product of numbers
        :rtype: BaseNumber
        """

        BaseNumber.validate_bases(num1,num2)

        num1 = deepcopy(num1)
        num2 = deepcopy(num2)

        b_base = num1.base

        karatsuba_comparator = BaseNumber(int("".join("9" for _ in range(KARATSUBA_THRESHOLD))),b_base)

        n1c = BaseNumber.compare(num1,karatsuba_comparator,ignore_negative=True)
        n2c = BaseNumber.compare(num2,karatsuba_comparator,ignore_negative=True)

        try:
            if allow_karatsuba and (n1c == ">" or n2c == ">"):
                return BaseNumber.karatsuba(num1,num2)
            else:
                return BaseNumber(int(num1) * int(num2),b_base,num1.negative ^ num2.negative)
        except:
            return BaseNumber.raw_multiply(num1,num2)

    @staticmethod
    def raw_multiply(num1:BaseNumber,num2:BaseNumber) -> BaseNumber:
        """
        Multiplies two numbers of equivalent base using fundamental arithmetic

        :param num1: number to be multiplied
        :type num1: BaseNumber
        :param num2: number to be multiplied
        :type num2: BaseNumber
        :return: product of numbers
        :rtype: BaseNumber
        """

        BaseNumber.validate_bases(num1,num2)

        num1 = deepcopy(num1)
        num2 = deepcopy(num2)

        b_base = num1.base

        if num1.value == (0,) or num2.value == (0,):
            return BaseNumber((0,),b_base,num1.negative ^ num2.negative)
        if num1.value == (1):
            return num2
        if num2.value == (1):
            return num1

        if BaseNumber.compare(num1,num2,ignore_negative=True) == "<":
            num1, num2 = num2, num1

        s_digits = []

        for bd in range(len(num2.value)):
            t_digits = []

            for td in range(len(num1.value)):
                t_digits.insert(0,num2.value[(bd+1) * -1] * num1.value[(td+1) * -1])

            for _ in range(bd):
                t_digits.append(0)

            while len(s_digits) < len(t_digits):
                s_digits.insert(0,0)

            for i in range(len(s_digits)):
                s_digits[i] = s_digits[i] + t_digits[i]

        if len(s_digits) == 0:
            return BaseNumber((0,),b_base,num1.negative ^ num2.negative)

        for i in range(len(s_digits)):
            val = s_digits[(i+1) * -1]
            s_digits[(i+1) * -1] = val % b_base
            try:
                s_digits[(i+2) * -1] += val // b_base
            except:
                s_digits.insert(0,val // b_base)

        while s_digits[0] > b_base:
            val = s_digits[0]
            s_digits[0] = val % b_base
            s_digits.insert(0,val // b_base)

        while len(s_digits) > 1 and s_digits[0] == 0:
            s_digits = s_digits[1:]

        return BaseNumber(tuple(digit for digit in s_digits),b_base,num1.negative ^ num2.negative)

    @staticmethod
    def exponent(num:BaseNumber,exponent:BaseNumber) -> BaseNumber|BaseRational:
        """
        Raises a BaseNumber to the power of a BaseNumber exponent

        :param num1: number to be raised
        :type num1: BaseNumber
        :param num2: exponent
        :type num2: BaseNumber
        :return: product of exponential, if exponent is negative, returns a BaseRational
        :rtype: BaseNumber|BaseRational
        """

        BaseNumber.validate_bases(num,exponent)

        num = deepcopy(num)
        exponent = deepcopy(exponent)

        b_base = num.base
        end_negative = num.negative
        exp_negative = exponent.negative

        num.negative = False
        exponent.negative = False

        if exp_negative and num.value == (0,):
            raise ZeroDivisionError("zero to a negative power")
    
        if exponent.value == (0,) and num.value == (0,):
            return BaseNumber((1,),b_base)
        if exponent.value == (1,):
            num.negative = end_negative
            if not exp_negative:
                return num
            else:
                return BaseRational.create_rational(num,b_base).deep_invert()
        if num.value == (0,) or num.value == (1,):
            num.negative = end_negative and abs(int(BaseNumber.divmod(exponent,BaseNumber(2,b_base))[1])) == 1
            return num

        raised = BaseNumber((1,),b_base)
        
        dm = BaseNumber.divmod(exponent,BaseNumber(2,b_base))

        odd_exp = dm[1]
        
        while BaseNumber.compare(exponent,BaseNumber((0,),b_base)) == ">":
            if dm[1].value == (1,):
                raised = BaseNumber.raw_multiply(raised,num)
            num = BaseNumber.raw_multiply(num,num)
            exponent = dm[0]
            dm = BaseNumber.divmod(exponent,BaseNumber(2,b_base))

        raised.negative = end_negative and (abs(int(odd_exp)) == 1)

        if not exp_negative:
            return raised
        else:
            return BaseRational.create_rational(raised,b_base).deep_invert()

    @staticmethod
    def karatsuba(num1:BaseNumber,num2:BaseNumber) -> BaseNumber:
        """
        Multiplies two numbers of equivalent base using the karatsuba algorithm

        :param num1: number to be multiplied
        :type num1: BaseNumber
        :param num2: number to be multiplied
        :type num2: BaseNumber
        :return: product of numbers
        :rtype: BaseNumber
        """

        def split_at(num:BaseNumber,d:int) -> tuple[BaseNumber,BaseNumber]:
            """
            Splits a number into its low "d" digits and its high digits

            :param num: number to be split
            :type num: BaseNumber
            :param d: low digits
            :type d: int
            :return: split numbers
            :rtype: tuple[BaseNumber,BaseNumber]
            """

            num = deepcopy(num)
            b_base = num.base

            if len(num.value) == 1:
                return num

            return BaseNumber(num.value[:(-1*d)],b_base), BaseNumber(num.value[(-1*d):],b_base)

        BaseNumber.validate_bases(num1,num2)

        num1 = deepcopy(num1)
        num2 = deepcopy(num2)

        vl = max(num1.value,num2.value)

        end_negative = num1.negative ^ num2.negative

        num1.negative = False
        num2.negative = False

        b_base = num1.base

        vl = max(len(num1.value),len(num2.value))

        num1.value = tuple(0 for _ in range(vl - len(num1.value))) + num1.value
        num2.value = tuple(0 for _ in range(vl - len(num1.value))) + num2.value

        if len(num1.value) < 2 or len(num2.value) < 2: # if the number is less than the base value return to traditional multiplication
            return BaseNumber.raw_multiply(num1,num2)

        m = max(len(num1.value),len(num2.value))
        m2 = m // 2

        high1, low1 = split_at(num1,m2)
        high2, low2 = split_at(num2,m2)

        z0 = BaseNumber.karatsuba(low1,low2)
        z3 = BaseNumber.karatsuba(BaseNumber.add(low1,high1),BaseNumber.add(low2,high2))
        z2 = BaseNumber.karatsuba(high1,high2)

        bb = BaseNumber((1,0),b_base)
        m22b = BaseNumber(m2*2,b_base)
        m2b = BaseNumber(m2,b_base)

        e0 = BaseNumber.exponent(bb,m22b)
        e1 = BaseNumber.exponent(bb,m2b)

        a0 = BaseNumber.raw_multiply(z2,e0)
        a1 = BaseNumber.raw_multiply(BaseNumber.subtract(BaseNumber.subtract(z3,z2),z0),e1)
        a2 = BaseNumber.add(a0,a1)
        f = BaseNumber.add(a2,z0)

        f.negative = end_negative

        return f

    @staticmethod
    def divmod(dividend:BaseNumber,divisor:BaseNumber) -> tuple[BaseNumber,BaseNumber]:
        """
        Divids two numbers of equivalent base and returns the floored divide and the modulus
        
        :param num1: dividend
        :type num1: BaseNumber
        :param num2: divisor
        :type num2: BaseNumber
        :return: floored quotient and modulus
        :rtype: tuple[BaseNumber,BaseNumber]
        """

        BaseNumber.validate_bases(dividend,divisor)

        dividend = deepcopy(dividend)
        divisor = deepcopy(divisor)

        orig_neg = (dividend.negative,divisor.negative)

        dividend.negative, divisor.negative = False, False

        b_base = dividend.base

        if divisor.value == (0,):
            raise ZeroDivisionError("cannot divide by 0")
        if dividend.value == (0,):
            return BaseNumber((0,),b_base), BaseNumber((0,),b_base)

        comp = BaseNumber.compare(dividend,divisor)

        if comp == "<": # if divisor is greater than dividend, return 0 as floor divide and dividend as modulus
            pos_floor_val = [0]
            pos_mod_val = [digit for digit in dividend.value]
        elif comp == "=": # if numbers are the same, then return 1 as floor divide and 0 as modulus
            pos_floor_val = [1]
            pos_mod_val = [0]
        else:
            pos_floor_bn = BaseNumber((0,),b_base)

            dividend_index = 0
            used_digits = 1
            prefix_digits = []

            dd_len = len(dividend.value)

            while dividend_index < dd_len:
                used_val = prefix_digits + [digit for digit in dividend.value[dividend_index:dividend_index + used_digits]]
                            
                while BaseNumber.compare(divisor,BaseNumber(tuple(digit for digit in used_val),b_base)) != "<":
                    used_digits += 1
                    used_val = prefix_digits + [digit for digit in dividend.value[dividend_index:dividend_index + used_digits]]
                    if dividend_index + used_digits > dd_len:
                        break

                dividend_index = dividend_index + used_digits - 1

                cur_div = BaseNumber(tuple(digit for digit in used_val),b_base)

                div_count = BaseNumber((0,),b_base)

                while BaseNumber.compare(divisor,cur_div) != ">":
                    cur_div = BaseNumber.subtract(cur_div,divisor)
                    div_count = BaseNumber.add(div_count,BaseNumber((1,),b_base))

                pos_floor_bn = BaseNumber.add(pos_floor_bn,BaseNumber(tuple([digit for digit in div_count.value] + [0 for _ in range(dd_len - 1 - dividend_index)]),b_base))
                prefix_digits = [digit for digit in cur_div.value]

                dividend_index += 1
                used_digits = 1

            pos_floor_val = [digit for digit in pos_floor_bn.value]
            if len(prefix_digits) > 0:
                pos_mod_val = prefix_digits
            else:
                pos_mod_val = [0]

        if orig_neg[0] and orig_neg[1]:
            floor_bn = BaseNumber(tuple(digit for digit in pos_floor_val),b_base)
            mod_bn = BaseNumber(tuple(digit for digit in pos_mod_val),b_base,negative=True)
        elif orig_neg[0] and not orig_neg[1]:
            if pos_mod_val == [0]:
                floor_bn = BaseNumber(tuple(digit for digit in pos_floor_val),b_base,negative=True)
                mod_bn = BaseNumber(tuple(digit for digit in pos_mod_val),b_base)
            else:
                floor_bn = BaseNumber(tuple(digit for digit in pos_floor_val),b_base)
                floor_bn = BaseNumber.add(floor_bn,BaseNumber((1,),b_base))
                floor_bn.negative = True
                mod_bn = BaseNumber(tuple(digit for digit in pos_mod_val),b_base)
                mod_bn = BaseNumber.subtract(divisor,mod_bn)
        elif not orig_neg[0] and orig_neg[1]:
            if pos_mod_val == [0]:
                floor_bn = BaseNumber(tuple(digit for digit in pos_floor_val),b_base,negative=True)
                mod_bn = BaseNumber(tuple(digit for digit in pos_mod_val),b_base)
            else:
                floor_bn = BaseNumber(tuple(digit for digit in pos_floor_val),b_base)
                floor_bn = BaseNumber.add(floor_bn,BaseNumber((1,),b_base))
                floor_bn.negative = True
                mod_bn = BaseNumber(tuple(digit for digit in pos_mod_val),b_base)
                divisor.negative = True
                mod_bn = BaseNumber.add(divisor,mod_bn)
        else:
            floor_bn = BaseNumber(tuple(digit for digit in pos_floor_val),b_base)
            mod_bn = BaseNumber(tuple(digit for digit in pos_mod_val),b_base)

        return floor_bn, mod_bn

    @staticmethod
    def gcd(num1:BaseNumber,num2:BaseNumber) -> BaseNumber:
        """
        Find greatest common denominator of two numbers of equivalent base
        
        :param num1: number to check
        :type num1: BaseNumber
        :param num2: number to check
        :type num2: BaseNumber
        :return: greatest common denominator
        :rtype: BaseNumber
        """

        BaseNumber.validate_bases(num1,num2)

        num1 = deepcopy(num1)
        num2 = deepcopy(num2)

        num1, num2 = abs(num1), abs(num2)

        while num2.value != (0,):
            num1, num2 = num2, BaseNumber.divmod(num1,num2)[1]

        return num1

class BaseRational:

    def __init__(self,numerator:BaseNumber|int|tuple,denominator:BaseNumber|int|tuple,b_base:int,negative:bool=False,simplify:bool=True):
        """
        numerator and denominator will be stored as positive. Accepts BaseNumber, integer, or tuple.
        Automatically simplifies upon creation if not otherwise set
        """

        if isinstance(numerator,BaseNumber):
            numerator = numerator.deep_convert(b_base)
        elif isinstance(numerator,(int,tuple)):
            numerator = BaseNumber(numerator,b_base)
        else:
            raise ValueError("numerator must be BaseNumber, int, or tuple")
        if isinstance(denominator,BaseNumber):
            denominator = denominator.deep_convert(b_base)
        elif isinstance(denominator,(int,tuple)):
            denominator = BaseNumber(denominator,b_base)
        else:
            raise ValueError("denominator must be BaseNumber, int, or tuple")

        numerator.negative, denominator.negative = False, False

        self.sim = simplify
        self.numerator, self.denominator = numerator, denominator
        self.simplify()
        self.base = b_base
        self.negative = negative

    @staticmethod
    def create_rational(input_val:BaseNumber|int|tuple,b_base:int,simplify:bool=True) -> BaseRational:
        """
        Creates and returns a BaseRational object from a single input value and base

        :param input_val: takes BaseNumber, integer, or tuple
        :type input_val: BaseNumber|int|tuple
        :param b_base: base of BaseRational
        :type b_base: int
        :param simplify: whether or not to simplify this object
        :type simplify: bool
        :return: BaseRational object
        :rtype: BaseRational
        """

        input_val = deepcopy(input_val)
        b_base = deepcopy(b_base)

        if isinstance(input_val,BaseNumber):
            input_negative = input_val.negative
            return BaseRational(abs(input_val.deep_convert(b_base)),BaseNumber((1,),b_base),b_base,negative=input_negative,simplify=simplify)
        elif isinstance(input_val,int):
            return BaseRational(input_val,BaseNumber((1,),b_base),b_base,negative=input_val < 0,simplify=simplify)
        elif isinstance(input_val,tuple):
            return BaseRational(input_val,BaseNumber((1,),b_base),b_base,simplify=simplify)
        else:
            raise ValueError("create_rational requires either BaseNumber, integer, or tuple")

    def __str__(self):
        return f"{str(self.numerator)[:str(self.numerator).index("b")]}\n---\n{str(self.denominator)[:str(self.denominator).index("b")]}\nb{self.base} negative:{self.negative} simplify:{self.sim}"

    def __float__(self):
        return {True:-1,False:1}[self.negative] * float(self.numerator) / float(self.denominator)

    def __abs__(self):
        new = deepcopy(self)
        new.negative = False
        return new

    def __neg__(self):
        new = deepcopy(self)
        new.negative = not new.negative
        return new

    def __eq__(self, other):
        if isinstance(other, BaseRational):
            return BaseRational.compare(self,other.deep_convert(self.base)) == "="
        elif isinstance(other, BaseNumber):
            return BaseRational.compare(self,BaseRational.create_rational(other,other.base).deep_convert(self.base)) == "="
        elif isinstance(other,(int,tuple)):
            return BaseRational.compare(self,BaseRational.create_rational(other,self.base)) == "="
        else:
            return False

    def __lt__(self, other):
        if isinstance(other, BaseRational):
            return BaseRational.compare(self,other.deep_convert(self.base)) == "<"
        elif isinstance(other, BaseNumber):
            return BaseRational.compare(self,BaseRational.create_rational(other,other.base).deep_convert(self.base)) == "<"
        elif isinstance(other,(int,tuple)):
            return BaseRational.compare(self,BaseRational.create_rational(other,self.base)) == "<"
        else:
            return False

    def __gt__(self, other):
        if isinstance(other, BaseRational):
            return BaseRational.compare(self,other.deep_convert(self.base)) == ">"
        elif isinstance(other, BaseNumber):
            return BaseRational.compare(self,BaseRational.create_rational(other,other.base).deep_convert(self.base)) == ">"
        elif isinstance(other,(int,tuple)):
            return BaseRational.compare(self,BaseRational.create_rational(other,self.base)) == ">"
        else:
            return False

    def __le__(self, other):
        if isinstance(other, BaseRational):
            return BaseRational.compare(self,other.deep_convert(self.base)) in ["=","<"]
        elif isinstance(other, BaseNumber):
            return BaseRational.compare(self,BaseRational.create_rational(other,other.base).deep_convert(self.base)) in ["=","<"]
        elif isinstance(other,(int,tuple)):
            return BaseRational.compare(self,BaseRational.create_rational(other,self.base)) in ["=","<"]
        else:
            return False

    def __ge__(self, other):
        if isinstance(other, BaseRational):
            return BaseRational.compare(self,other.deep_convert(self.base)) in ["=",">"]
        elif isinstance(other, BaseNumber):
            return BaseRational.compare(self,BaseRational.create_rational(other,other.base).deep_convert(self.base)) in ["=",">"]
        elif isinstance(other,(int,tuple)):
            return BaseRational.compare(self,BaseRational.create_rational(other,self.base)) in ["=",">"]
        else:
            return False

    def __add__(self, other):
        if isinstance(other, BaseRational):
            return BaseRational.add(self,other.deep_convert(self.base))
        elif isinstance(other, BaseNumber):
            return BaseRational.add(self,BaseRational.create_rational(other,other.base).deep_convert(self.base))
        elif isinstance(other,(int,tuple)):
            return BaseRational.add(self,BaseRational.create_rational(other,self.base))
        else:
            raise ValueError("BaseRational object can only be added with BaseNumber, BaseRational, int, or tuple")

    def __sub__(self, other):
        if isinstance(other, BaseRational):
            return BaseRational.subtract(self,other.deep_convert(self.base))
        elif isinstance(other, BaseNumber):
            return BaseRational.subtract(self,BaseRational.create_rational(other,other.base).deep_convert(self.base))
        elif isinstance(other,(int,tuple)):
            return BaseRational.subtract(self,BaseRational.create_rational(other,self.base))
        else:
            raise ValueError("BaseRational object can only be subtracted with BaseNumber, BaseRational, int, or tuple")

    def __mul__(self, other):
        if isinstance(other, BaseRational):
            return BaseRational.multiply(self,other.deep_convert(self.base))
        elif isinstance(other, BaseNumber):
            return BaseRational.multiply(self,BaseRational.create_rational(other,other.base).deep_convert(self.base))
        elif isinstance(other,(int,tuple)):
            return BaseRational.multiply(self,BaseRational.create_rational(other,self.base))
        else:
            raise ValueError("BaseRational object can only be multiplied with BaseNumber, BaseRational, int, or tuple")

    def __truediv__(self, other):
        if isinstance(other, BaseRational):
            return BaseRational.divide(self,other.deep_convert(self.base))
        elif isinstance(other, BaseNumber):
            return BaseRational.divide(self,BaseRational.create_rational(other,other.base).deep_convert(self.base))
        elif isinstance(other,(int,tuple)):
            return BaseRational.divide(self,BaseRational.create_rational(other,self.base))
        else:
            raise ValueError("BaseRational object can only be divided with BaseNumber, BaseRational, int, or tuple")

    def __pow__(self, other):
        if isinstance(other, BaseNumber):
            return BaseRational.exponent(self,other.deep_convert(self.base))
        elif isinstance(other,(int,tuple)):
            return BaseRational.exponent(self,BaseNumber(other,self.base))
        else:
            raise ValueError("BaseRational object can only use exponentiation with BaseNumber, int, or tuple")
    
    def simplify(self):
        """
        If simplifying is enabled for this instance, divides both the numerator and denominator by their gcd, and returns itself. If not, returns itself.
        """

        if self.sim:
            gcd = BaseNumber.gcd(self.numerator,self.denominator)
            self.numerator = self.numerator // gcd
            self.denominator = self.denominator // gcd
        return self

    def force_simplify(self):
        """
        Ignores whether simplifying is enabled, and divides both the numerator and denominator by their gcd, and returns itself.
        """

        gcd = BaseNumber.gcd(self.numerator,self.denominator)
        self.numerator = self.numerator // gcd
        self.denominator = self.denominator // gcd
        return self

    def deep_simplify(self):
        """
        Returns a copy of this instance force simplified.
        """

        new = deepcopy(self)
        new.force_simplify()
        return new

    def convert(self,b_base:int):
        """
        Converts the numerator and denominator to a new base and returns itself.

        :param b_base: new base
        :type b_base: int
        """

        self.numerator.convert(b_base)
        self.denominator.convert(b_base)
        self.base = b_base

        return self

    def deep_convert(self,b_base:int):
        """
        Returns a copy of this object converted to a new base

        :param b_base: new base
        :type b_base: int
        """

        new = deepcopy(self)
        new.convert(b_base)
        return new

    def invert(self):
        """
        Swaps numerator and denominator, returns itself
        """

        self.numerator, self.denominator = self.denominator, self.numerator

        return self

    def deep_invert(self):
        """
        Returns a copy of itself with numerator and denominator swapped
        """

        new = deepcopy(self)
        new.invert()
        return new

    def mixed(self,simplify:bool=True):
        """
        Returns a tuple of a mixed rational number, BaseNumber and BaseRational
        Will return None for any zero values
        """

        quotient, remainder = BaseNumber.divmod(self.numerator,self.denominator)

        if quotient.value == (0,):
            quotient = None
        else:
            quotient.negative = deepcopy(self.negative)
        if remainder.value == (0,):
            remainder = None
        else:
            remainder = BaseRational(remainder,deepcopy(self.denominator),deepcopy(self.base),negative=deepcopy(self.negative),simplify=simplify)

        return quotient, remainder

    @staticmethod
    def validate_bases(num1:BaseRational,num2:BaseRational):
        """
        Raises an error if either number is not a BaseRational object or if the bases are not the same.
        """

        num1 = deepcopy(num1)
        num2 = deepcopy(num2)

        if not isinstance(num1,BaseRational) or not isinstance(num2,BaseRational) or num1.base != num2.base:
            raise ValueError("must be two BaseRational objects of equivalent base")
        if num1.denominator.value == (0,) or num2.denominator.value == (0,):
            raise ZeroDivisionError("invalid BaseRational object: denominators cannot have a value of 0")

    @staticmethod
    def compare(num1:BaseRational,num2:BaseRational,algorithm:int=0,allow_karatsuba:bool=True,ignore_negative:bool=False) -> str:
        """
        Compares two BaseRational objects of equivalent base.
        Cross multiplies the denominators to have an equivalent denominator, then compares the modified numerators, then returns a string either "<" "=" or ">". 

        The algorithm called depends on the algorithm parameter
        Default value for aglorithm is 0:

        0 - BaseNumber.multiply
        1 - BaseNumber.raw_multiply
        2 - BaseNumber.karatsuba

        :param num1: number to be compared
        :type num1: BaseRational
        :param num2: number to be compared
        :type num2: BaseRational
        :param algorithm: value corresponding to the algorithm used, default is 0 for BaseRational.multiply
        :type algorithm: int
        :param allow_karatsuba: whether or not to permit calling karatsuba
        :type allow_karatsuba: bool
        :param ignore_negative: whether or not to ignore the negative, default is False
        :type ignore_negative: bool
        :return: comparison string
        :rtype: str
        """

        BaseRational.validate_bases(num1,num2)

        num1 = deepcopy(num1)
        num2 = deepcopy(num2)

        if algorithm == 0:
            n1_num = BaseNumber.multiply(num1.numerator,num2.denominator,allow_karatsuba=allow_karatsuba)
            n2_num = BaseNumber.multiply(num2.numerator,num1.denominator,allow_karatsuba=allow_karatsuba)
        elif algorithm == 1:
            n1_num = BaseNumber.raw_multiply(num1.numerator,num2.denominator)
            n2_num = BaseNumber.raw_multiply(num2.numerator,num1.denominator)
        elif algorithm == 2:
            n1_num = BaseNumber.karatsuba(num1.numerator,num2.denominator)
            n2_num = BaseNumber.karatsuba(num2.numerator,num1.denominator)
        else:
            raise ValueError(f"algorithm takes 0, 1, or 2, not {algorithm}")

        n1_num.negative = num1.negative
        n2_num.negative = num2.negative

        return BaseNumber.compare(n1_num,n2_num,ignore_negative=ignore_negative)

    @staticmethod
    def multiply(num1:BaseRational,num2:BaseRational,allow_karatsuba:bool=True,simplify:bool=True) -> BaseRational:
        """
        Multiplies two numbers of equivalent base by multiplying the numerator with the numerator and the denominator with the denominator, simplifying them, and returning.
        Will use karatsuba algorithm if the number in base 10 has more digits than the threshold (default 30)
        Converts them to integers, multiplying them, and reconverting them back
        If this or karatsuba fails, it will use the raw_multiply function

        :param num1: number to be multiplied
        :type num1: BaseRational
        :param num2: number to be multiplied
        :type num2: BaseRational
        :param allow_karatsuba: whether or not to permit calling karatsuba
        :type allow_karatsuba: bool
        :param simplify: whether or not the output should be a simplified value
        :type simplify: bool
        :return: product of numbers
        :rtype: BaseRational
        """

        BaseRational.validate_bases(num1,num2)

        num1 = deepcopy(num1)
        num2 = deepcopy(num2)

        if num1.numerator.value == (0,) or num2.numerator.value == (0,):
            return BaseRational(BaseNumber((0,),num1.base),BaseNumber((1,),num1.base),num1.base)

        return BaseRational(BaseNumber.multiply(num1.numerator,num2.numerator,allow_karatsuba=allow_karatsuba),BaseNumber.multiply(num1.denominator,num2.denominator,allow_karatsuba=allow_karatsuba),num1.base,negative=num1.negative ^ num2.negative,simplify=simplify)

    @staticmethod
    def raw_multiply(num1:BaseRational,num2:BaseRational,simplify:bool=True) -> BaseRational:
        """
        Multiplies two numbers of equivalent base by multiplying the numerator with the numerator and the denominator with the denominator, simplifying them, and returning.
        Uses basic arithmetic.

        :param num1: number to be multiplied
        :type num1: BaseRational
        :param num2: number to be multiplied
        :type num2: BaseRational
        :param simplify: whether or not the output should be a simplified value
        :type simplify: bool
        :return: product of numbers
        :rtype: BaseRational
        """

        BaseRational.validate_bases(num1,num2)

        num1 = deepcopy(num1)
        num2 = deepcopy(num2)

        if num1.numerator.value == (0,) or num2.numerator.value == (0,):
            return BaseRational(BaseNumber((0,),num1.base),BaseNumber((1,),num1.base),num1.base)

        return BaseRational(BaseNumber.raw_multiply(num1.numerator,num2.numerator),BaseNumber.raw_multiply(num1.denominator,num2.denominator),num1.base,negative=num1.negative ^ num2.negative,simplify=simplify)

    @staticmethod
    def karatsuba(num1:BaseRational,num2:BaseRational,simplify:bool=True) -> BaseRational:
        """
        Multiplies two numbers of equivalent base by multiplying the numerator with the numerator and the denominator with the denominator, simplifying them, and returning.
        Uses the karatsuba algorithm.

        :param num1: number to be multiplied
        :type num1: BaseRational
        :param num2: number to be multiplied
        :type num2: BaseRational
        :param simplify: whether or not the output should be a simplified value
        :type simplify: bool
        :return: product of numbers
        :rtype: BaseRational
        """

        BaseRational.validate_bases(num1,num2)

        num1 = deepcopy(num1)
        num2 = deepcopy(num2)

        if num1.numerator.value == (0,) or num2.numerator.value == (0,):
            return BaseRational(BaseNumber((0,),num1.base),BaseNumber((1,),num1.base),num1.base)

        return BaseRational(BaseNumber.karatsuba(num1.numerator,num2.numerator),BaseNumber.karatsuba(num1.denominator,num2.denominator),num1.base,negative=num1.negative ^ num2.negative,simplify=simplify)

    @staticmethod
    def divide(dividend:BaseRational,divisor:BaseRational,algorithm:int=0,allow_karatsuba:bool=True,simplify:bool=True) -> BaseRational:
        """
        Inverts the divisor, then calls a multiplication algorithm.

        The algorithm called depends on the algorithm parameter
        Default value for aglorithm is 0:

        0 - BaseRational.multiply
        1 - BaseRational.raw_multiply
        2 - BaseRational.karatsuba

        :param dividend: dividend
        :type dividend: BaseRational
        :param divisor: divisor
        :type divisor: BaseRational
        :param algorithm: value corresponding to the algorithm used, default is 0 for BaseRational.multiply
        :type algorithm: int
        :param allow_karatsuba: whether or not to permit calling karatsuba
        :type allow_karatsuba: bool
        :param simplify: whether or not the output should be a simplified value
        :type simplify: bool
        :return: product of numbers
        :rtype: BaseRational
        """

        BaseRational.validate_bases(dividend,divisor)

        dividend = deepcopy(dividend)
        divisor = divisor.deep_invert()

        if algorithm == 0:
            return BaseRational.multiply(dividend,divisor,allow_karatsuba=allow_karatsuba,simplify=simplify)
        elif algorithm == 1:
            return BaseRational.raw_multiply(dividend,divisor,simplify=simplify)
        elif algorithm == 2:
            return BaseRational.karatsuba(dividend,divisor,simplify=simplify)
        else:
            raise ValueError(f"algorithm takes 0, 1, or 2, not {algorithm}")

    @staticmethod
    def add(num1:BaseRational,num2:BaseRational,algorithm:int=0,allow_karatsuba:bool=True,simplify:bool=True) -> BaseRational:
        """
        Adds two BaseRational objects of equivalent base.
        Cross multiplies the denominators to have an equivalent denominator, then adds the modified numerators, then returns it simplified. 

        The algorithm called depends on the algorithm parameter
        Default value for aglorithm is 0:

        0 - BaseNumber.multiply
        1 - BaseNumber.raw_multiply
        2 - BaseNumber.karatsuba

        :param num1: number to be added
        :type num1: BaseRational
        :param num2: number to be added
        :type num2: BaseRational
        :param algorithm: value corresponding to the algorithm used, default is 0 for BaseRational.multiply
        :type algorithm: int
        :param allow_karatsuba: whether or not to permit calling karatsuba
        :type allow_karatsuba: bool
        :param simplify: whether or not the output should be a simplified value
        :type simplify: bool
        :return: sum of numbers
        :rtype: BaseRational
        """

        BaseRational.validate_bases(num1,num2)

        num1 = deepcopy(num1)
        num2 = deepcopy(num2)

        if algorithm == 0:
            den = BaseNumber.multiply(num1.denominator,num2.denominator,allow_karatsuba=allow_karatsuba)
            n1_num = BaseNumber.multiply(num1.numerator,num2.denominator,allow_karatsuba=allow_karatsuba)
            n2_num = BaseNumber.multiply(num2.numerator,num1.denominator,allow_karatsuba=allow_karatsuba)
        elif algorithm == 1:
            den = BaseNumber.raw_multiply(num1.denominator,num2.denominator)
            n1_num = BaseNumber.raw_multiply(num1.numerator,num2.denominator)
            n2_num = BaseNumber.raw_multiply(num2.numerator,num1.denominator)
        elif algorithm == 2:
            den = BaseNumber.karatsuba(num1.denominator,num2.denominator)
            n1_num = BaseNumber.karatsuba(num1.numerator,num2.denominator)
            n2_num = BaseNumber.karatsuba(num2.numerator,num1.denominator)
        else:
            raise ValueError(f"algorithm takes 0, 1, or 2, not {algorithm}")

        n1_num.negative = num1.negative
        n2_num.negative = num2.negative

        sum_num = n1_num + n2_num

        return BaseRational(sum_num,den,num1.base,negative=sum_num.negative,simplify=simplify)

    @staticmethod
    def subtract(num1:BaseRational,num2:BaseRational,algorithm:int=0,allow_karatsuba:bool=True,simplify:bool=True) -> BaseRational:
        """
        Subtracts two BaseRational objects of equivalent base.
        Cross multiplies the denominators to have an equivalent denominator, inverts the second number's negative value, then adds the modified numerators, then returns it simplified. 

        The algorithm called depends on the algorithm parameter
        Default value for aglorithm is 0:

        0 - BaseNumber.multiply
        1 - BaseNumber.raw_multiply
        2 - BaseNumber.karatsuba

        :param num1: number to be subtracted from
        :type num1: BaseRational
        :param num2: number to subtract
        :type num2: BaseRational
        :param algorithm: value corresponding to the algorithm used, default is 0 for BaseRational.multiply
        :type algorithm: int
        :param allow_karatsuba: whether or not to permit calling karatsuba
        :type allow_karatsuba: bool
        :param simplify: whether or not the output should be a simplified value
        :type simplify: bool
        :return: sum of numbers
        :rtype: BaseRational
        """

        BaseRational.validate_bases(num1,num2)

        num1 = deepcopy(num1)
        num2 = deepcopy(num2)

        num2.negative = not num2.negative

        return BaseRational.add(num1,num2,algorithm=algorithm,allow_karatsuba=allow_karatsuba,simplify=simplify)

    @staticmethod
    def exponent(num:BaseRational,exponent:BaseNumber,simplify:bool=True) -> BaseRational:
        """
        Raises a number to a BaseNumber exponent. Inverts if the exponent is negative.

        :param num: number to be raised
        :type num: BaseRational
        :param exponent: exponent
        :type exponent: BaseNumber
        :param simplify: whether or not the output should be a simplified value
        :type simplify: bool
        :return: product of exponential
        :rtype: BaseRational
        """

        num = deepcopy(num)
        exponent = deepcopy(exponent)
        
        BaseRational.validate_bases(num,BaseRational.create_rational(exponent,exponent.base))

        end_negative = num.negative
        exp_negative = exponent.negative

        exponent.negative = False

        p_num = abs(BaseNumber.exponent(num.numerator,exponent))
        p_den = abs(BaseNumber.exponent(num.denominator,exponent))

        if not exp_negative:
            return BaseRational(p_num,p_den,num.base,negative=end_negative and BaseNumber.divmod(exponent,BaseNumber(2,exponent.base))[1].value != (0,),simplify=simplify)
        else:
            return BaseRational(p_num,p_den,num.base,negative=end_negative and BaseNumber.divmod(exponent,BaseNumber(2,exponent.base))[1].value != (0,),simplify=simplify).deep_invert()
