# -*- coding: utf-8 -*-
# BioSTEAM: The Biorefinery Simulation and Techno-Economic Analysis Modules
# Copyright (C) 2020, Yoel Cortes-Pena <yoelcortes@gmail.com>
# 
# A significant portion of this module originates from:
# Chemical Engineering Design Library (ChEDL). Utilities for process modeling.
# Copyright (C) 2020 Caleb Bell <Caleb.Andrew.Bell@gmail.com>
# 
# This module is under a dual license:
# 1. The UIUC open-source license. See 
# github.com/BioSTEAMDevelopmentGroup/biosteam/blob/master/LICENSE.txt
# for license details.
# 
# 2. The MIT open-source license. See
# https://github.com/CalebBell/thermo/blob/master/LICENSE.txt for details.
"""
Data and methods for calculating the heat capacity of a chemical.

References
----------
.. [1] Lastovka, Vaclav, and John M. Shaw. "Predictive Correlations for
       Ideal Gas Heat Capacities of Pure Hydrocarbons and Petroleum Fractions."
       Fluid Phase Equilibria 356 (October 25, 2013): 338-370.
       doi:10.1016/j.fluid.2013.07.023.
.. [2] Kabo, G. J., and G. N. Roganov. Thermodynamics of Organic Compounds
       in the Gas State, Volume II: V. 2. College Station, Tex: CRC Press, 1994.
.. [3] Poling, Bruce E. The Properties of Gases and Liquids. 5th edition.
       New York: McGraw-Hill Professional, 2000.
.. [4] Gesellschaft, V. D. I., ed. VDI Heat Atlas. 2nd edition.
       Berlin; New York:: Springer, 2010.
.. [5] J.S. Rowlinson, Liquids and Liquid Mixtures, 2nd Ed.,
       Butterworth, London (1969).
.. [6] Dadgostar, Nafiseh, and John M. Shaw. "A Predictive Correlation for
       the Constant-Pressure Specific Heat Capacity of Pure and Ill-Defined
       Liquid Hydrocarbons." Fluid Phase Equilibria 313 (January 15, 2012):
       211-226. doi:10.1016/j.fluid.2011.09.015.
.. [7] Zabransky, M., V. Ruzicka Jr, V. Majer, and Eugene S. Domalski.
       Heat Capacity of Liquids: Critical Review and Recommended Values.
       2 Volume Set. Washington, D.C.: Amer Inst of Physics, 1996.
.. [8] Laštovka, Václav, Michal Fulem, Mildred Becerra, and John M. Shaw.
       "A Similarity Variable for Estimating the Heat Capacity of Solid Organic
       Compounds: Part II. Application: Heat Capacity Calculation for
       Ill-Defined Organic Solids." Fluid Phase Equilibria 268, no. 1-2
       (June 25, 2008): 134-41. doi:10.1016/j.fluid.2008.03.018.
.. [9] Green, Don, and Robert Perry.
       Perry's Chemical Engineers' Handbook,
       Eighth Edition. McGraw-Hill Professional, 2007.

"""
import os
from io import open
from math import log, exp
from cmath import log as clog, exp as cexp
import numpy as np
from ..base import (InterpolatedTDependentModel,
                    TDependentHandleBuilder, 
                    PhaseTHandleBuilder, 
                    thermo_model, 
                    functor)
from .data import (Cn_data_Poling,
                   Cn_data_TRC_gas,
                   Cn_data_CRC_standard,
                   Cn_data_PerryI,
                   zabransky_dict_sat_s,
                   zabransky_dict_sat_p,
                   zabransky_dict_const_s,
                   zabransky_dict_const_p,
                   zabransky_dict_iso_s,
                   zabransky_dict_iso_p,
                   VDI_saturation_dict, 
                   VDI_tabular_data)
from .._constants import R, calorie
from ..functional import polylog2
# from .electrochem import (LaliberteHeatCapacityModel,
#                           _Laliberte_Heat_Capacity_ParametersDict)
# from .coolprop import has_CoolProp, coolprop_dict, CoolProp_T_dependent_property,\
#                       coolprop_fluids, PropsSI

__all__ = ('heat_capacity_handle',

           'Lastovka_Shaw',
           'Lastovka_Shaw_Integral',
           'Lastovka_Shaw_Integral_Over_T',

           'TRCCn', 
           'TRCCn_Integral', 
           'TRCCn_Integral_Over_T',

           'Poling',
           'Poling_Integral', 
           'Poling_Integral_Over_T',
           
           'Rowlinson_Poling', 'Rowlinson_Bondi',

           'Zabransky_Cubic', 
           'Zabransky_Cubic_Integral', 
           'Zabransky_Cubic_Over_T_Integral',

           'Zabransky_Quasi_Polynomial', 
           'Zabransky_Quasi_Polynomial_Integral', 
           'Zabransky_Quasi_Polynomial_Over_T_Integral',

           'Dadgostar_Shaw', 
           'Dadgostar_Shaw_Integral', 
           'Dadgostar_Shaw_Over_T_Integral',

           'Lastovka_Solid', 
           'Lastovka_Solid_Integral', 
           'Lastovka_Solid_Over_T_Integral',
           
           'Perry_151', 
           'Perry_151_Integral', 
           'Perry_151_Over_T_Integral'
)


# %% Utilities

def CnHS(FCn, FH, FS, data):
    fCn = FCn.from_args(data)
    return {'evaluate': fCn,
            'integrate_by_T': FH.from_other(fCn),
            'integrate_by_T_over_T': FS.from_other(fCn)}

def CnHSModel(FCn, FH, FS, data=None, Tmin=None, Tmax=None, name=None):
    funcs = CnHS(FCn, FH, FS, data)
    return thermo_model(Tmin=Tmin, Tmax=Tmax, name=name, var='Cn', **funcs)

