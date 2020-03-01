from kivy_garden.graph import SmoothLinePlot


class CalcHandler:
    # contains all basic operators that can be performed
    operator_dict = {'+': lambda calc: str(float(calc[0]) + float(calc[2])),
                     '-': lambda calc: str(float(calc[0]) - float(calc[2])),
                     '*': lambda calc: str(float(calc[0]) * float(calc[2])),
                     '/': lambda calc: str(float(calc[0]) / float(calc[2])),
                     '^': lambda calc: str(float(calc[0]) ** float(calc[2]))}

    def __init__(self, main_window):
        self.calculations = main_window.ids.calc_input.text[4:]
        # self.add_brackets()  # adds proper brackets to self.calculations
        self.main_graph = main_window.ids.main_graph
        self.accuracy = 1

    # return ready to be displayed plot
    def get_plot(self):
        plot = SmoothLinePlot(color=[1, 0, 0, 1])
        plot.points = [(x / self.accuracy, self.get_result(
            x / self.accuracy)) for x in range(
                self.main_graph.xmin * self.accuracy,
                self.main_graph.xmax * self.accuracy + 1)]
        return plot

    # returns result of given calculations with given x
    def get_result(self, x):
        working_calc = self.change_x_for_values(x)
        # self.calculate_special_operators(current_calc)

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

    # returns result(string) of given calculations
    def calculate(self, calc, starting_pos=0):
        subcalculation = ['', '', ''] # [first number, operator, second number]
        char_pos = starting_pos  # contains index of current character
        while char_pos < len(calc):
            if isfloat(calc):
                return calc
            # calls self to calculate contains of brackets and them
            # replaces them with a result
            if calc[char_pos] == '(':
                calc = self.calculate(calc, (starting_pos + char_pos + 1))

            # if calc[char_pos] is part of number then adds it to
            # subcalculation
            if calc[char_pos] in '0123456789-.' and not (
                calc[char_pos] == '-' and calc[char_pos-1].isdigit() and not
                    char_pos == 0):
                if subcalculation[1] == '':
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
                                                   starting_pos, char_pos)
                    subcalculation = ['', '', '']
                    char_pos = starting_pos - 1

            elif calc[char_pos] == ')':
                if not subcalculation[1] == '':
                    calc = self.insert_calculation(calc, subcalculation,
                                                   starting_pos, char_pos + 1)
                return calc
            else:
                raise ValueError('Unknown character: ', calc[char_pos])
            char_pos += 1

        if not subcalculation[0] == '':
            calc = self.insert_calculation(calc, subcalculation,
                                           starting_pos, char_pos)
        return calc

    # returns inserted result of subcalculation
    def insert_calculation(self, calc, subcalc, starting_pos, end_pos):
        if starting_pos > 0:
            starting_pos -= 1

        return (calc[:starting_pos] + self.operator_dict[subcalc[1]](subcalc) +
                calc[end_pos:])


def isfloat(str):
    try:
        float(str)
        return True
    except ValueError:
        return False