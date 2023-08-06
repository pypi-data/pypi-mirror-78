from __future__ import print_function, unicode_literals
from colorama import init, Fore, Back, Style
from PyInquirer import prompt, print_json, Separator
from prompt_toolkit.validation import Validator, ValidationError
from examples import custom_style_2
import os 

class FolderValidator(Validator):
    def validate(self, document):
        query = document.text
        if query == '':
            raise ValidationError(
                message='Please enter something',
                cursor_position=len(document.text)) 

class PathValidator(Validator):
    def validate(self, document):
        query = document.text
        if query == '':
            raise ValidationError(
                message='Please enter something',
                cursor_position=len(document.text)) 



def prGreen(skk): print("\033[92m {}\033[00m" .format(skk)) 
def prRed(skk): print("\033[91m {}\033[00m" .format(skk)) 
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk)) 
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk)) 

html_format ="""<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
            <link rel="stylesheet" href="../css/style.css">
        </head>
        <body>
            <h1 style="color:red">Web Structuer</h1>
            {js}
        </body>
        </html>"""


que1 = [
        {
            'type': 'input',
            'name': 'folder',
            'message': 'Enter Folder Name:',
            'validate': FolderValidator
        },
        {
            'type': 'rawlist',
            'name': 'q1',
            'message': 'Choose option: ',
            'choices': ['Current Path', 'Manual Path','Quit'],
        },
        {
            'type': 'input',
            'name': 'm_path',
            'message': 'Enter Path: ',
            'validate': PathValidator,
            'when': lambda answers: answers['q1'] == 'Manual Path'
        }
    ]
que2 = [
        {
            'type': 'rawlist',
            'name': 'js',
            'message': 'Want Javascript: ',
            'choices': ['Yes','No']
        },
        {
            'type': 'rawlist',
            'name': 'css',
            'message': 'Want SCSS/CSS: ',
            'choices': ['SCSS','CSS']
        }
    ]




def create_parent_folder(path):
    folder = answers['folder']
    prCyan("The current working directory is %s" % path)
    
    pathfile = path+"\\"+ folder
    try:  
            os.mkdir(pathfile) 
            prGreen("Successfully created the directory %s " % pathfile) 
    except OSError as error:  
            print(error)   
    global pathfilesrc, pathfilecss, pathfileassetc
    pathfilesrc =pathfile+"\\"+"src"
    pathfilecss =pathfile+"\\"+"css"
    pathfileassetc =pathfile+"\\"+"assets"
    try:  
            os.mkdir(pathfilesrc)  
            os.mkdir(pathfilecss)  
            os.mkdir(pathfileassetc)
            prGreen("Successfully created the subdirectory " +"\n"+ pathfilesrc +"\n"+pathfilecss +"\n"+ pathfileassetc)  
    except OSError as error:  
            prRed(error) 



def files():
    htmlpath =pathfilesrc+"\\"+"intex.html"
    csspath =pathfilecss+"\\"+"style.css"
    javascriptpath =pathfilecss+"\\"+"script.js"
    scsspath =pathfilecss+"\\"+"style.scss"
    if answers2['js'] == 'Yes':
        javascriptfile = open(javascriptpath, "a")
        javascriptfile = open(javascriptpath, "a")
        javascript_tag = """<script type="text/javascript" src="../css/script.js"></script>"""
        htmlfile = open(htmlpath, "a")
        htmlfile.write(html_format.format(js = javascript_tag))
        htmlfile.close()
        prYellow("Successfully created HTML file") 
        prYellow("Successfully created Javascript")

    if answers2['js'] == 'No':
        htmlfile = open(htmlpath, "a")
        htmlfile.write(html_format)
        htmlfile.close()
        prYellow("Successfully created HTML file") 
            

    if answers2['css'] == 'SCSS':
        cssfile = open(scsspath, "a")
        prYellow("Successfully created scssfile")
    
    if answers2['css'] == 'CSS':
        cssfile = open(csspath, "a")
        prYellow("Successfully created CSS file")

    
    

def start():
    global answers 
    global answers2 
    answers = prompt(que1)
    if answers['q1'] == 'Quit':
        prRed("Okay as you wish.")
    else:
        if answers['q1'] == 'Current Path':
            path = os.getcwd()
            create_parent_folder(path)
            answers2 = prompt(que2)
            files()


        if answers['q1'] == 'Manual Path':
            create_parent_folder(answers['m_path'])
            answers2 = prompt(que2)
            files()

start()
        