import matplotlib.pyplot as plt
from matplotlib import rc
rc('text', usetex=True)
plt.style.use('atlas')
import matplotlib.mlab as mlab

dobckg = False
ptcut = 200
nconstcut = 3

jtypes = [
#    '',
    'rc06_','rc08_','rc10_','rc12_']
jlabels = [
#    'R=0.4',
    'R=0.6','R=0.8','R=1.0','R=1.2']
labeldict = dict(zip(jtypes,jlabels))

from numpy import load,arange

bins = arange(0.,350.,5.)

for jt in jtypes:
    signal_jmasses = load('../output/signal_jmass_'+jt+'.npy')
    signal_jpts = load('../output/signal_jpt_'+jt+'.npy')
    signal_nconsts = load('../output/signal_jnconst_'+jt+'.npy')
    if dobckg:
        bckg_jmasses = load('../output/bckg_jmass_'+jt+'.npy')
        bckg_jpts = load('../output/bckg_jpt_'+jt+'.npy')
        bckg_nconsts = load('../output/bckg_jnconst_'+jt+'.npy')
        
    signal_jmasses = signal_jmasses[
        (signal_jpts>ptcut) & 
        (signal_nconsts==nconstcut)
        ]
    if dobckg:
        bckg_jmasses = bckg_jmasses[bckg_jpts>ptcut]

    n,b,patches = plt.hist(signal_jmasses,bins=bins,normed=True,
                           histtype='step',label=labeldict[jt])

    if dobckg:
        plt.hist(bckg_jmasses,bins=bins,normed=True,
                 color=patches[0].get_edgecolor(),
                 histtype='step',linestyle='dashed')

plt.xlabel('$m_{j^{RT}}$ [GeV]')
plt.ylabel('a.u.')
plt.legend()
plt.savefig('../plots/jmasses_pt%d_nconst%s.png'%(ptcut,nconstcut))
plt.yscale('log')
plt.savefig('../plots/jmasses_pt%d_nconst%s_log.png'%(ptcut,nconstcut))
