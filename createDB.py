import pymysql

db = pymysql.connect(host="127.0.0.1", user="plaUser", password="plasystem", db="mysql", port=8744)

try:

    # Create a cursor object

    cur = db.cursor()

    # SQL query string
    plmDB = '''CREATE DATABASE plm;'''

    choise= '''use plm'''

    # meter = '''CREATE TABLE Employee(id int, LastName varchar(32), FirstName varchar(32), DepartmentCode int)'''
    meter = '''CREATE TABLE user_gadget_hw_meter(id INT(11) NOT NULL AUTO_INCREMENT,kWh DOUBLE NULL, kVArh_p
    DOUBLE NULL, kVArh_n DOUBLE NULL, kVAh DOUBLE NULL, cur_sum_V DOUBLE NULL, cur_L1_V DOUBLE NULL, cur_L2_V
    DOUBLE NULL, cur_L3_V DOUBLE NULL, cur_F DOUBLE NULL, meterDate BIGINT(15) NOT NULL, gadget_HW_id_id INT(11)
    NULL,PRIMARY KEY (id)) ENGINE = InnoDB DEFAULT CHARACTER SET = latin1;'''

    meterMaxD = '''CREATE TABLE user_gadget_hw_meter_max_dem_h(id INT(11) NOT NULL AUTO_INCREMENT, kW DOUBLE NULL, meterDate BIGINT(15) NOT NULL, gadget_HW_id_id INT(11) NULL, PRIMARY KEY (id)) ENGINE = InnoDB DEFAULT CHARACTER SET = latin1;'''

    # Execute the sqlQuery
    cur.execute(plmDB)
    cur.execute(choise)
    cur.execute(meter)
    cur.execute(meterMaxD)

except Exception as e:

    print("Exeception occured:{}".format(e))

finally:

    db.close()
