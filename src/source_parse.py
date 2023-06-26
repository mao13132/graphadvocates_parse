import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime, timedelta


class SourceParse:
    def __init__(self, driver, filter_count_day):
        self.driver = driver
        self.url = f'https://forum.graphadvocates.com/latest'
        self.source_name = 'Graphadvocates'
        self.links_post = []
        self.filter_count_day = timedelta(filter_count_day)

    def load_page(self, url):
        try:
            self.driver.get(url)
            return True
        except Exception as es:
            print(f'Ошибка при заходе на стартовую страницу "{es}"')
            return False

    def __check_load_page(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'post-activity')]")))
            return True
        except:
            return False

    def loop_load_page(self):
        count = 0
        count_ower = 10

        while True:

            count += 1

            if count >= count_ower:
                print(f'Не смог открыть {self.source_name}')
                return False

            start_page = self.load_page(self.url)

            if not start_page:
                continue

            check_page = self.__check_load_page()

            if not check_page:
                self.driver.refresh()
                continue

            print(f'Успешно зашёл на {self.source_name}')

            return True

    def get_all_post(self):
        try:
            rows_post = self.driver.find_elements(by=By.XPATH,
                                                  value=f"//*[contains(@class, 'topic-list-body')]//tr")

        except Exception as es:
            print(f'Ошибка при получение постов"{es}"')
            return False

        return rows_post
    def load_more_page(self, count):
        for x in range(count):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

        return True

    def get_date(self, row):
        try:
            date = row.find_element(by=By.XPATH,
                                    value=f".//*[contains(@class, 'relative-date')]").get_attribute('data-time')
        except:
            date = ''

        try:
            date = datetime.utcfromtimestamp(int(date) / 1000)

        except:
            date = ''

        return date

    def filter_date(self, date):

        time_now = datetime.now()

        target_time = time_now - date

        if target_time >= self.filter_count_day:
            return False

        return True

    def get_name_post(self, row):
        try:
            name_post = row.find_element(by=By.XPATH, value=f".//a[contains(@class, 'title')]").text
        except:
            name_post = ''

        return name_post

    def get_link(self, row):
        try:
            link_post = row.find_element(by=By.XPATH, value=f".//a[contains(@class, 'title')]").get_attribute('href')
        except:
            link_post = ''

        return link_post

    def get_views(self, row):
        try:
            views_post = row.find_element(by=By.XPATH, value=f".//*[contains(@class, 'views')]").text
        except:
            views_post = ''

        return views_post


    def itter_rows_post(self, rows_post):

        for row in rows_post:

            date_post = self.get_date(row)

            if date_post == '':
                continue

            filter_date = self.filter_date(date_post)

            if not filter_date:
                continue

            name_post = self.get_name_post(row)

            link = self.get_link(row)

            views_post = self.get_views(row)

            good_itter = {}

            good_itter['name_post'] = name_post
            good_itter['link'] = link
            good_itter['views_post'] = views_post
            good_itter['date_post'] = str(date_post.strftime('%d.%m.%Y'))

            self.links_post.append(good_itter)

        return True

    def loop_get_all_post(self):

        while True:

            rows_post = self.get_all_post()

            if rows_post == []:
                return []

            date_post = self.get_date(rows_post[-1])

            target_time = datetime.now() - date_post

            if target_time >= self.filter_count_day:
                return rows_post

            self.load_more_page(1)


    def step_one_parse(self):

        rows_post = self.loop_get_all_post()

        if not rows_post:
            return False

        response = self.itter_rows_post(rows_post)

        print(f'Обнаружил {len(self.links_post)} поста (ов)')

        return True

    def start_pars(self):
        result_start_page = self.loop_load_page()

        if not result_start_page:
            return False

        response_one_step = self.step_one_parse()

        return self.links_post
