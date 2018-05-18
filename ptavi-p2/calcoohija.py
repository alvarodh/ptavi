#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import calcoo


class CalculadoraHija(calcoo.Calculadora):

    def mult(self):
        return self.number1 * self.number2

    def div(self):
        try:
            return self.number1 / self.number2
        except ZeroDivisionError:
            print('Division by zero is not allowed')

if __name__ == '__main__':
    try:
        correct_usage = ('operand1 <suma|resta|multiplica|divide> operand2')
        number1 = int(sys.argv[1])
        operation = sys.argv[2]
        number2 = int(sys.argv[3])
        cuenta = CalculadoraHija(number1, number2)
        if operation == 'suma':
            print(cuenta.plus())
        elif operation == 'resta':
            print(cuenta.sub())
        elif operation == 'multiplica':
            print(cuenta.mult())
        elif operation == 'divide':
            print(cuenta.div())
        else:
            sys.exit(operation + ' is not allowed')

    except ValueError:
        sys.exit('Not an integer number')
    except IndexError:
        sys.exit('Usage error: python3 calcoohija.py ' + correct_usage)
