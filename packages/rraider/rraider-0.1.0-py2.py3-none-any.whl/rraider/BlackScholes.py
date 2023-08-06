# -*- coding: utf-8 -*-
"""
@author: Abhirup Mishra
@Description: The class contains the methods for pricing options using Black-Scholes Formula
"""

from math import sqrt, pi
import scipy as sp
import numpy as np
    
class IncorrectInputs(Exception): pass

class TimeoutException(Exception): pass

class BlackScholes:
    
    #the constructor for the class
    def __init__(self, spot_price, strike_price, time_to_maturity, interest_rate, sigma, dividend_yield=0):
        
        ''' initializtion parameters '''
        self.spot_price = np.asarray(spot_price).astype(float)
        
        #checking if strike price is an array or not
        if(not(hasattr(strike_price, "__len__"))):
            self.strike_price = np.ones(len(spot_price))*strike_price
        else:
            self.strike_price = strike_price

        #checking if time to maturity is an array or not
        if(not(hasattr(time_to_maturity, "__len__"))):
            self.time_to_maturity = np.ones(len(spot_price))*time_to_maturity
        else:
            self.time_to_maturity = time_to_maturity

        #checking if interest rate is an array or not
        if(not(hasattr(interest_rate, "__len__"))):
            self.interest_rate = np.ones(len(spot_price))*interest_rate
        else:
            self.interest_rate = interest_rate

        #checking if volatility is an array or not
        if(not(hasattr(sigma, "__len__"))):
            self.sigma = np.ones(len(spot_price))*sigma
        else:
            self.sigma = sigma
        
        #checking if dividend yield is an array or not
        if(not(hasattr(dividend_yield, "__len__"))):
            self.dividend_yield = np.ones(len(spot_price))*dividend_yield
        else:
            self.dividend_yield = dividend_yield                                         
            
    #private method for erf function    
    def bls_erf_value(self,input_number):
        erf_out = 0.5*(1 + sp.special.erf(input_number/sqrt(2.0)))
        return erf_out
    
    #vectorized method to price call option
    def european_option_price(self):
        
        "Price of the call option"
        "the vectorized method can compute price of multiple options in array"
        numerator = sp.add(sp.log(sp.divide(self.spot_price,self.strike_price)), sp.multiply((self.interest_rate - self.dividend_yield + 0.5*sp.power(self.sigma,2)),self.time_to_maturity))
        d1 = sp.divide(numerator,sp.prod([self.sigma,sp.sqrt(self.time_to_maturity)],axis=0))
        d2 = sp.add(d1, -sp.multiply(self.sigma,sp.sqrt(self.time_to_maturity)))
        
        ecall = sp.product([self.spot_price, self.bls_erf_value(d1), sp.exp(sp.multiply(-self.dividend_yield,self.time_to_maturity))],axis=0) \
                          - sp.product([self.strike_price,self.bls_erf_value(d2),sp.exp(-sp.multiply(self.interest_rate,self.time_to_maturity))],axis=0)
        
        eput = sp.product([-self.spot_price, self.bls_erf_value(-d1), sp.exp(sp.multiply(-self.dividend_yield,self.time_to_maturity))],axis=0) \
                          + sp.product([self.strike_price,self.bls_erf_value(-d2),sp.exp(-sp.multiply(self.interest_rate,self.time_to_maturity))],axis=0)
        return ecall, eput
     
    #delta of the option
    def european_option_delta(self):
        numerator = sp.add(sp.log(sp.divide(self.spot_price,self.strike_price)), sp.multiply((self.interest_rate - self.dividend_yield + 0.5*sp.power(self.sigma,2)),self.time_to_maturity))
        d1 = sp.divide(numerator,sp.prod([self.sigma,sp.sqrt(self.time_to_maturity)],axis=0))
        call_delta = self.bls_erf_value(d1)
        put_delta = call_delta - 1 
        
        return call_delta, put_delta
    
    #gamma of the option (under construction)
    def european_option_gamma(self):
        pass
        
    #vega of the option
    def european_option_vega(self):
        numerator = sp.add(sp.log(sp.divide(self.spot_price,self.strike_price)), sp.multiply((self.interest_rate - self.dividend_yield + 0.5*sp.power(self.sigma,2)),self.time_to_maturity))
        d1 = sp.divide(numerator,sp.prod([self.sigma,sp.sqrt(self.time_to_maturity)],axis=0))
        
        val = sp.multiply(sp.multiply(self.spot_price,sp.exp(-sp.multiply(self.dividend_yield,self.time_to_maturity))),sp.exp(-sp.square(d1)*0.5))
        val = sp.multiply(val,sp.sqrt(self.time_to_maturity))
        vega = (1/sqrt(2*pi))*val
        
        return vega
    
    #theta of the option
    def european_option_theta(self):
        pass
    
    #rho of the option
    def european_option_rho(self):
        pass
    
    '''
    #implied volatility of a european put option
    def european_put_implied_vol(self,option_price):
        
        def __bsm_difference(sigma):
            bsm_difference_estimate = (option_price - self.european_put_value(self.spot_price,self.strike_price,self.time_to_maturity,self.interest_rate,self.sigma,self.dividend_yield))
            return bsm_difference_estimate
        
        initial_sigma = 1.0
        impl_vol = newtons_method(__bsm_difference,initial_sigma)
        return impl_vol
    
    def european_call_implied_vol(self,option_price):
        pass
    '''