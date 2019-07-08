from .keywords import *
from decimal import *

# imported functions and constants
functions = ("d", "root", "factorial", "log10", "log2", "sin", "cos", "tan", "rad", "deg")
constants = ("pi", "e")

# global variables for evaluation purposes
variables = {}


getcontext().prec = 6


def to_expr(_string):

    """
    return type: string
    This function is used to make any string, 
    as eval()-friendly as possible.
    """

    string = ''
    for key in _string:
        if key.isupper():
            key = key.lower()
        string = string + key


    # making the string more operation-friendly.
    string = (
                string
                .replace(" ", "", -1)
                .replace("++", "+", -1)
                .replace("--", "-", -1)
             )

    # necessary variables.
    temp_string = ""
    parantheses = []
    operations = [0]
    i = 0

    # necessary changes if user is not python-friendly.
    for index, s in enumerate(string):
        if (index - 1) > -1:

            previous = string[index - 1]
            condition = (previous != "*" 
                        and previous != "-" 
                        and previous != "+" 
                        and previous != "/" 
                        and previous != "(")

            if s == "(" and condition:
                temp_string += "*" + s
                    
            elif s.isalpha() and condition and not previous.isalpha() and previous != "(":
                temp_string += "*" + s

            else:
                temp_string += s
        else:
            temp_string += s

    string = temp_string
    temp_string = ""

    for f in functions:
        target = string.find(f)
        if target != -1:
            string = string.replace(f+"*", f, -1)
    
    
    ###########################################################################################
    # loop through string and convert it to temp_string.
    for index, s in enumerate(string):

        # keeping index up to date with additional symbols.
        index += i

        # when the current position is "!".
        if s == '!': 

            # when the previous character was ")".
            if temp_string[index - 1] == ")" and parantheses:
                temp_string = (temp_string[:parantheses[-1]] 
                            + "!" 
                            + temp_string[parantheses[-1]:] 
                            + ")")
                i += 1 # added ")"

            # when there were no prior operations.
            elif not operations[-1] and string.find("(") == -1: ### PROBLEM WITH CORRECT FACTORIAL ORDER FOR FIRST CHARACTERS AFTER THE "(".
                temp_string = ("!" 
                            + temp_string 
                            + ")")
                i += 1 # added ")"
                ### PROBLEM WITH CORRECT FACTORIAL ORDER FOR FIRST CHARACTERS AFTER THE "(".

            # when there was nothing before it then ignore it.
            elif not temp_string or operations[-1] == index-1: 
                i -= 1 # removed "!"
                temp_string = temp_string[:operations[-1]]
                i -= 1

            # if none of the above.
            else:
                temp_string = (temp_string[:operations[-1] + 1] 
                            + "!" 
                            + temp_string[operations[-1] + 1:] 
                            + ")")
                i += 1 # added ")"

        else: # else

            # add s to temp_string
            temp_string += s

            # operation append conditions
            condition = (
                            s == '+'\
                            or s == '-'\
                            or s == '*'\
                            or s == '/'\
                            or s == '%'\
                            or s == '^'\
                        )

            # when s is "(" then append the index to the parantheses list.
            if s == "(": 
                parantheses.append(index)

            # when s is ")" and next element is not "!" then remove it from the list.
            elif s == ")": 
                try: 
                    if string[index - i + 1] != "!":
                        parantheses.pop()
                except:
                    parantheses.pop()

            # when s is not a diggit or a special character.
            elif condition:
                operations.append(index)
        

    # the end of iteration.
    ###########################################################################################

    # necessary replacements.
    temp_string = (
                    temp_string
                    .replace("!", "factorial(", -1)
                    .replace("^", "**", -1)
                    .replace("sqrt", "root", -1)
                  )

    # returning converted string.
    return temp_string



def evaluate(string):

    # make the expression evaluation-friendly.
    string = to_expr(string)

    # trying to evaluate the expression.

    try:
        return (Decimal(round(eval(string), 6)), string)
    except NameError as e:
        return (None, "Invalid Function")
    except ZeroDivisionError:
        return (None, "Division by zero is not allowed.")
    except:
        return (None, "Invalid Syntax")