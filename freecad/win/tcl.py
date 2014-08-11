from clbundler.formula import *
        
class tcl(Formula):
    version = "8.6.1"
    source = {
        "type":"archive", 
        "url":"http://prdownloads.sourceforge.net/tcl/tcl{0}-src.tar.gz".format(version)
    }
    supported = {"vc9":["x86", "x64"], "vc12":["x86", "x64"]}
    
    def __init__(self, context, options={}):
        super(tcl, self).__init__(context, options)
        
    def build(self):
        os.chdir("win")
        system.run_cmd("nmake", ["/f", "makefile.vc"])
        
        system.run_cmd("nmake", ["/f", "makefile.vc",
                                 "INSTALLDIR=" + self.context.install_dir, 
                                 "install"])
        os.chdir("..")
                
        files = FileSet()
        files.add(["generic/tclInt.h",
                   "generic/tclIntDecls.h",
                   "generic/tclIntPlatDecls.h",
                   "generic/tclPort.h",
                   "generic/tclOOInt.h",
                   "generic/tclOOIntDecls.h",
                   "win/tclWinPort.h"], "include", category=Categories.build)
        
        os.chdir(self.context.install_dir)
                
        files.add(["include/*"], "include", category=Categories.build)
        files.add(["lib/*"], "lib", category=Categories.build)
        files.add(["bin/*"], "bin", category=Categories.run)
        
        return files