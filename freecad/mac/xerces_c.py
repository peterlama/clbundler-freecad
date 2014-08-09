from clbundler.formula import *
        
class xerces_c(Formula):
    version = "3.1.1"
    source = {
        "type":"archive", 
        "url":"http://apache.mirrors.tds.net/xerces/c/3/sources/"
              "xerces-c-{0}.tar.gz".format(version)
    }
    supported = {"gcc":["x64"]}
    
    def __init__(self, context, options={}):
        super(xerces_c, self).__init__(context, options)
       
    def build(self):
        configure(self.context)
        
        system.run_cmd("make", ["-j4"])
        system.run_cmd("make", ["install"])
        
        os.chdir(self.context.install_dir)
        
        files = FileSet()
        files.add(["include/*"], "include", category="dev")
        files.add(["lib/*.dylib"], "lib", category="rel")
        
        return files