class ZabranskyModelBuilder:
    __slots__ = ('name', 'casdata', 'funcs', 'many')
    
    def __init__(self, name, casdata, funcs, many=False):
        self.name = name
        self.casdata = casdata
        self.funcs = funcs
        self.many = many
    
    def add_model(self, CAS, models):
        if CAS in self.casdata:
            if self.many:
                models.extend([self.build_model(i) for i in self.casdata[CAS]])
            else:
                models.append(self.build_model(self.casdata[CAS]))
    
    def build_model(self, data):
        *args, Tmin, Tmax = data
        return CnHSModel(*self.funcs, args, Tmin, Tmax, self.name)


# %% Heat Capacities Gas
 
def calculate_Lastovka_Shaw_term(iscyclic_aliphatic, similary_variable):
    if iscyclic_aliphatic:
        A1 = -0.1793547
        A2 = 3.86944439
        term = A1 + A2 * similary_variable
    else:
        A1 = 0.58
        A2 = 1.25
        A3 = 0.17338003 # 803 instead of 8003 in another paper
        A4 = 0.014
        term = A2 + (A1-A2)/(1. + exp((similary_variable - A3)/A4))
    return term

@functor(var='Cn.g')
def Lastovka_Shaw(T, MW, similarity_variable, iscyclic_aliphatic=False):
    r"""
    Create a functor of temperature (T; in K) that estimates the gas molar 
    heat capacity (Cn.g; in J/mol/K) of a chemical using the Lastovka Shaw 
    method, as described in [1]_.
    
    Parameters
    ----------
    MW : float
        Molecular weight [g/mol].
    similarity_variable : float
        Heat capacity similarity variable [-].
    iscyclic_aliphatic : bool
        Whether a chemical is cyclic aliphatic [-].
    
    Notes
    -----
    The ideal-gas heat capacity (Cn.g; in J/mol/K) is given by:

    .. math::
        C_n^0 = MW \left(A_2 + \frac{A_1 - A_2}{1 + \exp(\frac{\alpha-A_3}{A_4})}\right)
        + (B_{11} + B_{12}\alpha)\left(-\frac{(C_{11} + C_{12}\alpha)}{T}\right)^2
        \frac{\exp(-(C_{11} + C_{12}\alpha)/T)}{[1-\exp(-(C_{11}+C_{12}\alpha)/T)]^2}\\
        + (B_{21} + B_{22}\alpha)\left(-\frac{(C_{21} + C_{22}\alpha)}{T}\right)^2
        \frac{\exp(-(C_{21} + C_{22}\alpha)/T)}{[1-\exp(-(C_{21}+C_{22}\alpha)/T)]^2}

    Original model is in terms of J/g/K, but is translated to molar heat capacity in J/mol/K.

    A1 = 0.58, A2 = 1.25, A3 = 0.17338003, A4 = 0.014,
    
    B11 = 0.73917383, B12 = 8.88308889,
    
    C11 = 1188.28051, C12 = 1813.04613,
    
    B21 = 0.0483019, B22 = 4.35656721, 
    
    C21 = 2897.01927, C22 = 5987.80407.

    Examples
    --------
    Compute the heat capacity of Methane at 300 K:
    
    >>> f_Cng = Lastovka_Shaw(MW=16.043,
    ...                       similarity_variable=0.31166,
    ...                       iscyclic_aliphatic=False)
    >>> f_Cng
    Functor: Lastovka_Shaw(T, P=None) -> Cn.g [J/mol/K]
     MW: 16.043 g/mol
     similarity_variable: 0.31166
     iscyclic_aliphatic: 0
    >>> f_Cng(T=400.0)
    33.91574477458602
    
    """
    a = similarity_variable
    term = calculate_Lastovka_Shaw_term(iscyclic_aliphatic, a)
    B11 = 0.73917383
    B12 = 8.88308889
    C11 = 1188.28051
    C12 = 1813.04613
    B21 = 0.0483019
    B22 = 4.35656721
    C21 = 2897.01927
    C22 = 5987.80407
    return MW * (term
                 + (B11 + B12*a)*((C11+C12*a)/T)**2*exp(-(C11 + C12*a)/T)/(1.-exp(-(C11+C12*a)/T))**2
                 + (B21 + B22*a)*((C21+C22*a)/T)**2*exp(-(C21 + C22*a)/T)/(1.-exp(-(C21+C22*a)/T))**2)

@functor(var='H.g')
def Lastovka_Shaw_Integral(Ta, Tb, MW, similarity_variable, iscyclic_aliphatic=False):
    term = calculate_Lastovka_Shaw_term(iscyclic_aliphatic, similarity_variable)
    return (Lastovka_Shat_Indefinite_Integral(Tb, MW, similarity_variable, term)
            - Lastovka_Shat_Indefinite_Integral(Ta, MW, similarity_variable, term))

 
def Lastovka_Shat_Indefinite_Integral(T, MW, similarity_variable, term=None):
    a = similarity_variable
    B11 = 0.73917383
    B12 = 8.88308889
    C11 = 1188.28051
    C12 = 1813.04613
    B21 = 0.0483019
    B22 = 4.35656721
    C21 = 2897.01927
    C22 = 5987.80407
    return MW * (T*term - (B11 + B12*a)*(-C11 - C12*a)**2/(-C11 - C12*a + (C11 
                 + C12*a)*exp((-C11 - C12*a)/T)) - (B21 + B22*a)*(-C21 - C22*a)**2/(-C21 
                 - C22*a + (C21 + C22*a)*exp((-C21 - C22*a)/T)))

@functor(var='S.g')
def Lastovka_Shaw_Integral_Over_T(Ta, Tb, MW, similarity_variable,
                                  iscyclic_aliphatic=False):
    term = calculate_Lastovka_Shaw_term(iscyclic_aliphatic, similarity_variable)
    return (Lastovka_Shaw_Indefinite_Integral_Over_T(Tb, MW, similarity_variable, term)
            - Lastovka_Shaw_Indefinite_Integral_Over_T(Ta, MW, similarity_variable, term))

 
