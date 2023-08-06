# This file is used to symplify the definitions in stk for cages use.
import os
import stk
from rdkit.Chem import AllChem
import numpy as np

class block(stk.BuildingBlock):
    def __init__(self,*args,MMFFopt=False):
        '''
# [*][O][H] default bonders 1 deleters 2
    "-OH":stk.AlcoholFactory,
    # [*][C](=[O])[H] default bonders 1 deleters 2
    "-CHO":stk.AldehydeFactory,
    # [*][C](=[O])[N]([H])[H] default bonders 1 deleters 3,4,5
    "-CONH2":stk.AmideFactory,
    # [*][B]([O][H])[O][H] default bonders 1 deleters 2,3,4,5
    "-BOHOH":stk.BoronicAcidFactory,
    # [*][Br] default bonders 0 deleters 1
    "-Br":stk.BromoFactory,
    # [*][C](=[O])[O][H] default bonders 1 deleters 3,4
    "-COOH":stk.CarboxylicAcidFactory,
    # [Br][#6]~[#6][Br]  default bonders 1,2 deleters 0,3
    "-CBrCBr-":stk.DibromoFactory,
    # [F][#6]~[#6][F]  default bonders 1,2 deleters 0,3
    "-CFCF-":stk.Difluoro,
    # [H][O][#6]~[#6][O][H]  default bonders 2,3 deleters 0,1,4,5
    "-COHCOH-":stk.DiolFactory,
    # [*][F] default bonders 0 deleters 1
    "-F":stk.FluoroFactory,
    # [*][I] default bonders 0 deleters 1
    "-I":stk.IodoFactory,
    # [*][N]([H])[H] default bonders 1 deleters 2,3
    "-NH2":stk.PrimaryAminoFactory,
    # [N]([H])([H])[#6]~[#6]~[#6R1]
    "-RCCCNH2":stk.RingAmineFactory,
    # [H][N]([#6])[#6] default bonders 1 deleters 0
    ">NH":stk.SecondaryAminoFactory,
    # "custom" smarts='[Br][C]',bonders=(1, ), deleters=(0, )
    "custom":stk.SmartsFunctionalGroupFactory,
    # [*][C]([*])=[C]([H])[H] default bonders 1 deleters 3,4,5
    ">C=CH2":stk.TerminalAlkeneFactory,
    # [*][C]#[C][H]  bonders=1, deleters=2, 3
    "-C#CH":stk.TerminalAlkyneFactory,
    # [*][C](=[O])[S][H]  bonders=1, deleters=3, 4
    "-COSH":stk.ThioacidFactory,
    # [*][S][H] bonders=1, deleters=2
    "-SH":stk.ThiolFactory
        '''
        stk.BuildingBlock.__init__(self,*args)
        if MMFFopt:
            self.opt()
    def opt(self):
        mol=self.to_rdkit_mol()
        # In general, MMFFOptimizeMoleculeConfs(m2, numThreads=np) could be better for large molecules!!!
        AllChem.MMFFOptimizeMolecule(mol)
        self._position_matrix=mol.GetConformer().GetPositions().T

block_file=stk.BuildingBlock.init_from_file



class build_framework(stk.ConstructedMolecule):
    def __init__(self, topology_graph,MMFFopt=False):
        stk.ConstructedMolecule.__init__(self,topology_graph=topology_graph)
        if MMFFopt:
            self.opt()
    def opt(self):
        mol=self.to_rdkit_mol()
        AllChem.SanitizeMol(mol)
        AllChem.MMFFOptimizeMolecule(mol)
        self._position_matrix=mol.GetConformer().GetPositions().T

topo={
    "1+1":stk.cage.OnePlusOne,
    "2+2":stk.cage.TwoPlusTwo,
    "2+3":stk.cage.TwoPlusThree,
    "2+4":stk.cage.TwoPlusFour,
    "3+6":stk.cage.ThreePlusSix,
    "4+4":stk.cage.FourPlusFour,
    "4+6":stk.cage.FourPlusSix,
    "4+6_2":stk.cage.FourPlusSix2,
    "4+8":stk.cage.FourPlusEight,
    "5+10":stk.cage.FivePlusTen,
    "6+8":stk.cage.SixPlusEight,
    "6+9":stk.cage.SixPlusNine,
    "6+12":stk.cage.SixPlusTwelve,
    "8+12":stk.cage.EightPlusTwelve,
    "8+16":stk.cage.EightPlusSixteen,
    "10+20":stk.cage.TenPlusTwenty,
    "12+30":stk.cage.TwelvePlusThirty,
    "20+30":stk.cage.TwentyPlusThirty,
}

