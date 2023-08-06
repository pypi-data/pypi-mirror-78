# 简介
    xiaobaiauto2是一套自动化框架，功能覆盖UI自动化与API自动化
    意在帮助对自动化有更多需求且过多时间写代码的人群，让大家的时间
    花在业务的实现上
## 架构
    -----------------------------xiaobaiauto2---------------------------
                                      |
    --------------------------------------------------------------------
    |                            |                 |         |         |
    定时任务(xiaobaiauto2Timer)  邮件发送           数据管理   日志内容   测试报告
## 开始使用
#### 了解测试用例目录
    test
    |
    |--__init__.py
    |
    |--WebTest 
    |   |
    |   |--conftest.py
    |   |--testCases.py
    |
    |--APPTest
    |   |
    |   |--conftest.py
    |   |--testCases.py
    |
    |--APITest
    |   |
    |   |--testCases.py
    
#### 了解关键词
| 序号 | CMD | key |
| :--- | :--- | :--- |
| 1 | 打开网页 | URL |
|2 | 点击 | CLICK |
|3 | 输入 | SENDKEY |
|4 | 刷新页面 | REFRESH |
|5 | 后退 | BACK |
|6 | 关闭 | CLOSE |
|7 | 退出 | QUIT |
|8 | 标签 | CHECKTAG |
|9 | 属性[使用属性值定位] | CHECKATTR |
|10 | URL | CHECKURL |
|11 | 标题 | CHECKTITLE |
|12 | 跳转标签页[序号(1开始)] | SWITCHTOWINDOW |
|13 | Alert弹出框-[确定] | ALERT0 |
|14 | Alert弹出框-[取消] | ALERT1 |
|15 | Alert弹出框-[输入框] | ALERT2 |
|16 | Alert弹出框-[文本] | ALERT3 |
|17 | 停止时间 | WAIT |
|18 | 运行JS脚本 | SCRIPT |
|19 | 添加cookie | COOKIE |
|20 | 滑屏 | SWIPE |
|21 | 截屏 | SCREENSHOT |

#### 修改脚本
参考test目录下面的脚本

    `
    @pytest.mark.xiaobai_web
    def test_Case1(browser):
        # 以下是业务(动作)代码
        web_action(browser, cmd='打开', loc='', data='http://www.baidu.com')
        web_action(browser, '输入', '//*[@id="kw"]', '小白科技')
        web_action(browser, '点击', '//*[@id="su"]')
        web_action(browser, '停止时间', data=3)
        web_action(browser, '标题', contains_assert='小白')

若感觉关键词不足以使用，可以直接使用原生方法，示例如下

    browser.find_element_by_id('id属性值').click()
   
代码执行之前，若您需要发送邮件，请将`test_first`方法中的`email`的参数值进行自行修改即可

##### 备注
- 若APP测试需要获取toast信息可以写一个方法添加到自己的项目中,代码样例如下：
   ```
  def find_toast(self, message, timeout, poll_frequency):
        new_message = f"//*[@text=\'{message}\']"
        element = WebDriverWait(self.driver, timeout, poll_frequency).until(
            EC.presence_of_element_located((By.XPATH, new_message)))
        return element.text
  ```
  
#### 命令行运行脚本
    pytest --html=report.html --self-contained-html
    or
    pytest --html=report.html --self-contained-html -m xiaobai_web
    or
    pytest --html=report.html --self-contained-html -o log_cli=true -o log_cli_level=INFO

#### 定时任务界面运行脚本（CMD命令）
    xiaobaiauto2Timer

## 更新日志
| 版本 | 功能 |
| :---- | :---- |
| 0.0.1 | 添加邮件发送，用例排序，chrome提示框禁止等等 |
| 0.1.0.1 | 添加自动执行任务功能及UI界面 |
| 0.1.1 | fix缺陷，cmd执行xiaobaiauto2Timer |