from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'axes.spines.top':False, 'axes.spines.right':False,
                     'figure.dpi':150, 'axes.titleweight':'bold'})
(ROOT/'figures').mkdir(exist_ok=True)

import json
import numpy as np
from scipy.optimize import minimize
rng=np.random.default_rng(5262)
n=8
a=rng.normal(size=(n,n))
cov=(a@a.T)/n*0.025+np.eye(n)*0.008
mu=np.linspace(0.035,0.16,n)
weights=[]
for risk_aversion in np.geomspace(0.3,100,50):
    result=minimize(lambda w:risk_aversion*(w@cov@w)-mu@w,
        np.full(n,1/n),method='SLSQP',bounds=[(0,1)]*n,
        constraints=[{'type':'eq','fun':lambda w:w.sum()-1}],
        options={'ftol':1e-11,'maxiter':1000})
    if not result.success: raise RuntimeError(result.message)
    assert abs(result.x.sum()-1)<1e-7 and result.x.min()>-1e-7
    weights.append(result.x)
w=np.array(weights)
rand=rng.dirichlet(np.ones(n),size=1500)
vol=lambda z:np.sqrt(np.einsum('ij,jk,ik->i',z,cov,z))
fig,ax=plt.subplots(figsize=(7.5,4.5),layout='constrained')
ax.scatter(vol(rand),rand@mu,s=7,alpha=.2,color='#718eaa',label='Random feasible portfolios')
ax.plot(vol(w),w@mu,color='#157a83',lw=2.5,label='Optimized risk/return tradeoff')
ax.set(xlabel='Synthetic annual volatility',ylabel='Synthetic expected annual return',title='Long-only mean-variance illustration')
ax.legend()
fig.savefig(ROOT/'figures/synthetic-frontier.svg')
(ROOT/'figures/synthetic-results.json').write_text(json.dumps({'seed':5262,'assets':n,'solutions':len(w),'maximum_budget_error':float(np.abs(w.sum(axis=1)-1).max()),'minimum_weight':float(w.min())},indent=2))
print('Solved',len(w),'synthetic allocations; all budget/bound constraints passed.')
