from clbundler.formula import *
        
class freeimage(Formula):
    version = "3.15.4"
    source = {
        "type":"archive", 
        "url":"http://downloads.sourceforge.net/freeimage/FreeImage3154.zip"
    }
    supported = {"vc9":["x86", "x64"], "vc12":["x86", "x64"]}
    
    def __init__(self, context, options={}):
        super(freeimage, self).__init__(context, options)
        
        self.patches = ["cmake", "inc_algorithm"]
        
    def build(self):
        cmake(self.context, {"BUILD_SHARED_LIBS":"ON"})
        
        vcbuild(self.context, "cmake_build\\freeimage.sln", "Debug")
        vcbuild(self.context, "cmake_build\\freeimage.sln", "Release")
        
        vcproj = "cmake_build\\INSTALL" + vcproj_ext(vc_version(self.context.toolchain))
        vcbuild(self.context, vcproj, "Debug")
        vcbuild(self.context, vcproj, "Release")
        
        os.chdir(self.context.install_dir)
        
        files = FileSet()
        files.add(["include/*"], "include", category="dev")
        files.add(["lib/*"], "lib", category="dev")
        files.add(["bin/*[!d].dll"], "bin", category="rel")
        files.add(["bin/*d.dll"], "bin", category="dbg")
        
        return files
