from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from database_setup import Base, Catalog, User, Item
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///item_catalog_project.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # /catalogs displays Catalog list
        if self.path.endswith("/catalogs"):
            catalogs = session.query(Catalog).all()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += "<a href='/catalogs/new'>Create a new Catalog</a></br></br>"
            for catalog in catalogs:
                output += catalog.name
                output += "</br>"
                output += "<a href='/catalogs/%s/edit'>Edit</a>" % catalog.id
                output += "</br>"
                output += "<a href='/catalogs/%s/delete'>Delete</a>" % catalog.id
                output += "</br></br>"

            output += "</body></html>"
            self.wfile.write(output)    

        if self.path.endswith("/catalogs/new"): 
            output = ""
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output += "<html><body>"
            output += '''<form method='POST' enctype='multipart/form-data' action='/catalogs/new'><h2>New Catalog Name:</h2><input name='newCatalogName' type='text' /><input type='submit' value='Submit'></form>'''
            output += "</body></html>"
            self.wfile.write(output)
            print output
            return        

         # /edit displays a catalog
        if self.path.endswith("/edit"):
            catalogIDPath = self.path.split("/")[2]
            filterCatalog = session.query(Catalog).filter_by(id = catalogIDPath).one()
            if filterCatalog != []:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = "<html><body>"
                output += "<h1>"
                output += filterCatalog.name
                output += "</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/catalogs/%s/edit'>''' % catalogIDPath
                output += '''<h2>New Catalog Name:</h2><input name='newCatalogName' type='text' placeholder = '%s'/>''' % filterCatalog.name
                output += '''<input type='submit' value='Rename'></form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return        

        # /delete displays a confirmation form to delete a catalog
        if self.path.endswith("/delete"):
            catalogIDPath = self.path.split("/")[2]
            filterCatalog = session.query(Catalog).filter_by(id = catalogIDPath).one()
            if filterCatalog != []:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = "<html><body>"
                output += "<h1>Delete %s?</h1>" % filterCatalog.name
                output += '''<form method='POST' enctype='multipart/form-data' action='/catalogs/%s/delete'>''' % catalogIDPath
                output += '''<input type='submit' value='Yes, delete please'></form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return        

    def do_POST(self):
        try:
            if self.path.endswith("/new"): 
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                newCatalogName = fields.get('newCatalogName')

                #Create new Catalog class
                newCatalog = Catalog(name = newCatalogName[0])
                session.add(newCatalog)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/catalogs')
                self.end_headers()

            if self.path.endswith("/edit"): 
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                newCatalogName = fields.get('newCatalogName')
                catalogIDPath = self.path.split("/")[2]

                #Rename the Catalog
                editCatalog = session.query(Catalog).filter_by(id = catalogIDPath).one()
                if editCatalog != []:
                    editCatalog.name = newCatalogName[0]
                    session.add(editCatalog)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/catalogs')
                    self.end_headers()
            
            if self.path.endswith("/delete"): 
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                catalogIDPath = self.path.split("/")[2]

                #Delete the Catalog
                deleteCatalog = session.query(Catalog).filter_by(id = catalogIDPath).one()
                if deleteCatalog != []:
                    session.delete(deleteCatalog)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/catalogs')
                    self.end_headers()
        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()

if __name__ == '__main__':
    main()