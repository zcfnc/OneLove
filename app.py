from flask import Flask,render_template,request
from MyDButil import MysqlPool
app = Flask(__name__)
pool = MysqlPool('config.json')

@app.route('/')
def hello_world():
    return render_template("index.html")  #加入变量传
#返回主页
@app.route('/returnMainPage',methods=['POST','GET'])
def returnToMain():
    return render_template("index.html")  #加入变量传
# 取出失败
@app.route('/fetchFailed',methods=['POST','GET'])
def fetchFailed():
    return render_template("failed.html")
# 获取结果
@app.route('/getResult',methods=['POST','GET'])
def mainPage():
    if request.method=='POST':
        name = request.form['Name']
        sex = request.form['Sex']
        want_sex = request.form['Want_Sex']
        wechat = request.form['Wechat']
        pool.insert_one(sex,wechat,want_sex)
        try:
            want_wechat = pool.fetch_one(want_sex)
            return render_template("result.html", want_wechat=want_wechat, name=name)  # 加入变量传
        except Exception :
            return render_template("failed.html",name=name)  # 加入变量传

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, threaded=True)
