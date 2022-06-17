create database Restaurtant_2

use Restaurtant_2;

create table membership(
memberLevel int primary key check(memberLevel >= 0),
consumptionAmout int not null,
discount float);


create table customer(
telephonNo char(11) primary key,
coustomerName varchar(15) not null,
tatolAmount float not null,
sex char(1) check(sex = 'f' or sex = 'm'),
memberLevel int not null check(memberLevel >= 0),
foreign key(memberLevel) references membership(memberLevel));


create table diningTable(
tableNo char(2) primary key,
capacity int not null,
tableState char(1) check(tableState = 'e' or tableState = 'u' ));


create table dish(
dishNo char(2) primary key,
dishName varchar(15) not null,
dishIntroduction varchar(30),
price float not null,
memberPrice float);


create table reserve(
tableNo char(2) references diningTable(tableNo),
reserveDate smalldatetime,
customerPhone char(11),
primary key(tableNo,reserveDate),
foreign key(customerPhone) references customer(telephonNo));


create table orders(
orderNo char(12) primary key,
customer char(11) references customer(telephonNo),
orderDate smalldatetime,
orderEndDate smalldatetime,
consumption char(1) check(consumption = 'y' or consumption = 'n'),
consumptionAmount float,
tableNo char(2) references diningTable(tableNo),
finalConsumption float
);

create table orderDish(
orderNo char(12) references orders(orderNo),
dishNo char(2) references dish(dishNo),
amount int,
primary key(orderNo,dishNo));

create table staff(
staffNo char(2) primary key,
sex char(1) check(sex = 'f' or sex = 'm'),
post char(1) check(post = 'w' or post = 'c'),
goodDish char(2) references dish(dishNo),
monthBaseSalary int);


create table cooking(
staffNo char(2) references staff(staffNo),
orderNo char(12) references orders(orderNo),
dishNo char(2) references dish(dishNo),
amount int,
evaluate int check(0 <= evaluate and evaluate <=5)
primary key (staffNo,orderNo,dishNo));

create table serve(
staffNo char(2) references staff(staffNo),
orderNo char(12) references orders(orderNo),
evaluate int check(0 <= evaluate and evaluate <=5),
primary key (staffNo,orderNo));

create table salary(
staffNo char(2) references staff(staffNo),
salaryDate date,
meritPay int,
deduction int,
monthTotalSalary int);

ALTER TABLE salary ADD DEFAULT 0 FOR meritPay
ALTER TABLE salary ADD DEFAULT 0 FOR deduction
ALTER TABLE salary ADD DEFAULT 0 FOR monthTotalSalary
ALTER TABLE orders ADD DEFAULT 0 FOR consumptionAmount
ALTER TABLE orders ADD DEFAULT 0 FOR finalConsumption
ALTER TABLE serve ADD DEFAULT 3 FOR evaluate
ALTER TABLE cooking ADD DEFAULT 3 FOR evaluate


INSERT INTO [dbo].[membership] ([memberLevel], [consumptionAmout], [discount]) VALUES (0, 0, 1);
INSERT INTO [dbo].[membership] ([memberLevel], [consumptionAmout], [discount]) VALUES (1, 500, 1);
INSERT INTO [dbo].[membership] ([memberLevel], [consumptionAmout], [discount]) VALUES (2, 1000, 0.95);
INSERT INTO [dbo].[membership] ([memberLevel], [consumptionAmout], [discount]) VALUES (3, 1500, 0.9);
INSERT INTO [dbo].[membership] ([memberLevel], [consumptionAmout], [discount]) VALUES (4, 3000, 0.85);


