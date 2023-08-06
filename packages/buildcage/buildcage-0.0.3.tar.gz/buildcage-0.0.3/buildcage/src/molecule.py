import rdkit.Chem as Chem
import networkx as nx

class molecule():
    def __init__(self,mol):
        self.mol_name = mol
        self.mol = Chem.MolFromMolFile(mol,removeHs=False)
        self.atoms = self.mol.GetAtoms()
        self.atoms_idx = [i.GetIdx() for i in self.atoms]
        self.charge=[atom.GetFormalCharge() for atom in self.atoms]
        self.symbol=[i.GetSymbol() for i in self.atoms]
        self.bonds = self.mol.GetBonds()
        self.bonds_idx = [[bond.GetBeginAtomIdx(),bond.GetEndAtomIdx()] for bond in self.bonds]
        self.G = nx.Graph()
        self.G.add_edges_from(self.bonds_idx)
        self.angles_idx=[]
        self.dihedrals_idx=[]

        for node in self.G.nodes():
            for n1 in self.G.neighbors(node):
                for n2 in self.G.neighbors(n1):
                    if n2 != node:
                        if  n2>node:
                            self.angles_idx.append([node,n1,n2])
                        for n3 in self.G.neighbors(n2):
                            if n3!=n1 and n3>node:
                                self.dihedrals_idx.append([node,n1,n2,n3])
        # The first id is the center atom id. The same definition in lammps.
        # For OPLS, the second id is the center atom id in many Force Field file.?
        # For OPLSAA/AMBER, the 3rd id is the center atom id in many Force Field file.?
        self.impropers_idx = [[i, *list(self.G.neighbors(i))] for i in self.G.nodes() if self.G.degree(i) == 3]

