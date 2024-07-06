import optionpricer as op

price = op.Binomial_American(17.31, 17.5, 167, 0.0498, 59.19, 5000, 0, "put").CRR_method()
price_bsm = op.Options(17.31, 17.5, 167, 0.0498, 59.19, 0, "put").bsm_optionprice()

px_greekcheck = op.Binomial_American(17.31, 17.5, 167, 0.0498, 59.19, 5000, 0, "put").bsm_delta()
print(price, price_bsm, px_greekcheck)