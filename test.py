import dataingest as dg
import pandas as pd

opt = pd.DataFrame()

opt = dg.Getdata("SPY",type="option",api="yahoo").ProcessOptData()
opt.to_csv("chk.csv")