def Lastovka_Shaw_Indefinite_Integral_Over_T(T, MW, similarity_variable, term):
    a = similarity_variable
    a2 = a*a
    B11 = 0.73917383
    B12 = 8.88308889
    C11 = 1188.28051
    C12 = 1813.04613
    B21 = 0.0483019
    B22 = 4.35656721
    C21 = 2897.01927
    C22 = 5987.80407
    S = (term*clog(T) + (-B11 - B12*a)*clog(cexp((-C11 - C12*a)/T) - 1.) 
        + (-B11*C11 - B11*C12*a - B12*C11*a - B12*C12*a2)/(T*cexp((-C11
        - C12*a)/T) - T) - (B11*C11 + B11*C12*a + B12*C11*a + B12*C12*a2)/T)
    S += ((-B21 - B22*a)*clog(cexp((-C21 - C22*a)/T) - 1.) + (-B21*C21 - B21*C22*a
        - B22*C21*a - B22*C22*a2)/(T*cexp((-C21 - C22*a)/T) - T) - (B21*C21
        + B21*C22*a + B22*C21*a + B22*C22*a**2)/T)
    # There is a non-real component, but it is only a function of similariy 
    # variable and so will always cancel out.
    return MW * S.real

@functor(var='Cn.g')
def TRCCn(T, a0, a1, a2, a3, a4, a5, a6, a7):
    r"""
    Create a functor of temperature (T; in K) that estimates the gas molar 
    heat capacity (Cn.g; in J/mol/K) of a chemical using the TRCCn method, 
    as described in [2]_.
    
    Parameters
    ----------
    a0,a1,a2,a3,a4,a5,a6,a7 : float
        Regressed coefficients.
    
    Notes
    -----
    The ideal gas heat capacity (Cn.g; J/mol/K) is given by:

    .. math::
        C_n = R\left(a_0 + (a_1/T^2) \exp(-a_2/T) + a_3 y^2
        + (a_4 - a_5/(T-a_7)^2 )y^j \right)

        y = \frac{T-a_7}{T+a_6} \text{ for } T > a_7 \text{ otherwise } 0

    j is set to 8. Analytical integrals are available for this expression.

    Examples
    --------
    Calculate the heat capacity of Methane at 300 K:
    
    >>> f_Cng = TRCCn(4.0, 22350000, 2018, 32.767, -31.098, 1346090000, 1229, 473)
    >>> f_Cng
    Functor: TRCCn(T, P=None) -> Cn.g [J/mol/K]
     a0: 4
     a1: 2.235e+07
     a2: 2018
     a3: 32.767
     a4: -31.098
     a5: 1.3461e+09
     a6: 1229
     a7: 473
    >>> f_Cng(300)
    35.73249522521754
    
    """
    if T <= a7:
        y = 0.
    else:
        y = (T - a7)/(T + a6)
    return R*(a0 + (a1/T**2)*exp(-a2/T) + a3*y**2 + (a4 - a5/(T-a7)**2 )*y**8.)

 
def TRCCn_Indefinite_Integral(T, a0, a1, a2, a3, a4, a5, a6, a7):
    first = a6 + a7    
    y = 0. if T <= a7 else (T - a7)/(T + a6)
    y2 = y*y
    y4 = y2*y2
    if T <= a7:
        h = 0.0
    else:
        second = (2.*a3 + 8.*a4)*log(1. - y)
        third = (a3*(1. + 1./(1. - y)) + a4*(7. + 1./(1. - y)))*y
        fourth = a4*(3.*y2 + 5./3.*y*y2 + y4 + 0.6*y4*y + 1/3.*y4*y2)
        fifth = 1/7.*(a4 - a5/((a6 + a7)**2))*y4*y2*y
        h = first*(second + third + fourth + fifth)
    return (a0 + a1*exp(-a2/T)/(a2*T) + h/T)*R*T

@functor(var='H.g')
def TRCCn_Integral(Ta, Tb, a0, a1, a2, a3, a4, a5, a6, a7):
    return (TRCCn_Indefinite_Integral(Tb, a0, a1, a2, a3, a4, a5, a6, a7)
            - TRCCn_Indefinite_Integral(Ta, a0, a1, a2, a3, a4, a5, a6, a7))

 
def TRCCn_Over_T_Indefinite_Integral(T, a0, a1, a2, a3, a4, a5, a6, a7):
    # Possible optimizations: pre-cache as much as possible.
    # If this were replaced by a cache, much of this would not need to be computed.
    y = 0. if T <= a7 else (T - a7)/(T + a6)
    z = T/(T + a6)*(a7 + a6)/a7
    if T <= a7:
        s = 0.
    else:
        a72 = a7*a7
        a62 = a6*a6
        a7_a6 = a7/a6 # a7/a6
        a7_a6_2 = a7_a6*a7_a6
        a7_a6_4 = a7_a6_2*a7_a6_2
        x1 = (a4*a72 - a5)/a62 # part of third, sum
        first = (a3 + ((a4*a72 - a5)/a62)*a7_a6_4)*a7_a6_2*log(z)
        second = (a3 + a4)*log((T + a6)/(a6 + a7))
        fourth = -(a3/a6*(a6 + a7) + a5*y**6/(7.*a7*(a6 + a7)))*y
        third = np.array([(x1*(-a7_a6)**(6-i) - a4)*y**i/i for i in np.arange(1, 8)]).sum()
        s = first + second + third + fourth
    return a0*log(T) + a1/(a2*a2)*(1. + a2/T)*exp(-a2/T) + s

@functor(var='S.g')
def TRCCn_Integral_Over_T(Ta, Tb, a0, a1, a2, a3, a4, a5, a6, a7):
    return R*(TRCCn_Over_T_Indefinite_Integral(Tb, a0, a1, a2, a3, a4, a5, a6, a7)
              - TRCCn_Over_T_Indefinite_Integral(Ta, a0, a1, a2, a3, a4, a5, a6, a7))

