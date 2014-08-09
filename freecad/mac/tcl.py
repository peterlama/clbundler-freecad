from clbundler.formula import *
        
class tcl(Formula):
    version = "8.6.1"
    source = {
        "type":"archive", 
        "url":"http://prdownloads.sourceforge.net/tcl/tcl{0}-src.tar.gz".format(version)
    }
    supported = {"gcc":["x64"]}
    
    def __init__(self, context, options={}):
        super(tcl, self).__init__(context, options)
        
    def build(self):
        os.chdir("unix")
        
        configure(self.context, ["--exec-prefix=" + self.context.install_dir,
                                 "--enable-64bit"])
        system.run_cmd("make", ["-j4"])
        system.run_cmd("make", ["install"])
        
        os.chdir(self.context.install_dir)
        
        files = FileSet()
        files.add(["include/*"], "include", category="dev")
        files.add(["lib/*.a"], "lib", category="dev")
        files.add(["lib/*"], "lib", ["lib/pkgconfig", "lib/*.a"], category="rel")
        files.add(["bin/*"], "bin", category="rel")
        
        return files

