from clbundler.formula import *
        
class xerces_c(Formula):
    version = "3.1.1"
    source = {
        "type":"archive", 
        "url":"http://apache.mirrors.tds.net/xerces/c/3/sources/"
              "xerces-c-{0}.tar.gz".format(version)
    }
    supported = {"vc9":["x86", "x64"], "vc12":["x86", "x64"]}
    
    def __init__(self, context, options={}):
        super(xerces_c, self).__init__(context, options)
       
    def build(self):
        if self.context.toolchain == "vc12":
            vcproj = "projects/Win32/VC10/xerces-all/XercesLib/XercesLib.vcxproj"
            vc_dir = "VC10"
            extra = ["/p:PlatformToolset=v120"]
        else:
            vcproj = "projects/Win32/VC9/xerces-all/XercesLib/XercesLib.vcproj"
            vc_dir = "VC9"
            extra = []
               
        vcbuild(self.context, vcproj, "Debug", extra=extra)
        vcbuild(self.context, vcproj, "Release", extra=extra)
        
        files = FileSet()
        files.add(["src/xercesc/**/*.h",
                   "src/xercesc/**/*.hpp",
                   "src/xercesc/**/*.c"], "include/xercesc", category="dev")
        
        if self.context.arch == "x64":
            os.chdir("Build/Win64/" + vc_dir)
        else:
            os.chdir("Build/Win32/" + vc_dir)
        
        files.add(["Release/*.lib"], "lib", category="dev")
        files.add(["Debug/*.lib"], "lib", category="dev")
        files.add(["Release/*.dll"], "bin", category="rel")
        files.add(["Debug/*.dll"], "bin", category="dbg")
        
        return files