INSERT INTO [dbo].[customer] ([telephonNo], [coustomerName], [tatolAmount], [sex], [memberLevel]) VALUES ('18810569201', 'º«ÇàÕÜ', 190, NULL, 0);
INSERT INTO [dbo].[customer] ([telephonNo], [coustomerName], [tatolAmount], [sex], [memberLevel]) VALUES ('18810569202', '¹ùçù', 450, NULL, 0);
INSERT INTO [dbo].[customer] ([telephonNo], [coustomerName], [tatolAmount], [sex], [memberLevel]) VALUES ('18810569203', 'Ð¤¾°·½', 560, NULL, 1);
INSERT INTO [dbo].[customer] ([telephonNo], [coustomerName], [tatolAmount], [sex], [memberLevel]) VALUES ('18810569204', 'Àî×ÚºÆ', 870, NULL, 1);
INSERT INTO [dbo].[customer] ([telephonNo], [coustomerName], [tatolAmount], [sex], [memberLevel]) VALUES ('18810569205', 'ËïÖÙÔ¶', 1350, NULL, 2);
INSERT INTO [dbo].[customer] ([telephonNo], [coustomerName], [tatolAmount], [sex], [memberLevel]) VALUES ('18810569206', 'ÖÜÜÆÆ½', 1400, NULL, 2);
INSERT INTO [dbo].[customer] ([telephonNo], [coustomerName], [tatolAmount], [sex], [memberLevel]) VALUES ('18810569207', '³ÂÔó·æ', 2500, NULL, 3);
INSERT INTO [dbo].[customer] ([telephonNo], [coustomerName], [tatolAmount], [sex], [memberLevel]) VALUES ('18810569208', 'µ³²©', 2950, NULL, 3);
INSERT INTO [dbo].[customer] ([telephonNo], [coustomerName], [tatolAmount], [sex], [memberLevel]) VALUES ('18810569209', 'ÕÅ×Óº½', 3500, NULL, 4);


INSERT INTO [dbo].[diningTable] ([tableNo], [capacity], [tableState]) VALUES ('T1', 2, 'u');
INSERT INTO [dbo].[diningTable] ([tableNo], [capacity], [tableState]) VALUES ('T2', 2, 'e');
INSERT INTO [dbo].[diningTable] ([tableNo], [capacity], [tableState]) VALUES ('T3', 4, 'e');
INSERT INTO [dbo].[diningTable] ([tableNo], [capacity], [tableState]) VALUES ('T4', 4, 'u');
INSERT INTO [dbo].[diningTable] ([tableNo], [capacity], [tableState]) VALUES ('T5', 6, 'u');
INSERT INTO [dbo].[diningTable] ([tableNo], [capacity], [tableState]) VALUES ('T6', 6, 'e');


INSERT INTO [dbo].[dish] ([dishNo], [dishName], [dishIntroduction], [price], [memberPrice]) VALUES ('D1', 'ÏãËÖ±ý¸É', 'ÈáÈíÃÀÎ¶Ð¡±ý¸É', 40, 35);
INSERT INTO [dbo].[dish] ([dishNo], [dishName], [dishIntroduction], [price], [memberPrice]) VALUES ('D2', 'ÏÖÄ¥¿§·È', '¼ÓÀÕ±ÈÔ­²ú', 50, 45);
INSERT INTO [dbo].[dish] ([dishNo], [dishName], [dishIntroduction], [price], [memberPrice]) VALUES ('D3', 'Ö¥Ê¿ºº±¤', 'ÄÌÎ¶Ê®×ã', 90, 85);
INSERT INTO [dbo].[dish] ([dishNo], [dishName], [dishIntroduction], [price], [memberPrice]) VALUES ('D4', 'Å£Èâºº±¤', 'ÈáÈíÃÀÎ¶Ð¡±ý¸É', 100, 90);
INSERT INTO [dbo].[dish] ([dishNo], [dishName], [dishIntroduction], [price], [memberPrice]) VALUES ('D5', 'ºÚºú½·Å£ÅÅ', 'ÈáÈíÃÀÎ¶Ð¡±ý¸É', 200, 190);
INSERT INTO [dbo].[dish] ([dishNo], [dishName], [dishIntroduction], [price], [memberPrice]) VALUES ('D6', 'Ð¡³ÔÆ´ÅÌ', 'Êí±ý¼¦³áöÏÓãÈ¦', 100, 95);
INSERT INTO [dbo].[dish] ([dishNo], [dishName], [dishIntroduction], [price], [memberPrice]) VALUES ('D7', 'ÏãÀ±¼¦³á', 'ÓÍÕ¨µÄ', 80, 75);
INSERT INTO [dbo].[dish] ([dishNo], [dishName], [dishIntroduction], [price], [memberPrice]) VALUES ('D8', '±ù¼¤Áè', 'ÔôÌð', 50, 45);