@functor(var='Cn.g')
def Poling(T, a, b, c, d, e):
    r"""
    Create a functor of temperature (T; in K) that estimates the gas molar
    heat capacity (Cn.g; in J/mol/K) of a chemical using the Poling method,
    as described in [3]_.
    
    Parameters
    ----------
    a,b,c,d,e : float
        Regressed coefficients.
    
    
    Notes
    -----
    The ideal gas heat capacity (Cn.g; J/mol/K) is given by:
    
    .. math:: C_n = R*(a + bT + cT^2 + dT^3 + eT^4)
    
    The data is based on the Poling data bank.
    
    Examples
    --------
    Compute the gas heat capacity of Methane at 300 K:
    
    >>> f_Cng = Poling(a=4.568, b=-0.008975, c=3.631e-05, d=-3.407e-08, e=1.091e-11)
    >>> f_Cng
    Functor: Poling(T, P=None) -> Cn.g [J/mol/K]
     a: 4.568
     b: -0.008975
     c: 3.631e-05
     d: -3.407e-08
     e: 1.091e-11
    >>> f_Cng(300)
    35.85096123688382
    
    """
    return R*(a + b*T + c*T**2 + d*T**3 + e*T**4)

 
def Poling_Indefinite_Integral(T, a, b, c, d, e):
    return (((((0.2*e)*T + 0.25*d)*T + c/3.)*T + 0.5*b)*T + a)*T

@functor(var='H.g')
def Poling_Integral(Ta, Tb, a, b, c, d, e):
    return R*(Poling_Indefinite_Integral(Tb, a, b, c, d, e)
              - Poling_Indefinite_Integral(Ta, a, b, c, d, e))

 
def Poling_Over_T_Indefinite_Integral(T, a, b, c, d, e):
    return ((((0.25*e)*T + d/3.)*T + 0.5*c)*T + b)*T

@functor(var='S.g')
def Poling_Integral_Over_T(Ta, Tb, a, b, c, d, e):
    return R*(Poling_Over_T_Indefinite_Integral(Tb, a, b, c, d, e)
              - Poling_Over_T_Indefinite_Integral(Ta, a, b, c, d, e)
              + a*log(Tb/Ta))

# Heat capacity gas methods
TRCIG = 'TRC Thermodynamics of Organic Compounds in the Gas State (1994)'
POLING = 'Poling et al. (2001)'
POLING_CONST = 'Poling et al. (2001) constant'
CRCSTD = 'CRC Standard Thermodynamic Properties of Chemical Substances'
VDI_TABULAR = 'VDI Heat Atlas'
LASTOVKA_SHAW = 'Lastovka and Shaw (2013)'

TRCCn_Functors = (TRCCn,
                  TRCCn_Integral,
                  TRCCn_Integral_Over_T)
Poling_Functors = (Poling,
                   Poling_Integral, 
                   Poling_Integral_Over_T)


@TDependentHandleBuilder('Cn.g')
def heat_capacity_gas_handle(handle, CAS, MW, similarity_variable, iscyclic_aliphatic):
    add_model = handle.add_model
    if CAS in Cn_data_TRC_gas:
        _, Tmin, Tmax, a0, a1, a2, a3, a4, a5, a6, a7, _, _, _ = Cn_data_TRC_gas[CAS]
        funcs = CnHS(*TRCCn_Functors, (a0, a1, a2, a3, a4, a5, a6, a7))
        add_model(Tmin=Tmin, Tmax=Tmax, name=TRCIG, **funcs)
    if CAS in Cn_data_Poling:
        _, Tmin, Tmax, a, b, c, d, e, Cn_g, _ = Cn_data_Poling[CAS]
        if not np.isnan(a):
            funcs = CnHS(*Poling_Functors, (a, b, c, d, e))
            add_model(Tmin=Tmin, Tmax=Tmax, **funcs, name=POLING)
        if not np.isnan(Cn_g):
            add_model(Cn_g, Tmin, Tmax, name=POLING_CONST)
    if CAS in Cn_data_CRC_standard:
        Cn_g = Cn_data_CRC_standard[CAS][-1]
        if not np.isnan(Cn_g):
            add_model(Cn_g, name=CRCSTD)
    if MW and similarity_variable:
        data = (MW, similarity_variable, iscyclic_aliphatic)
        add_model(Lastovka_Shaw.from_args(data), name=LASTOVKA_SHAW)
    if CAS in VDI_saturation_dict:
        # NOTE: VDI data is for the saturation curve, i.e. at increasing
        # pressure; it is normally substantially higher than the ideal gas
        # value
        Ts, Cn_gs = VDI_tabular_data(CAS, 'Cp (g)')
        add_model(InterpolatedTDependentModel(Ts, Cn_gs, Tmin=Ts[0], Tmax=Ts[-1], name=VDI_TABULAR))
    
    
### Heat capacities of liquids

