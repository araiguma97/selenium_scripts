import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Todoリストを日報に変換するクラス
class TodoListToReportConverter:
    def convert(self, path):
        with open(path) as f:
            text = f.read()
        sections = text.split('---')
        return '*実績*' + sections[1] + '\r\n\r\n*予定*\r\n' + sections[0]


# Redmineを制御するクラス
class RedmineController:
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    def login(self, username, password):
        login_url = self.url + '/login'
        self.driver.get(login_url)
        
        # ユーザ名とパスワードを入力し、ログインボタンを押す
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
        
        # 件名と内容を入力し、送信ボタンを押す
        subject_textbox = self.driver.find_element_by_name('reply[subject]')
        subject_textbox.clear()
        subject_textbox.send_keys(subject)
        content_textbox = self.driver.find_element_by_name('reply[content]')
        content_textbox.send_keys(content)
        commit_button = self.driver.find_element_by_name('commit')
        commit_button.click()


# フォーマットされた日付を取得する
def get_formated_todays_date():
    time_now = datetime.datetime.now()
    year     = time_now.strftime('%Y')
    month    = time_now.strftime('%m').lstrip('0')
    day      = time_now.strftime('%d').lstrip('0')
    return year + '年' + month + '月' + day + '日'

def main():
    path     = 'C:\\Users\\[username]\\Desktop\\todo.txt'
    url      = 'https://my.redmine.jp/demo'
    username = 'developer'
    password = 'developer'
    board_id = 69
    topic_id = 398
        
    # 今日の日付を取得し、それを件名とする
    subject = subject = get_formated_todays_date()

    # Todoリストを変換し、それを内容とする
    converter = TodoListToReportConverter()
    content = converter.convert(path)

    # 内容を確認する
    print(content)
    ans = input('Write? [Y/n]: ')
    if ans == 'n':
        print('Canceled.')
        return

    # WebDriverを生成する
    options = Options()
    options.add_argument('--headless')
    capabilities = DesiredCapabilities.CHROME.copy()
    capabilities['acceptInsecureCerts'] = True
    driver = webdriver.Chrome(options=options, desired_capabilities=capabilities)

    # Redmineにログインして、返信する
    controller = RedmineController(driver, url)
    controller.login(username, password)
    controller.reply(subject, content, board_id, topic_id)

if __name__ == "__main__":
    main()
