import cgi, cgitb 
cgitb.enable()  # for troubleshooting

#the cgi library gets vars from html
data = cgi.FieldStorage()
#this is the actual output
print "Content-Type: text/html\n"
print "The name is: " + data["name"].value
print "<br />"
print "The body is: " + data["body"].value
print "<br />"
#print data