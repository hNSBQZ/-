# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
import flask
from flask import Flask, render_template, request, flash, session, g, make_response
import dataBaseOp

import settings

app=Flask(__name__)
app.config.from_object(settings)
app.config['SECRET_KEY']="sdfklas0lk42j"

db= dataBaseOp.DBOperator()

@app.before_request
def before_request():
    g.userName=None
    g.userPhone=None
    g.orderNo=None
    g.haveOrder=None
    if 'userPhone' in session:
        g.userPhone=session['userPhone']
    if 'userName' in session:
        g.userName=session['userName']
    if 'orderNo' in session:
        g.orderNo=session['orderNo']
    if 'haveOrder' in session:
        g.haveOrder=session['haveOrder']

@app.route("/Login",methods=["POST","GET"])
def Login():
    error=None
    if request.method=="POST":
        userName = request.form['user']
        phone = request.form['phone']
        if userName=="admin" and phone=="12345":
            return flask.redirect('/Admin')
        session.pop('userPhone',None)
        session.pop('userName',None)
        print(userName,phone)
        if db.HaveUser(phone,userName):
            session['userPhone']=phone
            session['userName']=userName
            orderNo=db.isEating(phone)
            if orderNo!="notEatingNow":
                session['orderNo']=orderNo
                return flask.redirect('/Menu')
            return flask.redirect('/Welcome')
        error='your phone is not exits,please sign up first'

    return render_template('Login.html',error=error)

@app.route("/Register",methods=["POST","GET"])
def Register():
    sign=None
    if request.method=="POST":
        userName=request.form['name']
        sex=request.form['gender']
        phone=request.form['phone']
        print(request.form)
        status=db.addUser(phone,userName,sex)
        print(status)
        if status==0:
            return render_template('Register.html',sign='Register OK')
        sign='your phone is already existed'
        print(sign)
    return render_template('Register.html',sign=sign)

@app.route("/Welcome")
def Welcome():
    db.deleteOrder(g.orderNo)
    session.pop('orderNo', None)
    if not g.userPhone:
        return flask.redirect('/Login')
    else:
        return render_template('Welcome.html',name=g.userName)

@app.route("/Profile")
def Profile():
    if not g.userPhone:
        return flask.redirect('/Login')
    userInfo=db.CheckUser(g.userPhone)
    historyOrders=db.CheckHistoryOrder(g.userPhone)
    return render_template('Profile.html',userInfo=userInfo,historyOrders=historyOrders)

@app.route("/EatingNow",methods=["POST","GET"])
def EatingNow():
    if not g.userPhone:
        return flask.redirect('/Login')
    feedback=None
    toWelcome=None
    toMenu=None
    if request.method=="POST":
        num=request.form["num"]
        print(num)
        t=db.EatingNowCheck(num,g.userPhone)
        if t[0]=="NoTable":
            feedback="对不起，这里没有可用桌子，请您稍后"
            toWelcome="您可以点击此返回首页等待"
            return render_template('EatingNow.html',feedback=feedback,toMenu=toMenu,toWelcome=toWelcome)
        else:
            session['orderNo']=t[1]
            feedback="欢迎您来到 "+t[0]+" 桌用餐"
            toMenu="点击此进入点餐界面"
            return render_template('EatingNow.html', feedback=feedback, toMenu=toMenu, toWelcome=toWelcome)
    return render_template('EatingNow.html', feedback=feedback, toMenu=toMenu, toWelcome=toWelcome)

@app.route("/Menu",methods=["POST","GET"])
def Menu():
    if not g.userPhone:
        return flask.redirect('/Login')
    sign=None
    orderedDishes=None
    totalCount=None
    '''orderedDishesReturn = db.getOrderedDishes(g.orderNo)
    if orderedDishesReturn!="noDishes":
        g.haveOrder=True
        session["haveOrder"]=True
        orderedDishes=orderedDishesReturn[0]
        totalCount = orderedDishesReturn[1]'''
    print(g.orderNo)
    Menu = db.getMenu()
    if request.method=='POST':
        print(request.form)
        submitList=[]
        allZero=True
        for dish in Menu:
            oneDishRecord={}
            amount=request.form[dish['dishNo']]
            print("hh"+amount)
            if amount!='0':
                allZero=False
                print("?")
                session['haveOrder']=True
                g.haveOrder=True
                oneDishRecord['dishNo']=dish['dishNo']
                oneDishRecord['amount']=amount
                submitList.append(oneDishRecord)
        print(submitList)
        print(g.haveOrder,allZero)
        if not allZero:
            db.addDishes(submitList,g.orderNo)
        if allZero and not g.haveOrder:
            sign="请您点餐"
        orderedDishesReturn=db.getOrderedDishes(g.orderNo)
        if orderedDishesReturn!="noDishes":
            orderedDishes=orderedDishesReturn[0]
            totalCount = orderedDishesReturn[1]
            print("zhe")
            for theDish in orderedDishes:
                print(theDish)
    return render_template("Menu.html",Menu=Menu,sign=sign,haveOrder=g.haveOrder,orderedDishes=orderedDishes,totalCount=totalCount)

