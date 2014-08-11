from clbundler.formula import *
        
class openssl(Formula):
    version = "1.0.1h"
    source = {
        "type":"archive", 
        "url":"http://www.openssl.org/source/openssl-{0}.tar.gz".format(version)
    }
    supported = {"vc9":["x86", "x64"], "vc12":["x86", "x64"]}
    
    def __init__(self, context, options={}):
        super(openssl, self).__init__(context, options)
        
    def build(self):
        self.context.env["PATH"] += self.context.bundle_path + "\\bin\\Perl\\bin;"
        
        if self.context.arch == "x64":
            system.run_cmd("perl", ["Configure", "--openssldir=" + self.context.install_dir, "no-asm", "VC-WIN64A"])
            system.run_cmd("ms\\do_win64a.bat")
        else:
            system.run_cmd("perl", ["Configure", "--openssldir=" + self.context.install_dir, "VC-WIN32"])
            system.run_cmd("ms\\do_ms.bat")
        
        system.run_cmd("nmake", ["/f", "ms\\ntdll.mak", "install"])
        
        os.chdir(self.context.install_dir)
        
        files = FileSet()
        files.add(["include/*"], "include", category=Categories.build)
        files.add(["lib/*.lib"], "lib", category=Categories.build)
        files.add(["lib/engines"], "lib", category=Categories.run)
        files.add(["bin/*"], "bin", category=Categories.run)
        
        return files