INSERT INTO [dbo].[reserve] ([tableNo], [reserveDate], [customerPhone]) VALUES ('T1', '2022-06-08 19:00:00', '18810569201');
INSERT INTO [dbo].[reserve] ([tableNo], [reserveDate], [customerPhone]) VALUES ('T1', '2022-06-10 21:00:00', '18810569208');
INSERT INTO [dbo].[reserve] ([tableNo], [reserveDate], [customerPhone]) VALUES ('T1', '2022-06-18 13:00:00', '18810569201');
INSERT INTO [dbo].[reserve] ([tableNo], [reserveDate], [customerPhone]) VALUES ('T2', '2022-06-10 12:00:00', '18810569209');
INSERT INTO [dbo].[reserve] ([tableNo], [reserveDate], [customerPhone]) VALUES ('T2', '2022-06-18 12:00:00', '18810569202');
INSERT INTO [dbo].[reserve] ([tableNo], [reserveDate], [customerPhone]) VALUES ('T3', '2022-06-07 18:00:00', '18810569202');
INSERT INTO [dbo].[reserve] ([tableNo], [reserveDate], [customerPhone]) VALUES ('T3', '2022-06-10 11:00:00', '18810569204');
INSERT INTO [dbo].[reserve] ([tableNo], [reserveDate], [customerPhone]) VALUES ('T3', '2022-06-17 18:00:00', '18810569201');
INSERT INTO [dbo].[reserve] ([tableNo], [reserveDate], [customerPhone]) VALUES ('T4', '2022-06-17 19:00:00', '18810569203');
INSERT INTO [dbo].[reserve] ([tableNo], [reserveDate], [customerPhone]) VALUES ('T6', '2022-06-17 20:00:00', '18810569205');

INSERT INTO [dbo].[orders] ([orderNo], [customer], [orderDate], [orderEndDate], [consumption], [consumptionAmount], [tableNo], [finalConsumption]) VALUES ('O92011060819', '18810569201', '2022-06-08 19:00:00', NULL, 'n', 0, 'T1', 2000);
INSERT INTO [dbo].[orders] ([orderNo], [customer], [orderDate], [orderEndDate], [consumption], [consumptionAmount], [tableNo], [finalConsumption]) VALUES ('O92011061619', '18810569201', '2022-06-16 19:00:00', '2022-06-16 20:00:00', 'y', 0, 'T1', 0);
INSERT INTO [dbo].[orders] ([orderNo], [customer], [orderDate], [orderEndDate], [consumption], [consumptionAmount], [tableNo], [finalConsumption]) VALUES ('O92011061813', '18810569201', '2022-06-18 13:00:00', NULL, 'n', 0, 'T1', 0);
INSERT INTO [dbo].[orders] ([orderNo], [customer], [orderDate], [orderEndDate], [consumption], [consumptionAmount], [tableNo], [finalConsumption]) VALUES ('O92021061718', '18810569202', '2022-06-17 18:20:00', NULL, 'y', 0, 'T1', 0);
INSERT INTO [dbo].[orders] ([orderNo], [customer], [orderDate], [orderEndDate], [consumption], [consumptionAmount], [tableNo], [finalConsumption]) VALUES ('O92081061021', '18810569208', '2022-06-10 21:00:00', '2022-06-10 22:00:00', 'y', 0, 'T1', 0);
INSERT INTO [dbo].[orders] ([orderNo], [customer], [orderDate], [orderEndDate], [consumption], [consumptionAmount], [tableNo], [finalConsumption]) VALUES ('O92092061012', '18810569209', '2022-06-10 12:00:00', '2022-06-10 17:00:00', 'y', 0, 'T2', 0);
INSERT INTO [dbo].[orders] ([orderNo], [customer], [orderDate], [orderEndDate], [consumption], [consumptionAmount], [tableNo], [finalConsumption]) VALUES ('O92022061812', '18810569202', '2022-06-18 12:00:00', NULL, 'n', 0, 'T2', 0);
INSERT INTO [dbo].[orders] ([orderNo], [customer], [orderDate], [orderEndDate], [consumption], [consumptionAmount], [tableNo], [finalConsumption]) VALUES ('O92012061613', '18810569201', '2022-06-16 13:00:00', '2022-06-16 14:00:00', 'y', 0, 'T2', 0);
INSERT INTO [dbo].[orders] ([orderNo], [customer], [orderDate], [orderEndDate], [consumption], [consumptionAmount], [tableNo], [finalConsumption]) VALUES ('O92013061718', '18810569201', '2022-06-17 18:00:00', NULL, 'n', 0, 'T3', 0);
INSERT INTO [dbo].[orders] ([orderNo], [customer], [orderDate], [orderEndDate], [consumption], [consumptionAmount], [tableNo], [finalConsumption]) VALUES ('O92023060718', '18810569202', '2022-06-07 18:00:00', NULL, 'n', 0, 'T3', 3000);
INSERT INTO [dbo].[orders] ([orderNo], [customer], [orderDate], [orderEndDate], [consumption], [consumptionAmount], [tableNo], [finalConsumption]) VALUES ('O92043061011', '18810569204', '2022-06-10 11:00:00', '2022-06-10 12:00:00', 'y', 0, 'T3', 0);
INSERT INTO [dbo].[orders] ([orderNo], [customer], [orderDate], [orderEndDate], [consumption], [consumptionAmount], [tableNo], [finalConsumption]) VALUES ('O92034061719', '18810569203', '2022-06-17 19:00:00', NULL, 'y', 0, 'T4', 0);
INSERT INTO [dbo].[orders] ([orderNo], [customer], [orderDate], [orderEndDate], [consumption], [consumptionAmount], [tableNo], [finalConsumption]) VALUES ('O92064061015', '18810569206', '2022-06-10 15:00:00', '2022-06-10 16:00:00', 'y', 0, 'T4', 0);
INSERT INTO [dbo].[orders] ([orderNo], [customer], [orderDate], [orderEndDate], [consumption], [consumptionAmount], [tableNo], [finalConsumption]) VALUES ('O09045061718', '18810569204', '2022-06-17 18:30:00', NULL, 'y', 0, 'T5', 0);
INSERT INTO [dbo].[orders] ([orderNo], [customer], [orderDate], [orderEndDate], [consumption], [consumptionAmount], [tableNo], [finalConsumption]) VALUES ('O92023060720', '18810569205', '2022-06-07 20:00:00', NULL, 'n', 0, 'T5', 1500);
INSERT INTO [dbo].[orders] ([orderNo], [customer], [orderDate], [orderEndDate], [consumption], [consumptionAmount], [tableNo], [finalConsumption]) VALUES ('O92056061009', '18810569205', '2022-06-10 09:00:00', '2022-06-10 10:00:00', 'y', 0, 'T6', 0);
INSERT INTO [dbo].[orders] ([orderNo], [customer], [orderDate], [orderEndDate], [consumption], [consumptionAmount], [tableNo], [finalConsumption]) VALUES ('O92056061720', '18810569205', '2022-06-17 20:00:00', NULL, 'n', 0, 'T6', 0);

