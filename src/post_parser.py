import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.get_commets import GetComments


class PostParser:
    def __init__(self, driver, links_post):
        self.driver = driver
        self.links_post = links_post
        self.post_data = {}

    def load_page(self, url):
        try:

            self.driver.get(url)
            return True
        except Exception as es:
            print(f'Ошибка при заходе на "{url}" "{es}"')
            return False

    def __check_load_page(self, name_post):

        if len(name_post) > 15:
            name_post = name_post[:15]

        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, f'//*[contains(text(), "{name_post[:-3]}")]')))
            return True
        except Exception as es:
            print(f'Ошибка при загрузке "{name_post}" поста "{es}"')
            return False

    def loop_load_page(self, post):
        coun = 0
        coun_ower = 10

        while True:
            coun += 1

            if coun >= coun_ower:
                print(f'Не смог зайти в пост {post["name_post"]}')
                return False

            response = self.load_page(post['link'])

            if not response:
                continue


            result_load = self.__check_load_page(post['name_post'])


            if not result_load:
                self.driver.refresh()
                return False

            return True

    def get_theme(self):
        try:
            theme = self.driver.find_element(by=By.XPATH, value=f"//*[contains(@class, 'title-wrapper')]"
                                                                f"//*[contains(@class, 'category-name')]").text

        except:
            theme = ''

        return theme

    def get_author(self):
        try:
            author = self.driver.find_element(by=By.XPATH, value=f"//*[contains(@class, 'topic-body')]"
                                                                 f"//*[contains(@class, 'username')]").text

        except:
            author = ''

        return author

    def get_text_post(self):
        try:
            text_post = self.driver.find_element(by=By.XPATH, value=f""
                                                                    f"//*[contains(@class, 'topic-owner')]"
                                                                    f"//*[contains(@class, 'topic-body')]"
                                                                    f"//*[contains(@class, 'regular contents')]"
                                                                    f"//*[@class='cooked']").text

        except:
            text_post = ''

        return text_post

    def get_like(self):
        try:
            like = self.driver.find_element(by=By.XPATH, value=f"//*[contains(@class, 'topic-owner')]"
                                                               f"//*[contains(@class, 'topic-map')]"
                                                               f"//*[contains(@class, 'likes')]").text


        except:
            like = 0

        try:
            like = like.split('\n')[0]
        except:
            like = 0

        if like == '':
            like = 0

        return like

    def click_show_voting(self):
        try:
            self.driver.find_element(by=By.XPATH, value=f"//*[contains(text(), 'Show results')]").click()

            time.sleep(0.5)

        except:
            return False

        return True

    def get_yes_no_voting(self):
        try:
            result_voting = self.driver.find_elements(by=By.XPATH, value=f"//*[contains(@data-poll-name, 'poll2')]"
                                                                         f"//*[contains(@class, 'results')]"
                                                                         f"//*[contains(@class, 'percentage')]")

        except:
            return '0%', '0%'

        try:
            yes = result_voting[0].text
            no = result_voting[1].text

        except:
            return '0%', '0%'

        return yes, no

    def get_title_voting(self):
        try:
            title_voting = self.driver.find_element(by=By.XPATH, value=f"//*[contains(@data-poll-name, 'poll2')]"
                                                                       f"//*[contains(@class, 'poll-title')]").text

        except:
            return ''

        return title_voting

    def start_pars(self):
        for count, post in enumerate(self.links_post):

            result_load_page = self.loop_load_page(post)

            if not result_load_page:
                continue

            self.click_show_voting()

            post['title_voting'] = self.get_title_voting()

            post['yes'], post['no'] = self.get_yes_no_voting()

            name_them = self.get_theme()
            post['name_them'] = name_them

            name_author = self.get_author()
            post['name_author'] = name_author

            text_post = self.get_text_post()
            post['text_post'] = text_post

            like = self.get_like()
            post['like'] = like

            list_comments = GetComments(self.driver).job_comments(post)

            if count % 5 == 0 and count != 0:
                print(f'Собрал {count} постов')


        print(f'Собрал всего {len(self.links_post)} постов')

        return self.links_post

if __name__ == '__main__':
    from browser.createbrowser import CreatBrowser
    from src.temp import data_good

    browser_core = CreatBrowser()

    good_pars_row = PostParser(browser_core.driver, data_good).start_pars()

    print()
