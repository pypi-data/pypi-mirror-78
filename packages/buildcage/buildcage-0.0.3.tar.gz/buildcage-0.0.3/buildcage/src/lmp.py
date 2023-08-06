import rdkit.Chem as Chem
import pickle
from collections import Counter
import re
import copy
import os
import numpy as np
import subprocess
from .stkcage import *
from .molecule import molecule
from .bash import BashCall
from .boss import GetParmsFromBOSS

def add_s(i):
    if len(i)==1:
        return i+" "
    else:
        return i

def OPLSAA_parm(strs,parm,improper=False):
    if improper==False:
        strs1=[add_s(i) for i in strs]
        s=['-'.join(strs1).strip(),'-'.join(strs1[::-1]).strip()]
        strs2 =copy.deepcopy(strs1)
        strs2[0]=strs2[0][0]+".?"
        strs2[-1] = strs2[-1][0] + ".?"
        ss = ['-'.join(strs2).strip(), '-'.join(strs2[::-1]).strip()]
        len_type={2:parm[1],3:parm[2],4:parm[3]}
        for i in s:
            if i in len_type[len(strs)]:
                return len_type[len(strs)][i]
            else:
                for i in ss:
                    for j in len_type[len(strs)]:
                        if len(re.findall(i,j)) ==1:
                            return len_type[len(strs)][j]
    elif improper==True:
        if strs[0]=="CA":
            return "1.100  0.0"
        elif strs[0][0]=="N":
            return "1.000  0.0"
        elif strs[0]=="CM" and "O" not in [strs[1][0],strs[2][0],strs[3][0]]:
            return "15.00  0.0"
        elif strs[0][0]=="C":
            return "10.50  0.0"

def useless_atom_set(f_groups):
    gs=list(f_groups)
    uas=set()
    for i in gs:
        uas=uas|(set(i.get_atom_ids())-set(i.get_core_atom_ids()))
    return uas

symb2mass = {
        'H': 1.008,
        'F': 18.998403163,
        'Cl': 35.45,
        'Br': 79.904,
        'I': 126.90447,
        'O': 15.999,
        'S': 32.06,
        'N': 14.007,
        'P': 30.973761998,
        'C': 12.011,
        'Si': 28.085,
        'Na': 22.98976928,
        'SOD': 22.98976928,
        'K': 39.0983,
        'Mg': 24.305,
        'Ca': 40.078,
        'Mn': 54.938044,
        'Fe': 55.845,
        'Co': 58.933194,
        'Ni': 58.6934,
        'Cu': 63.546,
        'Zn': 65.38, }

