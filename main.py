from datetime import datetime

from browser.createbrowser import CreatBrowser
from save_result import SaveResult
from src.post_parser import PostParser
from src.source_parse import SourceParse


def main():
    filter_count_day = 5

    browser_core = CreatBrowser()

    print(f'Парсер запущен. Получаю данные')

    data_good = SourceParse(browser_core.driver, filter_count_day).start_pars()
    #
    ower_good_data = PostParser(browser_core.driver, data_good).start_pars()

    file_name = f'{datetime.now().strftime("%H_%M_%S")}'

    SaveResult(ower_good_data).save_file(file_name)


if __name__ == '__main__':
    main()

    print(f'Работу закончил')