@app.route("/CheckOut",methods=["POST","GET"])
def ChenckOut():
    if not g.userPhone:
        return flask.redirect('/Login')
    if not g.orderNo:
        return flask.redirect('/Welcome')
    haveCheckedOut=None
    haveUpgrade=None
    selfTotalCount=None
    session.pop('haveOrder',None)
    memberInfo=db.getMemberLevel(g.userPhone)
    memberLevel=memberInfo['memberLevel']
    discount=memberInfo['discount']
    orderedDishesReturn = db.getOrderedDishes(g.orderNo)
    orderedDishes = orderedDishesReturn[0]
    totalCount = orderedDishesReturn[1]
    finalCount=totalCount*discount
    if request.method=='POST':
        haveCheckedOut=True
        serveEvaluate=request.form["serveEvaluate"]
        cookingEvaluate=request.form["cookingEvaluate"]
        afterCheck=db.CheckOut(g.orderNo,serveEvaluate,cookingEvaluate,g.userPhone)
        if memberLevel<afterCheck['memberLevel']:
            haveUpgrade=True
            memberLevel=afterCheck['memberLevel']
        selfTotalCount=afterCheck['totalAmount']
    return render_template("CheckOut.html",orderDishes=orderedDishes,totalCount=totalCount,haveCheckedOut=haveCheckedOut\
                           ,memberLevel=memberLevel,finalCount=finalCount,haveUpgrade=haveUpgrade,selfTotalCount=selfTotalCount)


@app.route("/Admin")
def Admin():
    users = db.ComputeWorkerSalary
    # flask 模板
    len_message = len(users)
    print(users)
    print(type(users))
    print(len_message)

    return render_template("Admin.html", users=users)



@app.route("/Reserve",methods=['POST','GET'])
def Reserve():
    if not g.userPhone:
        return flask.redirect('/Login')
    historyReserve=db.getHistoryReserve(g.userPhone)
    print(g.userPhone)
    print(historyReserve)
    availableReserve=None
    Date=None
    Num=None
    if request.method=='POST':
        Date=request.form['reserveDate']
        print(Date)
        Num=request.form['peopleNumber']
        print(Num)
        availableReserve=db.getAvailableReserve(Date,Num)
        for i in range(len(availableReserve)):
            newReserve=Date+" "+availableReserve[i]
            availableReserve[i]=newReserve
        print(availableReserve)
    return render_template('Reserve.html',historyReserve=historyReserve,availableReserve=availableReserve,theDate=str(Date),theNum=str(Num))

@app.route("/MakeReserve",methods=['POST'])
def makeReserve():
    if request.method == "POST":
        Info=request.get_json()["new_result"]
        if Info:  # 判断是否为空
            print(Info)
            Date=Info['time']
            Date=Date[0:16]
            db.makeReserve(Date,g.userPhone,Info["number"])
            resp = make_response('OK')
            resp.headers['Access-Control-Allow-Origin'] = '*'
            resp.headers['Access-Control-Allow-Methods'] = 'POST'
            return resp

@app.route("/JudgeToMenu",methods=['GET'])
def JudgeToMenu():
    historyReserve=db.getHistoryReserve(g.userPhone)
    canEat=False
    for reserve in historyReserve:
        if reserve['state']=="可用餐":
            session['orderNo']=reserve['orderNo']
            return flask.redirect('/Menu')
    return render_template("JudgeToMenu.html")

@app.route("/CancelReserve",methods=['POST'])
def CancelReserve():
    if request.method == "POST":
        Info = request.get_json()["new_result"]
        if Info:  # 判断是否为空
            print(Info)
            if db.CancelReserve(Info['Date'],g.userPhone,Info['Table'])==0:
                response='OK'
            else :
                response='wrong'
            resp = make_response('response')
            resp.headers['Access-Control-Allow-Origin'] = '*'
            resp.headers['Access-Control-Allow-Methods'] = 'POST'
            return resp

if __name__ == '__main__':
    app.run()


