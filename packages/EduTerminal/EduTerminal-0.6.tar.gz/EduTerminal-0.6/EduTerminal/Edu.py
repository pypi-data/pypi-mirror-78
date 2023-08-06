import requests
from bs4 import BeautifulSoup

class Edu:
    def __init__(self, login, password):
        self.login = login
        self.password = password
    
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0",
        'Content-type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html',
        'Referer': 'https://edu.tatar.ru/logon',
        'Upgrade-Insecure-Requests': '1'}
    
    def auth(self):
        r = self.session.get('https://edu.tatar.ru/logon', timeout=5)
        r.encoding = 'utf-8'
        response = self.session.post(url='https://edu.tatar.ru/logon/', data={'main_login': self.login, 'main_password': self.password}, headers=self.headers)
    
    def user(self, id):
        data = {"school": {}}
        r = self.session.get(f'https://edu.tatar.ru/user/{id}', timeout=5)
        soup = BeautifulSoup(r.content, "html.parser")
        soup = soup.find("div", {"id": "cabinet"})
        soup = soup.find("div",{"class": "col-md-9"})
        data['name'] = soup.find("h1").get_text()
        tags = soup.findAll("p")
        try:
            link = soup.find("img")['src']
        except:
            data['image'] = None
        else:
            data['image'] = f'https://edu.tatar.ru{link}'
        for i in range(len(tags)):
            if 'Школа:' in tags[i]:
                data['school']['name'] = tags[i+1].get_text()
                data['school']['way'] = tags[i+1].find("a")['href']
            if 'Должность:' in tags[i]:
                data['position'] = tags[i+1].get_text()
            if 'Квалификация:' in tags[i]:
                data['skill'] = tags[i+1].get_text()
            if 'Награды, звания:' in tags[i]:
                data['awards'] = tags[i+1].get_text()
            if 'Личная почта' in tags[i]:
                data['email'] = tags[i+1].get_text()
            if 'Дополнительная информация:' in tags[i]:
                data['info'] = tags[i+1].get_text()
        return data
    
    def diary(self, tunix):
        data = {"users": {}}
        r = self.session.get(f'https://edu.tatar.ru/user/diary/day?for={tunix}', timeout=5)
        soup = BeautifulSoup(r.content, "html.parser")
        tags = soup.find("table", {"class": "main"}).find("tbody").findAll("tr", {"style": "text-align: center;"})
        text = {}
        a = 0
        for i in tags:
            a += 1
            gain = i.findAll('td')
            text[str(a)] = {
                "name": gain[1].get_text(),
                "hw": gain[2].find("p").get_text(),
                "mark": gain[4].find('td'),
            }
            if not text[str(a)]["mark"] == None:
                text[str(a)]["title"] = text[str(a)]["mark"]['title']
                gg = ""
                for g in range(len(text[str(a)]["mark"].get_text())):
                    if text[str(a)]["mark"].get_text()[g].isdigit():
                        gg += text[str(a)]["mark"].get_text()[g]
                text[str(a)]["mark"] = gg
        return text

    def about(self, address):
        data = {"users": {}}
        r = self.session.get(f'https://edu.tatar.ru/facultative/index/{address}', timeout=5)
        soup = BeautifulSoup(r.content, "html.parser")
        tags = soup.find("div", {"class": "right"}).findAll("p")
        for i in tags:
            if 'Автор:' in i.get_text():
                data['users'][i.find("a").get_text()] = i.find("a")['href']
                name = i.find("a").get_text()
                break
        info = data['users'][name]
        text = ''
        for i in range(len(info)):
            if info[i].isdigit():
                text += info[i]
        data['users'][name] = text
        soup = soup.find("div", {"id": "container", "class": "clearfix"})
        try:
            soup = soup.find("div", {"class": "community_title"})
        except AttributeError:
            raise KeyError('You not auth at service.')
        else:
            medium = soup.findAll("div")
            soup = BeautifulSoup(str(medium[0]), "html.parser")
            data['teacher'] = soup.findAll("p")[1].get_text()
            data['name'] = soup.findAll("p")[0].get_text()
            r = self.session.get(f'https://edu.tatar.ru/facultative/subscribers/{address}', timeout=5)
            soup = BeautifulSoup(r.content, "html.parser").find("div", {"class": "left"})
            soup.find("div", {"class": "community_title"}).decompose()
            soup = soup.findAll("p")
            for i in soup:
                info = i.find("a")['href']
                text = ''
                for a in range(len(info)):
                    if info[a].isdigit():
                        text += info[a]
                data['users'][i.find("a").get_text()] = text
            return data
    
    def school(self, way):
        data = {}
        r = self.session.get(f'https://edu.tatar.ru/{way}', timeout=5)
        soup = BeautifulSoup(r.content, "html.parser")
        data['name'] = soup.find("table", {"id": "content"}).find("h2").get_text()
        tags = soup.find("table", {"id": "content"}).find("div", {"class": "col"}).find("tbody").findAll("tr")
        for i in tags:
            ii = i.findAll("td")
            if 'Адрес' in ii[0].get_text():
                data['address'] = ii[1].get_text()
            if 'Телефон' in ii[0].get_text():
                data['phoneNum'] = ii[1].get_text()
            if 'E-Mail' in ii[0].get_text():
                data['email'] = ii[1].get_text()
            if 'Министерство' in ii[0].get_text():
                data['ministry'] = ii[1].get_text()
            if 'Короткое название' in ii[0].get_text():
                data['shortName'] = ii[1].get_text()
            if 'Руководство' in ii[0].get_text():
                data['headTeacher'] = ii[1].get_text()
            if 'Год' in ii[0].get_text():
                data['year'] = ii[1].get_text()
        return data
    
    def profile(self):
        data = {}
        r = self.session.get('https://edu.tatar.ru/user/anketa/index', timeout=5)
        soup = BeautifulSoup(r.content, "html.parser")
        tags = soup.find("table", {"class": "tableEx"}).findAll("tr")
        for i in tags:
            ii = i.findAll("td")
            if 'Имя' in ii[0].get_text():
                data['name'] = ii[1].get_text()
            if 'Логин' in ii[0].get_text():
                data['login'] = ii[1].get_text()
            if 'Школа' in ii[0].get_text():
                data['school'] = ii[1].get_text()
            if 'Должность' in ii[0].get_text():
                data['position'] = ii[1].get_text()
            if 'Дата' in ii[0].get_text():
                data['date'] = ii[1].get_text()
            if 'Пол' in ii[0].get_text():
                data['gender'] = ii[1].get_text()
            if 'интересы' in ii[0].get_text():
                data['hobby'] = ii[1].get_text()
            if 'предметы' in ii[0].get_text():
                data['lessons'] = ii[1].get_text()
            if 'Дополнительная' in ii[0].get_text():
                data['info'] = ii[1].get_text()
            if 'Номер сертификата' in ii[0].get_text():
                data['id'] = ii[1].find("strong").get_text()
            if 'почта' in ii[0].get_text():
                data['email'] = ii[1].get_text()
        r = self.session.get('https://edu.tatar.ru/user/subscriptions/facultatives', timeout=5)
        soup = BeautifulSoup(r.content, "html.parser")
        soup = soup.findAll("div", {"class":"content", "class":"panel", "class":"panel-default"})[2].findAll("li")
        data['list'] = {}
        for i in soup:
            tags = i.find("a")
            text = ''
            for a in tags['href']:
                if str(a).isdigit():
                    text += a
            data['list'][tags.get_text()] = text
        return data

    def send(self, address, message, **known):
        if 'file' in known:
            try:
                message = str(message)
            except:
                raise TypeError("Message isn't a string.")
            else:
                data = {"facultative_comment[text]":f"<p>{message}</p>"}
                files = {}
                for i in range(len(known['file'])):
                    if not known['file'][i].closed:
                        files[f"facultative_file_field[{i+1}]"] = known['file'][i]
                        data[f"facultative_file_id[{i}]"] = "0"
                copy = self.headers
                copy.pop('Content-type')
                r = self.session.post(f'https://edu.tatar.ru/facultative/index/{address}', data=data, files=files, headers=copy)
                return r.text 
        else:
            try:
                message = str(message)
            except:
                raise TypeError("Message isn't a string.")
            else:
                data = {"facultative_comment[text]":f"<p>{message}</p>"}
                r = self.session.post(f'https://edu.tatar.ru/facultative/index/{address}', data=data, headers=self.headers)
    
    def message(self, address, id):
        r = self.session.get(f'https://edu.tatar.ru/facultative/index/{address}', timeout=5)
        soup = BeautifulSoup(r.content, "html.parser")
        medium = soup.find("div", {"id": "container", "class": "clearfix"})
        soup = BeautifulSoup(str(medium), "html.parser")
        medium = soup.find("div", {"class": "comments"})
        soup = BeautifulSoup(str(medium), "html.parser")
        medium = soup.find("p", {"class":"pages"})
        maxPage = []
        try:
            for i in medium.findAll("a"):
                maxPage.append(int(i.get_text()))
        except AttributeError:
            raise KeyError('You not auth at service.')
        else:
            r = self.session.get(f'https://edu.tatar.ru/facultative/index/{address}?page={max(maxPage)}', timeout=5)
            soup = BeautifulSoup(r.content, "html.parser")
            soup = soup.find("div", {"id": "container", "class": "clearfix"})
            soup = soup.find("div", {"class": "comments"})
            comments = soup.find("div", {"class": "mess"})
            maxM = ((max(maxPage) - 1) * 10) + len(comments) - 2
            if id > maxM:
                return None, None
            else:
                id, i = (id % 10) - 1 , (id / 10) + 1
                r = self.session.get(f'https://edu.tatar.ru/facultative/index/{address}?page={i}', timeout=5)
                soup = BeautifulSoup(r.content, "html.parser")
                medium = soup.findAll("div", {"id": "container", "class": "clearfix"})
                soup = BeautifulSoup(str(medium), "html.parser")
                medium = soup.findAll("div", {"class": "comments"})
                soup = BeautifulSoup(str(medium), "html.parser")
                comments = soup.findAll("div", {"class": "mess"})
                author = BeautifulSoup(str(BeautifulSoup(str(comments[id]), "html.parser").find("div", {"class": "user"})), "html.parser").find("strong").get_text()
                time = BeautifulSoup(str(BeautifulSoup(str(comments[id]), "html.parser").find("div", {"class": "user"})), "html.parser").find("span", {"class": "date"}).get_text()
                text = BeautifulSoup(str(BeautifulSoup(str(comments[id]), "html.parser").find("div", {"class": "mtext"})), "html.parser").get_text()
                tag = soup.findAll("div", {"class": "mess"})[id]['id']
                text = ''
                for i in range(len(tag)):
                    if tag[i] == '_':
                        text += '_text_'
                    else:
                        text += tag[i]
                text = BeautifulSoup(str(BeautifulSoup(str(comments[id]), "html.parser").find("div", {"class": "mtext"})), "html.parser").find("div", {"id": text}).get_text()
                return author, time, text
