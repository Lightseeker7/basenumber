"""Library for integers of arbitrary base system. Any positive integer above 2 for a base, any length of integer. 
Has built in operations of adding, subtracting, multiplication using different algorithms, division and modulus, and exponentiation"""

from baseconvert import base
from copy import deepcopy

class BaseNumber:

    KARATSUBA_THRESHOLD = 30 # amount of base-10 digits a value can be below without using karatsuba algorithm

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
        new.negative = True
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
        elif isinstance(other,(int,tuple)):
            return BaseNumber.compare(self,BaseNumber(other,self.base)) == "="
        else:
            return False

    def __lt__(self, other):
        if isinstance(other, BaseNumber):
            return BaseNumber.compare(self,other.deep_convert(self.base)) == "<"
        elif isinstance(other,(int,tuple)):
            return BaseNumber.compare(self,BaseNumber(other,self.base)) == "<"
        else:
            return False

    def __gt__(self, other):
        if isinstance(other, BaseNumber):
            return BaseNumber.compare(self,other.deep_convert(self.base)) == ">"
        elif isinstance(other,(int,tuple)):
            return BaseNumber.compare(self,BaseNumber(other,self.base)) == ">"
        else:
            return False

    def __le__(self, other):
        if isinstance(other, BaseNumber):
            return BaseNumber.compare(self,other.deep_convert(self.base)) in ["=","<"]
        elif isinstance(other,(int,tuple)):
            return BaseNumber.compare(self,BaseNumber(other,self.base)) in ["=","<"]
        else:
            return False

    def __ge__(self, other):
        if isinstance(other, BaseNumber):
            return BaseNumber.compare(self,other.deep_convert(self.base)) in ["=",">"]
        elif isinstance(other,(int,tuple)):
            return BaseNumber.compare(self,BaseNumber(other,self.base)) in ["=",">"]
        else:
            return False

    def __add__(self, other):
        if isinstance(other, BaseNumber):
            return BaseNumber.add(self,other.deep_convert(self.base))
        elif isinstance(other,(int,tuple)):
            return BaseNumber.add(self,BaseNumber(other,self.base))
        else:
            raise ValueError("BaseNumber object can only be added with BaseNumber, int, or tuple")

    def __sub__(self, other):
        if isinstance(other, BaseNumber):
            return BaseNumber.subtract(self,other.deep_convert(self.base))
        elif isinstance(other,(int,tuple)):
            return BaseNumber.subtract(self,BaseNumber(other,self.base))
        else:
            raise ValueError("BaseNumber object can only be subtracted with BaseNumber, int, or tuple")

    def __mul__(self, other):
        if isinstance(other, BaseNumber.deep_convert(self.base)):
            return BaseNumber.multiply(self,other)
        elif isinstance(other,(int,tuple)):
            return BaseNumber.multiply(self,BaseNumber(other,self.base))
        else:
            raise ValueError("BaseNumber object can only be added to BaseNumber, int, or tuple of integers")

    def __floordiv__(self, other):
        if isinstance(other, BaseNumber):
            return BaseNumber.divmod(self,other.deep_convert(self.base))[0]
        elif isinstance(other,(int,tuple)):
            return BaseNumber.divmod(self,BaseNumber(other,self.base))[0]
        else:
            raise ValueError("BaseNumber object can only be divided with BaseNumber, int, or tuple")
    
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

        num1 = deepcopy(num1)
        num2 = deepcopy(num2)

        BaseNumber.validate_bases(num1,num2)

        if not ignore_negative and num1.negative ^ num2.negative:
            if num1.negative:
                return "<"
            elif num2.negative:
                return ">"

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

        num1 = deepcopy(num1)
        num2 = deepcopy(num2)

        BaseNumber.validate_bases(num1,num2)

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

        num1 = deepcopy(num1)
        num2 = deepcopy(num2)

        BaseNumber.validate_bases(num1,num2)

        b_base = num1.base

        karatsuba_comparator = BaseNumber(int("".join("9" for _ in range(BaseNumber.KARATSUBA_THRESHOLD))),b_base)

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

        num1 = deepcopy(num1)
        num2 = deepcopy(num2)

        BaseNumber.validate_bases(num1,num2)

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
    def exponent(num:BaseNumber,exponent:BaseNumber) -> BaseNumber:
        """
        Raises a BaseNumber to the power of a BaseNumber exponent if the exponent is not negative

        :param num1: number to be raised
        :type num1: BaseNumber
        :param num2: exponent
        :type num2: BaseNumber
        :return: product of exponential
        :rtype: BaseNumber
        """

        num = deepcopy(num)
        exponent = deepcopy(exponent)

        BaseNumber.validate_bases(num,exponent)

        b_base = num.base
        end_negative = num.negative

        num.negative = False

        assert not exponent.negative, "exponent cannot be negative"
    
        if exponent.value == (0,) and num.value == (0,):
            return BaseNumber((1,),b_base)
        if exponent.value == (1,):
            num.negative = end_negative
            return num
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

        return raised

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

        num1 = deepcopy(num1)
        num2 = deepcopy(num2)

        vl = max(num1.value,num2.value)

        BaseNumber.validate_bases(num1,num2)

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

        dividend = deepcopy(dividend)
        divisor = deepcopy(divisor)

        BaseNumber.validate_bases(dividend,divisor)

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