from selenium import webdriver
from PIL import Image
from selenium.webdriver import ActionChains # 这个工具用于模拟浏览器的动作
import time

# 封装一个函数用于截图
def get_img(driver):
    time.sleep(2)
    # 截取网页的原图
    driver.save_screenshot("./page.png")
    # 将截图加载到程序中
    page_img = Image.open("./page.png")
    # 在网页原图中截取出验证码区域的图片
    code_div = driver.find_element_by_class_name("geetest_slicebg")
    # 找到上面的div在浏览器中的位置
    loc = code_div.location
    size = code_div.size
    print(loc,size)
    # 取出位置和大小信息
    left = loc["x"]
    top = loc["y"]
    right = loc["x"] + size["width"]
    bottom = loc["y"] + size["height"]
    # 根据边界的坐标来截取所有的图片范围
    code_img = page_img.crop((left*2,top*2,right*2,bottom*2))

    # code_img.show()
    return code_img


# 封装一个函数，用于根据图片的差异计算滑块所要滑动的距离
def get_distance(img1,img2):

    # 通过遍历图片上所有的像素点，找到存在像素差异的第一个像素点，取出其x位置即为滑块需要滑动的距离
    for i in range(50,img1.size[0]):
        for j in range(img1.size[1]):
            # 加载rgb值
            rgb1 = img1.load()[i,j]
            rgb2 = img2.load()[i,j]
            # 计算两张图片的rgb值的差异
            res1 = abs(rgb1[0]-rgb2[0])
            res2 = abs(rgb1[1]-rgb2[1])
            res3 = abs(rgb1[2] - rgb2[2])

            # 判断rgb三个值差异是否都大于60，如果大于就认为是缺口位置
            if res1 > 60 and res2 > 60 and res3 > 60:
                return i/2 - 6

# 封装一个函数，用于将计算出来的距离切分成一个个轨迹
def get_tracks(distance):
    # 先滑动一点点，然后再滑回来
    distance += 20

    v = 0
    t = 0.2
    # 定义一个列表，用于记录向前滑动的轨迹
    forward_tracks = []
    # 定义当前位置
    current = 0
    # 中间位置
    mid = distance * 3 / 5
    while current < distance:
        if current < mid:
            a = 2
        else:
            a = -3
        s = v*t + 0.5 * a * (t**2)
        v = v + a*t
        current += s
        # 把当前轨迹加入到轨迹列表中
        forward_tracks.append(round(s))

    # 由于我们多滑动了20，现在要划回来
    back_tracks = [-3,-3,-2,-2,-2,-2,-2,-2,-1,-1]

    return {"forward":forward_tracks,"back":back_tracks}

# 封装一个函数，用于破解验证码
def verify_code(driver):
    #1、点击验证按钮，弹出滑块验证码
    driver.find_element_by_class_name("geetest_radar_tip").click()
    #2、截取有缺口的网页图片
    img1 = get_img(driver)
    #3、去掉缺口，重新再截取出一张图片
    # 用driver执行相关的js代码，动态的去掉缺口
    js = "document.querySelector('.geetest_canvas_slice').style.display='block';document.querySelector('.geetest_canvas_slice').style.zIndex=10;document.querySelector('.geetest_canvas_fullbg').style.display='block';"
    driver.execute_script(js)

    img2 = get_img(driver)
    # img2.show()

    # 截完图以后把缺口显示出来
    js = "document.querySelector('.geetest_canvas_slice').style.display='block';document.querySelector('.geetest_canvas_slice').style.zIndex=10;document.querySelector('.geetest_canvas_fullbg').style.display='none';"
    driver.execute_script(js)

    # 4、根据有缺口和无缺口的两张图计算出滑块所需要移动的距离
    distance = get_distance(img1,img2)
    print(distance)

    # 5、模拟人类的动作进行滑动验证

    # 在滑动之前先得到轨迹
    tracks = get_tracks(distance)

    # 1) 按住滑动按钮
    btn = driver.find_element_by_class_name("geetest_slider_button")
    # 用鼠标按住
    ActionChains(driver).click_and_hold(btn).perform()

    # 2）按照一定的轨迹进行滑动

    # ActionChains(driver).move_by_offset(xoffset=distance,yoffset=0).perform()
    # 向前滑动
    for track in tracks["forward"]:
        ActionChains(driver).move_by_offset(xoffset=track, yoffset=0).perform()

    # 向后滑动
    for track in tracks["back"]:
        ActionChains(driver).move_by_offset(xoffset=track, yoffset=0).perform()

    time.sleep(0.5)
    # 3）松开手
    ActionChains(driver).release().perform()

def login_blog(url,name,password):
    # url = "https://passport.cnblogs.com/user/signin"
    driver = webdriver.Chrome()

    try:
        # 1、输入用户名和密码以登录
        driver.implicitly_wait(3) # 浏览器每运行一次操作休眠3s
        # 访问登录页
        driver.get(url=url)
        # 找到表单，将用户名和密码写入
        driver.find_element_by_id("loginName").send_keys(name)
        driver.find_element_by_id("loginPassword").send_keys(password)
        # 点击登录按钮，以弹出验证码窗口
        driver.find_element_by_id("loginAction").click()

        # 2、破解验证码
        verify_code(driver)

        time.sleep(5)
        # 返回浏览器中的cookie和响应体
        return driver.page_source,driver.get_cookies()
    except Exception as e:
        # 如果不是滑块验证码，需要手动验证
        print("请手动验证！")
        time.sleep(5)
        return driver.page_source, driver.get_cookies()
    finally:
        driver.close()








