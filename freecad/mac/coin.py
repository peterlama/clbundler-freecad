from clbundler.formula import *
        
class coin(Formula):
    version = "3.1.3"
    source = {
        "type":"archive", 
        "url":"https://bitbucket.org/Coin3D/coin/downloads/Coin-{0}.tar.gz".format(version)
    }
    supported = {"gcc":["x64"]}
    
    def __init__(self, context, options={}):
        super(coin, self).__init__(context, options)
        
    def build(self):
        configure(self.context, ["--disable-framework"])
        
        system.run_cmd("make", ["-j4"])
        system.run_cmd("make", ["install"])
        
        os.chdir(self.context.install_dir)
        
        files = FileSet()
        files.add(["include/*"], "include", category="dev")
        files.add(["bin/coin-config"], "bin", category="dev")
        files.add(["lib/*.dylib"], "lib", category="rel")
        files.add(["share/Coin"], "share", category="rel")
        
        return files
        