@functor(var='Cn.l')
def Rowlinson_Poling(T, Tc, ω, Cn_g):
    r"""
    Create a functor of temperature (T; in K) that estimates the liquid molar
    heat capacity (Cn.l; in J/mol/K) of a chemical using the Rowlinson Poling
    method, as described in [3]_.
    
    Parameters
    ----------
    Tc : float
        Critical point temperature [K].
    ω : float
        Acentric factor [-].
    Cn_g : float
        Gas molar heat capacity [-].
    
    Notes
    -----
    The heat capacity of a liquid is given by:

    .. math::
        \frac{Cn^{L} - Cn^{g}}{R} = 1.586 + \frac{0.49}{1-T_r} +
        \omega\left[ 4.2775 + \frac{6.3(1-T_r)^{1/3}}{T_r} + \frac{0.4355}{1-T_r}\right]

    This equation is not too accurate.
    Poling compared 212 substances, and found error at 298K larger than 10%
    for 18 of them, mostly associating. Of the other 194 compounds, AARD is 2.5%.

    Examples
    --------
    Compute the liquid heat capacity of methane at 100 K:
    
    >>> Cn_g = Poling(a=4.568, b=-0.008975, c=3.631e-05,
    ...               d=-3.407e-08, e=1.091e-11)
    >>> f_Cnl = Rowlinson_Poling(Tc=190.564, ω=0.008, Cn_g=Cn_g)
    Functor: Rowlinson_Poling(T, P=None) -> Cn.l [J/mol/K]
     Tc: 190.56 K
     ω: 0.008
     Cn_g: Poling(T, P=None) -> J/mol/K
    >>> f_Cnl(100)
    55.99104104081243
    
    """
    Tr = T/Tc
    return Cn_g(T) + R*(1.586 + 0.49/(1.-Tr) + ω*(4.2775 + 6.3*(1-Tr)**(1/3.)/Tr + 0.4355/(1.-Tr)))

@functor(var='Cn.l')
def Rowlinson_Bondi(T, Tc, ω, Cn_g):
    r"""
    Create a functor of temperature (T; in K) that estimates the liquid molar
    heat capacity (Cn.l; in J/mol/K) of a chemical using the Rowlinson Bondi
    method, as described in [3]_ [4]_ [5]_.
    
    Parameters
    ----------
    Tc : float
        Critical point temperature [K].
    ω : float
        Acentric factor [-].
    Cn_g : float
        Gas molar heat capacity [-].
    
    
    Notes
    -----
    The heat capacity of a liquid is given by:

    .. math::
        \frac{Cn^L - Cn^{ig}}{R} = 1.45 + 0.45(1-T_r)^{-1} + 0.25\omega
        [17.11 + 25.2(1-T_r)^{1/3}T_r^{-1} + 1.742(1-T_r)^{-1}]

    Less accurate than `Rowlinson_Poling`.

    Examples
    --------
    >>> Cn_g = Poling(a=4.568, b=-0.008975, c=3.631e-05,
    ...               d=-3.407e-08, e=1.091e-11)
    >>> f_Cnl = Rowlinson_Poling(Tc=190.564, ω=0.008,
    ...                          Cn_g=Cn_g)
    >>> f_Cnl
    Functor: Rowlinson_Poling(T, P=None) -> Cn.l [J/mol/K]
     Tc: 190.56 K
     ω: 0.008
     Cn_g: Poling(T, P=None) -> J/mol/K
    >>> f_Cnl(100)
    55.986088530998174
      
    """
    Tr = T/Tc
    return Cn_g(T) + R*(1.45 + 0.45/(1.-Tr) + 0.25*ω*(17.11 + 25.2*(1-Tr)**(1/3.)/Tr + 1.742/(1.-Tr)))

@functor(var='Cn.l')
def Dadgostar_Shaw(T, MW, similarity_variable):
    r"""
    Create a functor of temperature (T; in K) that estimates the liquid molar
    heat capacity (Cn.l; in J/mol/K) of a chemical using the Dadgostar Shaw
    method, as described in [6]_.
    
    Parameters
    ----------
    MW : float
        Molecular weight [g/mol].
    similarity_variable : float
        Heat capacity similarity variable [-].
    
    Notes
    -----
    The liquid heat capacity is given by:

    .. math::
        C_{p} = 24.5(a_{11}\alpha + a_{12}\alpha^2)+ (a_{21}\alpha
        + a_{22}\alpha^2)T +(a_{31}\alpha + a_{32}\alpha^2)T^2
        
        C_n = MW \cdot Cp

    Where :math:`\alpha` is the similarity variable. There are many 
    restrictions on its use.

    Original model is in terms of J/g/K, but it has been modified to give 
    molar heat capacity in J/mol/K.

    a11 = -0.3416; a12 = 2.2671; a21 = 0.1064; a22 = -0.3874l;
    a31 = -9.8231E-05; a32 = 4.182E-04
      
    """
    first, second, third = calculate_Dadgostar_Shaw_terms(MW, similarity_variable)
    first *= 3*R*(151.8675/T)**2*exp(151.8675/T)/(exp(151.8675/T)-1)**2
    return (first + second*T + third*T**2) * MW

 
def calculate_Dadgostar_Shaw_terms(MW, similarity_variable):
    a = similarity_variable
    a2 = a*a
    a11 = -0.3416
    a12 = 2.2671
    a21 = 0.1064
    a22 = -0.3874
    a31 = -9.8231E-05
    a32 = 4.182E-04
    # Didn't seem to improve the comparison; sum of errors on some
    # points included went from 65.5  to 286.
    # Author probably used more precision in their calculation.
    return (a11*a + a12*a2,
            a21*a + a22*a2,
            a31*a + a32*a2)

 
def Dadgostar_Shaw_Indefinte_Integral(T, first, second, third):
    T2 = T*T
    first *= 3*R*(151.8675/T)**2*exp(151.8675/T)/(exp(151.8675/T)-1)**2
    return T2*T/3.*third + T2*0.5*second + T*first

@functor(var='H.l')
def Dadgostar_Shaw_Integral(Ta, Tb, MW, similarity_variable):
    terms = calculate_Dadgostar_Shaw_terms(MW, similarity_variable)
    return MW*(Dadgostar_Shaw_Indefinte_Integral(Tb, *terms)
               - Dadgostar_Shaw_Indefinte_Integral(Ta, *terms))

 
def Dadgostar_Shaw_Over_T_Indefinte_Integral(T, first, second, third):
    first *= 3*R*(151.8675/T)**2*exp(151.8675/T)/(exp(151.8675/T)-1)**2
    return T*T*0.5*third + T*second + first*log(T)

