import re, os
from optparse import OptionParser as P

class PML(object):

    def _re_indent(self):
        """Re-indents the code strings, setting the leadeing
        left indent to zero.
        """
        if self.code:
            for line in self.code:
                if line.strip():
                    self.leading_indent = len(line) - len(line.lstrip())
                    break

        for line in self.code:
            self.re_indented_code += line[self.leading_indent:].rstrip() + os.linesep

    def __str__(self):
        return self.re_indented_code
    

class PMLBlock(PML):
    """PMLBlock to encapsulate and manage the rendering of PML
    blocks in rendered files.
    """
    def __init__(self,code,number):
        self.code = code.split(os.linesep)
        self.re_indented_code = r""
        self.number = number
        self.new_code = r""
        self.leading_indent = None
        self._re_indent()


class PMLFile(PML):
    """PMLFile to manage the PML file and its blocks.
    """

    def __init__(self,code):
        self.code = code.split(os.linesep)
        self.leading_indent = None
        self.re_indented_code = r""
        self.rendered_code = r""
        self.code_blocks = list()
        self.raw_blocks = list()
        self.place_holder = r'%s<pml id="%s"/>'
        self.place_holder_count = 0
        self.block_pattern = re.compile(r"(\s*<pml>.*?</pml>)", re.DOTALL)
        self.code_pattern = re.compile(r"<pml>(.*?)</pml>", re.DOTALL)
        self._re_indent()
        self._parse()

    def _place_holder(self,match):
        """Callback for 're.sub' function, using the match object passed to it
        decide what kind of relacement string to return.
        """
        leading_indent = self.raw_blocks[self.place_holder_count].leading_indent
        self.place_holder_count += 1
        return self.place_holder %(r" "*leading_indent,
                                   self.place_holder_count)

    def _parse(self):
        """Parses code string and interprets the PML.
        """
        self.code_blocks = [PMLBlock(each,1) for each in re.findall(self.code_pattern,self.re_indented_code)] # Find all PML code
        self.raw_blocks = [PMLBlock(each,1) for each in re.findall(self.block_pattern,self.re_indented_code)] # Find all PML blocks
        self.rendered_code = re.sub(self.block_pattern,
                                    self._place_holder,
                                    self.re_indented_code)
        try:
            for index in range(len(self.code_blocks)):
                pml = None
                leading_indent = r" "*(self.raw_blocks[index].leading_indent)
                exec(str(self.code_blocks[index]))
                pattern_string = r'%s<pml id="%s"/>' % (leading_indent,index + 1)
                pattern = re.compile(pattern_string)
                if pml:
                    if leading_indent.startswith(os.linesep):
                        self.rendered_code = re.sub(pattern,
                                                    r"%s%s" % (leading_indent,str(pml)),
                                                    self.rendered_code)
                    else:
                        self.rendered_code = re.sub(pattern,
                                                    r"%s%s%s" % (os.linesep,leading_indent,str(pml)),
                                                    self.rendered_code)
                else:
                    self.rendered_code = re.sub(pattern,
                                                r"",
                                                self.rendered_code)
        except IndentationError, e:
            raise IndentationError("The Python code in the PML document is not indented correctly.")

    def __str__(self):
        if self.rendered_code:
            return self.rendered_code
        else:
            return self.re_indented_code


if __name__ == "__main__":
    p = P(usage="%s options FILE" % os.path.basename(__file__))
    p.add_option('-f','--file',dest="filename",
                 help="write output to FILE",metavar="FILE")
    (opts,args) = p.parse_args()
    if len(args) and len(args) < 2:
        if os.path.isfile(args[0]):
            #parse(open(args[0],'r').readlines())
            pml_file = PMLFile(open(args[0],'r').read())
            if opts.filename and os.path.isfile(opts.filename):
                open(opts.filename,'w').write(str(pml_file))
            elif opts.filename:
                try:
                    open(os.path.expanduser(opts.filename),'w').write(str(pml_file))
                except IOError, e:
                    p.print_usage()
                    print("Check your output file path: '%s'" % e)
            else:
                print(pml_file)
        else:
            print("%s is not a file" % args[0])
    else:
        p.print_usage()

