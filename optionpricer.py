# Module containing various option pricing, greeks and plotting functions
# (c) Sanket Karve, 2024
# 2024

import math
from scipy.stats import norm
import numpy as np

# Think of adding Gamma curve, stock gamma net positioning for an expiry & all expiries, notional price O/S per strike for pin / witching trading
# Long term think of how this info can be entered into a database, updated on realtime and then pulled from there and used in python for undertaking calcs

# Graphs - Cdf for delta hedging, daily vol / std deviation changes for a stock by day of the week and by month chart, 3d IV function chart for a stock / options

# Features to be added to this module: Monte Carlo, Lambda, Charm

class Options:
    def __init__(self, S, K, dte, r, vol, div=0, type="call") -> None:
        """
        Parameters
        ============

        S: Stock / Underlying Price
        K: Strike Price
        dte: Days to Expiry (in days) (Create a days between dates module - will help when ingesting data from APIs)
        r: Risk-free rate --> 1yr or interpolated to time horizon
        vol: annualized volatility
        div: Dividend Yield -> Optional Value, set to 0 by default
        type: call or put (default is call)
        style: option exercise style whether european, american, asian etc

        """
        self.S = S
        self.K = K
        self.dte = dte / 365
        self.r = r / 100
        self.vol = vol / 100
        self.div = div / 100
        self.type = type.lower()

    # Below are Helper functions to help calculate the BSM option values

    def __d1f(self):
        d1 = (math.log(self.S / self.K) + (self.r + 0.5 * self.vol**2) * self.dte) / (
            (self.vol * math.sqrt(self.dte))
        )
        return d1

    def __d2f(self):
        d2 = self.__d1f() - self.vol * math.sqrt(self.dte)
        return d2

    # End of helper functions

    def bsm_optionprice(self):
        """
        Returns
        =======

        Value of the call or put option as specified by user

        """
        Nd1 = norm.cdf(self.__d1f())
        Nd2 = norm.cdf(self.__d2f())

        if self.type == "call":
            call_px = (
                math.exp(-self.div * self.dte) * self.S * Nd1
                - math.exp((-self.r) * self.dte) * self.K * Nd2
            )
            return round(call_px, 2)
        else:
            put_px = (
                (
                    math.exp(-self.div * self.dte) * self.S * Nd1
                    - math.exp((-self.r) * self.dte) * self.K * Nd2
                )
                - self.S
                + math.exp((-self.r) * self.dte) * self.K
            )
            return round(put_px, 2)

    # Calculation of First Order Option Greeks below

    def bsm_delta(self):
        """
        Returns:
        ========
        Delta value of the call option using BSM

        """
        if self.type == "call":

            call_delta = math.exp(-self.div * self.dte) * norm.cdf(self.__d1f())
            return round(call_delta, 2)
        else:
            put_delta = math.exp(-self.div * self.dte) * (norm.cdf(self.__d1f()) - 1)
            return round(put_delta, 2)

    def bsm_rho(self):
        """
        Returns:
        ========
        Rho for the call or put option

        """
        if self.type == "call":
            call_rho = (
                self.K
                / 100
                * self.dte
                * math.exp(-self.r * self.dte)
                * norm.cdf(self.__d2f())
            )
            return round(call_rho, 4)
        else:
            put_rho = (
                (-self.K / 100)
                * self.dte
                * math.exp(-self.r * self.dte)
                * norm.cdf(-self.__d2f())
            )
            return round(put_rho, 4)

    def bsm_gamma(self):
        """
        Returns:
        ========
        Gamma for the option using BSM model

        """
        N_d1 = norm.pdf(self.__d1f())

        gamma = N_d1 * (
            (math.exp(-self.div * self.dte) / (self.S * self.vol * math.sqrt(self.dte)))
        )
        return round(gamma, 4)

    def bsm_vega(self):
        """
        Returns:
        ========
        Vega for the option using BSM model

        """
        N_d1 = norm.pdf(self.__d1f())

        vega = (
            (self.S / 100) * math.exp(-self.div * self.dte) * math.sqrt(self.dte) * N_d1
        )
        return round(vega, 4)

    def bsm_theta(self):
        """
        Returns:
        ========
        Theta for the option using BSM model

        """
        N_d1 = norm.pdf(self.__d1f())

        # Note: 365 used for nper
        nper = 365

        if self.type == "call":
            theta = (
                (
                    -(
                        self.S
                        * self.vol
                        * math.exp(-self.div * self.dte)
                        * N_d1
                        / (2 * math.sqrt(self.dte))
                    )
                )
                - self.r * self.K * math.exp(-self.r * self.dte) * norm.cdf(self.__d2f())
                + self.div
                * self.S
                * math.exp(-self.div * self.dte * norm.cdf(self.__d1f()))
            ) / nper
            return round(theta, 4)

        else:  # for put option
            theta = (
                (
                    -(
                        self.S
                        * self.vol
                        * math.exp(-self.div * self.dte)
                        * N_d1
                        / (2 * math.sqrt(self.dte))
                    )
                )
                + self.r * self.K * math.exp(-self.r * self.dte) * norm.cdf(-self.__d2f())
                - self.div
                * self.S
                * math.exp(-self.div * self.dte * norm.cdf(-self.__d1f()))
            ) / nper
            return round(theta, 4)

    def bsm_vanna(self):
        '''
        Calculate Vanna for the option. Rate of Change of Delta per 1% Change in Vol. Output needs to be multiplied by 100 similar to other greeks
        '''
        vanna = 0.01 * (-math.exp(-self.div * self.dte)) * self.__d2f() / self.vol * norm.pdf(self.__d1f())
        return round(vanna, 4)


class Binomial_American(Options):
    def __init__(self, S, K, dte, r, vol, N, div=0, type="call") -> None:
        """
        S: Stock / Underlying Price
        K: Strike Price
        dte: Days to Expiry (in days)
        r: Risk-free rate --> 1yr or interpolated to time horizon
        vol: annualized volatility
        div: Dividend Yield -> Optional Value, set to 0 by default
        type: call or put (default is call)
        N = Number of timesteps for the binomial process (New Param)

        """
        super(Binomial_American, self).__init__(S, K, dte, r, vol, div, type) #Inheriting attributes from parent class
        self.N = N

    def CRR_method(self):
    # Calculating constants and Up / Down move(s)
        dt = self.dte / self.N
        u = np.exp(self.vol * np.sqrt(dt))
        d = 1 / u
        q = (np.exp(self.r * dt) - d) / (u-d)
        disc = np.exp(-self.r * dt)
    
    # Asset prices at maturity - Time step N
        S = np.zeros(self.N + 1)
        S[0] = self.S * d ** self.N
        for j in range(1, self.N + 1):
            S[j] = S[j - 1] * u / d
    
    # initialise option values at maturity
        C = np.zeros(self.N + 1)
        for j in range(0, self.N + 1):
            if self.type == 'call':
                C[j] = max(0, S[j] - self.K)
            else:
                C[j] = max(0, self.K - S[j])
        
    # step backwards through tree
        for i in np.arange(self.N, 0, -1):
            for j in range(0, i):
                C[j] = disc * (q * C[j + 1] + (1 - q) * C[j])
    
        return round(C[0], 2)
    
if __name__ == "__main__":
    # print("Module for option pricing and calculation of greeks")
    px = Options(17.31,17.5,167,4.919,59.2,0,"put").bsm_vanna()
    print(px)
