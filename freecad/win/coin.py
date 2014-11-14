from clbundler.formula import *
        
class coin(Formula):
    version = "4.0.0a"
    source = {
        "type":"hg", 
        "url":"https://bitbucket.org/Coin3D/coin"
    }
    supported = {"vc9":["x86", "x64"], "vc11":["x86", "x64"], "vc12":["x86", "x64"]}
    
    def __init__(self, context, options={}):
        super(coin, self).__init__(context, options)
        
        self.patches = ["vcproj_x64", "macro_error"]
        if vc_version(context.toolchain) > 10:
            self.patches.append("config")
       
    def build(self):
        vcproj = ""
        extra = []
        vc_ver = vc_version(self.context.toolchain)
        msvc_dir = "msvc9"
        if vc_ver == 9:
            os.chdir("build\\msvc9")
            vcproj = "coin4.vcproj"
        elif vc_ver >= 10:
            os.chdir("build\\msvc10")
            msvc_dir = "msvc10"
            vcproj = "coin4.vcxproj"
            if vc_ver != 10:
                extra = ["/p:PlatformToolset=v{0}0".format(vc_ver)]
                if vc_ver == 12:
                   extra.append("/tv:12.0")
        
        if "debug" in self.variant:
            vcbuild(self.context, vcproj, "DLL (Debug)", extra=extra)
        if "release" in self.variant:
            vcbuild(self.context, vcproj, "DLL (Release)", extra=extra)
        
        self.context.env["COINDIR"] = self.context.install_dir
        
        
        if "debug" in self.variant:
            system.run_cmd("..\\misc\\install-sdk.bat", ["dll", "debug", msvc_dir, "coin4"])
        if "release" in self.variant:
            system.run_cmd("..\\misc\\install-sdk.bat", ["dll", "release", msvc_dir, "coin4"])
        
        os.chdir(self.context.install_dir)
        
        files = FileSet()
        files.add(["include/*"], "include", category=Categories.build)
        files.add(["lib/*"], "lib", category=Categories.build)
        files.add(["bin/*[!d].dll"], "bin", category=Categories.run)
        files.add(["bin/*d.dll"], "bin", category=Categories.run_dbg)
        
        return files
        