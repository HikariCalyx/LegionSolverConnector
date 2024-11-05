from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import os
from pathlib import Path
import requests
import json
import union_level_calculator as ulc
from jobName import union_card_effect_type_cn as ucet, jobNameDict as jnd, union_card_tier_number_cn as uctn
import dialog

cms_world_list = {
    "路西德": {'AreaID': 1, 'ServerID': 0},
    "威尔": {'AreaID': 1, 'ServerID': 1},
    "奥尔卡": {'AreaID': 1, 'ServerID': 2},
    "戴米安": {'AreaID': 2, 'ServerID': 30},
    "希拉": {'AreaID': 3, 'ServerID': 60},
    "班雷昂": {'AreaID': 4, 'ServerID': 90},
    "麦格纳斯": {'AreaID': 5, 'ServerID': 120},
    # "测试区": {'AreaID': 999, 'ServerID': 100},
}

if __name__ == '__main__':
    if Path('./chromedriver.exe').exists():
        driver = webdriver.Chrome()
    elif Path('./msedgedriver.exe').exists():
        driver = webdriver.ChromiumEdge()
    else:
        print('异常：未找到浏览器驱动')
        print('提示：请下载对应版本的浏览器驱动，并放置于目录：' + os.getcwd())
        print('chrome: http://npm.taobao.org/mirrors/chromedriver/')
        print('edge: https://developer.microsoft.com/microsoft-edge/tools/webdriver/')
        input()
        exit(0)

    driver.set_window_size(width=1366, height=900, windowHandle="current")
    driver.get('https://login.u.sdo.com/sdo/Login/LoginFrameFC.php?pm=2&appId=991000350&areaId=1&customSecurityLevel=2&target=iframe%810%853_param=from%3D991000350&returnURL=https%3A%2F%2Fmxdact%2Eweb%2Esdo%2Ecom%2Fproject%2Fmxdts%2Flogin%2Easp?reurl=index.asp')
    # 自动跳转到叨鱼扫码登录
    driver.find_element(By.ID, 'isAgreementAccept').click()
    driver.find_element(By.ID, 'nav_btn_code2d').click()

    while(driver.current_url != 'https://mxdact.web.sdo.com/project/mxdts/index.asp'):
        sleep(0.1)

    cookie_cms = driver.get_cookies()
    get_legion_cookie = {}
    for i in cookie_cms:
        if i['domain'] == 'mxdact.web.sdo.com':
            get_legion_cookie.update({i['name']: i['value']})
            
    driver.get('about:blank')            
    print(dialog.create_selection_dialog('请选择区服', list(cms_world_list)))

    legion_info = json.loads(requests.get('https://mxdact.web.sdo.com/project/mxdts/inc/GetCharacter.asp', params=cms_world_list['威尔'], cookies=get_legion_cookie).text)['data']

    class_combo = []
    for i in legion_info:
        entry = [{'char_name': i['character_name'], 'job': int(i['career']), 'jobName': jnd[int(i['career'])], 'level': int(i['character_level'])}]
        class_combo += entry

    for i in class_combo:
        i.update(ulc.get_union_effect(i['job'], i['level']))
    for i in class_combo:
        if i['job'] % 100 == 0 or i['job'] % 100 == 1:
            class_combo.remove(i)
    legion_level = ulc.get_union_level(class_combo)
    print("Your Maple Legion level is: ", legion_level)
    if ulc.max_legion_member_quantity(legion_level) < len(class_combo):
        print('maximum legion character quantity is', ulc.max_legion_member_quantity(legion_level), 'but you have', len(class_combo), 'character(s) available')
        selected_items = dialog.create_multi_select_list(class_combo, dialog.additional_data, ulc.max_legion_member_quantity(legion_level))
    ldp = ulc.get_usable_grid_dict(selected_items)
    ldp.pop('C', None)

    driver.get('https://xenogents.github.io/LegionSolver/')
    Select(driver.find_element(By.ID, 'languageSelectBox')).select_by_visible_text('CMS')
    for i, j in zip(range(1, 16), ldp):
        driver.find_element(By.ID, 'piece' + str(i)).clear()
        driver.find_element(By.ID, 'piece' + str(i)).send_keys(str(ldp[j]))

    DISCONNECTED_MSG = 'Unable to evaluate script: no such window'

    while True:
        if DISCONNECTED_MSG in str(driver.get_log('driver')):
            break
        sleep(1)