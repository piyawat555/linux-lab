#Dependancies
from bs4 import BeautifulSoup
import requests
import json


def getJSON(html):
			
	data = {}
	data['poster'] = html.find(attrs={'class':'poster'}).find('img')['src']
	data['title'] =  html.find(itemprop='name').text.strip()
	data['rating'] = html.find(itemprop='ratingValue').text
	data['bestRating'] = html.find(itemprop='bestRating').text
	data['votes'] = html.find(itemprop='ratingCount').text
	data['rated'] = html.find(itemprop='contentRating')['content']
	tags = html.findAll("span",{"itemprop":"genre"})
	genres = []
	for genre in tags:
		genres.append(genre.text.strip())
	data['genre'] = genres	
		
	data['description'] = html.find(itemprop="description").text.strip()

	tags = html.findAll(itemprop="actors")
	actors = []
	for actor in tags:
		actors.append(actor.text.strip().replace(',',''))
	data['cast'] = actors	
		

	tags = html.findAll(itemprop="creator")
	creators = []
	for creator in tags:
		creators.append(creator.text.strip().replace(',',''))
	data['writers'] = creators	
		
	directors = []
	tags = html.findAll(itemprop="director")
	for director in tags:
		directors.append(director.text.strip().replace(',',''))
	data['directors'] = directors	
		
	json_data = json.dumps(data)
	return json_data
	
def getHTML(url):
	response = requests.get(url)
	return BeautifulSoup(response.content,'html.parser')	
	
def getURL(input):
	try:
		if input[0] == 't' and input[1] == 't':
			html = getHTML('http://www.imdb.com/title/'+input+'/')
			
		else:
			html = getHTML('https://www.google.co.in/search?q='+input)
			for cite in html.findAll('cite'):
				if 'imdb.com/title/tt' in cite.text:
					html = getHTML('http://'+cite.text)
					break
		return getJSON(html)	
	except Exception as e:
		return 'Invalid input or Network Error!'
		
	
input = raw_input("Enter IMDB ID or Title: ")
print('Getting information, Please Wait....')
print(getURL(input))
@click.command()
@click.option('--as-author', '-c', is_flag=True, help='Computer Science at UBU')
@click.argument('name', default='wichit2s', required=False)
def main(name, as_author):
    """Get Github Avatar"""
    #greet = 'Howdy' if as_cowboy else 'Hello'
    #click.echo('{0}, {1}.'.format(greet, name))
    api_user_url = 'https://api.github.com/users/{}'.format(name)
    json = requests.get(api_user_url).json()
    req = requests.get(json['avatar_url'])
    img = Image.open(StringIO(req.content))
    img.show()

