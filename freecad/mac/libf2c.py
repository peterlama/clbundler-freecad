from clbundler.formula import *
        
class libf2c(Formula):
    version = "2009"
    source = {
        "type":"archive",
        "url":"http://ftp.debian.org/debian/pool/main/libf/libf2c2/libf2c2_20090411.orig.tar.gz"
    }
    supported = {"gcc":["x64"]}
    
    def __init__(self, context, options={}):
        super(libf2c, self).__init__(context, options)
        
    def build(self):
        system.run_cmd("make", ["-f", "makefile.u"])
        
        files = FileSet()
        files.add(["f2c.h"], "include", category="dev")
        files.add(["libf2c.a"], "lib", category="dev")
        
        return files
        
