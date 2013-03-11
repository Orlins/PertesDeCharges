#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import math

material_list=(("Acier",0),("PVC",1),("Cuivre",2), ("Multicouche",3), ("PE-X", 4), ("PEHD PN12,5",5), ("PEHD PN16",6))

pipe_size = {0:(
                (8, 9.5), (12, 13.2), (15, 16.7), (20, 22.3), (25, 27.9), (32, 36.6),(40, 42.4), (50, 48.3), (65, 70.3), (80, 82.5), (100, 107.1), (125, 131.7), (150, 159.3), (200, 207.3), (250, 260.4), (300, 309.7), (350, 339.6), (400, 388.8), (900, 900)
                ),
            1:(
                (16, 12.4), (20, 15.4), (25, 19.4), (32, 27.2), (40, 34), (50, 42.6), (63, 53.6), (75, 64), (90, 76.8), (110, 93.8), (125, 113), (140, 127.8),
                (160, 147.6), (200, 184.6),(300,300),(400,400),(500,500),(600,600)
                ),
            2:(
                (6, 4), (8, 6), (10, 8), (12, 10), (14, 12), (15, 13), (16, 14), (18, 16), (20, 18), (22, 20), (28, 26), (32, 30), (35, 33), (40, 38), (42, 40), (52, 50),(54, 52), (63, 59.8)
                ),
            3:(
                (14,10), (16,12), (18,14), (20,15), (25,20), (32,26), (40,32), (50,41), (63,51),  (75,60), (90,73),  (110,90)
                ),
            4:(
                (12,8.9), (16,13), (20,16.2), (25,20.4), (32,26.2), (40,32.6), (50,40.8), (63,51.4)
                ),
            5:(
                (32,26),(40,32.6),(50,40.8),(63,51.4),(75,61.4),(90,76.6),(110,93.8),(125,106.6),(160,136.4)
                ),
            6:(
                (90,73.6),(110,90),(125,102.2),(140,114.6),(160,130.8),(180,147.2),(200,163.6),(225,184),(250,204.6)
                )
            }

roughness_list = {0:0.2, 1:0.03, 2:0.05, 3:0.03, 4:0.03, 5:0.02, 6:0.02}

def get_water_data_at(temp=20):
        water_data = [
            [0, 999.8, 0.00179],
            [10, 999.7, 0.00131],
            [20, 998.2, 0.001],
            [30, 995.7, 0.0008],
            [40, 992.2, 0.00065],
            [50, 988, 0.00055],
            [60, 983.2, 0.00047],
            [70, 977.8, 0.00040],
            [80, 971.8, 0.00036],
            [90, 965.3, 0.00031],
            [100, 958.4, 0.00028]
            ]
        print("temperature {0}".format(temp))
        if (temp < 0 or temp > 100):
            pass
            #raise TypeError, 'get_water_data_at() requires a parameter between 0 and 100'
        previous_data = [0, 999.8, 0.00179]
        data_output = [0, 0, 0]
        for data in water_data:
            temperature, massvol, visco = data
            if (temp == data[0]):
                return data
            if (temp > previous_data[0] and temp < data[0]):
                data_output[0] = temp
                ratio = (temp - previous_data[0]) / (data[0] - previous_data[0])
                data_output[1] = ratio * (data[1] - previous_data[1]) + previous_data[1]
                data_output[2] = ratio * (data[2] - previous_data[2]) + previous_data[2]
                return data_output
            previous_data = data
        #raise TypeError, 'Could not calculate acceptable value'

def get_next_diameter(size, material):
    avail_diameter = pipe_size[material]
    for diameter in avail_diameter:
        #print ("testing condition %f>%f" %(diameter[0],size))
        if diameter[0] >= size:
            return diameter
    return 0

def calc_reynolds(speed, diameter, temp=20):
    water_data = get_water_data_at(temp)
    specific_weight = water_data[1]
    dyn_viscosity = water_data[2]
    #print ("[calc_reynolds] speed %f" %speed)
    #print ("[calc_reynolds] specific weight %f" %specific_weight)
    #print ("[calc_reynolds] dynamic viscosity %f" %dyn_viscosity)
    #print ("[calc_reynolds] diameter %f" %diameter)
    reynolds = speed * diameter * specific_weight / (1000 * dyn_viscosity)
    #print ("[calc_reynolds] reynolds %f" %reynolds)
    return reynolds

def calc_speed(flowrate, diameter):
    if diameter != 0:
        diameter = diameter + 0.0 #this is to turn diameter into floating point number (because integer/1000 returns 0)
        speed = 4 * flowrate / (3600 * (diameter / 1000) ** 2 * 3.14)
        #print ("speed %f" %speed)
        return speed
    else: return 0