INSERT INTO [dbo].[orderDish] ([orderNo], [dishNo], [amount]) VALUES ('O09045061718', 'D3', 4);
INSERT INTO [dbo].[orderDish] ([orderNo], [dishNo], [amount]) VALUES ('O92011061619', 'D1', 1);
INSERT INTO [dbo].[orderDish] ([orderNo], [dishNo], [amount]) VALUES ('O92011061619', 'D2', 1);
INSERT INTO [dbo].[orderDish] ([orderNo], [dishNo], [amount]) VALUES ('O92012061613', 'D3', 1);
INSERT INTO [dbo].[orderDish] ([orderNo], [dishNo], [amount]) VALUES ('O92021061718', 'D5', 2);
INSERT INTO [dbo].[orderDish] ([orderNo], [dishNo], [amount]) VALUES ('O92034061719', 'D4', 3);
INSERT INTO [dbo].[orderDish] ([orderNo], [dishNo], [amount]) VALUES ('O92043061011', 'D1', 7);
INSERT INTO [dbo].[orderDish] ([orderNo], [dishNo], [amount]) VALUES ('O92056061009', 'D2', 10);
INSERT INTO [dbo].[orderDish] ([orderNo], [dishNo], [amount]) VALUES ('O92064061015', 'D5', 3);
INSERT INTO [dbo].[orderDish] ([orderNo], [dishNo], [amount]) VALUES ('O92081061021', 'D4', 5);
INSERT INTO [dbo].[orderDish] ([orderNo], [dishNo], [amount]) VALUES ('O92092061012', 'D3', 9);

