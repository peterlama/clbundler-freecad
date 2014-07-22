from clbundler.formula import *

class freecad(Formula):
    def __init__(self, context, options={}):
        super(freecad, self).__init__(context, options)
        
        self.is_kit = True
        
        self.add_deps([
            "boost",
            "coin",
            "eigen",
            "f2c",
            "freeimage",
            "freetype",
            "netgen",
            "oce",
            "pyside",
            "python",
            "qt",
            "shiboken",
            "soqt",
            "xerces_c",
            "zlib"
        ])
