from clbundler.formula import *
        
class swig(Formula):
    version = "1.3.40"
    source = {
        "type":"archive",
        "url":"http://sourceforge.net/projects/swig/files/swigwin/swigwin-{0}/swigwin-{0}.zip".format(version)
    }
    supported = {"vc9":["x86", "x64"], "vc12":["x86", "x64"]}
    
    def __init__(self, context, options={}):
        super(swig, self).__init__(context, options)
        
    def build(self):
        files = FileSet()
        files.add("./*", "bin/swig")
        
        return files
