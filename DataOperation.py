import xlrd
import xlwt
from xlutils.copy import copy
import re
import Common.const
CONST = Common.const


# 数据格式检查
def data_check():
    print("数据格式检查")
    workbook = xlrd.open_workbook(CONST.FILE_PATH, formatting_info=True)
    workbook_m = copy(workbook)
    worksheet = workbook_m.get_sheet(CONST.SHEET_NAME)
    result = True
    # 对齐方式（暂不生效）
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_LEFT
    alignment.vert = xlwt.Alignment.VERT_TOP
    # 边框宽度
    borders = xlwt.Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1
    for row in range(CONST.TITLE_ROW, CONST.DATA.nrows):
        for col in range(CONST.DATA_START_COLUMN - 1, CONST.DATA.ncols):
            str_check = CONST.DATA.row_values(row)[col]
            str_check = str_check.strip()
            if not(str_check == "" or _check_time_format(str_check)):
                style = xlwt.easyxf('pattern: pattern solid, fore_colour red;'
                                    'align: wrap on, vert centre, horiz center;')
                # style.alignment = alignment
                style.borders = borders
                worksheet.write(row, col, str_check, style)
                result = False
            else:
                style = xlwt.easyxf('pattern: pattern solid, fore_colour white;'
                                    'align: wrap on, vert centre, horiz center;')
                # style.alignment = alignment
                style.borders = borders
                worksheet.write(row, col, str_check, style)
    workbook_m.save(CONST.FILE_PATH)
    return result


def get_init_data():
    print("获取原始数据")
    try:
        data = xlrd.open_workbook(CONST.FILE_PATH)
        CONST.DATA = data.sheet_by_name(CONST.SHEET_NAME)
    except Exception as e:
        print(e)
    print("获取原始数据 完成")


# 写入数据
def set_data():
    print("写入数据")
    workbook = xlrd.open_workbook(CONST.FILE_PATH, formatting_info=True)
    workbook_m = copy(workbook)
    # 检查Excel是否存在名为Sheet
    is_sheet_valid = False
    for sheet_name in workbook.sheet_names():
        if sheet_name == CONST.SHEET_OUT:
            is_sheet_valid = True
    worksheet_m = xlwt.Worksheet
    if is_sheet_valid:
        # 清空Sheet中现有的数据
        print("Sheet[" + CONST.SHEET_OUT + "]已存在，清空数据")
        worksheet = workbook.sheet_by_name(CONST.SHEET_OUT)
        worksheet_m = workbook_m.get_sheet(CONST.SHEET_OUT)
        for w_row in range(worksheet.nrows):
            for w_col in range(worksheet.ncols):
                worksheet_m.write(w_row, w_col, "")
    else:
        # 新增Sheet
        print("新增Sheet[" + CONST.SHEET_OUT + "]")
        worksheet_m = workbook_m.add_sheet(CONST.SHEET_OUT)

    # 判断是否有待写入数据
    if len(CONST.USER_DATA) < 1:
        print("无待写入数据")
    else:
        # 写入标题
        print("写入标题数据")
        style_title = xlwt.easyxf('align: vert centre, horiz centre;')
        for key in CONST.USER_DATA.keys():
            n_user_data = CONST.USER_DATA[key]
        curr_col = 0
        user_data_title = []
        for key in n_user_data.keys():
            worksheet_m.write(0, curr_col, key, style_title)
            user_data_title.append(key)
            curr_col = curr_col + 1
        print("写入标题数据 完成")
        # 写入数据
        print("写入结果数据")
        style_data = xlwt.easyxf('align: vert centre, horiz left;')
        curr_row = 1
        for key in CONST.USER_DATA.keys():
            for col in range(len(user_data_title)):
                worksheet_m.write(curr_row, col, CONST.USER_DATA[key][user_data_title[col]], style_data)
            curr_row = curr_row + 1
        print("写入结果数据 完成")

    # 保存Excel
    print("保存Excel")
    workbook_m.save(CONST.FILE_PATH)


# 检查打卡时间是否符合规则
def _check_time_format(data="09:07  \n20:38"):
    regex = re.compile(CONST.TIME_FORMAT)
    if regex.match(data):
        return True
    else:
        return False
