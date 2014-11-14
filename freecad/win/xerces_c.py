from clbundler.formula import *
        
class xerces_c(Formula):
    version = "3.1.1"
    source = {
        "type":"archive", 
        "url":"http://apache.mirrors.tds.net/xerces/c/3/sources/"
              "xerces-c-{0}.tar.gz".format(version)
    }
    supported = {"vc9":["x86", "x64"], "vc11":["x86", "x64"], "vc12":["x86", "x64"]}
    
    def __init__(self, context, options={}):
        super(xerces_c, self).__init__(context, options)
       
    def build(self):
        if vc_version(self.context.toolchain) > 9:
            vcproj = "projects/Win32/VC10/xerces-all/XercesLib/XercesLib.vcxproj"
            vc_dir = "VC10"
            extra = ["/p:PlatformToolset=v{0}0".format(vc_version(self.context.toolchain))]
        else:
            vcproj = "projects/Win32/VC9/xerces-all/XercesLib/XercesLib.vcproj"
            vc_dir = "VC9"
            extra = []
        
        if "debug" in self.variant:        
            vcbuild(self.context, vcproj, "Debug", extra=extra)
        if "release" in self.variant:
            vcbuild(self.context, vcproj, "Release", extra=extra)
        
        files = FileSet()
        files.add(["src/xercesc/**/*.h",
                   "src/xercesc/**/*.hpp",
                   "src/xercesc/**/*.c"], "include/xercesc", category=Categories.build)
        
        if self.context.arch == "x64":
            os.chdir("Build/Win64/" + vc_dir)
        else:
            os.chdir("Build/Win32/" + vc_dir)
        
        files.add(["Release/*.lib"], "lib", category=Categories.build)
        files.add(["Debug/*.lib"], "lib", category=Categories.build)
        files.add(["Release/*.dll"], "bin", category=Categories.run)
        files.add(["Debug/*.dll"], "bin", category=Categories.run_dbg)
        
        return files