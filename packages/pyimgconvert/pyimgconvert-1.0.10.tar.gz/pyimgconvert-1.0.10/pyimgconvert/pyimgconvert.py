#System imports
import os, sys

# Project specific imports
import      pfmisc
from        pfmisc._colors      import  Colors
from        pfmisc.debug        import  debug
from        pfmisc              import  other
from        pfmisc              import  error
import argparse
import pudb
import subprocess

class pyimgconvert(object):
    """
        A class based on "magick convert" that accepts CLI arguments that need to be passed 
        to the Linux CLI utility to convert images to required outputs.
    """

    def __init__(self, **kwargs):
        """
        A block to declare self variables
        """

        self.str_desc                   = ''
        self.__name__                   = "pyimgconvert"
        self.str_version                = "1.0.10"
        self.verbosity                  = 1
        self.dp                         = pfmisc.debug(
                                            verbosity   = self.verbosity,
                                            within      = self.__name__
                                            )

         # Directory and filenames
        self.str_inputDir                   = ''
        self.str_outputDir                  = ''
        self.str_args                       = ''
        self.str_inputFile                  = ''
        self.str_outputFile                 = ''
                
        for key, value in kwargs.items():
           if key == "inputDir":              self.str_inputDir              = value
           if key == "outputDir":             self.str_outputDir             = value
           if key == "args":                  self.str_args                  = value
           if key == "inputFile":             self.str_inputFile             = value
           if key == "outputFile":            self.str_outputFile            = value

    def job_run(self, str_cmd):
        """
        Running some CLI process via python is cumbersome. The typical/easy
        path of
                            os.system(str_cmd)
        is deprecated and prone to hidden complexity. The preferred
        method is via subprocess, which has a cumbersome processing
        syntax. Still, this method runs the `str_cmd` and returns the
        stderr and stdout strings as well as a returncode.
        Providing readtime output of both stdout and stderr seems
        problematic. The approach here is to provide realtime
        output on stdout and only provide stderr on process completion.
        """
        d_ret = {
            'stdout':       "",
            'stderr':       "",
            'returncode':   0
        }

        p = subprocess.Popen(
                    str_cmd.split(),
                    stdout      = subprocess.PIPE,
                    stderr      = subprocess.PIPE,
        )

        # Realtime output on stdout
        str_stdoutLine  = ""
        str_stdout      = ""
        while True:
            stdout      = p.stdout.readline()
            if p.poll() is not None:
                break
            if stdout:
                str_stdoutLine = stdout.decode()
                if int(self.verbosity):
                    print(str_stdoutLine, end = '')
                str_stdout      += str_stdoutLine
        d_ret['stdout']     = str_stdout
        d_ret['stderr']     = p.stderr.read().decode()
        d_ret['returncode'] = p.returncode
        if int(self.verbosity):
            print('\nstderr: \n%s' % d_ret['stderr'])
        return d_ret

    def job_stdwrite(self, d_job):
        """
        Capture the d_job entries to respective files.
        """
        for key in d_job.keys():
            with open(
                 '%s/%s-%s' % (self.str_outputDir, self.str_outputFile, key), "w"
            ) as f:
                f.write(str(d_job[key]))
                f.close()
        return {
            'status': True
        }

    def img_convert(self):
        """
        Define the code to be run by this python app.
        """

        str_cmd     = ""

        l_appargs = self.str_args.split('ARGS:')
        if len(l_appargs) == 2:
            self.str_args = l_appargs[1]
        else:
            self.str_args = l_appargs[0]

        os.chdir(self.str_outputDir)
        str_cmd = "convert %s/%s %s %s/%s" % (self.str_inputDir, self.str_inputFile, 
                self.str_args, self.str_outputDir, self.str_outputFile)

        # Run the job and provide realtime stdout
        # and post-run stderr
        self.job_stdwrite(
            self.job_run(str_cmd)
        )

class object_factoryCreate:
    """
    A class that examines input file string for extension information and
    returns the relevant convert object.
    """

    def __init__(self, args):
        """
        Parse relevant CLI args.
        """
        # str_outputFileStem, str_outputFileExtension = os.path.splitext(args.outputFileStem)
        # if len(str_outputFileExtension):
        #     str_outputFileExtension = str_outputFileExtension.split('.')[1]
        # # try:
        # #     str_inputFileStem, str_inputFileExtension = os.path.splitext(args.inputFile)
        # # except:
        # #     sys.exit(1)

        # if not len(args.outputFileType) and len(str_outputFileExtension):
        #     args.outputFileType = str_outputFileExtension

        # if len(str_outputFileExtension):
        #     args.outputFileStem = str_outputFileStem

        self.C_convert = pyimgconvert(
            inputFile            = args.inputFile,
            inputDir             = args.inputDir,
            outputDir            = args.outputDir,
            outputFile           = args.outputFile,
            args                 = args.args,
            man                  = args.man,
            synopsis             = args.synopsis,
            verbosity            = args.verbosity,
            version              = args.version
        )
