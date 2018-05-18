#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import calcoohija
import csv

with open(sys.argv[1], newline="") as csvfile:
    operaciones = csv.reader(csvfile)
    for operacion in operaciones:
        operador = operacion[0]
        result = int(operacion[1])
        Not_Allowed = False
        try:
            for number in operacion[2:]:
                operando = int(number)
                cuenta = calcoohija.CalculadoraHija(result, operando)
                if operador == 'suma':
                    result = cuenta.plus()
                elif operador == 'resta':
                    result = cuenta.sub()
                elif operador == 'multiplica':
                    result = cuenta.mult()
                elif operador == 'divide':
                    result = cuenta.div()
                else:
                    Not_Allowed = True
            if not Not_Allowed:
                print(result)
            else:
                print(operador + ' is not allowed')
        except ValueError:
            print('Not an integer number')
