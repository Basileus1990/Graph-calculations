from kivy_garden.graph import SmoothLinePlot
from .Correctness import Correctness
from . import main_graph
from math import sin, cos, log


class CalcHandler:
    def __init__(self, main_window):
        # contains all basic operators that can be performed
        self.operator_dict = {'+': lambda calc: str(float(calc[0]) + float(calc[2])),
                              '-': lambda calc: str(float(calc[0]) - float(calc[2])),
                              '*': lambda calc: str(float(calc[0]) * float(calc[2])),
                              '/': self.divide,
                              '^': self.power}
        # contains all special operators that can be performed
        self.special_operators_dict = {'sin': self.calc_sin_cos,
                                       'cos': self.calc_sin_cos,
                                       'log': self.calc_log,
                                       'root': self.calc_root}

        self.calculations = main_window.ids.calc_input.text[4:]
        # self.add_brackets()  # adds proper brackets to self.calculations
        self.main_graph_object = main_window.ids.main_graph
        Correctness(main_graph, self, self.calculations)

        self.accuracy = 10  # accuracy > 0

    # return ready to be displayed plot
    def get_plot(self):
        plot = SmoothLinePlot(color=[1, 0, 0, 1])
        plot.points = []
        for x in range(self.main_graph_object.xmin * self.accuracy,
                       self.main_graph_object.xmax * self.accuracy + 1):
            try:
                result = self.get_result(x / self.accuracy)
                plot.points.append((x / self.accuracy, result))
            except ImpossibleToCalculateError as e:
                if not str(e) == '':
                    print(e)
                continue
        return plot

    # returns result of given calculations with given x
    def get_result(self, x):
        working_calc = self.change_x_for_values(x)
        working_calc = self.calculate_special_operators(working_calc)
        # working_calc = self.add_additional_brackets(working_calc)

        return float(self.calculate(working_calc, 0))

    # returns self.calculations but with replaced x for given number
    def change_x_for_values(self, x):
        working_calc = self.calculations
        x_pos = working_calc.find('x')
        while(not x_pos == -1):
            working_calc = (working_calc[:x_pos] + str(x)
                            + working_calc[(x_pos + 1):])
            x_pos = working_calc.find('x')
        return working_calc

    # calculates special operators like: cos, sin, root, log
    def calculate_special_operators(self, calc):
        calc = self.calc_sin_cos(calc)
        calc = self.calc_log(calc)
        calc = self.calc_root(calc)
        return calc

    # returns result(string) of given calculations
    def calculate(self, calc, starting_pos=0):
        subcalculation = ['', '', '']  # [first number, operator, second number]
        char_pos = starting_pos  # contains index of current character
        while(char_pos < len(calc)):
            if isfloat(calc):
                return calc

            # calls self to calculate contains of brackets and them
            # replaces them with a result
            if calc[char_pos] == '(':
                calc = self.calculate(calc, (char_pos + 1))
                if isfloat(calc):
                    return calc

            # if calc[char_pos] is part of number then adds it to
            # subcalculation
            if calc[char_pos] in '0123456789-.' and not (
                calc[char_pos] == '-' and calc[char_pos-1].isdigit() and not
                    char_pos == 0):

                # check if they arent't two minuses, if so they nullyfy eachotcher
                if calc[char_pos] == '-' and calc[char_pos + 1] == '-':
                    calc = calc[:char_pos] + calc[char_pos+2:]
                    continue

                elif subcalculation[1] == '':
                    subcalculation[0] += calc[char_pos]
                else:
                    subcalculation[2] += calc[char_pos]

            # adds operator to current_calc and if it is already set, it starts
            # the subcalculation
            elif calc[char_pos] in self.operator_dict.keys():
                if subcalculation[1] == '':
                    subcalculation[1] = calc[char_pos]
                else:
                    calc = self.insert_calculation(calc, subcalculation,
                                                   starting_pos+1, char_pos)
                    subcalculation = ['', '', '']
                    char_pos = starting_pos - 1

            elif calc[char_pos] == ')':
                if not subcalculation[1] == '':
                    calc = self.insert_calculation(calc, subcalculation,
                                                   starting_pos, char_pos + 1)
                else:
                    calc = (calc[:starting_pos-1] +
                            calc[starting_pos:char_pos] + calc[char_pos+1:])
                return calc

            else:
                raise main_graph.WrongInput('Unknown character: ' + calc[char_pos])
            char_pos += 1

        if not subcalculation[0] == '':
            calc = self.insert_calculation(calc, subcalculation,
                                           starting_pos, char_pos)
        return calc

    # returns inserted result of subcalculation
    def insert_calculation(self, calc, subcalc, starting_pos, end_pos):
        if starting_pos > 0:
            starting_pos -= 1

        if subcalc[2] == '':
            raise main_graph.WrongInput('Wrong input: ' + subcalc[0] + subcalc[1])
        else:
            try:
                return (calc[:starting_pos] + self.operator_dict[subcalc[1]](subcalc) +
                        calc[end_pos:])
            except KeyError as e:
                print(calc)
                raise e

    # calculates all sin(x) and cos(x) and returns calc with inserted results
    def calc_sin_cos(self, calc):
        for operator in ('sin', 'cos'):
            pos = calc.find(operator)
            end_pos = 0

            while(not pos == -1):
                # sets end_sin_pos
                calc, end_pos = self.find_internal_special_operators(calc, pos + 3)

                if calc[(pos+4):(end_pos)] == '':
                    raise main_graph.WrongInput('Interior of bracket in special' +
                                                ' operator can\'t be empty')
                # calculates and inserts relults to calc
                if operator == 'sin':
                    calc = (calc[:pos] + str(sin(float(self.calculate(
                           calc[(pos+4):(end_pos)])))) + calc[end_pos+1:])
                else:
                    calc = (calc[:pos] + str(cos(float(self.calculate(
                           calc[(pos+4):(end_pos)])))) + calc[end_pos+1:])

                pos = calc.find(operator)
                end_pos = 0
        return calc

    # calculates loga(b) => Logarithm of a given number 'b' with a base 'a'
    def calc_log(self, calc):
        pos = calc.find('log')
        end_pos = 0

        while(not pos == -1):
            # checks if base calculation doesn't have errors
            self.check_operators_correctness(calc[pos + 3:calc.find('(', pos + 3)])
            base = self.calculate(calc[pos + 3:calc.find('(', pos + 3)])
            if base == '':
                base = '10'
            elif float(base) <= 0:
                raise ImpossibleToCalculateError()
            # sets end_pos
            begining_pos = calc.find('(', pos + 3)  # pos of '('

            calc, end_pos = self.find_internal_special_operators(calc, begining_pos)

            if calc[begining_pos + 1:end_pos] == '':
                raise main_graph.WrongInput('Interior of bracket in special' +
                                            ' operator can\'t be empty')
            number = self.calculate(calc[begining_pos + 1:end_pos])
            if float(number) <= 0:
                raise ImpossibleToCalculateError()
            # calculates and inserts relults to calc
            try:
                calc = (calc[:pos] + str(log(float(number), float(base)))
                        + calc[end_pos+1:])
            except ZeroDivisionError:
                raise ImpossibleToCalculateError()

            pos = calc.find('log')
            end_pos = 0
        return calc

    # calculates roota(b) => root of a given number 'b' with a base 'a'
    def calc_root(self, calc):
        pos = calc.find('root')
        end_pos = 0

        while(not pos == -1):
            # checks if base calculation doesn't have errors
            self.check_operators_correctness(calc[pos + 4:calc.find('(', pos + 4)])
            base = self.calculate(calc[pos + 4:calc.find('(', pos + 4)])
            if base == '':
                base = '2'
            elif float(base) <= 0:
                raise ImpossibleToCalculateError()

            begining_pos = calc.find('(', pos + 4)  # pos of '('

            calc, end_pos = self.find_internal_special_operators(calc, begining_pos)

            if calc[begining_pos + 1:end_pos] == '':
                raise main_graph.WrongInput('Interior of bracket in special' +
                                            ' operator can\'t be empty')
            number = self.calculate(calc[begining_pos + 1:end_pos])
            if float(number) <= 0:
                raise ImpossibleToCalculateError()
            # calculates and inserts relults to calc
            calc = (calc[:pos] + str(float(number) ** (1/float(base)))
                    + calc[end_pos+1:])

            pos = calc.find('root')
            end_pos = 0
        return calc

    # finds and returns positon of coresponding bracket
    def find_end_bracked_pos(self, begining_pos, calc):
        end_pos = begining_pos
        while(True):
            bracket_pos = calc[end_pos:].find(')')
            # raises error when bracket does't have a corresponding bracket
            if bracket_pos == -1:
                raise main_graph.WrongInput('\')\' not found')

            elif end_pos == begining_pos:
                end_pos += bracket_pos
            else:
                end_pos += bracket_pos + 1

            # checks if between bracket there are not other '('
            is_end_pos = calc[begining_pos+1:end_pos].find('(')
            if not is_end_pos == -1:
                begining_pos += is_end_pos+1
            else:
                break
        return end_pos

    # finds and calculates special operators inside of another special
    # operators if there are any
    # retruns changed calc and end_pos
    def find_internal_special_operators(self, calc, begining_pos):
        end_pos = self.find_end_bracked_pos(begining_pos, calc)
        for operator in self.special_operators_dict:
            if calc[begining_pos + 1:end_pos].find(operator) > 0:
                calc = (calc[:begining_pos+1] +
                        self.special_operators_dict[operator](
                        calc[begining_pos + 1:end_pos]) +
                        calc[end_pos:])
                end_pos = self.find_end_bracked_pos(begining_pos, calc)
        return calc, end_pos

    # retruns power of given numbers in calc, takes care of impossible roots
    def power(self, calc):
        if float(calc[0]) < 0 and isfloat(calc[2]):
            raise ImpossibleToCalculateError()
        return str(float(calc[0])**float(calc[2]))

    # retunrs division of given numbers in calc, takes care of dividing by 0
    def divide(self, calc):
        if float(calc[2]) == 0:
            raise ImpossibleToCalculateError()
        return str(float(calc[0])/float(calc[2]))


# when raised the calculation is omitted and goes to the next one
class ImpossibleToCalculateError(ValueError):
    pass


def isfloat(str):
    try:
        float(str)
        return True
    except ValueError:
        return False