INSERT INTO [dbo].[staff] ([staffNo], [sex], [post], [goodDish], [monthBaseSalary]) VALUES ('C1', 'm', 'c', 'D3', 4500);
INSERT INTO [dbo].[staff] ([staffNo], [sex], [post], [goodDish], [monthBaseSalary]) VALUES ('C2', 'm', 'c', 'D4', 3000);
INSERT INTO [dbo].[staff] ([staffNo], [sex], [post], [goodDish], [monthBaseSalary]) VALUES ('C3', 'm', 'c', 'D4', 3000);
INSERT INTO [dbo].[staff] ([staffNo], [sex], [post], [goodDish], [monthBaseSalary]) VALUES ('W1', 'f', 'w', 'D2', 2500);
INSERT INTO [dbo].[staff] ([staffNo], [sex], [post], [goodDish], [monthBaseSalary]) VALUES ('W2', 'm', 'w', 'D3', 3500);
INSERT INTO [dbo].[staff] ([staffNo], [sex], [post], [goodDish], [monthBaseSalary]) VALUES ('W3', 'm', 'w', 'D4', 3500);
INSERT INTO [dbo].[staff] ([staffNo], [sex], [post], [goodDish], [monthBaseSalary]) VALUES ('W4', 'm', 'w', 'D5', 3500);

INSERT INTO [dbo].[salary] ([staffNo], [salaryDate], [meritPay], [deduction], [monthTotalSalary]) VALUES ('W4', '2022-06-01', 0, 0, 3500);
INSERT INTO [dbo].[salary] ([staffNo], [salaryDate], [meritPay], [deduction], [monthTotalSalary]) VALUES ('W1', '2022-06-01', 100, -75, 2525);
INSERT INTO [dbo].[salary] ([staffNo], [salaryDate], [meritPay], [deduction], [monthTotalSalary]) VALUES ('W2', '2022-06-01', 0, -150, 3350);
INSERT INTO [dbo].[salary] ([staffNo], [salaryDate], [meritPay], [deduction], [monthTotalSalary]) VALUES ('C1', '2022-06-01', 0, -200, 4300);
INSERT INTO [dbo].[salary] ([staffNo], [salaryDate], [meritPay], [deduction], [monthTotalSalary]) VALUES ('C2', '2022-06-01', 0, -150, 2850);
INSERT INTO [dbo].[salary] ([staffNo], [salaryDate], [meritPay], [deduction], [monthTotalSalary]) VALUES ('C3', '2022-06-01', 0, 0, 3000);
INSERT INTO [dbo].[salary] ([staffNo], [salaryDate], [meritPay], [deduction], [monthTotalSalary]) VALUES ('W3', '2022-06-01', 0, 0, 3500);


INSERT INTO [dbo].[serve] ([staffNo], [orderNo], [evaluate]) VALUES ('W1', 'O92011060819', 4);
INSERT INTO [dbo].[serve] ([staffNo], [orderNo], [evaluate]) VALUES ('W1', 'O92023060720', 2);
INSERT INTO [dbo].[serve] ([staffNo], [orderNo], [evaluate]) VALUES ('W1', 'O92034061719', 3);
INSERT INTO [dbo].[serve] ([staffNo], [orderNo], [evaluate]) VALUES ('W2', 'O09045061718', 3);
INSERT INTO [dbo].[serve] ([staffNo], [orderNo], [evaluate]) VALUES ('W2', 'O92021061718', 3);
INSERT INTO [dbo].[serve] ([staffNo], [orderNo], [evaluate]) VALUES ('W2', 'O92023060718', 2);
INSERT INTO [dbo].[serve] ([staffNo], [orderNo], [evaluate]) VALUES ('W2', 'O92064061015', 5);
INSERT INTO [dbo].[serve] ([staffNo], [orderNo], [evaluate]) VALUES ('W3', 'O92011061619', 5);
INSERT INTO [dbo].[serve] ([staffNo], [orderNo], [evaluate]) VALUES ('W3', 'O92012061613', 1);
INSERT INTO [dbo].[serve] ([staffNo], [orderNo], [evaluate]) VALUES ('W3', 'O92092061012', 4);
INSERT INTO [dbo].[serve] ([staffNo], [orderNo], [evaluate]) VALUES ('W4', 'O92043061011', 2);
INSERT INTO [dbo].[serve] ([staffNo], [orderNo], [evaluate]) VALUES ('W4', 'O92056061009', 5);
INSERT INTO [dbo].[serve] ([staffNo], [orderNo], [evaluate]) VALUES ('W4', 'O92081061021', 1);

