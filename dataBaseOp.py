import datetime
from typing import List
#--coding:utf-8--
import pymssql

class DBOperator:
    def __init__(self):
        server = "(local)"
        user = 'sa'
        password = '123456'
        database = 'Restaurtant_2'
        self.conn=pymssql.connect(host=server,user=user,password=password,database=database,autocommit=True,charset='cp936')
        if self.conn:
            print("连接成功")
        self.cursor=self.conn.cursor(as_dict=True)
        self.now=datetime.datetime(2022,6,17,19,40)

    def HaveUser(self,phoneNum,userName)->bool:
        l=list()
        checkSentence="where telephonNo='"+phoneNum+"'"
        sql=u'select coustomerName from customer '+checkSentence
        print(sql)
        self.cursor.execute(sql.encode('cp936'))
        l=self.cursor.fetchall()
        print(l)
        if len(l) ==0:
            return False
        print(l[0]['coustomerName'])
        if l[0]['coustomerName']==userName:
            return True
        return False

    def addUser(self,phoneNum,userName,sex)->int:
        sql=u"insert into customer(telephonNo,coustomerName,sex,tatolAmount,memberLevel)\
                values('%s','%s','%s',0,0)"%(phoneNum,userName,sex)
        status=0
        print(sql)
        try:
            self.cursor.execute(sql.encode('cp936'))
        except:
            status=1
        return status

    def CheckUser(self, phone: str) -> dict:  # gq
        '''根据手机号返回客户信息'''
        inquiry1 = u"SELECT telephonNo,coustomerName,tatolAmount,customer.memberLevel,discount FROM customer,membership WHERE " \
                   u"customer.memberLevel = membership.memberLevel and" \
                   u" telephonNo=%s" % (phone)
        tabler = list()
        print(inquiry1.encode('cp936'))
        self.cursor.execute(inquiry1.encode('cp936'))
        tabler = self.cursor.fetchall()
        if tabler:
            return tabler[0]
        else:
            strr = "NO such customer"
            print(strr)
            return tabler

    def CheckHistoryOrder(self, phone: str) -> List:  # gq
        '''根据手机号返回客户历史订单'''
        inquiry1 = u"SELECT orderNo,orderDate,consumptionAmount,finalConsumption " \
                   u"FROM orders " \
                   u"WHERE consumption = 'y' " \
                   u"and customer=%s" % (phone)
        print(inquiry1.encode('cp936'))
        table = list()
        self.cursor.execute(inquiry1.encode('cp936'))
        table = self.cursor.fetchall()
        return table

    def EatingNowCheck(self, num: int, phone: str) -> tuple:  # xjf
        now = self.now
        month = now.month
        if month < 9:
            month = '0' + str(month)
        day = now.day
        if day < 9:
            day = '0' + str(day)
        hour = now.hour
        if hour < 9:
            hour = '0' + str(hour)
        table = list()

        chekSentence = "where capacity >= " + str(num) + " and tableState= " + "'e'"
        sql = "select tableNo from diningTable" + " " + chekSentence + " order by capacity"
        print(sql)
        self.cursor.execute(sql)
        table = self.cursor.fetchall()

        for tableNo in table:
            print(tableNo)
            sql = "select reserveDate from reserve where tableNo = '" + str(
                tableNo['tableNo']) + "'" + " and reserveDate between '" + str(now.year) + '-' + str(
                now.month) + '-' + str(now.day) + " 00:00:00' and '" + str(now.year) + '-' + str(now.month) + '-' + str(
                now.day) + " 23:59:59'"
            print(sql)
            self.cursor.execute(sql)
            reserveDate = self.cursor.fetchall()
            if len(reserveDate) == 0:
                print(str(tableNo['tableNo']),
                      'O' + str(phone[7:]) + str(tableNo['tableNo'][1:]) + str(month) + str(day) + str(hour))
                update_sql = "update diningTable set tableState = 'u' where tableNo = '" + str(tableNo['tableNo']) + "'"
                print(update_sql)
                self.cursor.execute(update_sql)
                insert_sql = "insert into orders(tableNo,orderNo,customer,orderDate,consumption) values('" + str(
                    tableNo['tableNo']) + "','" + 'O' + str(phone[7:]) + str(tableNo['tableNo'][1:]) + str(month) + str(
                    day) + str(hour) + "','" + str(phone) + "','" + str(
                    now.strftime('%Y-%m-%d %H:%M:%S')) + "','" + "n" + "')"
                print(insert_sql)
                self.cursor.execute(insert_sql)
                return (str(tableNo['tableNo']),
                        'O' + str(phone[7:]) + str(tableNo['tableNo'][1:]) + str(month) + str(day) + str(hour))
            else:
                for date in reserveDate:
                    reserve = datetime.datetime.strptime(str(date['reserveDate']), '%Y-%m-%d %H:%M:%S')
                    print(reserve)
                    if reserve >= now:
                        if (reserve.hour <= 14 and now.hour <= 14) or (reserve.hour >= 14 and now.hour >= 14):
                            print("同一时间")
                            break
                        else:
                            update_sql = "update diningTable set tableState = 'u' where tableNo = '" + str(
                                tableNo['tableNo']) + "'"
                            print(update_sql)
                            self.cursor.execute(update_sql)
                            insert_sql = "insert into orders(tableNo,orderNo,customer,orderDate,consumption) values('" + str(
                                tableNo['tableNo']) + "','" + 'O' + str(phone[7:]) + str(tableNo['tableNo'][1:]) + str(
                                month) + str(day) + str(hour) + "','" + str(phone) + "','" + str(
                                now.strftime('%Y-%m-%d %H:%M:%S')) + "','" + "n" + "')"
                            print(insert_sql)
                            self.cursor.execute(insert_sql)
                            return (str(tableNo['tableNo']),
                                    'O' + str(phone[7:]) + str(tableNo['tableNo'][1:]) + str(month) + str(day) + str(
                                        hour))
                    else:
                        if (now - reserve).seconds > 1800:
                            try:
                                sql = "delete from orders where orderDate = '" + str(
                                    date['reserveDate']) + "' and tableNo = '" + str(tableNo[tableNo]) + "'"
                                print(sql)
                                self.cursor.execute(sql)
                            except:
                                print("无订单信息")
                                pass
                        else:
                            if (now - reserve).seconds <= 1800:
                                break
                        print("find fit table")
                        update_sql = "update diningTable set tableState = 'u' where tableNo = '" + str(
                            tableNo['tableNo']) + "'"
                        print(update_sql)
                        self.cursor.execute(update_sql)
                        insert_sql = "insert into orders(tableNo,orderNo,customer,orderDate,consumption) values('" + str(
                            tableNo['tableNo']) + "','" + 'O' + str(phone[7:]) + str(tableNo['tableNo'][1:]) + str(
                            month) + str(day) + str(hour) + "','" + str(phone) + "','" + str(
                            now.strftime('%Y-%m-%d %H:%M:%S')) + "','" + "n" + "')"
                        print(insert_sql)
                        self.cursor.execute(insert_sql)
                        return (str(tableNo['tableNo']),
                                'O' + str(phone[7:]) + str(tableNo['tableNo'][1:]) + str(month) + str(day) + str(hour))
        return ('NoTable', 'xx')

    def getHistoryReserve(self,phone:str)->List:#szy
        sql=u"select tableNo,reserveDate from reserve where customerPhone='%s'"%phone
        self.cursor.execute(sql.encode('cp936'))
        reserveInfo=self.cursor.fetchall()
        for reserve in reserveInfo:
            if reserve['reserveDate']>self.now:
                reserve['state']="未开始"
            elif (reserve['reserveDate']+datetime.timedelta(minutes=30))<self.now:
                reserve['state']="过期"
                sql2=u"delete from orders where tableNo='%s' and orderDate='%s' and consumption='n'"%(reserve['tableNo'],reserve['reserveDate'])
                print(sql2)
                try:
                    self.cursor.execute(sql2.encode('cp936'))
                except:
                    print("fuck lizonghao")
            else:
                reserve['state']='可用餐'
            sql3=u"select orderNo from orders where tableNo='%s' and orderDate='%s' and consumption='n'"%(reserve['tableNo'],reserve['reserveDate'])
            self.cursor.execute(sql3.encode('cp936'))
            orderNoList=self.cursor.fetchall()
            if len(orderNoList)!=0:
                reserve['orderNo']=orderNoList[0]['orderNo']
        return reserveInfo

    def getAvailableReserve(self, checkDate: str, num: int) -> List:  # xjf

        available1 = list()
        available = list()
        true_available = list()
        true_reserveDate = list()
        available1.append(str(checkDate) + " 11:00:00")
        available1.append(str(checkDate) + " 12:00:00")
        available1.append(str(checkDate) + " 13:00:00")
        available1.append(str(checkDate) + " 17:00:00")
        available1.append(str(checkDate) + " 18:00:00")
        available1.append(str(checkDate) + " 19:00:00")
        available1.append(str(checkDate) + " 20:00:00")

        now = str(self.now.strftime('%Y-%m-%d %H:%M:%S'))
        now_date = str(self.now.strftime('%Y-%m-%d'))

        for date in available:
            print(date)

        if now_date == checkDate:
            print("预定今天")
            for date in available1:
                print(date)
                if now < date:
                    print(str(now) + "<" + str(date))
                    available.append(date)
        else:
            print(now_date)
            print(checkDate)
            available = available1

        print("修改后date")
        for date in available:
            print(date)

        if now_date == checkDate:
            now = self.now
            if now.hour < 14:
                chekSentence = "where capacity >= " + str(num)
                sql = "select tableNo from diningTable" + " " + chekSentence + " order by capacity"
                print(sql)
                self.cursor.execute(sql)
                table = self.cursor.fetchall()
                for tableNo in table:
                    true_reserveDate.clear()
                    print(tableNo)
                    sql = "select reserveDate from reserve where tableNo = '" + str(tableNo[
                                                                                        'tableNo']) + "'" + " and reserveDate between '" + checkDate + " 00:00:00' and '" + checkDate + " 23:59:59'"
                    print(sql)
                    self.cursor.execute(sql)
                    reserveDate = self.cursor.fetchall()
                    for date in reserveDate:
                        date = str(date['reserveDate'])
                        if datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S') < now and (
                                now - datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')).seconds > 1800:
                            print((now - datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')).seconds)
                            continue
                        else:
                            true_reserveDate.append(date)
                            for available_time in available:
                                if (date < available_time):
                                    print("日期")
                                    print(date)
                                    print("日期后时间：")
                                    print(available_time)
                                    true_reserveDate.append(available_time)
                            for date in true_reserveDate:
                                print("不可用时间")
                                print(date)

                    sql = "select 'tableState' from diningTable where tableNo ='" + str(tableNo['tableNo']) + "'"
                    print(sql)
                    self.cursor.execute(sql)
                    state = self.cursor.fetchone()

                    if state['tableState'] == 'u':
                        true_reserveDate.append(str(checkDate) + " 11:00:00")
                        true_reserveDate.append(str(checkDate) + " 12:00:00")
                        true_reserveDate.append(str(checkDate) + " 13:00:00")

                    true_available = true_available + [x for x in available if x not in true_reserveDate]

                return_result = list()

                true_available = list(set(true_available))
                true_available.sort()

                for date in true_available:
                    print("真实有效时间")
                    print(date)
                    return_result.append(str(datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').hour) + ":00-" + str(
                        datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').hour + 1) + ":00")

                for hour in return_result:
                    print(hour)
                return return_result
            else:
                chekSentence = "where capacity >= " + str(num) + " and tableState= " + "'e'"
                sql = "select tableNo from diningTable" + " " + chekSentence + " order by capacity"
                print(sql)
                self.cursor.execute(sql)
                table = self.cursor.fetchall()
                for tableNo in table:
                    true_reserveDate.clear()
                    print(tableNo)
                    sql = "select reserveDate from reserve where tableNo = '" + str(tableNo[
                                                                                        'tableNo']) + "'" + " and reserveDate between '" + checkDate + " 00:00:00' and '" + checkDate + " 23:59:59'"
                    print(sql)
                    self.cursor.execute(sql)
                    reserveDate = self.cursor.fetchall()
                    for date in reserveDate:
                        date = str(date['reserveDate'])
                        if datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S') < now and (
                                now - datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')).seconds > 1800:
                            print((now - datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')).seconds)
                            continue
                        else:
                            true_reserveDate.append(date)
                            for available_time in available:
                                if (date < available_time):
                                    print("日期")
                                    print(date)
                                    print("日期后时间：")
                                    print(available_time)
                                    true_reserveDate.append(available_time)
                            for date in true_reserveDate:
                                print("不可用时间")
                                print(date)
                    true_available = true_available + [x for x in available if x not in true_reserveDate]

                return_result = list()

                true_available = list(set(true_available))
                true_available.sort()

                for date in true_available:
                    print("真实有效时间")
                    print(date)
                    return_result.append(str(datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').hour) + ":00-" + str(
                        datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').hour + 1) + ":00")

                for hour in return_result:
                    print(hour)
                return return_result

        else:
            table = list()

            sql = "select reserveDate from reserve where reserveDate between '" + str(
                checkDate) + " 00:00:00' and '" + str(checkDate) + " 23:59:59'"
            print(sql)
            self.cursor.execute(sql)
            reserveDate = self.cursor.fetchall()
            if len(reserveDate) == 0:
                return_result = list()
                print("no reserve")
                for date in available:
                    return_result.append(str(datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').hour) + ":00-" + str(
                        datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').hour + 1) + ":00")
                return return_result
            else:
                chekSentence = "where capacity >= " + str(num)
                sql = "select tableNo from diningTable" + " " + chekSentence + " order by capacity"
                print(sql)
                self.cursor.execute(sql)
                table = self.cursor.fetchall()
                for tableNo in table:
                    true_reserveDate.clear()
                    print(tableNo)
                    sql = "select reserveDate from reserve where tableNo = '" + str(tableNo[
                                                                                        'tableNo']) + "'" + " and reserveDate between '" + checkDate + " 00:00:00' and '" + checkDate + " 23:59:59'"
                    print(sql)
                    self.cursor.execute(sql)
                    reserveDate = self.cursor.fetchall()
                    for date in reserveDate:
                        date = str(date['reserveDate'])
                        true_reserveDate.append(date)
                        for available_time in available:
                            if (date < available_time):
                                print("日期")
                                print(date)
                                print("日期后时间：")
                                print(available_time)
                                true_reserveDate.append(available_time)
                        for date in true_reserveDate:
                            print("不可用时间")
                            print(date)
                    true_available = true_available + [x for x in available if x not in true_reserveDate]

                return_result = list()

                true_available = list(set(true_available))
                true_available.sort()

                for date in true_available:
                    print("真实有效时间")
                    print(date)
                    return_result.append(str(datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').hour) + ":00-" + str(
                        datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').hour + 1) + ":00")

                for hour in return_result:
                    print(hour)
                return return_result

    def makeReserve(self, reserveDateTime: str, phone: str, num: int) -> tuple:  # xjf
        now = datetime.datetime.strptime(reserveDateTime+":00", '%Y-%m-%d %H:%M:%S')
        month = now.month
        if month < 9:
            month = '0' + str(month)
        day = now.day
        if day < 9:
            day = '0' + str(day)
        hour = now.hour
        if hour < 9:
            hour = '0' + str(hour)
        table = list()

        chekSentence = "where capacity >= " + str(num) + " and tableState= " + "'e'"
        sql = "select tableNo from diningTable" + " " + chekSentence + " order by capacity"
        print(sql)
        self.cursor.execute(sql)
        table = self.cursor.fetchall()

        for tableNo in table:
            print(tableNo)
            sql = "select reserveDate from reserve where tableNo = '" + str(
                tableNo['tableNo']) + "'" + " and reserveDate between'" + str(now.year) + '-' + str(
                now.month) + '-' + str(now.day) + " 00:00:00' and '" + str(now.year) + '-' + str(now.month) + '-' + str(
                now.day) + " 23:59:59'"
            print(sql)
            self.cursor.execute(sql)
            self.cursor.execute(sql)
            reserveDate = self.cursor.fetchall()
            if len(reserveDate) == 0:
                print("1")
                print(str(tableNo['tableNo']),
                      'O' + str(phone[7:]) + str(tableNo['tableNo'][1:]) + str(month) + str(day) + str(hour))
                insert_reserve = "insert into reserve values('" + str(tableNo['tableNo']) + "','" + str(
                    reserveDateTime) + "','" + str(phone) + "')"
                print(insert_reserve)
                self.cursor.execute(insert_reserve)
                insert_sql = "insert into orders(tableNo,orderNo,customer,orderDate,consumption) values('" + str(
                    tableNo['tableNo']) + "','" + 'O' + str(phone[7:]) + str(tableNo['tableNo'][1:]) + str(month) + str(
                    day) + str(hour) + "','" + str(phone) + "','" + str(
                    now.strftime('%Y-%m-%d %H:%M:%S')) + "','" + "n" + "')"
                print(insert_sql)
                self.cursor.execute(insert_sql)
                return (str(tableNo['tableNo']),
                        'O' + str(phone[7:]) + str(tableNo['tableNo'][1:]) + str(month) + str(day) + str(hour))
            else:
                for date in reserveDate:
                    reserve = datetime.datetime.strptime(str(date['reserveDate']), '%Y-%m-%d %H:%M:%S')
                    print(reserve)
                    if reserve >= now:
                        if (reserve.hour <= 14 and now.hour <= 14) or (reserve.hour >= 14 and now.hour >= 14):
                            print("同一时间")
                            break
                        else:
                            print("2")
                            insert_reserve = "insert into reserve values('" + str(tableNo['tableNo']) + "','" + str(
                                reserveDateTime) + "','" + str(phone) + "')"
                            print(insert_reserve)
                            self.cursor.execute(insert_reserve)
                            insert_sql = "insert into orders(tableNo,orderNo,customer,orderDate,consumption) values('" + str(
                                tableNo['tableNo']) + "','" + 'O' + str(phone[7:]) + str(tableNo['tableNo'][1:]) + str(
                                month) + str(day) + str(hour) + "','" + str(phone) + "','" + str(
                                now.strftime('%Y-%m-%d %H:%M:%S')) + "','" + "n" + "')"
                            print(insert_sql)
                            self.cursor.execute(insert_sql)
                            return (str(tableNo['tableNo']),
                                    'O' + str(phone[7:]) + str(tableNo['tableNo'][1:]) + str(month) + str(day) + str(
                                        hour))
                    else:
                        if (now - reserve).seconds > 1800:
                            try:
                                sql = "delete from orders where orderDate = '" + str(
                                    date['reserveDate']) + "' and tableNo = '" + str(tableNo[tableNo]) + "'"
                                print(sql)
                                self.cursor.execute(sql)
                            except:
                                print("无订单信息")
                                pass
                        else:
                            if (now - reserve).seconds <= 1800:
                                break
                        print("find fit table")
                        print("3")
                        insert_reserve = "insert into reserve values('" + str(tableNo['tableNo']) + "','" + str(
                            reserveDateTime) + "','" + str(phone) + "')"
                        print(insert_reserve)
                        self.cursor.execute(insert_reserve)
                        insert_sql = "insert into orders(tableNo,orderNo,customer,orderDate,consumption) values('" + str(
                            tableNo['tableNo']) + "','" + 'O' + str(phone[7:]) + str(tableNo['tableNo'][1:]) + str(
                            month) + str(day) + str(hour) + "','" + str(phone) + "','" + str(
                            now.strftime('%Y-%m-%d %H:%M:%S')) + "','" + "n" + "')"
                        print(insert_sql)
                        self.cursor.execute(insert_sql)
                        return (str(tableNo['tableNo']),
                                'O' + str(phone[7:]) + str(tableNo['tableNo'][1:]) + str(month) + str(day) + str(hour))
        print("no table can reserve")
        # return ('T1', 'O88791060719')

    def CancelReserve(self,reserveDateTime:str,phone:str,table:str)->int:#szy
        sql1 = "DELETE FROM reserve WHERE reserveDate='%s' AND customerPhone = '%s' AND tableNo='%s'" \
               % (reserveDateTime, phone, table)
        sql2 = "DELETE FROM orders WHERE orderDate='%s' AND customer='%s' AND tableNo='%s'" \
               % (reserveDateTime, phone, table)
        status = 0
        try:
            self.cursor.execute(sql1)
        except:
            status=1
        try:
            self.cursor.execute(sql2)
        except:
            status = 1
        return status

    def addDishes(self,dishForm:List,orderNo:str)->int:#gq
        inquiry1 = u"SELECT consumption " \
                   u"FROM orders " \
                   u"where orderNo = '%s'" % (orderNo)
        print(inquiry1.encode('cp936'))
        self.cursor.execute(inquiry1.encode('cp936'))
        table = self.cursor.fetchall()
        if table == [{'consumption': 'y'}]:
            for tables in dishForm:
                sre = tables['dishNo']
                scr = tables['amount']
                inquiry7 = u"SELECT orderNo,dishNo " \
                           u"FROM orderDish " \
                           u"where orderNo = '%s'" \
                           u"      and dishNo = '%s'" % (orderNo, sre)
                print(inquiry7.encode('cp936'))
                self.cursor.execute(inquiry7.encode('cp936'))
                tawss = self.cursor.fetchall()
                if tawss:
                    inquiry6 = u"update  orderDish set amount = amount + %s " \
                               u"where orderNo = '%s'" \
                               u"      and dishNo = '%s'" % (scr,orderNo, sre)
                    print(inquiry6.encode('cp936'))
                    self.cursor.execute(inquiry6.encode('cp936'))
                else:
                        inquiry6 = u"insert into orderDish(orderNo,dishNo,amount) " \
                           u"values ('%s','%s','%s')" % (orderNo, sre, scr)
                        print(inquiry6.encode('cp936'))
                        self.cursor.execute(inquiry6.encode('cp936'))
            return 0
        else:
            inquiry2 = u"update orders " \
                       u"set consumption = 'y' " \
                       u"where orderNo = '%s'" % (orderNo)
            print(inquiry2.encode('cp936'))
            self.cursor.execute(inquiry2.encode('cp936'))
            inquiry3 = u"select  staffNo " \
                       u"from staff " \
                       u"where post = 'w'" \
                       u"order by NEWID()"
            print(inquiry3.encode('cp936'))
            self.cursor.execute(inquiry3.encode('cp936'))
            dict1 = {}
            dict1 = self.cursor.fetchone()
            s = dict1['staffNo']
            inquiry4 = u"insert into serve(staffNo,orderNo)" \
                       u"values('%s','%s')" % (s, orderNo)
            print(inquiry4.encode('cp936'))
            self.cursor.execute(inquiry4.encode('cp936'))
            for tables in dishForm:
                sre = tables['dishNo']
                scr = tables['amount']
                inquiry5 = u"insert into orderDish " \
                       u"values('%s','%s','%s')" % (orderNo, sre, scr)
                print(inquiry5.encode('cp936'))
                self.cursor.execute(inquiry5.encode('cp936'))
            return 0

    def getOrderedDishes(self,orderNo):
        sql=u"select dish.dishNo,dish.dishName,orderDish.amount,dish.price,dish.memberPrice from dish,orderDish where orderDish.dishNo=dish.dishNo and orderNo='%s'"%(orderNo)
        self.cursor.execute(sql.encode('cp936'))
        print(sql)
        L=self.cursor.fetchall()
        print(L)
        if L is None:
            return "noDishes"
        sql_1=u"select customer from orders where orderNo='%s'"%orderNo
        self.cursor.execute(sql_1.encode('cp936'))
        phoneNum=self.cursor.fetchall()[0]['customer']
        sql_2=u"select memberLevel from customer where telephonNo='%s'"%phoneNum
        self.cursor.execute(sql_2.encode('cp936'))
        memberLevel = self.cursor.fetchall()[0]['memberLevel']
        totalCost=0
        print(memberLevel)
        for dish in L:
            if memberLevel>0:
                singleCost=dish['memberPrice']
            else:
                singleCost=dish['price']
            theCost=singleCost*dish['amount']
            dish['singleCost']=singleCost
            dish['theCost']=theCost
            totalCost+=theCost
        return L,totalCost
        #return ([{'dishNo': 'D1', 'dishName': '香酥饼干', 'amount': 2, 'price': 40.0, 'memberPrice': 35.0, 'singleCost': 35.0, 'theCost': 70.0}, {'dishNo': 'D2', 'dishName': '现磨咖啡', 'amount': 2, 'price': 50.0, 'memberPrice': 45.0, 'singleCost': 45.0, 'theCost': 90.0}, {'dishNo': 'D3', 'dishName': '芝士汉堡', 'amount': 1, 'price': 90.0, 'memberPrice': 85.0, 'singleCost': 85.0, 'theCost': 85.0}], 245.0)

    def CheckOut(self, orderNo: str, serveEvaluate: int, cookingEvaluate: str, phoneNo: str) -> dict:  # szy
        dict0 = {"phoneNo": "18810918879", "tableNo": "T1", "orderNo": orderNo,
                 "orderDate": "2022-06-07 19:00:00",
                 "orderEndDate": "2022-6-17 19:00:00",
                 "memberLevel": 0, "consumptionAmount": 0, "finalConsumption": 0, "totalAmount": 0}
        sql1 = u"UPDATE cooking SET evaluate = %s  WHERE  orderNo = '%s'" % (cookingEvaluate, orderNo)
        sql2 = u"UPDATE serve SET evaluate = CONVERT(int,'%s')  WHERE  orderNo = '%s'" % (serveEvaluate, orderNo)
        sql3 = u"UPDATE orders SET orderEndDate = CONVERT(smalldatetime,'%s') where orderNo = '%s'" % (
        str(self.now), orderNo)
        amount = 0

        try:
            self.cursor.execute(sql1)
            self.cursor.execute(sql2)
            self.cursor.execute(sql3)

        except:
            print(sql1)
        sql4 = u"SELECT memberLevel FROM customer where telephonNo=(select customer from orders where orderNo= '%s')" % orderNo
        sql10 = "select customer from orders where orderNo= '%s'" % orderNo
        self.cursor.execute(sql4)
        dict0['memberLevel'] = self.cursor.fetchall()[0]['memberLevel']
        self.cursor.execute(sql10)
        dict0['phoneNo'] = self.cursor.fetchall()[0]['customer']
        sql5 = u"SELECT discount FROM membership where memberLevel=%s" % dict0.get('memberLevel')
        self.cursor.execute(sql5)
        discount0 = self.cursor.fetchone()
        discount = discount0.get('discount')
        sql6 = u"SELECT orderDish.amount,dish.memberPrice from  orderDish, dish  where orderNo= '%s' and  dish.dishNo=orderDish.dishNo" % orderNo
        try:
            self.cursor.execute(sql6)
            result0 = self.cursor.fetchall()  # 获取菜品数量和对应价格

        except:
            print("1")
        i = 0
        print(result0)
        while i < len(result0):
            k = result0[i]
            m = k.get('amount')
            n = k.get('memberPrice')

            s = float(m) * float(n)
            amount = amount + s
            i = i + 1
        dict0['consumptionAmount'] = amount
        dict0['finalConsumption'] = amount * discount

        try:
            sql7 = u"UPDATE customer SET tatolAmount = tatolAmount + %s where telephonNo='%s'" % (
                dict0['finalConsumption'], dict0['phoneNo'])
            self.cursor.execute(sql7)  # 更新总消费额
            sql11 = u"UPDATE orders SET finalConsumption = %s where orderNo='%s'" % (
                dict0['finalConsumption'], dict0['orderNo'])
            self.cursor.execute(sql11)
        except:
            print("ERROR2")

        try:

            sql8 = u"SELECT customer,orderDate, tableNo FROM orders where customer='%s'" % dict0['phoneNo']
            self.cursor.execute(sql8)
            result1 = self.cursor.fetchall()
            dict0['phoneNo'] = result1[0]['customer']
            dict0['orderDate'] = str(result1[0]['orderDate'])
            dict0['tableNo'] = result1[0]['tableNo']
            sql12 = u"SELECT tatolAmount FROM customer where telephonNo= '%s'" % dict0['phoneNo']
            self.cursor.execute(sql12)
            result2 = self.cursor.fetchall()
            dict0['totalAmount'] = result2[0]['tatolAmount']
            sql13 = u"SELECT memberLevel FROM customer where telephonNo= '%s'" % dict0['phoneNo']
            self.cursor.execute(sql13)
            result3 = self.cursor.fetchall()
            dict0['memberLevel'] = result3[0]['memberLevel']
        except:
            print("ERROR1")

        return dict0


    @property
    def ComputeWorkerSalary(self) -> List:  # lzh
        sql_getstaffno_W = "EXEC getstaffno_W"
        self.cursor.execute(sql_getstaffno_W)
        staffno_W = self.cursor.fetchall()
        # print(staffno_W)

        # 获取厨师名单
        sql_getstaffno_C = "EXEC getstaffno_C"
        self.cursor.execute(sql_getstaffno_C)
        staffno_C = self.cursor.fetchall()
        # print(staffno_C)

        # 计算服务员绩效
        for d in range(0, len(staffno_W)):
            tmp = staffno_W[d]["staffNo"]
            self.cursor.execute("EXEC countMeritPay_W %s" % tmp)

        # 计算厨师绩效
        for d in range(0, len(staffno_C)):
            tmp = staffno_C[d]["staffNo"]
            self.cursor.execute("EXEC countMeritPay_C %s" % tmp)

        # 计算服务员扣款
        for d in range(0, len(staffno_W)):
            tmp = staffno_W[d]["staffNo"]
            self.cursor.execute("EXEC countDeduction_W %s" % tmp)

        # 计算厨师扣款
        for d in range(0, len(staffno_C)):
            tmp = staffno_C[d]["staffNo"]
            self.cursor.execute("EXEC countDeduction_C %s" % tmp)

        # 计算员工实付工资
        for d in range(0, len(staffno_W)):
            tmp = staffno_W[d]["staffNo"]
            self.cursor.execute("EXEC countTotalSalary %s" % tmp)
        for d in range(0, len(staffno_C)):
            tmp = staffno_C[d]["staffNo"]
            self.cursor.execute("EXEC countTotalSalary %s" % tmp)

        # 获取员工实际账单
        ComputeWorkerSalary = []
        print(type(ComputeWorkerSalary))
        val_222 = []
        try:
            for d in range(0, len(staffno_W)):
                tmp = staffno_W[d]["staffNo"]
                self.cursor.execute("EXEC showComputeWorkerSalary %s" % tmp)
                val_222.append(self.cursor.fetchall())
            for d in range(0, len(staffno_C)):
                tmp = staffno_C[d]["staffNo"]
                self.cursor.execute("EXEC showComputeWorkerSalary %s" % tmp)
                val_222.append(self.cursor.fetchall())
            # for ComputeWorkerSalary in ComputeWorkerSalary:
            # print(ComputeWorkerSalary)
            # print(ComputeWorkerSalary[1][0]["staffNo"])
            for m in range(0, len(val_222)):
                ComputeWorkerSalary.append(val_222[m][0])
            print(type(val_222[0][0]))
            # print(ComputeWorkerSalary)

            # 有这个遍历居然会从列表变为字典?
            # for ComputeWorker in ComputeWorkerSalary:
            #     print(ComputeWorkerSalary)
            print(ComputeWorkerSalary)
            # gggg = [ComputeWorkerSalary]
            print(type(ComputeWorkerSalary))
            # print(gggg)
        except Exception as e:
            print(e)
            print("失败")

        return ComputeWorkerSalary

    def getMenu(self):
        sql=u"select * from dish"
        self.cursor.execute(sql.encode('cp936'))
        l=self.cursor.fetchall()
        return l

    def deleteOrder(self,orderNo):
        if orderNo is None:
            return
        sql1=u"update diningTable set tableState='e' where tableNo=(select tableNo from orders where orderNo='%s')"%orderNo
        self.cursor.execute(sql1.encode('cp936'))
        sql=u"delete from orders where orderNo='%s'"%orderNo
        status=0
        try:
            self.cursor.execute(sql.encode('cp936'))
        except:
            status=1
        print("deleteStatus"+str(status))
        return status

    def getMemberLevel(self,phoneNo):
        sql=u"select membership.memberLevel,discount from customer,membership where telephonNo='%s' and customer.memberLevel=membership.memberLevel"%phoneNo
        self.cursor.execute(sql)
        return self.cursor.fetchall()[0]

    def isEating(self,phoneNo):
        '''sql = u"select orderNo,tableNo,orderEndDate from orders where customer='%s' and orderNo not in \
                (select orderNo from reserve where reserve.customerPhone='%s')" % (phoneNo, phoneNo)
        sql1 = u"select tableNo from diningTable where tableState='u'"
        self.cursor.execute(sql.encode('cp936'))
        L1 = self.cursor.fetchall()
        self.cursor.execute(sql1.encode('cp936'))
        L2 = self.cursor.fetchall()
        print(L1)
        print(L2)
        for eatingInfo in L1:
            if eatingInfo['orderEndDate'] is None:
                tableNo = eatingInfo['tableNo']
                for table in L2:
                    if table['tableNo'] == tableNo:
                        return eatingInfo['orderNo']'''
        return "notEatingNow"

    def closeAll(self):
        self.cursor.close()
        self.conn.close()

db=DBOperator()
print(db.getHistoryReserve('18810569201'))
