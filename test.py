import optionpricer as op
import dataingest as di
import functionutil as fu
import volcalc as vc

# price = op.Binomial_American(17.31, 17.5, 167, 0.0498, 59.19, 200, 0, "put").CRR_method()
# price_bsm = op.Options(17.31, 17.5, 167, 0.0498, 59.19, 0, "put").bsm_optionprice()
# px_greekcheck = op.Options(17.31, 17.5, 160, 0.0498, 59.19, 0, "put").bsm_vega()

# print(price, price_bsm, px_greekcheck)

iv_test = vc.IV_Option(0.85,18.99,15,160,5.198,0,"put").ImpliedVol_Calc()
print(iv_test)

# stock_px = di.Getdata("VSCO", "6mo","1d",True,type="stock",api="yahoo").ProcessStockData(delzero=True)
# stock_px = fu.stockret(stock_px,rettype="daily")
