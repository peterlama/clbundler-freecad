from clbundler.formula import *
        
class freeimage(Formula):
    version = "3.15.4"
    source = {
        "type":"archive", 
        "url":"http://downloads.sourceforge.net/freeimage/FreeImage3154.zip"
    }
    supported = {"vc9":["x86", "x64"], "vc12":["x86", "x64"], "gcc":["x64"]}
    
    def __init__(self, context, options={}):
        super(freeimage, self).__init__(context, options)
        
        self.patches = ["cmake", "inc_algorithm"]
        
    def build(self):
        cmake(self.context, {"BUILD_SHARED_LIBS":"ON", "CMAKE_BUILD_TYPE":"Release"})
        
        if self.context.toolchain.startswith("vc"):
            vcbuild(self.context, "cmake_build\\freeimage.sln", "Debug")
            vcbuild(self.context, "cmake_build\\freeimage.sln", "Release")
            
            vcproj = "cmake_build\\INSTALL" + vcproj_ext(vc_version(self.context.toolchain))
            vcbuild(self.context, vcproj, "Debug")
            vcbuild(self.context, vcproj, "Release")
        else:
            os.chdir("cmake_build")
            system.run_cmd("make", ["-j4"])
            system.run_cmd("make", ["install/fast"])
        
        os.chdir(self.context.install_dir)
        
        files = FileSet()
        files.add(["include/*"], "include", category="dev")
        
        if self.context.toolchain.startswith("vc"):
            files.add(["lib/*"], "lib", category="dev")
            files.add(["bin/*[!d].dll"], "bin", category="rel")
            files.add(["bin/*d.dll"], "bin", category="dbg")
        else:
            if self.context.os_name == "mac":
                files.add(["lib/*.dylib"], "lib", category="rel")
            else:
                files.add(["lib/*.so"], "lib", category="rel")
        
        return files

