from clbundler.formula import *
        
class tk(Formula):
    version = "8.6.1"
    source = {
        "type":"archive", 
        "url":"http://prdownloads.sourceforge.net/tcl/tk{0}-src.tar.gz".format(version)
    }
    supported = {"vc9":["x86", "x64"], "vc12":["x86", "x64"]}
    
    def __init__(self, context, options={}):
        super(tk, self).__init__(context, options)
        
        self.add_deps("tcl")
        
    def build(self):
        #tk requires some tcl source files
        self.context.env["TCLDIR"] = os.path.join(self.context.build_dir,
                                                  "tcl-" + self.version)
        
        os.chdir("win")
        system.run_cmd("nmake", ["/f", "makefile.vc"])
        
        system.run_cmd("nmake", ["/f", "makefile.vc",
                                 "_INSTALLDIR=" + self.context.install_dir, 
                                 "install"])
        os.chdir("..")
        
        files = FileSet()
        files.add(["generic\\tklInt.h",
                   "generic\\tkIntDecls.h",
                   "generic\\tkIntPlatDecls.h",
                   "generic\\tkPort.h",
                   "win\\tkWinPort.h",
                   "win\\tkWinInt.h",
                   "win\\tkWin.h"], "include", category=Categories.build)
        
        os.chdir(self.context.install_dir)
                
        files.add(["include/*"], "include", category=Categories.build)
        files.add(["lib/*"], "lib", category=Categories.build)
        files.add(["bin/*"], "bin", category=Categories.run)
        
        return files