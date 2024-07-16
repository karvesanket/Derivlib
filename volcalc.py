# Module for IV, Vol Cone, Historical Vol Calculations
# (c) Sanket Karve, 2024
# 2024

# Term Structure plot
# 3d surface
# vol smile / smirk

from scipy.stats import norm
import math

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
    errtol = error tolerace. Default set to 1e-5
    div = dividend yield ---> use non percentage form
    type = call or put option. Default set to call

    """
    def __init__(self, mktpx, S, K, dte, r, errtol=1e-5, div=0, type="call") -> None:
        
        self.mktpx = mktpx
        self.S = S
        self.K = K
        self.dte = dte / 365
        self.r = r
        self.errtol = errtol
        self.div = div / 100
        self.type = type.lower()

    def IV_NewtonRaph(self, iter=100):
        """
        Parameters
        ============
        iter: Number of iterations to calculate IV. Default set to 100
        
        Returns
        ==========
        Implied Vol of an Option Contract

        """
        if self.type == "call":
            cp = 1
        else:
            cp = -1
        imp_vol = math.sqrt(2 * math.pi / self.dte) * self.mktpx / self.S
        # print("Initial volatility:", imp_vol) Commented out as it's not required unless needed to be seen

        for i in range(iter):
            d1 = (math.log(self.S / self.K) + (self.r + 0.5 * imp_vol ** 2) * self.dte) / (imp_vol * math.sqrt(self.dte))
            d2 = d1 - imp_vol * math.sqrt(self.dte)
            vega = self.S * norm.pdf(d1) * math.sqrt(self.dte)
            price0 = cp * self.S * norm.cdf(cp * d1) - cp * self.K * math.exp(-self.r * self.dte) * norm.cdf(cp * d2)
            imp_vol = imp_vol - (price0 - self.mktpx) / vega

            if abs(price0 - self.mktpx) < self.errtol:
                break

        return round(imp_vol, 4) * 100

if __name__ == "__main__":
    implied_volatility = IV_Option(1.25,18.05,15,159,.05198,type="put").IV_NewtonRaph()
    print("Implied volatility:", implied_volatility)
