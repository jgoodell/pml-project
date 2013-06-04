import os

from unittest import TestCase
from pml import PMLBlock, PMLFile


class PMLTestCase(TestCase):
    def setUp(self):
        self.broken_code = '''
        <html>
          <body>
            <h1>Hello World!</h1>
            <pml>
              def f():
                output = "<h2>Bad News!</h2>"
                  return output

              pml = f()
            </pml>
          </body>
        </html>'''
        
        self.code01 = '''
        <html>
          <body>
            <h1>Hello World!</h1>
            <pml>
              def f():
                  return "<h2>Good Bye</h2>"

              pml = f()
            </pml>
          </body>
        </html>'''

        self.code02 = '''
        <html>
          <body>
            <h1>Hello World!</h1>
            <pml>
              def f():
                  return "<h2>Good Bye</h2>"
            </pml>
            <pml>
              pml = f()
            </pml>
          </body>
        </html>'''

        self.bad_code = '''
        <html>
        <body>
            <h1>Hello Class!</h1>
           <pml>
              class HelloClass(object):
                  
                  def __init__(self,name):
                      self.name = name

                  def __str__(self):
                      return self.name
            </pml>
            <pml>
              pml = str(HelloClass("Jason"))
          </pml>
          </body>
        </html>'''

        self.rendered_bad = '''
        <html>
        <body>
            <h1>Hello Class!</h1>
            Jason
          </body>
        </html>'''

        self.code03 = '''
        <html>
          <body>
            <h1>Hello Class!</h1>
            <pml>
              class HelloClass(object):
                  
                  def __init__(self,name):
                      self.name = name

                  def __str__(self):
                      return self.name
            </pml>
            <pml>
              pml = str(HelloClass("Jason"))
            </pml>
          </body>
        </html>'''

        self.rendered03 = '''
        <html>
          <body>
            <h1>Hello Class!</h1>
            Jason
          </body>
        </html>'''

        self.output = '''
        <html>
          <body>
            <h1>Hello World!</h1>
            <h2>Good Bye</h2>
          </body>
        </html>'''

        self.block = '''
        class HelloClass(object):
            
            def __init__(self,name):
                self.name = name
                
                def __str__(self):
                    return self.name
        pml = str(HelloClass("Jason"))
        '''

    def test_broken_code(self):
        '''Test submission of broken Python indentation
        '''
        try:
            pml = PMLFile(self.broken_code)
        except IndentationError:
            self.assertTrue(True)
        else:
            self.assertFalse(True)
        
    def test_pml_01(self):
        '''Test PML object.
        '''
        pml = PMLBlock(self.block,3)
        self.assertEqual(pml.leading_indent,8)
        self.assertEqual(pml.number,3)
        self.assertEqual(pml.code,self.block.split(os.linesep))

    def test_bad_code(self):
        '''Test submission of poorly indented HTML
        '''
        pml_file = PMLFile(self.bad_code)
        self.assertEqual(len(pml_file.raw_blocks),2)
        self.assertEqual(len(pml_file.code_blocks),2)
        print(pml_file)
        rendered_code = PMLFile(self.bad_code)
        print(rendered_code)
        self.assertEqual(str(pml_file),str(rendered_code))
        self.assertEqual(pml_file.place_holder_count,2)

    def test_pml_file(self):
        '''Test PML File object.
        '''
        pml_file = PMLFile(self.code03)
        self.assertEqual(len(pml_file.raw_blocks),2)
        self.assertEqual(len(pml_file.code_blocks),2)
        rendered_code = PMLFile(self.rendered03)
        print(pml_file)
        print(rendered_code)
        self.assertEqual(str(pml_file),str(rendered_code))
        self.assertEqual(pml_file.place_holder_count,2)

