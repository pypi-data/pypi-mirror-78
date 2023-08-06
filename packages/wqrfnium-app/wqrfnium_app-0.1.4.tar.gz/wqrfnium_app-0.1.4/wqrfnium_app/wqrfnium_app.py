# -*- coding: utf-8 -*-
import os,sys
import re,time
import Levenshtein
import xlrd,xlwt
from xlutils.copy import copy
import os,platform
import configparser
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass
#----------------------------------

# diy your elements_xls_path

def create_xls(elements_xls_path):
    if not os.path.exists(elements_xls_path):
        book = xlwt.Workbook(encoding='utf-8',style_compression=0)
        book.add_sheet('Sheet1',cell_overwrite_ok=True)
        book.save(elements_xls_path)

def get_elements(icon):
    try:
        Data = xlrd.open_workbook(elements_xls_path)
    except Exception:
        print('Please put the element into the elements.xls first!')
        print('First column:icon,Second column:tmp_find_method,Third column:tmp_find_value,Fourth column:index,Fifth column:html_element')
        print('For example:seachinput,id,kw,0,<input type="text" class="s_ipt" name="wd" id="kw" maxlength="100" autocomplete="off">')
        exit(0)
    table = Data.sheet_by_name("Sheet1")
    nrows = table.nrows
    for i in range(nrows):
        element_tmp = table.cell(i,0).value
        if element_tmp == icon:
            try:
                html_element = table.cell(i,4).value
            except:
                html_element = ''
            return [table.cell(i,1).value,table.cell(i,2).value,int(table.cell(i,3).value),html_element,i]
    print('not fonund the element: [ %s ],please fixed it by yourself...'%icon)
    exit(0)

def update_elements(id,html,tmp,tmp_value,index):
    Data = xlrd.open_workbook(elements_xls_path)
    ww = copy(Data)
    ww.get_sheet(0).write(id, 1,tmp)
    ww.get_sheet(0).write(id, 2,tmp_value)
    ww.get_sheet(0).write(id, 3,index)
    ww.get_sheet(0).write(id, 4,html)
    os.remove(elements_xls_path)
    ww.save(elements_xls_path)

def input_html_element(id,html):
    Data = xlrd.open_workbook(elements_xls_path)
    ww = copy(Data)
    ww.get_sheet(0).write(id, 4, html)
    os.remove(elements_xls_path)
    ww.save(elements_xls_path)

def likescore(oldstr,newstr):
    score = Levenshtein.ratio(str(oldstr), str(newstr))
    return score

def search_new(driver,old_html):
    old_html = old_html.split(' wqrf ')

    old_text = old_html[0]
    old_resource_id = old_html[1]
    old_class = old_html[2]
    old_content_desc = old_html[3]
    old_checkable = old_html[4]
    old_checked = old_html[5]
    old_clickable = old_html[6]
    old_enabled = old_html[7]
    old_focusable = old_html[8]
    old_focused= old_html[9]
    old_scrollable = old_html[10]
    old_long_clickable = old_html[11]
    old_password = old_html[12]
    old_selected = old_html[13]
    old_bounds = old_html[14]
    #--------------------------------------------------------get all par
    new_elements = driver.find_elements_by_class_name(old_class) #必须根据一个确定不会变的东西比如class

    end_element = new_elements[0]
    end_index = 0
    tmp_score = 0
    for i in range(len(new_elements)):
        score = 0
        new_text = new_elements[i].get_attribute("text")
        new_resource_id = new_elements[i].get_attribute("resource-id")
        new_class = new_elements[i].get_attribute("class")
        new_content_desc = new_elements[i].get_attribute("content-desc")
        new_checkable = new_elements[i].get_attribute("checkable")
        new_checked = new_elements[i].get_attribute("checked")
        new_clickable = new_elements[i].get_attribute("clickable")
        new_enabled = new_elements[i].get_attribute("enabled")
        new_focusable = new_elements[i].get_attribute("focusable")
        new_focused = new_elements[i].get_attribute("focused")
        new_scrollable = new_elements[i].get_attribute("scrollable")
        new_long_clickable = new_elements[i].get_attribute("long-clickable")
        new_password = new_elements[i].get_attribute("password")
        new_selected = new_elements[i].get_attribute("selected")
        new_bounds = new_elements[i].get_attribute("bounds")

        score += likescore(old_text, new_text)
        score += likescore(old_resource_id, new_resource_id)
        score += likescore(old_class, new_class)
        score += likescore(old_content_desc, new_content_desc)
        score += likescore(old_checkable, new_checkable)
        score += likescore(old_checked, new_checked)
        score += likescore(old_clickable, new_clickable)
        score += likescore(old_enabled, new_enabled)
        score += likescore(old_focusable,new_focusable)
        score += likescore(old_focused,new_focused)
        score += likescore(old_scrollable,new_scrollable)
        score += likescore(old_long_clickable,new_long_clickable)
        score += likescore(old_password,new_password)
        score += likescore(old_selected,new_selected)
        score += likescore(old_bounds,new_bounds)

        if score > tmp_score:
            end_element = new_elements[i]
            end_index = i
            tmp_score = score
    new_html =  get_html(end_element)
    new_tmp = 'id' #use id,name
    # 这里要验证是用id的话，下标是多少
    new_tmp_value = end_element.get_attribute('resource-id')
    id_elements = driver.find_elements_by_id(new_tmp_value)
    for nid in range(len(id_elements)):
        if get_html(id_elements[nid]) == get_html(end_element):
            new_index = nid
            break
    else:
        # id情况不行，用class
        new_tmp = 'class'
        new_tmp_value = end_element.get_attribute('class')
        new_index = i
    return [end_element,new_html,new_tmp,new_tmp_value,new_index]

