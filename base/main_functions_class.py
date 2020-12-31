

class MainFunc():

    def __init__(self, session, url):
        self.request = session.get(url)
        self.text = self.request.text
        self.json_list = eval(self.request.text)

    def check_text(self, name_list):
        check_list = [i in self.text for i in name_list]
        return all(check_list)

    def check_json(self, keys_list ):
        for key in keys_list[:-5]:
            index = 0
            for part in self.json_list:
                # with open('C:\\Users\\wsu\\Desktop\\api.txt', 'a') as file:
                #     file.write(str(part)+'\n'+str(key)+'\n')
                if all([str(i) in str(part) for i in key]):
                    index+=1


            if index!=1:
                return False
        return True

