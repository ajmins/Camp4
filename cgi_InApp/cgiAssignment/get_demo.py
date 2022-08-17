#!C:\Users\Ajmi\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\python.exe
#(the shebang/SHArp bang line)

#this line is mandatory
print("content-type: text/html\n\n")

#os and cgi is needed for file uploading
import os 
import cgi
import html
import cgitb
cgitb.enable()

#create an instance of FieldStorage class
form = cgi.FieldStorage()

name = form.getvalue('fname','Name not provided')
email = form.getvalue('mail','Mail not provided')
password = form.getvalue('password','Password not provided')
location = form.getvalue('location','Location not provided')

emotion_list = form.getlist('emotion')

satisfaction = form.getvalue('satisfaction')

comments = form.getvalue('comments','no comments')


#avoid script injection, we can escape user input
name = html.escape(name)
email = html.escape(email)
password = html.escape(password)
comments = html.escape(comments)
location = html.escape(location)

try: #windows needs stdio set for binary mode
    import msvcrt
    #set mode for stdin and standard output(stdout)
    msvcrt.setmode(0,os.O_BINARY) #setting stdin to 0
    msvcrt.setmode(1,os.O_BINARY) #setting stdout to 1
except ImportError:
    pass

#to get the file from the nested FieldStorage instance
fileitem = form['profileimg']
imageFileName = None
#checking if a valide file was uploaded
if fileitem.filename:
    #remove path and keep only the filename 
    imageFileName = os.path.basename(fileitem.filename)
    open('files/'+imageFileName,'wb').write(fileitem.file.read())
    msg = "The file was uploaded to files/"+imageFileName
else:
    msg = "No file was uploaded"

print("""
<html>
    <head>
        <link type="text/css" rel="stylesheet" href="css/style.css">
        <title>Test Title</title>
    </head>
    <body style="background-color:rgb(222, 248, 252);">
        <div class="myheadstyle">
            <h2>Feedback Form</h2>
            <p>Name : %s </p>
            <p>Email : %s </p>
            <p>Password : %s </p>"""%(name,email,password))
print("<p> Emotions listed are: </p>")
for count, emotion in enumerate(emotion_list,1):
    print(f"{count}-{emotion}",end="<br>")

print("<p>Satisfaction level: %s </p>"%(satisfaction))

print("<p> Further comments are: %s </p>"%(comments))


if imageFileName:
    print("Profile Picture: <br><img width=\"250px\" src=\"files/%s\">" %(imageFileName))
else:
    print(f"Profile Picture:<br> {msg}" )
print("<p> Location: %s </p>"%(location))
print("""
        </div>
    </body>
</html>
""")