@functor(var='S.l')
def Dadgostar_Shaw_Over_T_Integral(Ta, Tb, MW, similarity_variable):
    terms = calculate_Dadgostar_Shaw_terms(MW, similarity_variable)
    return MW*(Dadgostar_Shaw_Over_T_Indefinte_Integral(Tb, *terms)
               - Dadgostar_Shaw_Over_T_Indefinte_Integral(Ta, *terms))

@functor(var='Cn.l')
def Zabransky_Quasi_Polynomial(T, Tc, a1, a2, a3, a4, a5, a6):
    r"""
    Create a functor of temperature (T; in K) that estimates the liquid molar
    heat capacity (Cn.l; in J/mol/K) of a chemical using the Zabransky Quasi
    Polynomial method, as described in [7]_.
    
    Parameters
    ----------
    Tc : float
        Critical point temperature [K].
    a1,a2,a3,a4,a5,a6 : float
        Regressed coefficients.
    
    Notes
    -----
    The liquid heat capacity is given by:
    
    .. math::
        \frac{C_n}{R}=A_1\ln(1-T_r) + \frac{A_2}{1-T_r}
        + \sum_{j=0}^m A_{j+3} T_r^j

    Used only for isobaric heat capacities, not saturation heat capacities.
    Designed for reasonable extrapolation behavior caused by using the reduced
    critical temperature. Used by the authors of [1]_ when critical temperature
    was available for the fluid.

    """
    Tr = T/Tc
    return R*(a1*log(1-Tr) + a2/(1-Tr) + a3 + a4*Tr + a5*Tr**2 + a6*Tr**3)

 
def Zabransky_Quasi_Polynomial_Indefinte_Integral(T, Tc, a1, a2, a3, a4, a5, a6):
    Tc2 = Tc*Tc
    Tc3 = Tc2*Tc    
    term = (T - Tc)**2
    return R*(T*(T*(T*(T*a6/(4.*Tc3) + a5/(3.*Tc2)) + a4/(2.*Tc)) - a1 + a3) 
              + T*a1*log(1. - T/Tc) - 0.5*Tc*(a1 + a2)*log(term))

@functor(var='H.l')
def Zabransky_Quasi_Polynomial_Integral(Ta, Tb, Tc, a1, a2, a3, a4, a5, a6):
    return (Zabransky_Quasi_Polynomial_Indefinte_Integral(Tb, Tc, a1, a2, a3, a4, a5, a6)
            - Zabransky_Quasi_Polynomial_Indefinte_Integral(Ta, Tc, a1, a2, a3, a4, a5, a6))

def Zabransky_Quasi_Polynomial_Over_T_Indefinte_Integral(T, Tc, a1, a2, a3, a4, a5, a6):
    Tc2 = Tc*Tc
    Tc3 = Tc2*Tc    
    term = (T - Tc)**2
    term = T - Tc
    logT = log(T)
    return R*(a3*logT -a1*polylog2(T/Tc) - a2*(-logT + 0.5*log(term*term))
              + T*(T*(T*a6/(3.*Tc3) + a5/(2.*Tc2)) + a4/Tc))

@functor(var='S.l')
def Zabransky_Quasi_Polynomial_Over_T_Integral(Ta, Tb, Tc, a1, a2, a3, a4, a5, a6):
    return (Zabransky_Quasi_Polynomial_Over_T_Indefinte_Integral(Tb, Tc, a1, a2, a3, a4, a5, a6)
            - Zabransky_Quasi_Polynomial_Over_T_Indefinte_Integral(Ta, Tc, a1, a2, a3, a4, a5, a6))

@functor(var='Cn.l')
def Zabransky_Cubic(T, a1, a2, a3, a4):
    r"""
    Create a functor of temperature (T; in K) that estimates the liquid molar
    heat capacity (Cn.l; in J/mol/K) of a chemical using the Zabransky Cubic
    method, as described in [7]_.
    
    Parameters
    ----------
    a1,a2,a3,a4 : float
        Regressed coefficients.
    
    Notes
    -----
    The liquid heat capacity is given by:
    
    .. math::
        \frac{C}{R}=\sum_{j=0}^3 A_{j+1} \left(\frac{T}{100}\right)^j
    
    """
    T = T/100.
    return R*(((a4*T + a3)*T + a2)*T + a1)

 
def Zabransky_Cubic_Indefinite_Integral(T, a1, a2, a3, a4):
    T = T/100.
    return 100.*R*T*(T*(T*(T*a4*0.25 + a3/3.) + a2*0.5) + a1)

@functor(var='H.l')
def Zabransky_Cubic_Integral(Ta, Tb, a1, a2, a3, a4):
    return (Zabransky_Cubic_Indefinite_Integral(Tb, a1, a2, a3, a4)
            - Zabransky_Cubic_Indefinite_Integral(Ta, a1, a2, a3, a4))

 
def Zabransky_Cubic_Over_T_Indefinite_Integral(T, a1, a2, a3, a4):
    T = T/100.
    return R*(T*(T*(T*a4/3. + a3/2.) + a2) + a1*log(T))

@functor(var='S.l')
def Zabransky_Cubic_Over_T_Integral(Ta, Tb, a1, a2, a3, a4):
    return (Zabransky_Cubic_Over_T_Indefinite_Integral(Tb, a1, a2, a3, a4)
            - Zabransky_Cubic_Over_T_Indefinite_Integral(Ta, a1, a2, a3, a4))
    

# Heat capacity liquid methods:
ZABRANSKY_SPLINE = 'Zabransky spline, averaged heat capacity'
ZABRANSKY_QUASIPOLYNOMIAL = 'Zabransky quasipolynomial, averaged heat capacity'
ZABRANSKY_SPLINE_C = 'Zabransky spline, constant-pressure'
ZABRANSKY_QUASIPOLYNOMIAL_C = 'Zabransky quasipolynomial, constant-pressure'
ZABRANSKY_SPLINE_SAT = 'Zabransky spline, saturation'
ZABRANSKY_QUASIPOLYNOMIAL_SAT = 'Zabransky quasipolynomial, saturation'
ROWLINSON_POLING = 'Rowlinson and Poling (2001)'
ROWLINSON_BONDI = 'Rowlinson and Bondi (1969)'
DADGOSTAR_SHAW = 'Dadgostar and Shaw (2011)'

