.PHONY: clean

site : site.hs
	stack build site

rebuild: site
	stack exec site rebuild

serve : rebuild
	stack exec site watch

deploy: rebuild
	rsync -ra --delete _site/ jerin@preon.iiit.ac.in:public_html/
	rsync -ra --delete .htpasswd/ jerin@preon.iiit.ac.in:.htpasswd/

clean : 
	stack exec site clean

