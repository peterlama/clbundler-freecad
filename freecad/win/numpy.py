from clbundler.formula import *
        
class numpy(Formula):
    version = "1.9.1"
    source = {
        "type":"archive",
        "url":"http://sourceforge.net/projects/numpy/files/NumPy/{0}/numpy-{0}.zip".format(version)
    }
    supported = {"vc9":["x86", "x64"], "vc11":["x86", "x64"], "vc12":["x86", "x64"]}
    
    def __init__(self, context, options={}):
        super(numpy, self).__init__(context, options)
        
        self.add_deps("python")
        
    def build(self):
        self.context.env["INCLUDE"] += self.context.bundle_path + "\\include\python2.7;"
        self.context.env["LIB"] += self.context.bundle_path + "\\lib;"
        if "debug" in self.variant:
            distutils(self.context, debug=True)
        if "release" in self.variant:
            distutils(self.context)
        
        os.chdir(self.context.install_dir)
        
        files = FileSet()
        files.add(["Lib/site-packages/*"], "bin/Lib/site-packages")
        
        return files
        