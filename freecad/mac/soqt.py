from clbundler.formula import *
        
class soqt(Formula):
    version = "1.5.0"
    source = {
        "type":"archive", 
        "url":"https://bitbucket.org/Coin3D/coin/downloads/SoQt-{0}.tar.gz".format(version)
    }
    supported = {"gcc":["x64"]}
    
    def __init__(self, context, options={}):
        super(soqt, self).__init__(context, options)
        
        self.add_deps("coin", "qt")
        
    def build(self):
        self.context.env["QTDIR"] = self.context.bundle_path
        
        configure(self.context, ["--without-framework"])
        
        system.run_cmd("make", ["-j4"])
        system.run_cmd("make", ["install"])
        
        os.chdir(self.context.install_dir)
        
        files = FileSet()
        files.add(["include/Inventor/Qt"], "include/Inventor", category=Categories.build)
        files.add(["bin/soqt-config"], "bin", category=Categories.build)
        files.add(["lib/*.dylib"], "lib", category=Categories.run)
        files.add(["share/Coin/conf/*"], "share/Coin/conf", category=Categories.run)
        
        return files
        
