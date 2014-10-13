from clbundler.formula import *
        
class boost(Formula):
    version = "1.55"
    source = {
        "type":"archive", 
        "url":"http://sourceforge.net/projects/boost/files/boost/1.55.0"
              "/boost_1_55_0.zip"
    }
    supported = {"vc9":["x86", "x64"], "vc12":["x86", "x64"]}
    
    def __init__(self, context, options={}):
        super(boost, self).__init__(context, options)
       
        if context.toolchain == "vc12":
            self.patches.append("vc12")
        
        self.add_option("with_libraries", ["filesystem",
                                           "program_options",
                                           "regex",
                                           "signals",
                                           "system",
                                           "thread"])
    def build(self):
        system.run_cmd("bootstrap.bat")
        
        toolset = "toolset=msvc-" + vc_version(self.context.toolchain) + ".0"
        if self.variant == "release+debug":
            variants = "release,debug"
        else:
            variants = self.variant
        
        system.run_cmd("b2.exe", [toolset, 
                                  "link=shared",
                                  "variant=" + variants,
                                  "--with-libraries=" + ",".join(self.with_libraries)])
        
        files = FileSet()
        files.add(["boost"], "include", category=Categories.build)
        files.add(["stage/lib/*.lib"], "lib", category=Categories.build)
        files.add(["stage/lib/*mt-????.dll"], "bin", category=Categories.run)
        files.add(["stage/lib/*mt-gd-????.dll"], "bin", category=Categories.run_dbg)
        
        return files