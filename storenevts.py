import ROOT as r
from sys import stdout,argv

lepmulti = 1
#metcut = 150.
#mtwcut = 140.
samp = 'signal'

boostedWs = range(5-lepmulti)
boostedTops = range(5-lepmulti)
resolved = range(4,13-lepmulti*2)

fnamedict = {'signal':'../data/mc14_13TeV.204534.Herwigpp_UEEE4_CTEQ6L1_Gtt_G1300_T5000_L100.merge.AOD.e3094_a266_a265_r5853.root',
             'bckg':'../data/mc14_13TeV.110401.PowhegPythia_P2012_ttbar_nonallhad.merge.AOD.e2928_s1982_s2008_r5787_r5853.root',
             }

filename = fnamedict[samp]
ff = r.TFile(filename)
tree = ff.Get('tree')
nentries = tree.GetEntries()

selections = ['%dtops_%dWs_%dresolved'%(t,w,r) for t in boostedTops 
              for w in boostedWs for r in resolved]

nevts = {k:0 for k in selections} 
def jetselection(ptcut,njetscut,type):
    jetpts = getattr(tree,type+'jets_pt')
    return len([1 for jpt in jetpts
                if jpt>ptcut])>=njetscut
    
for jentry in xrange(nentries):
    tree.GetEntry(jentry)
    
    if not jentry%1000:
        stdout.write('\r%d'%jentry)
        stdout.flush()

    if (tree.electrons_n+tree.muons_n)!=lepmulti: continue
#    if (tree.metcst<metcut): continue
#    if (tree.mt<mtwcut): continue

    for nr in resolved:
        if not jetselection(25.,nr,''): break
        for nw in boostedWs:
            if not jetselection(200.,nw,'rc08_'): break
            for nt in boostedTops:
                if not jetselection(200.,nt,'rc12_'): break
                nevts['%dtops_%dWs_%dresolved'%(nt,nw,nr)]+=1
                
import json
with open('../output/'+samp+'_nevts.json','w') as outfile:
    json.dump(nevts,outfile)

