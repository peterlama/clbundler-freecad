from clbundler.formula import *
        
class soqt(Formula):
    version = "1.5.0"
    source = {
        "type":"archive", 
        "url":"https://bitbucket.org/Coin3D/coin/downloads/SoQt-{0}.tar.gz".format(version)
    }
    supported = {"vc9":["x86", "x64"], "vc12":["x86", "x64"]}
    
    def __init__(self, context, options={}):
        super(soqt, self).__init__(context, options)
        
        self.add_deps("coin", "qt")
        
        self.patches.append("vcproj_x64")
        
    def build(self):
        os.chdir("build\\msvc9")
        
        vcproj = "soqt1.vcproj"
        if self.context.toolchain == "vc12":
            vcproj = vcproj_upgrade(vcproj)
        
        self.context.env["QTDIR"] = self.context.bundle_path
        self.context.env["COINDIR"] = self.context.bundle_path
        
        if "debug" in self.variant:
            vcbuild(self.context, vcproj, "DLL (Debug)")
        if "release" in self.variant:
            vcbuild(self.context, vcproj, "DLL (Release)")
        
        self.context.env["COINDIR"] = self.context.install_dir
        
        if "debug" in self.variant:
            system.run_cmd("..\\misc\\install-sdk.bat", ["dll", "debug", "msvc9", "soqt1"])
        if "release" in self.variant:
            system.run_cmd("..\\misc\\install-sdk.bat", ["dll", "release", "msvc9", "soqt1"])
        
        os.chdir(self.context.install_dir)
        
        files = FileSet()
        files.add(["include/Inventor/Qt"], "include/Inventor", category=Categories.build)
        files.add(["lib/*"], "lib", category=Categories.build)
        files.add(["bin/*[!d].dll"], "bin", category=Categories.run)
        files.add(["bin/*d.dll"], "bin", category=Categories.run_dbg)
        
        return files
        