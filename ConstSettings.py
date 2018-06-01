import Common.const
CONST = Common.const


def define():
    # Excel路径位置
    CONST.FILE_PATH = r"D:\PycharmProjects\jiabf\Data\201805.xls"
    # Excel中数据源Sheet的名称
    CONST.SHEET_NAME = "打卡时间"
    # Excel中输出Sheet的名称
    CONST.SHEET_OUT = "计算结果"
    # 标题所在行数
    CONST.TITLE_ROW = 3
    #姓名所在列
    CONST.NAME_COLUMN = 0
    #当前输出人员名称
    CONST.CURR_NAME = "孔凡军"
    # 打卡时间开始列数
    CONST.DATA_START_COLUMN = 6
    # 时间正则表达式
    CONST.TIME_FORMAT = '^[0-9][0-9]:[0-9][0-9](\s*)[0-9][0-9]:[0-9][0-9]$'
    # 午饭开始时间
    #CONST.LUNCH_BEGIN_TIME = "12:00"
    # 午饭结束时间
    #CONST.LUNCH_END_TIME = "13:00"
    #加班餐费时间
    CONST.OVERTIME_TIME = "20:30"
    #加班餐费金额
    CONST.OVERTIME_MONEY = 15
