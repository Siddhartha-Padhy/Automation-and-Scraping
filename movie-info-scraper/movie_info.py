from bs4 import BeautifulSoup
import requests

headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }

URL = "https://www.rottentomatoes.com/m/"

#function to write the data into a file named with movie name
def file_writer(movie, data):
    with open(f'{movie}.txt', 'w') as file:
        for key, val in data.items():
            text = ""
            if type(val) == list:
                text = ""
                for item in val:
                    text = text + str(item) + "  "
                text = key + ': ' + text.strip().replace('  ',', ') + '\n'
                file.write(text)
            else:
                text = str(key + ': '+val+ '\n')
                file.write(text)
    print("[Task Completed]")


movie = str(input("Movie Name: "))
movie = movie.lower().replace(' ','_')

try:
    response = requests.get(URL+movie, headers=headers)
    soup = BeautifulSoup(response.text,'lxml')
    data = {}

    #tomatometer score and audience score
    top_sec = soup.find('div',attrs={'id':'topSection'})
    score_board = top_sec.find('div',attrs={'class':'thumbnail-scoreboard-wrap'})
    scores = score_board.find('score-board', attrs={'class':'scoreboard','data-qa':'score-panel'})
    data['Tomatometer Score'] = str(scores['tomatometerscore'])
    data['Audience Score'] = str(scores['audiencescore'])

    #critic consensus
    critic_sec = soup.find('section',attrs={'id':'what-to-know'})
    consensus = critic_sec.find('p',attrs={'class':'what-to-know__section-body'}).span.text.strip()
    data['Consensus'] = consensus

    #movie info
    movie_info = soup.find('section',attrs={'class':'panel panel-rt panel-box movie_info media'})
    movie_synopsis = movie_info.find('div',attrs={'id':'movieSynopsis'}).text.strip()
    data['Synopsis']  = movie_synopsis

    info = movie_info.find('ul',attrs={'class':'content-meta info'})
    info_list = info.find_all('li')

    for item in info_list:
        label = item.find('div',attrs={'class':'meta-label subtle'}).text.strip()
        label = label.replace(':','')
        if label == 'Director' or label == 'Producer' or label == 'Writer':
            values_loc = item.find('div',attrs={'class':'meta-value'})
            value_list = values_loc.find_all('a')
            value = ""
            for val in value_list:
                value = value + val.text + "  "
            value = value.strip().replace('  ',', ')
        else:
            value = item.find('div',attrs={'class':'meta-value'}).text.strip()

        data[label] = value

    #cast
    cast_sec = soup.find('section',attrs={'id':'movie-cast'})
    cast = cast_sec.find('div',attrs={'class':'castSection'})
    cast_list = cast.find_all('div',attrs={'class':'cast-item media inlineBlock'})

    names = []
    for item in cast_list:
        name = item.find('div',attrs={'class':'media-body'}).a.span.text.strip()
        names.append(name)

    data['Cast'] = names
    file_writer(movie, data)

except Exception as e:
    print("Invalid Movie Name. Retry.")
