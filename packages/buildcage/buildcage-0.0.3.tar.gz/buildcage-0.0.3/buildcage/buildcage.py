import argparse
from buildcage.src.readjson import ArgsFromJson
from buildcage.src.boss import GetParmsFromBOSS
from buildcage.src.stkcage import *
from buildcage.src.lmp import get_lmp

parser=argparse.ArgumentParser(prog='buildcage')
parser.add_argument("json",help="Cage definition json file")
parser.add_argument("--MMFF",action='store_true',help="Wheter to start a MMFF optimization initially")
parser.add_argument("--pair",action='store_true',help="Wheter to include pair interactions during minimization")
args=parser.parse_args()

def main():
    config=ArgsFromJson(args.json)
    config_block=config["cage"]["blocks"]
    if config_block[0][0].split(".")[-1]=="mol":
        b1=block_file(config_block[0][0],[group[i]() for i in config_block[0][1]])
    else:
        b1=block(config_block[0][0],[group[i]() for i in config_block[0][1]])
    if config_block[1][0].split(".")[-1]=="mol":
        b2=block_file(config_block[1][0],[group[i]() for i in config_block[1][1]])
    else:
        b2=block(config_block[1][0],[group[i]() for i in config_block[1][1]])
    MMFFflag=True if args.MMFF else False
    Pairflag=True if args.pair else False
    mycage=cage(config["cage"]["topology"],(b1,b2),MMFFopt=MMFFflag)
    mycage.write("{}.mol".format(config["name"]))
    get_lmp(config["name"],b1,b2,mycage.frame,config["BOSSdir"],config["BABELexe"],config["LMPexe"],"\n".join(config["MDArgs"]),Pairflag)

if __name__=="__main__":
    main()
    pass
