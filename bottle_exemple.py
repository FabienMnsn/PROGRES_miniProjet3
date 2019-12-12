import bottle

#structure d'une page bottle
"""

@bottle.route("/url")
@bottle.view("html_page.tpl")
def fonction_name(){
	...
	// content
	...
	return { "title" : "this_is_a_title", "body" : "html_page_body"}


	//place this at the end of the file
bottle.run(bottle.app(), host='0.0.0.0', port='8080', debug=True, reloader=True)
"""