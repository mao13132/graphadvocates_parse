import time

from datetime import datetime

from selenium.webdriver.common.by import By


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
                                             value=f".//*[contains(@class, 'relative-date')]") \
                .get_attribute('data-time')

        except:
            return ''

        try:
            date_comment = datetime.utcfromtimestamp(int(date_comment) / 1000)

        except:
            date_comment = ''

        return str(date_comment.strftime('%d.%m.%Y'))

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

    def check_replieds(self, comment):
        try:
            comment.find_element(by=By.XPATH, value=f".//button[contains(@class, 'replies')]").click()
        except:
            return []
        time.sleep(0.5)
        try:
            reply_list = comment.find_elements(by=By.XPATH, value=f".//div[contains(@aria-label, 'reply')]")
        except:
            return []

        return reply_list

    def itter_rows_comm(self, rows_comm, post):

        comments_list = []

        for comm in rows_comm:
            comment_dict = {}

            author_comment = self.get_author_comment(comm)
            if author_comment == '':
                continue

            comment_dict['author_comment'] = author_comment

            time_comment = self.get_date_comment(comm)
            comment_dict['date_comment'] = time_comment

            text_comment = self.get_text_comment(comm)
            comment_dict['text_comment'] = text_comment

            like = self.get_likes_comments(comm)
            comment_dict['like_comment'] = like

            comments_list.append(comment_dict)

            list_repost = self.check_replieds(comm)

            if list_repost != []:
                list_replieys = self.itter_rows_comm(list_repost, post)
                comments_list.extend(list_replieys)

        return comments_list

    def job_comments(self, post):
        old_elem = []
        post['comments'] = []

        _count_try = 3

        for cont_tru in range(_count_try):

            rows_comm = self.get_row_comments()

            if rows_comm == []:
                return old_elem

            if old_elem == []:
                old_elem.extend(rows_comm)
                temp_list = rows_comm
            else:
                temp_list = []

                old_id = [x.id for x in old_elem]

                for row in rows_comm:
                    if not row.id in old_id:
                        temp_list.append(row)
                        old_elem.append(row)

            if temp_list == []:
                return True

            list_comments = self.itter_rows_comm(temp_list, post)

            post['comments'].extend(list_comments)

            try:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            except:
                continue

            time.sleep(2)

        return True