def calc_darcy(flowrate, diameter, material=0, temp=10):
    #diameter must be a real geometric inside diameter
    #flowrate is m3/h, diameter is mm
    #material is :
    #0 - steel
    #1 - PVC
    #2 - copper
    #3- cast iron
    #4- concrete
    roughness = roughness_list[material]
    speed = calc_speed(flowrate, diameter)
    #print ("[calc_darcy] speed %f" %speed)
    reynolds = calc_reynolds(speed, diameter, temp)
    water_data = get_water_data_at(temp)
    specific_weight = water_data[1]
    #print ("[calc_darcy] reynolds %f" %reynolds)
    if reynolds < 2000:
        if reynolds != 0:
            lambda_factor = 64 / reynolds
        else: lambda_factor = 0
    elif (reynolds <= 2000 and reynolds < 40000):
        lambda_factor = 0.316 / reynolds ** 0.25
    else:
        lambda_factor = 0.790 * math.sqrt(roughness / diameter)
        #print ("[calc_darcy] roughness %f" %roughness)
        #print ("[calc_darcy] diameter %f" %diameter)
        #print ("[calc_darcy] lambda %f" %lambda_factor)
    if diameter != 0:
        j = (lambda_factor * speed ** 2) / (9.81 * 2 * diameter / 1000)
    else: j = 0
    #print "c'est là"
    return j * 1000

def search_headloss_darcy(flowrate, diameter, material=0, temp=20):
    #this function provide the same capability as calc_darcy,
    # but the diameter parameter is a nominal diameter
    #Use the fact that the real diameter is always larger than nominal
    #FIXME the assertion above is false i.e. PVC
    diameter_result = get_next_diameter(diameter, material)
    if diameter_result:
        nominal_diameter = diameter_result[0]
        real_diameter = diameter_result[1]
        headloss = calc_darcy(flowrate, real_diameter, material, temp)
        return (headloss, nominal_diameter, real_diameter)
    else: return 0


def calc_hazenwilliams(flowrate, diameter, material):
    #flowrate is m3/h, diameter is mm
    #material is :
    #0 - steel
    #1 - PVC
    #2 - copper
    #3- cast iron
    #4- concrete
    hw_factor_list = {0:120, 1:150, 2:150, 3:140, 4:130}
    hw_factor = hw_factor_list[material]
    speed = calc_speed(flowrate, diameter)
    diameter = diameter + 0.0
    j = 6.819 * (speed / hw_factor) ** 1.852 * (diameter / 1000) ** -1.167
    return j * 1000

def search_diam_hw(flowrate, headloss=20, material=0):
    diameter = 0
    calc_headloss = 1000
    while calc_headloss > headloss:
        #print ("diameter before is %f" %diameter)
        result = get_next_diameter(diameter, material)
        if result:
            nominal_diam = result[0]
            diameter = result[1]
            #print ("diameter after is %f" %diameter)
            #print ("calculating for %f(m3/h) - %f(mm) - %i(material)" %(flowrate, diameter, material))
            calc_headloss = calc_hazenwilliams(flowrate, diameter, material)
            result = [diameter, nominal_diam, calc_headloss]
        else:
            return 0
    return result

def search_diam_darcy(flowrate, headloss=20, material=0, temp=20):
    #TODO il y a un pb dans cette fonction avec get_net_diametre qui reste bloqué à 50 (48,3
    diameter = 0
    calc_headloss = 1000
    while calc_headloss > headloss:
        #print ("diameter before is %f" %diameter)
        result = get_next_diameter(diameter, material)
        if result:
            nominal_diam = result[0]
            diameter = result[1]
            #print ("diameter after is %f" %diameter)
            #print ("calculating for %f(m3/h) - %f(mm) - %i(material)" %(flowrate, diameter, material))
            calc_headloss = calc_darcy(flowrate, diameter, material, temp)
            result = [diameter, nominal_diam, calc_headloss]
            #print ("diamètre : %f - Perte de charge %f") % (diameter,calc_headloss)
        else:
            return 0
    return result


if (__name__ == "__main__"):
    search_result = search_headloss_darcy(112, 150, 0)
    #print ("Perte de charge 112m3/h DN150 : %f (DN=%i)" % (search_result[0], search_result[1]))
    #erreur print ("Recherche diametre débit 112m3/h pcd max 35mm/m : %i (pdc=%f)" % (search_diam_darcy(112, 35, 0)[1], search_diam_darcy(112, 35, 0)[2]))
    search_result = search_headloss_darcy(2, 40, 0)
    #print ("Perte de charge 2m3/h DN40 : %f (DN=%i)" % (search_result[0], search_result[1]))
    #print ("Recherche diametre débit 25m3/h pcd max 15mm/m : DN %i (pdc=%f)" % (search_diam_darcy(2, 15, 0)[1], search_diam_darcy(2, 15, 0)[2]))