INSERT INTO [dbo].[cooking] ([staffNo], [orderNo], [dishNo], [amount], [evaluate]) VALUES ('C1', 'O92011060819', 'D1', 2, 1);
INSERT INTO [dbo].[cooking] ([staffNo], [orderNo], [dishNo], [amount], [evaluate]) VALUES ('C1', 'O92023060720', 'D4', 4, 3);
INSERT INTO [dbo].[cooking] ([staffNo], [orderNo], [dishNo], [amount], [evaluate]) VALUES ('C1', 'O92034061719', 'D4', 3, 3);
INSERT INTO [dbo].[cooking] ([staffNo], [orderNo], [dishNo], [amount], [evaluate]) VALUES ('C1', 'O92043061011', 'D1', 7, 4);
INSERT INTO [dbo].[cooking] ([staffNo], [orderNo], [dishNo], [amount], [evaluate]) VALUES ('C1', 'O92064061015', 'D5', 3, 5);
INSERT INTO [dbo].[cooking] ([staffNo], [orderNo], [dishNo], [amount], [evaluate]) VALUES ('C2', 'O09045061718', 'D3', 4, 3);
INSERT INTO [dbo].[cooking] ([staffNo], [orderNo], [dishNo], [amount], [evaluate]) VALUES ('C2', 'O92021061718', 'D5', 2, 3);
INSERT INTO [dbo].[cooking] ([staffNo], [orderNo], [dishNo], [amount], [evaluate]) VALUES ('C2', 'O92023060718', 'D3', 5, 2);
INSERT INTO [dbo].[cooking] ([staffNo], [orderNo], [dishNo], [amount], [evaluate]) VALUES ('C2', 'O92081061021', 'D4', 5, 5);
INSERT INTO [dbo].[cooking] ([staffNo], [orderNo], [dishNo], [amount], [evaluate]) VALUES ('C2', 'O92092061012', 'D3', 9, 1);
INSERT INTO [dbo].[cooking] ([staffNo], [orderNo], [dishNo], [amount], [evaluate]) VALUES ('C3', 'O92011061619', 'D1', 1, 5);
INSERT INTO [dbo].[cooking] ([staffNo], [orderNo], [dishNo], [amount], [evaluate]) VALUES ('C3', 'O92011061619', 'D2', 1, 2);
INSERT INTO [dbo].[cooking] ([staffNo], [orderNo], [dishNo], [amount], [evaluate]) VALUES ('C3', 'O92012061613', 'D3', 1, 1);
INSERT INTO [dbo].[cooking] ([staffNo], [orderNo], [dishNo], [amount], [evaluate]) VALUES ('C3', 'O92056061009', 'D2', 10, 4);


CREATE PROCEDURE countMeritPay_W @staff_no char(2) AS 
BEGIN
SELECT SUM(orders.finalConsumption)*0.05 AS tmp INTO #tmp_meritPay
FROM orders,serve
WHERE serve.orderNo = orders.orderNo
AND   serve.evaluate = 4
AND serve.staffNo = @staff_no

INSERT #tmp_meritPay SELECT SUM(orders.finalConsumption)*0.1 
FROM orders,serve
WHERE serve.orderNo = orders.orderNo
AND   serve.evaluate = 5
AND serve.staffNo = @staff_no

