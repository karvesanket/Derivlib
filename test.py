import dataingest as dg
import pandas as pd
import optionpricer as op

opt = pd.DataFrame()

opt = dg.Getdata("SPY",type="option",api="yahoo").ProcessOptData(opex="Yes")
opt.to_csv("chk.csv")

op.Options()