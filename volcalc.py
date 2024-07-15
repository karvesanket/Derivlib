# Module for IV, Vol Cone, Historical Vol Calculations
# (c) Sanket Karve, 2024
# 2024

# Term Structure plot
# 3d surface
# vol smile / smirk

# import optionpricer as op
from optionpricer import Binomial_American
from scipy.stats import norm
import numpy as np

class IV_Option:
    """
    Uses Newton Raphson method to find IV of an option by extending the Options module functionality

    Parameters
    ===========
    mktpx = current option price as quoted or mid-price for less liquid options
    S = underlying or stock price
    K = Strike Price
    dte = days to expiry
    r = interest rate --> use non percentage form
    div = dividend yield ---> use non percentage form
    type = call or put option

    """
    def __init__(self, mktpx, S, K, dte, r, div=0, type="put") -> None:
        
        self.mktpx = mktpx
        self.S = S
        self.K = K
        self.dte = dte / 365
        self.r = r / 100
        self.div = div / 100
        self.type = type.lower()

        
    def ImpliedVol_Calc(self):
        errortolerance = 1.0e-2
        vol_est = 0.05        
        d1 = (np.log(self.S/self.K) + (self.r + 0.5 * vol_est ** 2) * self.dte) / (vol_est * np.sqrt(self.dte))
        
        

        while True:
            # optpx = op.Options(self.S,self.K,self.dte,self.r,vol_est, self.div, self.type).bsm_optionprice()
            optpx = Binomial_American(self.S, self.K, self.dte, self.r, vol_est, 200, 0, self.type).CRR_method()
            print(optpx)

            px_diff = self.mktpx - optpx
            print(px_diff)
            vega = self.S * norm.pdf(d1) * np.sqrt(self.dte)

            vol_est += px_diff / vega

            if abs(self.mktpx - optpx < errortolerance):
                break
        return vol_est

if __name__ == "__main__":
    print("Module for volatility related calculations")
