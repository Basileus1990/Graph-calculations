# Checks correctness of given calculations. If they are wrong raises WrongInput
# doesn't return anything, just raises errors if needed


class Correctness:
    def __init__(self, main_graph, calc_handler, calc):
        self.main_graph = main_graph
        self.calc_handler = calc_handler

        self.check_correctness(calc)

    def check_correctness(self, calc):
        if calc == '':
            raise self.main_graph.WrongInput('Your calculations can\'t be empty')
        # checks if there are any gaps in calc, if so raises WrongInput
        if calc.find(' ') >= 0 or calc.find('\n') >= 0 or calc.find('\t') >= 0:
            raise self.main_graph.WrongInput('There can\'t be any gaps between')

        self.check_dots(calc)
        self.check_operators_correctness(calc)
        self.check_brackets(calc)

    # checks if operators ale placed properly
    def check_operators_correctness(self, calc):
        for operator in self.calc_handler.operator_dict.keys():
            buffer_pos = 0
            current_pos = 0
            while(True):
                buffer_pos = calc[current_pos:].find(operator)
                if buffer_pos == -1:
                    break
                current_pos += buffer_pos
                if (current_pos == 0 and not calc[current_pos] == '-' or
                        current_pos == len(calc) - 1):
                    raise self.main_graph.WrongInput('Operator can\'t be at' +
                                                     ' the begining or the end: ' + calc[current_pos])

                elif calc[current_pos] == '-':
                    if not calc[current_pos+1] in '0123456789(-lscrx':
                        raise self.main_graph.WrongInput('Operators can\'t be next to eachother: ' +
                                                         calc[current_pos-1:current_pos+2])

                elif not (calc[current_pos-1] in '0123456789)lscrx' and
                          calc[current_pos+1] in '0123456789(-lscrx'):
                    raise self.main_graph.WrongInput('Operators can\'t be next to eachother: ' +
                                                     calc[current_pos-1:current_pos+2])
                current_pos += 1

    # checks if brackets have a corresponding one and checks if operators
    # brackets are placed properly
    def check_brackets(self, calc):
        bracket_pos = 0
        bracket_buffer = 0
        bracket_count = [0, 0]  # (, )
        while(True):
            bracket_buffer = calc[bracket_pos:].find('(')
            if bracket_buffer == -1:
                break
            bracket_pos += bracket_buffer
            self.calc_handler.find_end_bracked_pos(bracket_pos, calc)

            if (not bracket_pos == 0 and not calc[bracket_pos-1] in '*/-+^ns(' and
               self.check_if_log_or_root(calc, bracket_pos) is False):
                raise self.main_graph.WrongInput('Before \"(\" has to be an operator')

            bracket_count[0] += 1
            bracket_pos += 1

        bracket_pos = 0
        while(True):
            bracket_buffer = calc[bracket_pos:].find(')')
            if bracket_buffer == -1:
                break
            bracket_pos += bracket_buffer

            if not bracket_pos == len(calc)-1 and not calc[bracket_pos+1] in '*/-+^lrsc)':
                raise self.main_graph.WrongInput('After \")\" has to be an operator')

            bracket_pos += 1
            bracket_count[1] += 1

        if not bracket_count[0] == bracket_count[1]:
            raise self.main_graph.WrongInput('Missing brackets')

    # chceck if is bracket of root or Logarithm
    def check_if_log_or_root(self, calc, bracket_pos):
        if bracket_pos < 3:
            return False
        current_pos = bracket_pos - 1
        while(not calc[current_pos] in 'tg'):
            if current_pos == 0:
                return False
            current_pos -= 1
        return True

    # checks if dots are surrounded by numbers, if not raises WrongInput error
    def check_dots(self, calc):
        dot_pos = 0
        dot_pos_buffer = 0
        while(True):
            dot_pos_buffer = calc[dot_pos:].find('.')
            if dot_pos_buffer == -1:
                break

            dot_pos += dot_pos_buffer

            if dot_pos in (0, len(calc) - 1):
                raise self.main_graph.WrongInput('Dot can\'t be at the begining' +
                                                 'or at the end')
            elif not calc[dot_pos - 1].isnumeric() or not calc[dot_pos + 1].isnumeric():
                raise self.main_graph.WrongInput('Dots must be surrounded by numbers: ' +
                                                 calc[dot_pos-1:dot_pos+2])
            dot_pos += 1
