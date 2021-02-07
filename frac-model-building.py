import pandas as pd
import statsmodels.formula.api as smf
import numpy as np

fracturas = pd.read_csv("fracturas-06-02-21.csv")
np.random.seed(27)

desord =  fracturas.sample(frac=1)
desord["arena_total_tn"] = desord["arena_bombeada_nacional_tn"] + desord["arena_bombeada_importada_tn"]
desord.loc[desord.agua_inyectada_m3>200000]=np.nan

training = desord.iloc[:1819]
test = desord.iloc[1819:]


def getPoissonModel(gdata):
    
    formula = "agua_inyectada_m3 ~ cantidad_fracturas + C(tipo_reservorio)" #  + arena_total_tn + C(tipo_reservorio) + C(tipo_reservorio)
    model = smf.poisson(formula, data=gdata)
    
    
    return model


modelo =  getPoissonModel(training)
results = modelo.fit()

results.save("fracmod.pickle")

