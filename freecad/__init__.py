from clbundler.formula import *

class freecad(Formula):
    def __init__(self, context, options={}):
        super(freecad, self).__init__(context, options)
        
        self.is_kit = True
        
        self.add_deps(
            "boost",
            "coin",
            "eigen",
            "freetype",
            "matplotlib",
            "oce",
            "pcl",
            "pivy",
            "pyside",
            "pyside_tools",
            "python",
            "qt",
            "xerces_c"
        )

        if context.os_name == "win":
            self.add_deps("netgen")

