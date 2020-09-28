import datetime
from selenium import webdriver

# https://qiita.com/memakura/items/20a02161fa7e18d8a693
# https://qiita.com/samunohito/items/40a03e1464899225e698

class Todo2Repo:
    def __init__(self):
        self.todo_path = 'C:\\Users\\[username]\\Desktop\\todo.txt'
        self.url = 'https://my.redmine.jp/demo'
        self.username = 'developer'
        self.password = 'developer'
        self.board_id = 69
        self.topic_id = 398

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
        self.write()
        self.driver.quit()

    def write(self):
        reply_subject = self.get_formated_todays_date()
        reply_content = self.get_content(self.todo_path)
        self.login(self.username, self.password)
        self.reply(reply_subject, reply_content, self.board_id, self.topic_id)

    def get_formated_todays_date(self):
        time_now = datetime.datetime.now()
        year = time_now.strftime('%Y')
        month = time_now.strftime('%m').lstrip('0')
        day = time_now.strftime('%d').lstrip('0')
        return year + '年' + month + '月' + day + '日'

    def get_content(self, path):
        with open(path) as f:
            text = f.read()
        sections = text.split('---')
        content = '*実績*' + sections[1] + '\r\n\r\n*予定*\r\n' + sections[0]
        return content

    def login(self, username, password):
        login_url = self.url + '/login'
        self.driver.get(login_url)
        
        username_textbox = self.driver.find_element_by_name('username')
        username_textbox.send_keys(username)
        
        password_textbox = self.driver.find_element_by_name('password')
        password_textbox.send_keys(password)
        
        login_button = self.driver.find_element_by_name('login')
        login_button.submit()

    def reply(self, subject, content, board_id, topic_id):
        reply_url = self.url + '/boards/' + str(board_id) + '/topics/' + str(topic_id)
        self.driver.get(reply_url)
        self.driver.execute_script("javascript:$('#reply').toggle(); $('#message_content').focus(); return false")
        
        subject_textbox = self.driver.find_element_by_name('reply[subject]')
        subject_textbox.clear()
        subject_textbox.send_keys(subject)
        
        content_textbox = self.driver.find_element_by_name('reply[content]')
        content_textbox.send_keys(content)
        
        commit_button = self.driver.find_element_by_name('commit')
        commit_button.click()

def main():
    writer = Todo2Repo()
    writer.write()

if __name__ == "__main__":
    main()
