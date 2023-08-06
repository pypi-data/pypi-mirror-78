from .core import *

def main():
    import fire
    fire.Fire({'if': Ifc, 'iw': Iwc})
    # ifc = Ifc('lo0')
    # print(ifc.params)
    # iwc = Iwc('lo0')
    # print(iwc.params)
