from clbundler.formula import *
        
class pivy(Formula):
    version = "HEAD"
    source = {
        "type":"hg",
        "url":"https://bitbucket.org/Coin3D/pivy"
    }
    supported = {"vc9":["x86", "x64"], "vc12":["x86", "x64"]}
    
    def __init__(self, context, options={}):
        super(pivy, self).__init__(context, options)
        
        self.add_deps("python", "coin", "swig")
        
        self.patches = ["no_gui"]
        
    def build(self):
        self.context.env["PATH"] += os.path.join(self.context.bundle_path, "bin", "swig")
        self.context.env["COINDIR"] = self.context.bundle_path
        
        distutils(self.context)
        
        os.chdir(self.context.install_dir)
        
        files = FileSet()
        files.add(["Lib/site-packages/*"], "bin/Lib/site-packages")
        
        return files