# class cage():
#     def __init__(self):


# bb= stk.BuildingBlock('BrCCBr', [stk.BromoFactory()])
# print(bb._position_matrix)


group={# 留下原子bonders  删除原子 deleters
    # [*][O][H] default bonders 1 deleters 2
    "-OH":stk.AlcoholFactory,
    # [*][C](=[O])[H] default bonders 1 deleters 2
    "-CHO":stk.AldehydeFactory,
    # [*][C](=[O])[N]([H])[H] default bonders 1 deleters 3,4,5
    "-CONH2":stk.AmideFactory,
    # [*][B]([O][H])[O][H] default bonders 1 deleters 2,3,4,5
    "-BOHOH":stk.BoronicAcidFactory,
    # [*][Br] default bonders 0 deleters 1
    "-Br":stk.BromoFactory,
    # [*][C](=[O])[O][H] default bonders 1 deleters 3,4
    "-COOH":stk.CarboxylicAcidFactory,
    # [Br][#6]~[#6][Br]  default bonders 1,2 deleters 0,3
    "-CBrCBr-":stk.DibromoFactory,
    # [F][#6]~[#6][F]  default bonders 1,2 deleters 0,3
    "-CFCF-":stk.Difluoro,
    # [H][O][#6]~[#6][O][H]  default bonders 2,3 deleters 0,1,4,5
    "-COHCOH-":stk.DiolFactory,
    # [*][F] default bonders 0 deleters 1
    "-F":stk.FluoroFactory,
    # [*][I] default bonders 0 deleters 1
    "-I":stk.IodoFactory,
    # [*][N]([H])[H] default bonders 1 deleters 2,3
    "-NH2":stk.PrimaryAminoFactory,
    # [N]([H])([H])[#6]~[#6]~[#6R1]
    "-RCCCNH2":stk.RingAmineFactory,
    # [H][N]([#6])[#6] default bonders 1 deleters 0
    ">NH":stk.SecondaryAminoFactory,
    # "custom" smarts='[Br][C]',bonders=(1, ), deleters=(0, )
    "custom":stk.SmartsFunctionalGroupFactory,
    # [*][C]([*])=[C]([H])[H] default bonders 1 deleters 3,4,5
    ">C=CH2":stk.TerminalAlkeneFactory,
    # [*][C]#[C][H]  bonders=1, deleters=2, 3
    "-C#CH":stk.TerminalAlkyneFactory,
    # [*][C](=[O])[S][H]  bonders=1, deleters=3, 4
    "-COSH":stk.ThioacidFactory,
    # [*][S][H] bonders=1, deleters=2
    "-SH":stk.ThiolFactory
}



class cage():
    def __init__(self,topo_str,blocks,name="test",MMFFopt=False):
        self.frame=build_framework(topo[topo_str](blocks))
        self.name=name
        self.blocks=blocks
        if MMFFopt:
            self.frame.opt()
    def write(self,file):
        self.frame.write(file)









def example():
    print(
        '''
    #这是一个基于stk的简单包装库, 建立cage分两步
    #1. 第一步定义cage的组成单元, 即block
    #block: 第一个参数是block的SMILES表示, 第二个参数是连接基团们组成的list, 注意group后面小括号表示这是个可有参数的函数值
b1=block("NC1CCCCC1N",[group["-NH2"]()]) #CHDNH2
b2=block("O=Cc1cc(C=O)cc(C=O)c1",[group["-CHO"]()])  # BTMCHO
    #2. 第二步, 根据由cage的拓扑结构和block
    #cage: 第一个参数是拓扑结构的字符串(从1+1到20+30), 第二个参数是blocks, 可选参数opt表示是否需要优化, 默认关闭
test=cage("2+3",(b1,b2),MMFFopt=True)
    #3. 第三步, 输出cage的结构文件
test.write("cage.mol")   
        '''
    )
if __name__=="__main__":
    example()