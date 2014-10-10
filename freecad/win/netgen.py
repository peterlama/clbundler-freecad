from clbundler.formula import *
        
class netgen(Formula):
    version = "5.1"
    source = {
        "type":"archive", 
        "url":"http://sourceforge.net/projects/netgen-mesher/files/netgen-mesher/"
              "{0}/netgen-{0}.tar.gz".format(version)
    }
    supported = {"vc9":["x86", "x64"], "vc12":["x86", "x64"]}
    
    def __init__(self, context, options={}):
        super(netgen, self).__init__(context, options)
        
        self.add_deps(["oce", "pthreads", "zlib"])
        
        self.patches = ["vcproj", "dllexport", "occ67"]
        
    def build(self):
        self.context.env["BUNDLE_PATH"] = self.context.bundle_path
        
        vcproj = "windows/nglib.vcproj"
        if self.context.toolchain == "vc12":
            vcproj = vcproj_upgrade(vcproj)
        
        if "debug" in self.variant:
            vcbuild(self.context, vcproj, "Debug(OCC)")
        if "release" in self.variant:
            vcbuild(self.context, vcproj, "Release(OCC)")
        
        files = FileSet()
        files.add(["nglib/nglib.h"], "include", category=Categories.build)
        files.add(["libsrc/**/*.hpp", "libsrc/**/*.h"], "include/netgen", category=Categories.build)
        
        os.chdir("windows/nglib")
        if self.context.arch == "x64":
            os.chdir("x64")
        
        files.add(["Debug(OCC)/*.lib", "Release(OCC)/*.lib"], "lib", category=Categories.build)
        files.add(["Release(OCC)/*.dll"], "bin", category=Categories.run)
        files.add(["Debug(OCC)/*.dll"], "bin", category=Categories.run_dbg)
        
        return files
        