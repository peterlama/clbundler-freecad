from clbundler.formula import *
        
class coin(Formula):
    version = "3.1.3"
    source = {
        "type":"archive", 
        "url":"https://bitbucket.org/Coin3D/coin/downloads/Coin-{0}.tar.gz".format(version)
    }
    supported = {"vc9":["x86", "x64"], "vc12":["x86", "x64"]}
    
    def __init__(self, context, options={}):
        super(coin, self).__init__(context, options)
        
        self.patches = ["vcproj_x64", "macro_error"]
        if context.toolchain == "vc12":
            self.patches.append("config")
       
    def build(self):
        os.chdir("build\\msvc9")
        
        vcproj = "coin3.vcproj"
        if self.context.toolchain == "vc12":
            vcproj = vcproj_upgrade(vcproj)
        
        vcbuild(self.context, vcproj, "DLL (Debug)")
        vcbuild(self.context, vcproj, "DLL (Release)")
        
        self.context.env["COINDIR"] = self.context.install_dir
        
        system.run_cmd("..\\misc\\install-sdk.bat", ["dll", "debug", "msvc9", "coin3"])
        system.run_cmd("..\\misc\\install-sdk.bat", ["dll", "release", "msvc9", "coin3"])
        
        os.chdir(self.context.install_dir)
        
        files = FileSet()
        files.add(["include/*"], "include", category="dev")
        files.add(["lib/*"], "lib", category="dev")
        files.add(["bin/*[!d].dll"], "bin", category="rel")
        files.add(["bin/*d.dll"], "bin", category="dbg")
        
        return files
        