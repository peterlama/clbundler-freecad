from clbundler.formula import *
        
class pip(Formula):
    version = "1.5.6"
    source = {
        "type":"archive",
        "url":"https://pypi.python.org/packages/source/p/pip/pip-{0}.tar.gz".format(version)
    }
    supported = {"vc9":["x86", "x64"], "vc12":["x86", "x64"]}
    
    def __init__(self, context, options={}):
        super(pip, self).__init__(context, options)
        
        self.add_deps(["python"])
        
    def build(self):
        distutils(self.context)
        
        os.chdir(self.context.install_dir)
        
        files = FileSet()
        files.add(["Lib/site-packages/*"], "bin/Lib/site-packages")
        files.add(["Scripts/*"], "bin/Scripts")
        
        return files
        