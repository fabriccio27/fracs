# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 17:43:43 2021

@author: Fabricio
"""

import streamlit as st
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

import patsy

import statsmodels.formula.api as smf

st.header("Water requirement estimate for fracking operations in Argentina")
         
st.text("This simple model gives you an estimate of how much water the frac-op should require. \nBlue markers are historical data. Green marker is model prediction")

# obtener features de usuario

def userInputFeatures():
    
    n_fracs = st.sidebar.slider("Nro de fracturas", 1,70,1)
    t_reserv = st.sidebar.selectbox(
        "Choose a type of reservoir",
        ["NO CONVENCIONAL", "CONVENCIONAL"])
    data = {
        'cantidad_fracturas': n_fracs,
        'tipo_reservorio': t_reserv
        }
    features = pd.DataFrame(data, index=[0])
    return features

udf = userInputFeatures()

st.subheader("Your inputs")
st.write(udf)

fracturas = pd.read_csv("fracturas-06-02-21.csv")
fracturas.loc[fracturas.agua_inyectada_m3>200000] = np.nan

# cargar modelo


from statsmodels.discrete.discrete_model import GeneralizedPoissonResults as PoissonResults

impresults= PoissonResults.load('fracmod.pickle')
pred = impresults.predict(udf)
pred_valor = pred.tolist()[0]

# string_valor = ("%.2f"%pred_valor) esto funciona

string_valor = "{:.2f}".format(pred_valor)


st.sidebar.subheader("Estimated Water Requirement [m3]")

st.sidebar.write(string_valor)

# graficar

#quitar valores extremos para tener un mejor grafico

plt.scatter(fracturas.cantidad_fracturas, fracturas.agua_inyectada_m3, alpha=0.4, s=10 )
plt.scatter(udf.cantidad_fracturas, pred_valor, c='green' , marker="x",s=200)
plt.xlabel("Number of fractures"), plt.ylabel("Injected water [m3]")
st.pyplot(plt)