Zabransky_Cubic_Functors = (Zabransky_Cubic,
                            Zabransky_Cubic_Integral,
                            Zabransky_Cubic_Over_T_Integral)
Zabransky_Quasi_Polynomial_Functors = (Zabransky_Quasi_Polynomial,
                                    Zabransky_Quasi_Polynomial_Integral, 
                                    Zabransky_Quasi_Polynomial_Over_T_Integral)
Dadgostar_Shaw_Functors = (Dadgostar_Shaw,
                           Dadgostar_Shaw_Integral,
                           Dadgostar_Shaw_Over_T_Integral)

zabransky_model_data = ((ZABRANSKY_SPLINE,
                         zabransky_dict_const_s,
                         Zabransky_Cubic_Functors),
                        (ZABRANSKY_QUASIPOLYNOMIAL,
                         zabransky_dict_const_p,
                         Zabransky_Quasi_Polynomial_Functors),
                        (ZABRANSKY_SPLINE_C,
                         zabransky_dict_iso_s, 
                         Zabransky_Cubic_Functors),
                        (ZABRANSKY_QUASIPOLYNOMIAL_C, 
                         zabransky_dict_iso_p,
                         Zabransky_Quasi_Polynomial_Functors),
                        (ZABRANSKY_SPLINE_SAT,
                         zabransky_dict_sat_s,
                         Zabransky_Cubic_Functors),
                        (ZABRANSKY_QUASIPOLYNOMIAL_SAT, 
                         zabransky_dict_sat_p,
                         Zabransky_Quasi_Polynomial_Functors))

zabransky_model_builders = [ZabranskyModelBuilder(*i) for i in zabransky_model_data]
zabransky_model_builders[0].many = True
zabransky_model_builders[2].many = True
zabransky_model_builders[4].many = True

@TDependentHandleBuilder('Cn.l')
def heat_capacity_liquid_handle(handle, CAS, Tb, Tc, omega, MW, similarity_variable, Cn_g):
    for i in zabransky_model_builders: i.add_model(CAS, handle.models)        
    add_model = handle.add_model
    if CAS in VDI_saturation_dict:
        # NOTE: VDI data is for the saturation curve, i.e. at increasing
        # pressure; it is normally substantially higher than the ideal gas
        # value
        Ts, Cn_ls = VDI_tabular_data(CAS, 'Cp (l)')
        add_model(InterpolatedTDependentModel(Ts, Cn_ls, Ts[0], Ts[-1], name=VDI_TABULAR))
    if Tc and omega and Cn_g:
        args = (Tc, omega, Cn_g, 200, Tc)
        add_model(Rowlinson_Bondi.from_args(args), Tmin=0, Tmax=Tc, name=ROWLINSON_BONDI)
        add_model(Rowlinson_Poling.from_args(args),Tmin=0, Tmax=Tc, name=ROWLINSON_POLING)
    # Other
    if MW and similarity_variable:
        add_model(CnHSModel(*Dadgostar_Shaw_Functors,
                               data=(MW, similarity_variable),
                               name=DADGOSTAR_SHAW))
    # Constant models
    if CAS in Cn_data_Poling:
        _, Tmin, Tmax, a, b, c, d, e, Cn_g, Cn_l = Cn_data_Poling[CAS]
        if not np.isnan(Cn_g):
            add_model(Cn_l, Tmin, Tmax, name=POLING_CONST)
    if CAS in Cn_data_CRC_standard:
        Cn_l = Cn_data_CRC_standard[CAS][-5]
        if not np.isnan(Cn_l):
            add_model(Cn_l, 0, Tc, name=CRCSTD)

# %% Heat Capacity Solid

@functor(var='Cn.s')
def Lastovka_Solid(T, similarity_variable, MW):
    r"""
    Create a functor of temperature (T; in K) that estimates the solid molar 
    heat capacity (Cn.s; in J/mol/K) of a chemical using the Lastovka Solid
    method, as described in [8]_.
    
    Parameters
    ----------
    similarity_variable : float
        Heat capacity similarity variable [-].
    MW : float
        Molecular weight [g/mol].
    
    Notes
    -----
    The solid heat capacity is given by:

    .. math::
        C_p = 3(A_1\alpha + A_2\alpha^2)R\left(\frac{\theta}{T}\right)^2
        \frac{\exp(\theta/T)}{[\exp(\theta/T)-1]^2}
        + (C_1\alpha + C_2\alpha^2)T + (D_1\alpha + D_2\alpha^2)T^2
    
    Many restrictions on its use. Trained on data with MW from 12.24 g/mol
    to 402.4 g/mol, C mass fractions from 61.3% to 95.2%,
    H mass fractions from 3.73% to 15.2%, N mass fractions from 0 to 15.4%,
    O mass fractions from 0 to 18.8%, and S mass fractions from 0 to 29.6%.
    Recommended for organic compounds with low mass fractions of hetero-atoms
    and especially when molar mass exceeds 200 g/mol. This model does not show
    and effects of phase transition but should not be used passed the triple
    point.
    
    Original model is in terms of J/g/K, but it has been translated to J/mol/K.
    
    A1 = 0.013183; A2 = 0.249381; theta = 151.8675; C1 = 0.026526;
    C2 = -0.024942; D1 = 0.000025; D2 = -0.000123.
    
    Examples
    --------
    Calculate the solid heat capacity of Ethanol at 150 K:
    
    >>> f = Lastovka_Solid(similarity_variable=0.19536150996213458,
    ...                    MW=46.06844)
    >>> f
    Functor: Lastovka_Solid(T, P=None) -> Cn.s [J/mol/K]
     similarity_variable: 0.19536
     MW: 46.068 g/mol
    >>> f(150)
    42.196379547807
    
    """
    A1 = 0.013183
    A2 = 0.249381
    theta = 151.8675
    C1 = 0.026526
    C2 = -0.024942
    D1 = 0.000025
    D2 = -0.000123
    sim2 = similarity_variable*similarity_variable
    return MW * (3*(A1*similarity_variable + A2*sim2)*R*(theta/T)**2
                 * exp(theta/T)/(exp(theta/T)-1)**2
                 + (C1*similarity_variable + C2*sim2)*T
                 + (D1*similarity_variable + D2*sim2)*T**2)

 