UPDATE salary
SET salary.meritPay = 
(SELECT SUM(#tmp_meritPay.tmp)
FROM #tmp_meritPay)
WHERE salary.staffNo = @staff_no
END;



CREATE PROCEDURE countMeritPay_C @staff_no char(2) AS 
BEGIN
SELECT SUM(orders.finalConsumption)*0.05 AS tmp INTO #tmp_meritPay
FROM orders,cooking
WHERE cooking.orderNo = orders.orderNo
AND   cooking.evaluate = 4
AND cooking.staffNo = @staff_no

INSERT #tmp_meritPay SELECT SUM(orders.finalConsumption)*0.1 
FROM orders,cooking
WHERE cooking.orderNo = orders.orderNo
AND   cooking.evaluate = 5
AND cooking.staffNo = @staff_no

UPDATE salary
SET salary.meritPay = 
(SELECT SUM(#tmp_meritPay.tmp)
FROM #tmp_meritPay)
WHERE salary.staffNo = @staff_no
END;



CREATE PROCEDURE countDeduction_C @staff_no char(2) AS 
BEGIN
SELECT SUM(orders.finalConsumption)*-0.1 AS tmp INTO #tmp_deduction
FROM cooking,orders
WHERE cooking.orderNo = orders.orderNo
AND   cooking.evaluate = 1
AND cooking.staffNo = @staff_no

INSERT #tmp_deduction SELECT SUM(orders.finalConsumption)*-0.05 
FROM cooking,orders
WHERE cooking.orderNo = orders.orderNo
AND   cooking.evaluate = 2
AND cooking.staffNo = @staff_no

UPDATE salary
SET salary.deduction = 
(SELECT SUM(#tmp_deduction.tmp)
FROM #tmp_deduction)
WHERE salary.staffNo = @staff_no
END;



CREATE PROCEDURE countDeduction_W @staff_no char(2) AS 
BEGIN
SELECT SUM(orders.finalConsumption)*-0.1 AS tmp INTO #tmp_deduction
FROM serve,orders
WHERE serve.orderNo = orders.orderNo
AND   serve.evaluate = 1
AND serve.staffNo = @staff_no

INSERT #tmp_deduction SELECT SUM(orders.finalConsumption)*-0.05 
FROM serve,orders
WHERE serve.orderNo = orders.orderNo
AND   serve.evaluate = 2
AND serve.staffNo = @staff_no

UPDATE salary
SET salary.deduction = 
(SELECT SUM(#tmp_deduction.tmp)
FROM #tmp_deduction)
WHERE salary.staffNo = @staff_no
END;


CREATE PROCEDURE countTotalSalary @staff_no CHAR(6) AS
BEGIN
UPDATE salary
SET monthTotalSalary = staff.monthBaseSalary+salary.deduction+salary.meritPay
FROM staff
WHERE salary.staffNo = @staff_no
AND staff.staffNo = salary.staffNo
END;


CREATE PROCEDURE showComputeWorkerSalary @staff_no CHAR(2) AS
BEGIN
SELECT salary.staffNo,staff.post,staff.monthBaseSalary,salary.meritPay,salary.deduction,salary.monthTotalSalary
FROM salary,staff
WHERE staff.staffNo = @staff_no
AND salary.staffNo = @staff_no
END;



CREATE PROCEDURE getstaffno_W AS
BEGIN
SELECT staff.staffNo
FROM staff
WHERE staff.post = 'w'
END;


CREATE PROCEDURE getstaffno_C AS
BEGIN
SELECT staff.staffNo
FROM staff
WHERE staff.post = 'c'
END;

CREATE TRIGGER srr
on orderDish 
after insert 
as 
begin
declare @orderNos nchar(20),@amounts nchar(20),@dishNos nchar(20),@cooker nchar(20),@cooker2 nchar(20)
select @orderNos=orderNo ,@dishNos = dishNo , @amounts = amount
from inserted
select  top 1 @cooker= staffNo 
                from staff 
    where post = 'c' 
    order by NEWID()
select  top 1 @cooker2=  staffNo 
                 from staff  
     where   post = 'c'
     and goodDish =  @dishNos 
     order by NEWID()
if (EXISTS(select  staffNo from staff where post = 'c' and goodDish = @dishNos )) 
begin
insert into cooking(staffNo,orderNo,dishNo,amount) 
         values(@cooker2,@orderNos,@dishNos,@amounts) 
end
else 
begin
insert into cooking(staffNo,orderNo,dishNo,amount) 
         values(@cooker,@orderNos,@dishNos,@amounts) 
end
end


CREATE TRIGGER srr2
on orderDish 
after update 
as 
begin
declare @orderNos nchar(20),@amounts nchar(20),@dishNos nchar(20),@cooker nchar(20),@cooker2 nchar(20)
select @orderNos=orderNo ,@dishNos = dishNo , @amounts = amount
from inserted
begin
update cooking
set amount = @amounts
where orderNo = @orderNos
  and dishNo = @dishNos
end
end


 CREATE TRIGGER updatelevel ON customer
   FOR UPDATE 
AS IF UPDATE(tatolAmount)
begin
declare @memLevel int
declare @consumptionAmount int
set @memLevel = (SELECT memberLevel FROM inserted)
set @consumptionAmount = (SELECT tatolAmount FROM inserted)
select @memLevel=min(memberLevel)
from membership
where consumptionAmout > @consumptionAmount
if @memLevel is null
begin
UPDATE customer SET memberLevel =4 where telephonNo=(SELECT telephonNo FROM inserted)
end
else
begin
UPDATE customer SET memberLevel = @memLevel-1 where telephonNo=(SELECT telephonNo FROM inserted)
end
end