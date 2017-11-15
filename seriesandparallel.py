#!/usr/bin/python

# Cole Deaton

# s&pcomplexmath

import math

import Adafruit_CharLCD as LCD

lcd = LCD.Adafruit_CharLCDPlate()



pi = 3.141592653589793238462643



def complex_add(complex_a,complex_b):



    x1 = float(complex_a[0]) * math.cos(pi/180 * complex_a[1])

    x2 = float(complex_b[0]) * math.cos(pi/180 * complex_b[1])

    y1 = float(complex_a[0]) * math.sin(pi/180 * complex_a[1])

    y2 = float(complex_b[0]) * math.sin(pi/180 * complex_b[1])

    x_total = x1 + x2

    y_total = y1 + y2

    answer = rect_to_polar(x_total, y_total)

    return answer[0], answer[1]





def complex_division(complex_a, complex_b):

    real_answer = complex_a[0] / complex_b[0]

    imag_answer = complex_a[1] - complex_b[1]

    return real_answer, imag_answer





def complex_multiplication(complex_a, complex_b):

    real_answer = complex_a[0] * complex_b[0]

    imag_answer = complex_a[1] + complex_b[1]

    return real_answer, imag_answer





def rect_to_polar(x, y):

    angle = math.atan((y/x))

    angle = angle * (180/pi)

    magnitude = (math.sqrt((x*x)+(y*y)))

    answer = magnitude, angle

    return answer





def polar_to_rect(polar_num):

    y = polar_num[0] * (math.sin(polar_num[1] * pi/180))

    x = polar_num[0] * (math.cos(polar_num[1] * pi/180))

    rect = x, y

    return rect





def magnitude(number):

    absolute = math.sqrt((number[0] * number[0]) + (number[1] * number[1]))

    return absolute





# Mode select

mode_select = raw_input('Series or parallel circuit?:')



# Series calculations

if (mode_select == 'Series') or (mode_select == 'series'):

    print('I will only be capable of series AC calculations with one R, L & C.\n')

    print('If a value is not present, enter a 0')

    frequency = input('\nWhat is the frequency? (in Hz): ')

    voltage = input('\nWhat is the source voltage? (in RMS): ')

    resistor_value = input('\nWhat is your resistor? (in Ohms): ')

    inductor_value = input('\nWhat is your inductor? (in Henrys): ')

    inductor_resistance = input('\nWhat is the resistance of the winding of the inductor? (in Ohms): ')

    capacitor_value = input('\nWhat is your capacitor? (in Farads): ')



# Basic math



    total_resistance = inductor_resistance + resistor_value

    inductance =2 * pi * frequency * inductor_value

    mag_inductance = (inductor_resistance, inductance)

    mag_inductance = magnitude(mag_inductance)

    capacitance = (1/(2 * pi * frequency * capacitor_value))

    impedance = total_resistance, (inductance + -capacitance)

    mag_impedance = magnitude(impedance)

    current = float(voltage) / float(mag_impedance)

    v_r = current * resistor_value

    v_l = current * inductance

    v_c = current * capacitance



# Phase angle 

    if inductance > capacitance:

        argument_send = impedance[1] / impedance[0]

    else:

        if capacitance > inductance:

            argument_send = impedance[0] / impedance[1]

        else:

            argument_send = 0

    phase_radians = math.atan(argument_send)

    phase_angle = phase_radians * 180/pi



# Results

    if capacitance > inductance:

        print('Your current leads your voltage by %f degrees ' % phase_angle)

    if inductance > capacitance:

        print('Your current lags your voltage by %f degrees' % phase_angle)

    print('\nThe total impedance is: %.2f + %.2fj' % (impedance[0], impedance[1]))

    print('That means the magnitude of your impedance is: %.2f' % mag_impedance)

    print('Your current is: %f A' % current)

    print('V(R) = %.2f, V(L) = %.2f, V(C) = %.2f' % (v_r, v_l, v_c))



# Parallel

if (mode_select == 'Parallel') or (mode_select == 'parallel'):

    print('I will be doing parallel calculations. One R,L, and C is expected')

    print('If a value is not present, enter a 0')

    frequency = input('\nWhat is the frequency? (Hz): ')

    voltage = input('\nWhat is the source voltage? (RMS): ')

    resistor_value = input('\nWhat is your resistor? (Ohms): ')

    inductor_value = input('\nWhat is your inductor? (Henrys): ')

    inductor_resistance = input('\nWhat is the resistance of the winding of the inductor? (Ohms): ')

    capacitor_value = input('\nWhat is your capacitor? (Farads): ')



# Basic calculations

    polar_voltage = voltage, 0

    resistor_value = float(resistor_value)

    resistance = float(resistor_value), 0

    inductor_resistance = inductor_resistance, 0

    inductance = (2 * pi * frequency * inductor_value), 90

    capacitance = 1/(2 * pi * frequency*capacitor_value), -90

    inductor_branch = complex_add(inductor_resistance, inductance)

    one = 1, 0



# Inverse of the impedances for adding together

    inverse_resistance = complex_division(one, resistance)

    inverse_p_capacitance = complex_division(one, capacitance)

    inverse_p_inductance = complex_division(one, inductor_branch)



# Sum of the denominator in to variables for total impedance

# Uses the formula 1 / ((1/Xl) + (1/R) + (1/Xc))

    denominator = complex_add(inverse_p_capacitance, inverse_p_inductance)

    denominator_f = complex_add(denominator, inverse_resistance)

    total_impedance = complex_division(one, denominator_f)



# Current calculations

    total_current = voltage / total_impedance[0]

    inductor_branch_current = total_current * (total_impedance[0] / inductor_branch[0])

    cap_branch_current = total_current * (total_impedance[0] / capacitance[0])

    resistor_branch_current = total_current * (total_impedance[0] / resistance[0])



# Final results for the user



    print('The magnitude of your impedance is %f with a phase of %f degrees' % (total_impedance[0], total_impedance[1]))

    if total_impedance[1] > 0:

        print('Your current lags your voltage by %f degrees' % total_impedance[1])

    if total_impedance[1] < 0:

        print('Your current leads your voltage by %f degrees' % total_impedance[1])

    if total_impedance[1] == 0:

        print('Your voltage and current will be in phase')

    print('Your total current will be %f A' % total_current)
