import time

from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class GetComments:
    def __init__(self, driver):
        self.driver = driver

    def get_row_comments(self):
        try:

            rows_comm = self.driver.find_elements(by=By.XPATH, value=f"//*[contains(@class, 'topic-post')]")


        except Exception as es:
            print(f'Не могу получить комментарии "{es}"')
            return []

        if len(rows_comm) == 1:
            return []

        return rows_comm[1:]

    # def try_element_itter(self, old_list):
    #     good_list = []
    #
    #     for elem in old_list:
    #
    #         try:
    #             good_list.append(elem.id)
    #         except:
    #             continue
    #
    #     return good_list

    def get_author_comment(self, comm):
        try:
            author_comment = comm.find_element(by=By.XPATH, value=f".//*[contains(@class, 'names')]").text

        except:
            try:
                author_comment = comm.text.split('\n')[0]

            except:
                author_comment = ''

        return author_comment

    def get_date_comment(self, comm):
        try:
            date_comment = comm.find_element(by=By.XPATH,
                                             value=f".//*[contains(@class, 'relative-date')]")\
                .get_attribute('data-time')

        except:
            date_comment = ''

        try:
            date_comment = datetime.utcfromtimestamp(int(date_comment) / 1000)

        except:
            date_comment = ''

        return date_comment

    def get_text_comment(self, comm):
        try:
            text_comment = comm.find_element(by=By.XPATH, value=f".//*[contains(@class, 'cooked')]").text

        except:
            text_comment = ''

        return text_comment

    def get_likes_comments(self, comm):
        try:
            likes_comment = comm.find_element(by=By.XPATH, value=f".//*[contains(@class, 'like')]").text

        except:
            return 0

        if likes_comment == '':
            return 0

        return likes_comment

    def itter_rows_comm(self, rows_comm, post):

        comments_list = []

        # print(f'Начинаю обработку {len(rows_comm)}')

        for comm in rows_comm:
            comment_dict = {}

            author_comment = self.get_author_comment(comm)
            if author_comment == '':
                continue

            comment_dict['author_comment'] = author_comment

            time_comment = self.get_date_comment(comm)
            comment_dict['date_comment'] = str(time_comment.strftime('%d.%m.%Y'))

            text_comment = self.get_text_comment(comm)
            comment_dict['text_comment'] = text_comment

            like = self.get_likes_comments(comm)
            comment_dict['like_comment'] = like

            comments_list.append(comment_dict)

        post['comments'].extend(comments_list)

        return True

    def job_comments(self, post):
        old_elem = []
        post['comments'] = []

        # rows_comm = self.get_comment(5)
        _count_try = 3

        for cont_tru in range(_count_try):

            # temp_list = []

            rows_comm = self.get_row_comments()

            if rows_comm == []:
                return old_elem

            if old_elem == []:
                old_elem.extend(rows_comm)
                temp_list = rows_comm
            else:
                temp_list = []

                # old_id = self.try_element_itter(old_elem)
                old_id = [x.id for x in old_elem]

                for row in rows_comm:
                    if not row.id in old_id:
                        temp_list.append(row)
                        old_elem.append(row)


            if temp_list == []:
                return True

            response_itter = self.itter_rows_comm(temp_list, post)

            try:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            except:
                continue

            time.sleep(2)

        print(f'Собрал {len(post["comments"])} комментариев')

        return True
