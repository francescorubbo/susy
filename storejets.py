import ROOT as r
from sys import stdout,argv

lepmulti = 1
samp = 'signal'

fnamedict = {'signal':'../data/mc14_13TeV.204534.Herwigpp_UEEE4_CTEQ6L1_Gtt_G1300_T5000_L100.merge.AOD.e3094_a266_a265_r5853.root',
             'bckg':'../data/mc14_13TeV.110401.PowhegPythia_P2012_ttbar_nonallhad.merge.AOD.e2928_s1982_s2008_r5787_r5853.root',
             }

filename = fnamedict[samp]
ff = r.TFile(filename)
tree = ff.Get('tree')
nentries = tree.GetEntries()

jtypes = ['','rc06_','rc08_','rc10_','rc12_']
                                                                         
jmasses = {k:[] for k in jtypes}
jpts = {k:[] for k in jtypes}
jnconsts = {k:[] for k in jtypes}

def getjetvars(thetree,jtype):
    jmass = []
    jpt = []
    jnconst = []

    if 'rc' not in jtype:
        for pt,eta,phi,e in zip(getattr(thetree,jtype+'jets_pt'),
                                getattr(thetree,jtype+'jets_eta'),
                                getattr(thetree,jtype+'jets_phi'),
                                getattr(thetree,jtype+'jets_e')):
            jet = r.TLorentzVector()
            jet.SetPtEtaPhiE(pt,eta,phi,e)
            jmass.append(jet.M())
            jpt.append(pt)
            jnconst.append(1)
        return jmass,jpt,jnconst

    for pt,eta,phi,e,nconst in zip(getattr(thetree,jtype+'jets_pt'),
                                   getattr(thetree,jtype+'jets_eta'),
                                   getattr(thetree,jtype+'jets_phi'),
                                   getattr(thetree,jtype+'jets_e'),
                                   getattr(thetree,jtype+'jets_nconst')):
        jet = r.TLorentzVector()
        jet.SetPtEtaPhiE(pt,eta,phi,e)
        jmass.append(jet.M())
        jpt.append(pt)
        jnconst.append(nconst)
    return jmass,jpt,jnconst
    
for jentry in xrange(nentries):
    tree.GetEntry(jentry)
    
    if not jentry%1000:
        stdout.write('\r%d'%jentry)
        stdout.flush()

    if (tree.electrons_n+tree.muons_n)!=lepmulti: continue
    for jt in jtypes:
        jmass,jpt,jnconst = getjetvars(tree,jt)
        jmasses[jt] += jmass
        jpts[jt] += jpt
        jnconsts[jt] += jnconst

from numpy import save
for jt in jtypes:
    save('../output/'+samp+'_jmass_'+jt,jmasses[jt])
    save('../output/'+samp+'_jpt_'+jt,jpts[jt])
    save('../output/'+samp+'_jnconst_'+jt,jnconsts[jt])
