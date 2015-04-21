import urllib.request
import urllib.parse
import requests

API = 'http://bbs.byr.cn/open/'
USER = API + 'user'
SECTION = API + 'section'
BOARD = API + 'board'
ARTICLE = API + 'article'
THREAD = API + 'threads'
ATTACHMENT = API + "attachment"
MAIL = API + "mail"
FAVORITE = API + "favorite"
COLLECTION = API + 'collection'
SEARCH = API + "search"
REFER = API + "refer"
WIDGET = API + "widget"
BLACK = API + 'blacklist'
VOTE = API + 'vote'


class Byr:
    token = ''

    def __init__(self, token):
        self.token = token

    @staticmethod
    def add_param(key, value, data):
        # used in get_thread()
        if value is None:
            pass
        else:
            data[key] = value

    def set_req(self, url, data=None, method='GET'):
        url += '.json'
        if data is None:
            data = {}
        data['oauth_token'] = self.token
        data = urllib.parse.urlencode(data)
        if method == 'GET':
            url += '?' + data
            req = urllib.request.Request(url)
        else:
            data = data.encode()
            req = urllib.request.Request(url, data)
        return req

    @staticmethod
    def send_req(req):
        html = urllib.request.urlopen(req)
        return html.read().decode('utf-8')

    def get_user_info(self, id=None):
        if id is None:
            req = self.set_req(USER + '/getinfo')
        else:
            url = USER + '/query/' + id
            req = self.set_req(url)
        return self.send_req(req)

    def get_sections(self, name=None):
        if name is not None:
            req = self.set_req(SECTION + '/' + str(name))
        else:
            req = self.set_req(SECTION)
        return self.send_req(req)

    def get_board(self, name, mode=2, count=10 ,page=1):
        """
        get board information
        :param name: board name
        :param mode:
        :param count:
        :param page:
        :return:
        """
        data = {
            'name': name,
            'mode': str(mode),
            'count': str(count),
            'page': str(page)
        }
        req = self.set_req(BOARD + '/' + name, data)
        return self.send_req(req)

    def get_article(self, name, id, mode=None):
        """
        :param name:board name
        :param id:article of thread id
        :param mode: 0-6
        :return:json
        """
        data = {
            'mode': mode
        }
        req = self.set_req(ARTICLE + '/%s/%s' % (name, str(id)), data)
        return self.send_req(req)

    def get_thread(self, name, id, au=None, count=10, page=1):
        """
        :param name: board name
        :param id:thread id
        :param au:only show the article of this user
        :param count:
        :param page:
        :return:
        """
        data={
            'au': au,
            'count': str(count),
            'page': str(page)
        }
        req = self.set_req(THREAD + '/%s/%s' % (name, str(id)), data)
        return self.send_req(req)

    def post_article(self, name, title, content, reid=None):
        """
        :param name: board name
        :param title:
        :param content:
        :param reid: article id which you want to reply
        :return:
        """
        data = {
                'title': title,
                'content': content
        }
        self.add_param('reid', reid, data)
        req = self.set_req(ARTICLE + '/%s/post' % name, data, "POST")
        return self.send_req(req)

    def forward_article(self, name, id, target, threads=0, noref=0, noatt=0, noansi=0, big5=0):
        """
        forward article to a user
        :param name: board name
        :param id: article id
        :param target: target user id
        :param threads: as collection or not
        :param noref: keep quote or not
        :param noatt: keep attachment or not
        :param noansi: keep ansi or not
        :param big5: use big5 or not
        :return:
        """
        data={
            'target': target,
            'threads': threads,
            'noref': noref,
            'noatt': noatt,
            'noansi': noansi,
            'big5': big5
        }
        req = self.set_req(ARTICLE + '/%s/forward/%s' % (name, id), data, "POST")
        return self.send_req(req)

    def cross_article(self, name, id, target):
        """
        reproduce article to another board
        :param name:board name
        :param id: article id
        :param target:target board name
        :return:
        """
        data = {
            'target': target
        }
        req = self.set_req(ARTICLE + "/%s/cross/%s" % (name, id), data, 'POST')
        return self.send_req(req)

    def update_article(self,name, id, title, content):
        """
        :param name: board name
        :param id:article id
        :param title:
        :param content:
        :return:
        """
        data = {
            'title': title,
            'content': content
        }
        req = self.set_req(ARTICLE + "/%s/update/%s" % (name, id), data, 'POST')
        return self.send_req(req)

    def del_article(self, name, id):
        """
        :param name: board name
        :param id: article id
        :return:
        """
        data = {}
        req = self.set_req(ARTICLE + "/%s/delete/%s" % (name, id), data, "POST")
        return self.send_req(req)

    def get_attachment(self, name, id=None):
        """
        if id is None,get attachment of one article which is post by the user authorized
        else,get the attachment list of the user authorized
        :param name: board
        :param id: article id
        :return:
        """
        if id is None:
            req = self.set_req(ATTACHMENT + '/%s' % name)
        else:
            req = self.set_req(ATTACHMENT + '/%s/%s' % (name, id))
        return self.send_req(req)

    def post_attachment(self, name, fileHandle, id=None):
        """
        post attachment,rely on requests
        :param name: board name
        :param fileHandle: eg:open('index.html','rb')
        :param id:article id,if none,post the attachment to user attachment list
        :return:
        """
        data = {}
        if id is None:
            req = self.set_req(ATTACHMENT + '/%s/add' % name, data, "POST")
        else:
            req = self.set_req(ATTACHMENT + '/%s/add/%s' % (name, id), data, "POST")
        req.full_url += '?oauth_token=' + self.token
        files = {
            'file': fileHandle
        }
        html = requests.post(req.full_url, files=files)
        return html.text

    def del_attachment(self, board, name, id=None):
        data = {
            'name': name
        }
        if id is None:
            req = self.set_req(ATTACHMENT + '/%s/delete' % board, data, "POST")
        else:
            req = self.set_req(ATTACHMENT + '/%s/delete/%s' % (board, id), data, "POST")
        return self.send_req(req)

    def get_info_by_box(self, box, count=20, page=1):
        """

        :param box: inbox or outbox or deleted
        :param count:
        :param page:
        :return:
        """
        data = {
            'count': count,
            'page':page
        }
        req = self.set_req(MAIL + '/' + box, data)
        return self.send_req(req)

    def get_mailbox_info(self):
        """
        get mailbox info,including checking new mail
        :return:
        """
        req = self.set_req(MAIL + '/info')
        return self.send_req(req)

    def get_mailinfo(self, box, index):
        """

        :param box: inbox|outbox|deleted
        :param index:
        :return:
        """
        req = self.set_req(MAIL + '/%s/%s' % (box, index))
        return self.send_req(req)

    def post_mail(self, id, title=' ', content=' ', signature='0', backup='0'):
        """

        :param id:target user id
        :param title:
        :param content:
        :param signature:use signature or not
        :param backup:backup or not
        :return:
        """
        data = {
            'id':id,
            'title':title,
            'content':content,
            'signature':signature,
            'backup':backup
        }
        req = self.set_req(MAIL + '/send',data,"POST")
        return self.send_req(req)

    def forward_mail(self, box, index, target_id, noansi='0', big5='0'):
        data = {
            'target':target_id,
            'noansi':noansi,
            'big5':big5
        }
        req = self.set_req(MAIL + '/%s/forward/%s' % (box,index),data,"POST")
        return self.send_req(req)

    def reply_mail(self, box, index, title=' ', content=' ', signature='0', backup='0'):
        data = {
            'title':title,
            'content':content,
            'signature':signature,
            'backup':backup
        }
        req = self.set_req(MAIL + '/%s/reply/%s' % (box,index) ,data,"POST")
        return self.send_req(req)

    def del_mail(self, box, index):
        req = self.set_req(MAIL + '/%s/delete/%s' % (box,index),None,"POST")
        return self.send_req(req)

    def get_favorite(self, level='0'):
        """
        get favorite selection or board
        :param level:
        :return:
        """
        req = self.set_req(FAVORITE + '/' + level)
        return self.send_req(req)

    def add_favoriet(self, name, level='0', isdir='0'):
        data = {
            'name':name,
            'dir':isdir
        }
        req = self.set_req(FAVORITE + '/add/%s' % level,data,"POST")
        return self.send_req(req)

    def del_favorite(self, name, level='0', isdir='0'):
        data = {
            'name':name,
            'dir':isdir
        }
        req = self.set_req(FAVORITE + '/delete/'+level,data,"POST")
        return self.send_req(req)

    def get_collection(self, count='30', page='1'):
        data = {
            'count':count,
            'page':page
        }
        req = self.set_req(COLLECTION,data)
        return self.send_req(req)

    def add_collection(self, board, id):
        data = {
            'board': board,
            'id': id
        }
        req = self.set_req(COLLECTION + '/add',data,'POST')
        return self.send_req(req)

    def del_collection(self, id):
        data = {
            'id': id
        }
        req = self.set_req(COLLECTION + '/delete',data,"POST")
        return self.send_req(req)

    def search_board(self, board):
        data = {
            'board': board
        }
        req = self.set_req(SEARCH + '/board', data)

        return self.send_req(req)

    def search_article(self, board, title1=' ', title2=' ', titlen=' ', author=' ', day='7', m='0', attachment='0', o='0', count='30', page='1'):
        """
        :param board:board name
        :param title1: keyword
        :param title2:
        :param titlen: title does not contain the keyword
        :param author:
        :param day: how many days ago
        :param m:
        :param attachment: contain attachment or not
        :param o: only display thread or not
        :param count:
        :param page:
        :return:
        """
        data = {
            'board': board,
            'title1': title1,
            'title2': title2,
            'titlen': titlen,
            'author': author,
            'day': day,
            'm': m,
            'a': attachment,
            'o': o,
            'count': count,
            'page': page
        }
        req = self.set_req(SEARCH + '/article', data)
        return self.send_req(req)

    def search_threads(self, board, title1=' ', title2=' ', titlen=' ', author=' ', day='7', m='0', attachment='0', count='30', page='1'):
        data = {
            'board': board,
            'title1': title1,
            'title2': title2,
            'titlen': titlen,
            'author': author,
            'day': day,
            'm': m,
            'a': attachment,
            'count': count,
            'page': page
        }
        req = self.set_req(SEARCH + '/threads', data)
        return self.send_req(req)

    def get_refer(self, type, count='20', page='1'):
        """
        :param type:at|reply
        :param count:
        :param page:
        :return:
        """
        data = {
            'count': count,
            'page': page
        }
        req = self.set_req(REFER + '/' + type, data)
        return self.send_req(req)

    def get_refer_info(self, type):
        req = self.set_req(REFER + '/' + type)
        return self.send_req(req)

    def set_read(self, type, index):
        req = self.set_req(REFER + '/%s/setRead/%s' % (type,index), None, "POST")
        return self.send_req(req)

    def del_refer(self, type, index):
        req = self.set_req(REFER + '/%s/delete/%s' % (type, index), None, "POST")
        return self.send_req(req)

    def get_top_ten(self):
        req = self.set_req(WIDGET + '/topten')
        return self.send_req(req)

    def get_recommend(self):
        req = self.set_req(WIDGET + '/recommend')
        return self.send_req(req)

    def get_section_hot(self, selection_id):
        req = self.set_req(WIDGET + '/section-' + selection_id)
        return self.send_req(req)

    def get_blacklist(self, count='20', page='1'):
        data = {
            'count': count,
            'page': page
        }
        req = self.set_req(BLACK + '/list', data)
        return self.send_req(req)

    def add_black(self, id):
        data = {
            'id': id
        }
        req = self.set_req(BLACK + '/add',data,"POST")
        return self.send_req(req)

    def del_black(self, id):
        data = {
            'id':id
        }
        req = self.set_req(BLACK + '/delete', data, "POST")
        return self.send_req(req)

    def get_vote(self, id):
        req = self.set_req(VOTE + '/' + id)
        return self.send_req(req)

    def get_vote_list(self, cate='new', id=None):
        if cate != 'list':
            req = self.set_req(VOTE + '/category/' + cate)
        else:
            data = {
                'u': id
            }
            req = self.set_req(VOTE + '/category/' + cate, data)
        return self.send_req(req)

    def vote(self, id, votelist):
        url = VOTE + '/' + id
        url +='.json'
        url += '?oauth_token=' + self.token
        votedata = ''
        if type(votelist) is list:
            for i in votelist:
                votedata += 'vote[]=' + i + '&'
        else:
            votedata = 'vote=' + votelist
        votedata = votedata.encode()
        req = urllib.request.Request(url, votedata, method="POST")
        return self.send_req(req)
