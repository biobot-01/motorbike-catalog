#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Manufacturer, Motorbike

# Connect to database
engine = create_engine('sqlite:///motorbike_catalog.db')
# Bind engine to metadata of Base class to access through DBSession
Base.metadata.bind = engine
# Create a DBSession instance
DBSession = sessionmaker(bind=engine)
# Create a session for the database
session = DBSession()

manufacturers = [
    'Aprilia',
    'BMW',
    'Ducati',
    'Harley-Davidson',
    'Honda',
    'Kawasaki',
    'KTM',
    'MV Agusta',
    'Royal Enfield',
    'Suzuki',
    'Triumph',
    'Yamaha'
]

bikes = [
    {
        'model': 'Tuono V4 1100 Factory',
        'year': '2019',
        'engine': ('Longitudinal 65° V-4 cylinder, 4-stroke, '
                   'liquid cooled, DOHC, 4 valves per cylinder'),
        'displacement': '1077 cc',
        'curb_mass': '209 kg',
        'fuel_capacity': '18.5 l',
        'max_power': '175 hp (129 kW) at 11,000 rpm',
        'max_torque': '121 Nm at 9,000 rpm',
        'image': ('https://motorcyclespecs.co.za/Gallery_A-L_16/'
                  'Aprilia-Tuono-V4-Fac-19-04.jpg'),
        'manufacturer_id': 1,
    },
    {
        'model': 'Shiver 900',
        'year': '2019',
        'engine': ('Longitudinal 90° V-twin engine, 4-stroke, '
                   'liquid cooled, DOHC with mixed gear/chain '
                   'timing system, 4 valves per cylinder'),
        'displacement': '896.1 cc',
        'curb_mass': '218 kg',
        'fuel_capacity': '15 l',
        'max_power': '70 kW (95.2 hp) at 8,750 rpm ',
        'max_torque': '90 Nm (9.17 kgm) at 6,500 rpm',
        'image': ('https://motorcyclespecs.co.za/Gallery_A-L_16/'
                  'Aprilia-Shiver-900-19-02.jpg'),
        'manufacturer_id': 1,
    },
    {
        'model': 'S1000R',
        'year': '2018',
        'engine': ('Liquid-cooled, 4-stroke, inline 4-cylinder, '
                   '4 valves per cylinder, DOHC, wet sump lubrication'),
        'displacement': '999 cc',
        'curb_mass': '205 kg',
        'fuel_capacity': '17.5 l',
        'max_power': '165 hp (121 kW) at 11,000 rpm',
        'max_torque': '84 lb-ft (114 Nm) at 9,250 rpm',
        'image': ('https://motorcyclespecs.co.za/Gallery_A-L_16/'
                  'bmw_s1000_r_rr_xr_17_03.jpg'),
        'manufacturer_id': 2,
    },
    {
        'model': 'R nineT Pure',
        'year': '2019',
        'engine': ('Air/oil-cooled, 4-stroke, flat twin-cylinder with '
                   'balance shaft, 4 valves per cylinder, DOHC, '
                   'wet sump lubrication'),
        'displacement': '1,170 cc',
        'curb_mass': '219 kg',
        'fuel_capacity': '17 l',
        'max_power': '110 hp (81 kW) at 7,750 rpm',
        'max_torque': '86 lb-ft (116 Nm) at 6,000 rpm',
        'image': ('https://motorcyclespecs.co.za/Gallery_A-L_16/'
                  'BMW_RnineT_pure_1-19.jpg'),
        'manufacturer_id': 2,
    },
    {
        'model': 'Hypermotard 950 SP',
        'year': '2019',
        'engine': ('Testastretta 11°, L-Twin cylinder, 4 valves '
                   'per cylinder, Desmodromic, liquid cooled, '
                   'magnesium head covers'),
        'displacement': '937 cc',
        'curb_mass': '198 kg',
        'fuel_capacity': '14.5 l',
        'max_power': '114 hp (84 kW) @ 9,000 rpm',
        'max_torque': '71 lb-ft (96 Nm) @ 7,250 rpm',
        'image': ('https://motorcyclespecs.co.za/Gallery_A-L_16/'
                  'Ducati-Hypermotard-950-SP-01.jpg'),
        'manufacturer_id': 3,
    },
    {
        'model': 'Monster 821',
        'year': '2019',
        'engine': ('Testastretta 11°, L-Twin, 4 Desmodromically '
                   'actuated valves per cylinder, liquid cooled'),
        'displacement': '821 cc',
        'curb_mass': '206 kg',
        'fuel_capacity': '16.5 l',
        'max_power': '109 hp (80 kW) @ 9,250 rpm',
        'max_torque': '63 lb-ft (8.8 kgm, 86 Nm) @ 7,750 rpm',
        'image': ('https://motorcyclespecs.co.za/Gallery_A-L_16/'
                  'ducati_monster_821-05.jpg'),
        'manufacturer_id': 3,
    },
    {
        'model': 'Street 750',
        'year': '2019',
        'engine': ('4-stroke, liquid-cooled, Revolution X™ V-Twin, '
                   '4 valves per cylinder'),
        'displacement': '749 cc',
        'curb_mass': '233 kg',
        'fuel_capacity': '13.2 l',
        'max_power': '56 hp (41.8 kW) @ 7,500 rpm',
        'max_torque': '59 Nm (6.0 kgf-m, 43.5 lb-ft) @ 4,000 rpm',
        'image': ('https://motorcyclespecs.co.za/Gallery_A-L_16/'
                  'Harley-Street-750-18-02.jpg'),
        'manufacturer_id': 4,
    },
    {
        'model': 'Street Rod',
        'year': '2019',
        'engine': ('4-stroke, High Output Revolution X™ V-Twin, '
                   'SOHC, 4 valves per cylinder'),
        'displacement': '749 cc',
        'curb_mass': '238 kg',
        'fuel_capacity': '13.2 l',
        'max_power': '66 hp (49.2 kW) @ 8,750 rpm',
        'max_torque': '63.7 Nm (47 lb-ft) @ 4,000 rpm',
        'image': ('https://motorcyclespecs.co.za/Gallery_A-L_16/'
                  'Harley-Street-Rod-19-01.jpg'),
        'manufacturer_id': 4,
    },
    {
        'model': 'CB1000R',
        'year': '2019',
        'engine': ('Liquid-cooled, 4-stroke, inline 4-cylinder, '
                   'DOHC, 4 valves per cylinder'),
        'displacement': '998 cc',
        'curb_mass': '212 kg',
        'fuel_capacity': '16.3 l',
        'max_power': '143.5 hp (107 kW) @ 10,500 rpm',
        'max_torque': '104 Nm (77 lb-ft) @ 8,250 rpm',
        'image': ('https://motorcyclespecs.co.za/Gallery_A-L_16/'
                  'Honda-CB1000R-19-01.jpg'),
        'manufacturer_id': 5,
    },
    {
        'model': 'CB650F',
        'year': '2018',
        'engine': ('Liquid-cooled, 4-stroke, inline 4-cylinder, '
                   'DOHC, 4 valves per cylinder'),
        'displacement': '649 cc',
        'curb_mass': '206 kg',
        'fuel_capacity': '17.4 l',
        'max_power': '89.8 hp (67 kW) @ 11,000 rpm',
        'max_torque': '46.4 lb-ft (62.9 Nm) @ 8,000 rpm',
        'image': ('https://motorcyclespecs.co.za/Gallery_A-L_16/'
                  'honda_cb650f_17_02.jpg'),
        'manufacturer_id': 5,
    },
    {
        'model': 'Z900',
        'year': '2019',
        'engine': ('4-stroke, inline 4-cylinder, DOHC, '
                   '4 valves per cylinder, liquid-cooled'),
        'displacement': '948 cc',
        'curb_mass': '210 kg',
        'fuel_capacity': '17 l',
        'max_power': '125 hp (91.2 kW) @ 9,500 rpm',
        'max_torque': '73.1 lb-ft (99.1 Nm) @ 7,700 rpm',
        'image': ('https://motorcyclespecs.co.za/Gallery_A-L_16/'
                  'Kawasaki-Z900-19-02.jpg'),
        'manufacturer_id': 6,
    },
    {
        'model': 'Z650',
        'year': '2019',
        'engine': ('4-stroke, parallel twin-cylinder, DOHC, '
                   '4 valves per cylinder, liquid-cooled'),
        'displacement': '649 cc',
        'curb_mass': '410.1 lb',
        'fuel_capacity': '4.0 gal',
        'max_power': '67.3 hp (50.2 kW) @ 8,500 rpm',
        'max_torque': '48.5 lb-ft (65.7 Nm) @ 6,500 rpm',
        'image': ('https://motorcyclespecs.co.za/Gallery_A-L_16/'
                  'Kawasaki%20Z650_17_1.jpg'),
        'manufacturer_id': 6,
    },
    {
        'model': '790 Duke "The Scalpel"',
        'year': '2019',
        'engine': ('4-stroke, parallel twin-cylinder, DOHC, '
                   '4 valves per cylinder, liquid cooled'),
        'displacement': '799 cc',
        'curb_mass': '174 kg',
        'fuel_capacity': '14 l',
        'max_power': '105 hp (78.3 kW) @ 9,000 rpm',
        'max_torque': '87 Nm (64.2 lb-ft) @ 8,000 rpm',
        'image': ('https://motorcyclespecs.co.za/Gallery_A-L_16/'
                  'KTM%20790%20Duke_18_01.jpg'),
        'manufacturer_id': 7,
    },
    {
        'model': '690 SMC R "Street Slayer"',
        'year': '2019',
        'engine': ('4-stroke, single-cylinder, SOHC, '
                   '4 valves per cylinder, liquid cooled'),
        'displacement': '690 cc',
        'curb_mass': '160 kg',
        'fuel_capacity': '13.5 l',
        'max_power': '55 kW (73.7 hp) @ 8,000 rpm',
        'max_torque': '73.5 Nm (54.2 lb-ft) @ 6,500 rpm',
        'image': ('https://motorcyclespecs.co.za/Gallery_A-L_16/'
                  'KTM-690-SMC-R-19-04.jpg'),
        'manufacturer_id': 7,
    },
    {
        'model': 'Brutale 800 RC',
        'year': '2019',
        'engine': ('4-stroke, 3-cylinder, DOHC, '
                   '4 valves per cylinder, liquid cooled'),
        'displacement': '798 cc',
        'curb_mass': '190 kg',
        'fuel_capacity': '16.5 l',
        'max_power': '104 kW (140 hp) at 12,300 rpm',
        'max_torque': '87 Nm (64.2 lb-ft) at 10,100 rpm',
        'image': ('https://motorcyclespecs.co.za/Gallery_M-Z_16/'
                  'MV-Agusta-Brutale-800-RC-03.jpg'),
        'manufacturer_id': 8,
    },
    {
        'model': 'Dragster 800 RC',
        'year': '2019',
        'engine': ('4-stroke, 3-cylinder, DOHC, '
                   '4 valves per cylinder, liquid cooled'),
        'displacement': '798 cc',
        'curb_mass': '183 kg',
        'fuel_capacity': '16.5 l',
        'max_power': '104 kW (140 hp) at 12,500 rpm',
        'max_torque': '87 Nm (64.2 lb-ft) at 10,100 rpm',
        'image': ('https://motorcyclespecs.co.za/Gallery_M-Z_16/'
                  'MV%20Agusta%20Dragster%20800RC_18_03.jpg'),
        'manufacturer_id': 8,
    },
    {
        'model': 'Interceptor',
        'year': '2019',
        'engine': ('4-stroke, parallel twin-cylinder, SOHC, '
                   '4 valves per cylinder, air/oil cooled'),
        'displacement': '648 cc',
        'curb_mass': '214 kg',
        'fuel_capacity': '13.7 l',
        'max_power': '47 hp (35 kW) @ 7,250 rpm',
        'max_torque': '52 Nm (38.3 lb-ft) @ 5,250 rpm',
        'image': ('https://motorcyclespecs.co.za/Gallery_M-Z_16/'
                  'Royal%20Enfield%20Interceptor_04.jpg'),
        'manufacturer_id': 9,
    },
    {
        'model': 'Continental GT',
        'year': '2019',
        'engine': ('4-stroke, parallel twin-cylinder, SOHC, '
                   '4 valves per cylinder, air/oil cooled'),
        'displacement': '648 cc',
        'curb_mass': '210 kg',
        'fuel_capacity': '12.5 l',
        'max_power': '47 hp (35 kW) @ 7,250 rpm',
        'max_torque': '52 Nm (38.3 lb-ft) @ 5,250 rpm',
        'image': ('https://motorcyclespecs.co.za/Gallery_M-Z_16/'
                  'Royal%20Enfield%20Continental%20GT%2005.jpg'),
        'manufacturer_id': 9,
    },
    {
        'model': 'GSX-S750',
        'year': '2019',
        'engine': ('4-stroke, 4-cylinder, DOHC, '
                   '4 valves per cylinder, liquid cooled'),
        'displacement': '749 cc',
        'curb_mass': '211 kg',
        'fuel_capacity': '16 l',
        'max_power': '73.8 kW (99 hp) @ 10,170 rpm',
        'max_torque': '73.6 Nm (54.3 lb-ft) @ 9,060 rpm',
        'image': ('https://motorcyclespecs.co.za/Gallery_M-Z_16/'
                  'Suzuki-GSX-S750-19-02.jpg'),
        'manufacturer_id': 10,
    },
    {
        'model': 'DR-Z400SM',
        'year': '2019',
        'engine': ('4-stroke, single-cylinder, DOHC, '
                   '4 valves per cylinder, liquid cooled'),
        'displacement': '398 cc',
        'curb_mass': '147 kg',
        'fuel_capacity': '10 l',
        'max_power': '29.6 kW (39.7 hp) @ 8,500 rpm ',
        'max_torque': '39 Nm (28.8 lb-ft) @ 6,600 rpm',
        'image': ('https://motorcyclespecs.co.za/Gallery_M-Z_16/'
                  'Suzuki-DR-Z400SM-19-04.jpg'),
        'manufacturer_id': 10,
    },
    {
        'model': 'Street Triple RS',
        'year': '2019',
        'engine': ('4-stroke, inline 3-cylinder, DOHC, '
                   '4 valves per cylinder, liquid cooled'),
        'displacement': '765 cc',
        'curb_mass': '182 kg',
        'fuel_capacity': '17.4 l',
        'max_power': '121.2 hp (90.4 kW) @ 11,750 rpm',
        'max_torque': '57 lb-ft (77.3 Nm) @ 11,000 rpm',
        'image': ('https://motorcyclespecs.co.za/Gallery_M-Z_16/'
                  'Triumph%20Street%20Triple%20765RS_7.jpg'),
        'manufacturer_id': 11,
    },
    {
        'model': 'Street Twin',
        'year': '2019',
        'engine': ('4-stroke, 270° crank angle parallel twin-cylinder, '
                   'SOHC, 4 valves per cylinder, liquid cooled'),
        'displacement': '900 cc',
        'curb_mass': '210 kg',
        'fuel_capacity': '12 l',
        'max_power': '65 hp (48.5 kW) @ 7,500 rpm',
        'max_torque': '59 lb-ft (80 Nm) @ 3,800 rpm',
        'image': ('https://motorcyclespecs.co.za/Gallery_M-Z_16/'
                  'Triumph_Street_twin_16_03.jpg'),
        'manufacturer_id': 11,
    },
    {
        'model': 'MT-09',
        'year': '2019',
        'engine': ('4-stroke, inline 3-cylinder, DOHC, '
                   '4 valves per cylinder, liquid cooled'),
        'displacement': '847 cc',
        'curb_mass': '193 kg',
        'fuel_capacity': '14 l',
        'max_power': '85.7 kW (115 hp) @ 10,000 rpm',
        'max_torque': '87.5 Nm (64.5 lb-ft) @ 8,500 rpm',
        'image': ('https://motorcyclespecs.co.za/Gallery_M-Z_16/'
                  'Yamaha%20MT-09_18_03.jpg'),
        'manufacturer_id': 12,
    },
    {
        'model': 'XSR900',
        'year': '2019',
        'engine': ('4-stroke, inline 3-cylinder, DOHC, '
                   '4 valves per cylinder, liquid cooled'),
        'displacement': '847 cc',
        'curb_mass': '195 kg',
        'fuel_capacity': '14 l',
        'max_power': '113 hp (84.2 kW) @ 10,000 rpm',
        'max_torque': '64.5 lb-ft (87.5 Nm) @ 8,500 rpm',
        'image': ('https://motorcyclespecs.co.za/Gallery_M-Z_16/'
                  'Yamaha%20XSR%20900_18_04.jpg'),
        'manufacturer_id': 12,
    }
]


def add_manufacturers(list_of_names):
    for name in list_of_names:
        manufacturer = Manufacturer(name=name)
        session.add(manufacturer)
    session.commit()


def add_bikes(list_of_bikes):
    for dic in list_of_bikes:
        bike = Motorbike(
            model=dic['model'],
            year=dic['year'],
            engine=dic['engine'],
            displacement=dic['displacement'],
            curb_mass=dic['curb_mass'],
            fuel_capacity=dic['fuel_capacity'],
            max_power=dic['max_power'],
            max_torque=dic['max_torque'],
            image=dic['image'],
            manufacturer_id=dic['manufacturer_id'],
        )
        session.add(bike)
    session.commit()


def main():
    print('Adding data to database...')
    add_manufacturers(manufacturers)
    add_bikes(bikes)
    print('Successfully added all data!')


if __name__ == '__main__':
    main()
