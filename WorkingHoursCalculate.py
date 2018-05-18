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
    standard_hour = get_standard_working_hours()
    for row in range(CONST.TITLE_ROW, CONST.DATA.nrows):
        user_d_info = {}
        for col in range(CONST.DATA_START_COLUMN - 1):
            user_d_info[CONST.TITLE_DATA[col]] = CONST.DATA.row_values(row)[col]
        user_name = CONST.DATA.row_values(row)[CONST.NAME_COLUMN]
        if user_name == CONST.CURR_NAME:
            print(user_name)
        user_d_info["正常工时"] = 0
        user_d_info["加班工时"] = 0
        user_d_info["请假工时"] = 0
        user_d_info["标准工时"] = standard_hour
        for col in range(CONST.DATA_START_COLUMN - 1,len(CONST.TITLE_DATA)):
            title = CONST.TITLE_DATA[col]
            data = CONST.DATA.row_values(row)[col]
            hour_data = get_working_hours(title, data)
            #输出请假工时大于0的考勤记录
            # if hour_data["请假工时"] > 0:
            #     print("--------------------------------------------------")
            #     print(title)
            #     print(hour_data)
            #     print("--------------------------------------------------")
            # 输出每天考勤记录
            if user_name == CONST.CURR_NAME:
                print("--------------------------------------------------")
                print(title)
                print(hour_data)
                print("--------------------------------------------------")
            user_d_info["正常工时"] = user_d_info["正常工时"] + hour_data["正常工时"]
            user_d_info["加班工时"] = user_d_info["加班工时"] + hour_data["加班工时"]
            user_d_info["请假工时"] = user_d_info["请假工时"] + hour_data["请假工时"]
        user_info[CONST.DATA.row_values(row)[0]] = user_d_info
    CONST.USER_DATA = user_info
    print("计算人员信息数据 完成")


# 工时计算
def get_working_hours(title, data):
    result = dict()
    result["正常工时"] = 0
    result["加班工时"] = 0
    result["请假工时"] = 0

    # 工作日无考勤，标记为请假
    if data == "":
        if check_working_day(title):
            result["请假工时"] = 8
        return result

    s_str_time, e_str_time = data.split("\n")
    s_time = convert_str_time_to_int(s_str_time.strip())
    e_time = convert_str_time_to_int(e_str_time.strip())

    if e_time < s_time:
        e_time = e_time + 24 * 60
    working_hour = int((e_time - s_time) / 30) / 2
    working_hour = round(working_hour, 2)

    # 判断是否减去午饭时间
    if check_lunch(s_time, e_time):
        working_hour = working_hour - 1

    if check_working_day(title):
        # 工作日
        if working_hour < 8:
            result["正常工时"] = working_hour
            result["请假工时"] = 8 - working_hour
        else:
            result["正常工时"] = 8
            overtime = working_hour - 8
            # 判断加班
            if overtime > 1.5:
                # 加班
                if check_dinner(s_time, e_time):
                    result["加班工时"] = overtime - 0.5
                else:
                    result["加班工时"] = overtime
    else:
        # 非工作日
        overtime = working_hour
        if check_dinner(s_time, e_time):
            result["加班工时"] = overtime - 0.5
        else:
            result["加班工时"] = overtime
    return result


# 工作日判断
def check_working_day(title):
    return title.isdigit()


# 判断 是否减去午饭一小时（上下班时间同为上午或同为下午，返回Ture）
def check_lunch(s_time, e_time):
    lunch_b_time = convert_str_time_to_int(CONST.LUNCH_BEGIN_TIME)
    lunch_e_time = convert_str_time_to_int(CONST.LUNCH_END_TIME)
    if (s_time < lunch_b_time and e_time < lunch_b_time) or (s_time > lunch_e_time and e_time > lunch_e_time):
        return False
    else:
        return True


# 判断 是否应减去晚饭 0.5 小时
def check_dinner(s_time, e_time):
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


# 月标准工时计算
def get_standard_working_hours():
    hours = 0
    for col in range(CONST.DATA_START_COLUMN-1, len(CONST.TITLE_DATA)):
        if check_working_day(CONST.TITLE_DATA[col]):
            hours = hours + 8
    return hours
