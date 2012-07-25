'''
Created on Nov 4, 2011

@author: Manuel Miranda (manu.mirandad@gmail.com)
'''
import sys 
try:
    import mechanize
    import cookielib
    import random
    import string
    import re
except ImportError:
    print "Library mechanize, cookielib or re are missing. Install them please"
    sys.exit(-1)


__PASSWORD='adminadmin'

class FacebookAccess(object):
    
    __AUTHPAGE='http://www.facebook.com/'
    __AUTHFORM='login_form'
    __USERNAME='amysmithdoe@hotmail.com'
    __ADVSEARCHFORM='WOS_AdvancedSearch_input_form'
    __PAPERSOPTFORM='output_form'
    __SAVEFILEFORM='etsForm'
    __CHARS="abcd"                       # string.ascii_lowercase + string.ascii_uppercase + string.digits
    __SIZE=8
    
    #br=None
    
    def __init__(self):
        '''
        Set browser
        '''
        #Initialize browser
        self.br = mechanize.Browser()
        # Browser options
        self.br.set_handle_equiv(True)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_robots(False)
        
        #Cookie handler
        cj = cookielib.LWPCookieJar()
        self.br.set_cookiejar(cj)



#=======================================================================#
    def openAuthUrlSubmitAuthForm(self,password,a=0):
        """
        openUrlAuthForm() returns mechanize.Browser or None
        
        Function used to open the specified __URL and submit __USERNAME and __PASSOWRD to the __FORM of this __URL    
        """
        try:
            self.br.open(self.__AUTHPAGE) #Login
            assert self.br.viewing_html()        
        except (mechanize.URLError,mechanize.BrowserStateError) as e:
            print "openUrlAuthForm:",e,"=> Check __AUTHURL value"
            return None  
        
        try:
            self.br.select_form(nr=0)
            self.br['email']=self.__USERNAME
            self.br['pass']=str(password)
            self.br.form.set_all_readonly(False)
            self.br.submit()
        except mechanize.FormNotFoundError as e:
            print "openAuthUrlSubmitAuthForm:",e,"=> Check __AUTHFORM value"
            return None
            
        return self.br
    
    def passwordChecker(self):
        
        while (True):
            password=''.join(random.choice(self.__CHARS) for x in range(self.__SIZE))
            
            br=self.openAuthUrlSubmitAuthForm(self,password)
            try:
                br.select_form(name="navSearch")
                print "Found!!:",password
                break
            except mechanize.FormNotFoundError as e:
                print "Password ",password," failed"
                pass


            
    def extractFriendButtons(self,br_actual):
	page = br_actual.response().read()
    	links = []
	#while True:
        m=re.search('<input\ value=\"Add\ Friend\"\ type=\"button\"\ id=\"([a-zA-Z0-9]{6}\_[0-9]{2})\"\>',page)
#input\ value=\"Add\ friend\"\ type=\"button\"\ id=\"(.*)\"',page
	if m:
	    print m.group(1)
            links.append(m.group(1))
	    endpos=page.find(m.group(1))
            page = page[endpos:]
        else:
            pass
        return links



if __name__ == '__main__':
    import FacebookAccess
    f = open('/tmp/workfile', 'w')
    w=FacebookAccess.FacebookAccess()
    #br=w.passwordChecker() Brute force kind of...
    if sys.argv[1]: 
    	br=w.openAuthUrlSubmitAuthForm(__PASSWORD)
    	#print w.openAuthUrlSubmitAuthForm().response().read()

    f.write(br.response().read())
    br.open("http://www.facebook.com/find-friends/browser/?ref=tn")
    l=w.extractFriendButtons(br)
    print l
    f.close()    
    
