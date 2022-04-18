#!/usr/bin/env python3

import ROOT
import argparse
from array import array
from tqdm import tqdm

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="+", help="input flattrees to boost to the center-of-momentum frame")
    args = parser.parse_args()

    for path in args.input:
        tf_in = ROOT.TFile.Open(path, "READ")
        tf_out = ROOT.TFile.Open(path.replace(".root", "_boosted.root"), "READ")
        tt_name = tfile_in.GetListOfKeys()[0].GetName()
        tt_in = tf_in.Get(tt_name)
        NumFinalState = array('i', [0])
        Weight = array('f', [0.])
        E_Beam = array('f', [0.])
        Px_Beam = array('f', [0.])
        Py_Beam = array('f', [0.])
        Pz_Beam = array('f', [0.])
        E_FinalState = array('f', n_fs*[0.])
        Px_FinalState = array('f', n_fs*[0.])
        Py_FinalState = array('f', n_fs*[0.])
        Pz_FinalState = array('f', n_fs*[0.])
        M_FinalState = array('f', [0.])
        tt_out.Branch("NumFinalState", NumFinalState, "NumFinalState/I")
        tt_out.Branch("Weight", Weight, "Weight/F")
        tt_out.Branch("E_Beam", E_Beam, "E_Beam/F")
        tt_out.Branch("Px_Beam", Px_Beam, "Px_Beam/F")
        tt_out.Branch("Py_Beam", Py_Beam, "Py_Beam/F")
        tt_out.Branch("Pz_Beam", Pz_Beam, "Pz_Beam/F")
        tt_out.Branch("E_FinalState", E_FinalState, "E_FinalState[NumFinalState]/F")
        tt_out.Branch("Px_FinalState", Px_FinalState, "Px_FinalState[NumFinalState]/F")
        tt_out.Branch("Py_FinalState", Py_FinalState, "Py_FinalState[NumFinalState]/F")
        tt_out.Branch("Pz_FinalState", Pz_FinalState, "Pz_FinalState[NumFinalState]/F")
        tt_out.Branch("M_FinalState", M_FinalState, "M_FinalState/F")
        for event in tqdm(tt_in, total=n_events, dynamic_ncols=True, unit='event'):
            beam_lab = ROOT.TLorentzVector(event.Px_Beam, event.Py_Beam, event.Pz_Beam, event.E_Beam)
            recoil_lab = ROOT.TLorentzVector(event.Px_FinalState[0], event.Py_FinalState[0], event.Pz_FinalState[0], event.E_FinalState[0])
            p1_lab = ROOT.TLorentzVector(event.Px_FinalState[1], event.Py_FinalState[1], event.Pz_FinalState[1], event.E_FinalState[1])
            p2_lab = ROOT.TLorentzVector(event.Px_FinalState[2], event.Py_FinalState[2], event.Pz_FinalState[2], event.E_FinalState[2])
            com_boost = ROOT.TLorentzRotation((recoil_lab + p1_lab + p2_lab).BoostVector())
            beam = com_boost * beam_lab
            recoil = com_boost * recoil_lab
            p1 = com_boost * p1_lab
            p2 = com_boost * p2_lab
            NumFinalState[0] = 3
            Weight[0] = event.Weight
            E_Beam[0] = beam.E()
            Px_Beam[0] = beam.Px()
            Py_Beam[0] = beam.Py()
            Pz_Beam[0] = beam.Pz()
            E_FinalState[0] = recoil.E()
            Px_FinalState[0] = recoil.Px()
            Py_FinalState[0] = recoil.Py()
            Pz_FinalState[0] = recoil.Pz()
            E_FinalState[1] = p1.E()
            Px_FinalState[1] = p1.Px()
            Py_FinalState[1] = p1.Py()
            Pz_FinalState[1] = p1.Pz()
            E_FinalState[2] = p2.E()
            Px_FinalState[2] = p2.Px()
            Py_FinalState[2] = p2.Py()
            Pz_FinalState[2] = p2.Pz()
            tt_out.Fill()
        tt_out.Write()
        tt_out.Close()
        tt_in.Close()

if __name__ == "__main__":
    main()