def get_lmp(name,block1,block2,cageobj,BOSSdir,BABELexe,LMPexe,MDArgs,Pairflag):
    # b1=block("NC1CCCCC1N",[group["-NH2"]()]) #CHDNH2
    # b2=block("O=Cc1cc(C=O)cc(C=O)c1",[group["-CHO"]()])  # BTMCHO
    # cage1=build_framework(topo_dict["4+6"]((b1,b2)),opt=True)
    b1=copy.deepcopy(block1)
    b2=copy.deepcopy(block2)
    cage1=copy.deepcopy(cageobj)
    #write cage mol file
    print("# 1. Create "+name+" mdp file")
    cage1.write(name+".mol")
    b2._placer_ids=b2._placer_ids[:2]
    b2._functional_groups=b2._functional_groups[:2]   # 这里改变内定的值, 已经无法再用于build了, 所以build cage需要靠前.
    fra=build_framework(stk.polymer.Linear((b1,b2),"AB",1),MMFFopt=True)
    # write 2 linker made fragments mol file
    print("# 2. Create fragment mdp file")
    fra.write(name+"_linker.mol")
    # get paramenters from fra.mol file
    print("# 3. Create fragment parameters file using BOSS")
    GetParmsFromBOSS(BOSSdir,BABELexe,name+"_linker")
    parameters = pickle.load(open(name + "_linker_parm", "rb"))
    # fra refine mol and rdkit mol
    fra=stk.BuildingBlock.init_from_molecule(fra,functional_groups=[group["-NH2"](),group["-CHO"]()])
    framol=fra.to_rdkit_mol()
    print("# 4. Begin cage & fragment match!")
    # fragment ids without replaced atoms
    smarts_id=[i for i in range(len(framol.GetAtoms())) if i not in useless_atom_set(fra.get_functional_groups())]
    smarts_id=tuple(smarts_id)
    # fragment without replaced atoms
    fra_smarts=Chem.MolFragmentToSmarts(framol,smarts_id)
    # build map from fragments atoms to cage atoms
    patt=Chem.MolFromSmarts(fra_smarts)
    if framol.HasSubstructMatch(patt):
        fraid=framol.GetSubstructMatch(patt)
    cage_mol=cage1.to_rdkit_mol()
    type_map_dict=dict()
    if cage_mol.HasSubstructMatch(patt):
        atomids = cage_mol.GetSubstructMatches(patt,maxMatches=100000000)
        for i in range(len(fraid)):
            if fraid[i] not in fra._placer_ids:
                for j in atomids:
                    if j[i] not in type_map_dict:
                        type_map_dict[j[i]]=[fraid[i]]
                    else:
                        type_map_dict[j[i]]+=[fraid[i]]
    # atom parameters projection
    type_dict=dict()
    pair_dict=dict()
    charge_dict=dict()
    for i in type_map_dict:
        if i not in type_dict:
            type_dict[i] = []
            pair_dict[i] = []
            charge_dict[i] = []
        for j in type_map_dict[i]:
            type_dict[i]+=parameters[0][j][:1]
            pair_dict[i] += [" ".join(parameters[0][j][2:])]
            charge_dict[i] += [float(parameters[0][j][1])]
        type_dict[i]=Counter(type_dict[i]).most_common()[0][0]
        pair_dict[i]=Counter(pair_dict[i]).most_common()[0][0]
        charge_dict[i]=sum(charge_dict[i])/len(charge_dict[i])
    total_q=sum([charge_dict[i] for i in charge_dict])/len(charge_dict)
    for i in charge_dict:charge_dict[i]-=total_q
    cage_mol=molecule(name+".mol")
    atoms=len(cage_mol.atoms_idx)
    bonds=len(cage_mol.bonds_idx)
    angles=len(cage_mol.angles_idx)
    dihedrals=len(cage_mol.dihedrals_idx)
    impropers=len(cage_mol.impropers_idx)
    # write lammps input files
    print("# 5. Write lammps input files")
    f=open(name+".data","w")
    print("LAMMPS "+name+" CAGE",file=f)
    print(atoms,"atoms\n",bonds,"bonds\n",angles,"angles",file=f)
    print(dihedrals,"dihedrals\n",impropers,"impropers\n",file=f)
    print(atoms, "atom types\n", bonds, "bond types\n", angles, "angle types",file=f)
    print(dihedrals, "dihedral types\n",impropers, "improper types\n",file=f)
    print("-100 100  xlo xhi\n-100 100 ylo yhi\n-100 100 zlo zhi",file=f)
    print("\nMasses\n",file=f)
    for i,atom in enumerate(cage_mol.mol.GetAtoms()):
        print(i+1,symb2mass[atom.GetSymbol()],"# "+type_dict[i],file=f)
    print("\nAtoms\n",file=f)
    position=cage_mol.mol.GetConformer().GetAtomPosition
    for i in range(atoms):
        print(i+1,1,i+1,charge_dict[i],position(i)[0],position(i)[1],position(i)[2],file=f)
    if Pairflag:
        print("\nPair Coeffs\n",file=f)
        for i in range(atoms):
            print(i + 1, pair_dict[i],file=f)
    print("\nBond Coeffs\n",file=f)
    for id,i in enumerate(cage_mol.bonds_idx):
        print(id+1, *OPLSAA_parm([type_dict[i[0]], type_dict[i[1]]], parameters)[::-1],"#", type_dict[i[0]]+"-"+type_dict[i[1]],file=f)
    print("\nAngle Coeffs\n",file=f)
    for id,i in enumerate(cage_mol.angles_idx):
        print(id+1, *OPLSAA_parm([type_dict[i[0]], type_dict[i[1]], type_dict[i[2]]], parameters)[::-1],
              "#", type_dict[i[0]]+"-"+type_dict[i[1]]+"-"+type_dict[i[2]],file=f)
    print("\nDihedral Coeffs\n",file=f)
    for id,i in enumerate(cage_mol.dihedrals_idx):
        print(id+1, OPLSAA_parm([type_dict[i[0]], type_dict[i[1]], type_dict[i[2]],type_dict[i[3]]], parameters),
              "#", type_dict[i[0]]+"-"+type_dict[i[1]]+"-"+type_dict[i[2]]+"-"+type_dict[i[3]],file=f)
    print("\nImproper Coeffs\n",file=f)
    for id,i in enumerate(cage_mol.impropers_idx):
        print(id+1, OPLSAA_parm([type_dict[i[0]], type_dict[i[1]], type_dict[i[2]],type_dict[i[3]]], parameters,improper=True),
              "#", type_dict[i[0]]+"-"+type_dict[i[1]]+"-"+type_dict[i[2]]+"-"+type_dict[i[3]],file=f)
    print("\nBonds\n",file=f)
    for id,i in enumerate(cage_mol.bonds_idx):
        print(id+1,id+1,i[0]+1,i[1]+1,file=f)
    print("\nAngles\n",file=f)
    for id,i in enumerate(cage_mol.angles_idx):
        print(id+1,id+1,i[0]+1,i[1]+1,i[2]+1,file=f)
    print("\nDihedrals\n",file=f)
    for id,i in enumerate(cage_mol.dihedrals_idx):
        print(id+1,id+1,i[0]+1,i[1]+1,i[2]+1,i[3]+1,file=f)
    print("\nImpropers\n",file=f)
    for id,i in enumerate(cage_mol.impropers_idx):
        print(id+1,id+1,i[0]+1,i[1]+1,i[2]+1,i[3]+1,file=f)
    f.close()
    f = open(name+".in", 'w')
    print("units real\nboundary f f f\natom_style full\nbond_style harmonic\nangle_style harmonic\ndihedral_style opls\n"
          "improper_style harmonic",file=f)
    if Pairflag:
        print("pair_style lj/cut/coul/cut 14.0 14.0\nspecial_bonds lj/coul 0.0 0.0 0.5\npair_modify mix geometric",file=f)
    print('read_data "'+name+'.data"', file=f)
    print('neighbor 6 bin\nneigh_modify every 1 delay 0 check yes\nthermo 100', file=f)
    print(MDArgs,file=f)
    print("#dump 1 all movie 1 movie.mp4 type type size 640 480 zoom 10\ndump 2 all custom 1 dump.lammpstrj id mass x y z", file=f)
    print('minimize 1.0e-5 1.0e-7 10000 100000\ntimestep 1', file=f)
    f.close()
    BashCall("rm {0}_linker_parm {0}_linker.mol".format(name))
    print("# 6. Run lammps!")
    BashCall(LMPexe+" < "+name+".in")
    with open("dump.lammpstrj",'r') as f:
        coors=f.readlines()[-atoms:]
    coor_mat=[[0. for j in range(atoms)]for i in range(3)]
    for i in coors:
        coor_mat[0][int(i.split()[0])-1]=float(i.split()[2])
        coor_mat[1][int(i.split()[0]) - 1] = float(i.split()[3])
        coor_mat[2][int(i.split()[0]) - 1] = float(i.split()[4])
    cage1._position_matrix=np.array(coor_mat)
    print("# 7. Write optimized cage mdp file!!!!\nEND!!!")
    cage1.write(name+"_opt.mol")
    BashCall("rm -f log.lammps {0}.data {0}.in dump.lammpstrj log".format(name))
    BashCall("$BABELexe {0}.mol -O {0}.init.mol 2>>log".format(name))
    BashCall("$BABELexe {0}_opt.mol -O {0}.opt.mol 2>>log".format(name))
    BashCall("rm -f {0}.mol {0}_opt.mol log".format(name))
