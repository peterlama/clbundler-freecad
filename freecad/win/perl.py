from clbundler.formula import *
        
class perl(Formula):
    version = "5.20.0"
    source = {
        "type":"archive", 
        "url":"http://www.cpan.org/src/5.0/perl-{0}.tar.gz".format(version)
    }
    supported = {"vc9":["x86", "x64"], "vc12":["x86", "x64"]}
    
    def __init__(self, context, options={}):
        super(perl, self).__init__(context, options)
       
    def build(self):
        os.chdir("win32")
        
        def64 = ""
        if self.context.arch == "x86":
            def64 = "WIN64=undef"
        
        system.run_cmd("nmake", ["install", "INST_TOP=" + self.context.install_dir + "\\Perl",
                                 def64, "CCTYPE=MSVC{0}0FREE".format(vc_version(self.context.toolchain))])
        
        os.chdir(self.context.install_dir)
        
        files = FileSet()
        files.add(["Perl"], "bin")
        
        #with open("perl.bat", "w") as f:
        #    f.write("@echo off\n\r%~dp0\\Perl\\bin\\perl.exe %*\n\r")
        #files.add(["perl.bat"], "bin")
        
        return files