def get_html(element):
    new_html = ' wqrf '.join([
        str(element.get_attribute("text")),
        str(element.get_attribute("resource-id")),
        str(element.get_attribute("class")),
        str(element.get_attribute("content-desc")),
        str(element.get_attribute("checkable")),
        str(element.get_attribute("checked")),
        str(element.get_attribute("clickable")),
        str(element.get_attribute("enabled")),
        str(element.get_attribute("focusable")),
        str(element.get_attribute("focused")),
        str(element.get_attribute("scrollable")),
        str(element.get_attribute("long-clickable")),
        str(element.get_attribute("password")),
        str(element.get_attribute("selected")),
        str(element.get_attribute("bounds")),
    ])
    return new_html

def getelement(driver,icon):
    time1 = time.time()
    element = get_elements(icon)
    if element == 'error':
        raise Exception
    print('find: %s ...'%icon)
    old_html = element[3]
    try:
        el = driver.find_elements(element[0],element[1])[element[2]]
        print('success in %s s'%str(time.time()-time1)[:5])
        if old_html == '':
            html_element = get_html(el)
            input_html_element(element[-1],html_element)
        return el
    except Exception as e:
        print('find_faild,begin fix....')
        if element[-2] == '':
            print('this element:%s is you first set,but set wrong.Please set right in first time.'%icon)
            exit(0)
        newel_detail = search_new(driver,old_html)
        newel = newel_detail[0]
        new_html = newel_detail[1]
        new_tmp = newel_detail[2]
        new_tmp_value = newel_detail[3]
        new_index = newel_detail[4]
        update_elements(element[4],html=new_html,tmp=new_tmp,tmp_value=new_tmp_value,index=new_index)
        print('find success in %s s'%str(time.time()-time1)[:5])
        return newel

try:
    cfp = configparser.ConfigParser()
    cfp.read('wqrfnium.ini')
    elements_xls_path = cfp.get('Excel','elements_xls_path')
except: # create wqrfnium.ini
    cfp = configparser.ConfigParser()
    cfp["Excel"] = {"elements_xls_path":""}
    with open('wqrfnium.ini','w') as fp:
        cfp.write(fp)
    elements_xls_path = cfp.get('Excel','elements_xls_path')

def begin_wqrf(path):
    global elements_xls_path
    if 'xls' not in path.split('.')[-1]:
        if path[-1] == '/':
            path += 'elements.xls'
        else:
            path += '/elements.xls'
    if elements_xls_path != path:
        print("----------------------------------")
        print("You are changeing the elements_xls_path,the new path is %s now!"%path)
        print("你正在自定义元素表elements.xls的存放路径,新路径为：%s"%path)
        print("You'd better handle the old elements_xls : %s by yourself."%elements_xls_path)
        print("你最好处理掉旧的元素表：%s"%elements_xls_path)
        create_xls(path)
    cfp.set("Excel","elements_xls_path",path)
    with open("wqrfnium.ini","w+") as f:
        cfp.write(f)
    elements_xls_path = path


if elements_xls_path == '': #no path
    # begin to set the elements
    if 'arwin' in platform.system() or 'inux' in platform.system() :
        elements_xls_path =os.environ['HOME']+"/elements.xls"
    else:
        elements_xls_path = "C:\\elements.xls"
    print('You are first use wqrfnium,it is creating elements.xls,you must edit elements.xls and play wqrfnium after!')
    print('这是您第一次使用wqrfnium,它正在自动创建元素表elements.xls,您必须在这次启动后再去使用wqrfnium和添加元素到elements.xls等操作！')
    print('Your elements.xls tmp path is %s' % elements_xls_path)
    print('你的元素表elements.xls的临时路径是 %s'%elements_xls_path)
    print("First colum is element's icon,second is element's tmp_find_method,third is element's tmp_find_value,forth is element's index,the last is element's html_element")
    print("元素表:第一列为元素的标识,第二列为元素的临时定位方式,第三列为元素的临时定位值,第四列为元素的下标,最后一列元素的html标签源码")
    print("You can also read the README to get help or wirte email to 1074321997@qq.com")
    print("你也可以去阅读README.md来获取更多帮助,或者发送邮件到1074321997@qq.com联系作者")
    print('You can use code [begin_wqrf("your diy new elements_xls_path ")] to diy your elements_xls_path!')
    print('你可以在文件开头添加代码[begin_wqrf("你的元素表elements.path的自定义存放路径")] 来 自定义 你的元素表存放路径！')
    create_xls(elements_xls_path)
    cfp.set("Excel", "elements_xls_path", elements_xls_path)
    with open("wqrfnium.ini", "w+") as f:
        cfp.write(f)


else:
    if 'arwin' in platform.system() or 'inux' in platform.system() :
        if elements_xls_path == os.environ['HOME']+"/elements.xls": # default path
            print('Your elements.xls tmp path is default : %s'%elements_xls_path)
            print('你的elements.xls 的临时存放路径为默认：%s'%elements_xls_path)
        else:
            print('Your elements.xls tmp path is diy by yourself : %s' % elements_xls_path)
            print('你的elements.xls 的自定义存放路径为：%s' % elements_xls_path)
    else:
        if elements_xls_path == "C:\\elements.xls": # default path
            print('Your elements.xls tmp path is default : %s'%elements_xls_path)
            print('你的elements.xls 的临时存放路径为默认：%s' % elements_xls_path)
        else:
            print('Your elements.xls tmp path is diy by yourself : %s' % elements_xls_path)
            print('你的elements.xls 的自定义存放路径为：%s' % elements_xls_path)
