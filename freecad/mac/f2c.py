from clbundler.formula import *
        
class f2c(Formula):
    version = "2010"
    source = {
        "type":"archive",
        "url":"http://ftp.debian.org/debian/pool/main/f/f2c/f2c_20100827.orig.tar.gz"
    }
    supported = {"gcc":["x64"]}
    
    def __init__(self, context, options={}):
        super(f2c, self).__init__(context, options)
        
        self.add_deps("libf2c")
        
    def build(self):
        os.chdir("src")
        
        system.run_cmd("make", ["-f", "makefile.u"])
        
        files = FileSet()
        files.add(["f2c"], "bin")
        
        return files
        
