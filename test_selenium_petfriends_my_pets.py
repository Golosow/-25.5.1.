import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('D:\chromedriver_win32\chromedriver.exe')
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends1.herokuapp.com/login')

    yield

    pytest.driver.quit()


def test_show_my_pets():
    # Вводим email
    pytest.driver.find_element_by_id('email').send_keys('dima555g@yandex.ru')
    # Вводим пароль
    pytest.driver.find_element_by_id('pass').send_keys('se3h7y3ug6gaw')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    pytest.driver.implicitly_wait(10)
    pytest.driver.find_element_by_css_selector('div#navbarNav > ul > li > a').click()
    # Проверяем, что мы оказались на странице пользователя
    pytest.driver.save_screenshot('result_my_pets.png')
    assert pytest.driver.find_element_by_tag_name('div#navbarNav > ul > li > a').text == "Мои питомцы"
    all_my_pets = pytest.driver.find_elements_by_xpath('//tbody/tr')
    count_of_my_pets = pytest.driver.find_element_by_css_selector('div.\\.col-sm-4.left').text.split()


    images = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody/tr/th.img')
    names = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
    breed = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody/tr/td[2]')
    age = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody/tr/td[3]')

# Присутствуют все питомцы
    assert len(all_my_pets) is int(str(count_of_my_pets[(2)]))

# Хотя бы у половины питомцев есть фото.
    assert len(images) / 3 >= 0, 5

# У всех питомцев есть имя, возраст и порода.
    for i in range(len(names)):
        assert names[i].text != ''
    for i in range(len(breed)):
        assert breed[i].text != ''
    for i in range(len(age)):
        assert age[i].text != ''

# У всех питомцев разные имена.
    unique_name = "Marta"
    count_unique_name = 1
    for i in range(len(names[1:])):
        if names[i].text != unique_name:
            count_unique_name += i
            return
    assert len(names) == count_unique_name