def Lastovka_Solid_Indefinite_Integral(T, similarity_variable, MW):
    A1 = 0.013183
    A2 = 0.249381
    theta = 151.8675
    C1 = 0.026526
    C2 = -0.024942
    D1 = 0.000025
    D2 = -0.000123
    sim2 = similarity_variable*similarity_variable
    return MW * (T**3*(D1*similarity_variable/3. 
        + D2*sim2/3.) + T*T*(C1*similarity_variable 
        + C2*sim2)/2.
        + 3. * (A1*R*similarity_variable*theta
        + A2*R*sim2*theta)/(exp(theta/T) - 1.))

@functor(var='H.s')
def Lastovka_Solid_Integral(Ta, Tb, similarity_variable, MW):
    return (Lastovka_Solid_Indefinite_Integral(Tb, similarity_variable, MW)
            - Lastovka_Solid_Indefinite_Integral(Ta, similarity_variable, MW))

 
def Lastovka_Solid_Over_T_Indefinite_Integral(T, similarity_variable, MW):
    A1 = 0.013183
    A2 = 0.249381
    theta = 151.8675
    C1 = 0.026526
    C2 = -0.024942
    D1 = 0.000025
    D2 = -0.000123
    sim2 = similarity_variable*similarity_variable
    exp_theta_T = exp(theta/T)
    return MW * (-3.*R*similarity_variable*(A1 + A2*similarity_variable)*log(exp_theta_T - 1.) 
                 + T**2*(D1*similarity_variable + D2*sim2) / 2.
                 + T*(C1*similarity_variable + C2*sim2)
                 + (3.*A1*R*similarity_variable*theta 
                    + 3.*A2*R*sim2*theta)/(T*exp_theta_T - T) 
                 + (3.*A1*R*similarity_variable*theta 
                    + 3.*A2*R*sim2*theta)/T)
 
@functor(var='S.s')
def Lastovka_Solid_Over_T_Integral(Ta, Tb, similarity_variable, MW):
    return (Lastovka_Solid_Over_T_Indefinite_Integral(Tb, similarity_variable, MW)
            - Lastovka_Solid_Over_T_Indefinite_Integral(Ta, similarity_variable, MW))
    
    
@functor(var='Cn.s')
def Perry_151(T, a, b, c, d):
    r"""
    Create a functor of temperature (T; in K) that estimates the solid molar 
    heat capacity (Cn.s; in J/mol/K) of a chemical using the Perry 151 method,
    as described in [9]_.
    
    Parameters
    ----------
    a,b,c,d : float
        Regressed coefficients.
    
    Notes
    -----
    The solid heat capacity is given by:
    
    .. math:: C_n = 4.184 (a + bT + \frac{c}{T^2} + dT^2)
    
    Coefficients are listed in section 2, table 151 of [9]_. Note that the
    original model was in a Calorie basis, but has been translated to Joules.
    
    """
    return (a + b*T + c/T**2 + d*T**2)*calorie

@functor(var='H.s')
def Perry_151_Integral(Ta, Tb, a, b, c, d):
    H1 = (a*Ta + 0.5*b*Ta**2 - d/Ta + c*Ta**3/3.)
    H2 = (a*Tb + 0.5*b*Tb**2 - d/Tb + c*Tb**3/3.)
    return (H2 - H1)*calorie

@functor(var='S.s')
def Perry_151_Over_T_Integral(Ta, Tb, a, b, c, d):
    S1 = a*log(Ta) + b*Ta - d/(2.*Ta**2) + 0.5*c*Ta**2
    S2 = a*log(Tb) + b*Tb - d/(2.*Tb**2) + 0.5*c*Tb**2
    return (S2 - S1)*calorie

Lastovka_Solid_Functors = (Lastovka_Solid, Lastovka_Solid_Integral, Lastovka_Solid_Over_T_Integral)
Perry_151_Functors = (Perry_151, Perry_151_Integral, Perry_151_Over_T_Integral)

# Heat capacity solid methods
LASTOVKA_S = 'Lastovka, Fulem, Becerra and Shaw (2008)'
PERRY151 = "Perry's Table 2-151"

@TDependentHandleBuilder('Cn.s')
def heat_capacity_solid_handle(handle, CAS, similarity_variable, MW):
    Tmin = 0
    Tmax = 2000
    add_model = handle.add_model
    if CAS in Cn_data_PerryI:
        vals = Cn_data_PerryI[CAS]
        if 'c' in vals:
            c = vals['c']
            Tmin = c['Tmin']
            Tmax = c['Tmax']
            data = (c['Const'], c['Lin'], c['Quad'], c['Quadinv'])
            add_model(CnHSModel(*Perry_151_Functors, data), Tmin, Tmax,
                      name=PERRY151)
    if CAS in Cn_data_CRC_standard:
        Cnc = Cn_data_CRC_standard[CAS][3]
        if not np.isnan(Cnc):
            add_model(float(Cnc), 200, 350)
    if similarity_variable and MW:
        data = (similarity_variable, MW)
        add_model(CnHSModel(*Lastovka_Solid_Functors, data), Tmin, Tmax,
                  name=LASTOVKA_S)

heat_capacity_handle = PhaseTHandleBuilder('Cn', heat_capacity_solid_handle, heat_capacity_liquid_handle, heat_capacity_gas_handle)
