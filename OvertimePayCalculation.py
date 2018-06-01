import Common.const
CONST = Common.const


# 获取标题数据
def get_title_data():
    print("获取标题数据")
    CONST.TITLE_DATA = CONST.DATA.row_values(CONST.TITLE_ROW-1)
    print("获取标题数据 完成")


# 计算人员信息数据
def get_user_data():
    print("计算人员信息数据")
    user_info = {}
    hour_data = {}
    for row in range(CONST.TITLE_ROW, CONST.DATA.nrows):
        user_d_info = {}
        for col in range(CONST.DATA_START_COLUMN - 1):
            user_d_info[CONST.TITLE_DATA[col]] = CONST.DATA.row_values(row)[col]
        user_name = CONST.DATA.row_values(row)[CONST.NAME_COLUMN]
        # if user_name == CONST.CURR_NAME:
        #     print(user_name)
        #加班次数
        user_d_info["加班次数"] = 0
        #加班餐费金额
        user_d_info["加班餐费"] = 0
        for col in range(CONST.DATA_START_COLUMN - 1,len(CONST.TITLE_DATA)):
            title = CONST.TITLE_DATA[col]
            data = CONST.DATA.row_values(row)[col]
            hour_data = get_working_hours(title, data)

            #打印单个人的信息
            if user_name == CONST.CURR_NAME:
                print("--------------------------------------------------")
                print(title)
                print(hour_data)
                print("--------------------------------------------------")

            user_d_info["加班次数"] = user_d_info["加班次数"] + hour_data["加班次数"]
            user_d_info["加班餐费"] = user_d_info["加班餐费"] + hour_data["加班餐费"]
        user_info[CONST.DATA.row_values(row)[0]] = user_d_info
    CONST.USER_DATA = user_info
    print("计算人员信息数据 完成")


# 工时计算
def get_working_hours(title, data):
    result = dict()
    result["加班次数"] = 0
    result["加班餐费"] = 0

    #去除打卡时间为空的
    if data == "":
        return result

    s_str_time, e_str_time = data.split("\n")
    s_time = convert_str_time_to_int(s_str_time.strip())
    e_time = convert_str_time_to_int(e_str_time.strip())
    overtime_time = convert_str_time_to_int(CONST.OVERTIME_TIME)
    overtime_money = CONST.OVERTIME_MONEY

    #跨午夜
    if e_time < s_time:
        e_time = e_time + 24 * 60
    else:
        e_time = e_time

    # 加班次数
    overtimes = 0

    # 工作日加班餐费
    if check_working_day(title):
        # 工作日
        if e_time >= overtime_time:
            overtimes = overtimes + 1
            result["加班次数"] = overtimes
            result["加班餐费"] = overtimes * overtime_money
            # print(result)

    #   非工作日加班餐费
    else:
        if e_time >= overtime_time:
            overtimes = overtimes + 1
            result["加班次数"] = overtimes
            result["加班餐费"] = overtimes * overtime_money
            if check_arrive(s_time, e_time):
                overtimes = overtimes + 1
                result["加班次数"] = overtimes
                result["加班餐费"] = overtimes * overtime_money
        elif check_arrive(s_time, e_time):
            overtimes = overtimes + 1
            result["加班次数"] = overtimes
            result["加班餐费"] = overtimes * overtime_money
    return result



# 工作日判断
def check_working_day(title):
    return title.isdigit()


# 判断 非工作日加班餐费(12:00前上班打卡，并且上班时间大于等于4个小时）
def check_arrive(s_time,e_time):
    if s_time <= 720 and (e_time - s_time) >= 240 :
        return True
    else:
        return False


# 将时间转换为分钟数
def convert_str_time_to_int(str_time):
    s_time,e_time = str_time.strip().split(":")
    return int(s_time) * 60 + int(e_time)


# 数据计算（模块主函数）
def calculate_data():
    print("数据计算")
    get_title_data()
    get_user_data()


