import DataOperation
import Common.const
import ConstSettings
import OvertimePayCalculation
CONST = Common.const
ConstSettings.define()


# 主函数
def main():
    print("Begin")
    print("-----------------------------------------------------")
    # print("获取原始数据")
    DataOperation.get_init_data()
    print("-----------------------------------------------------")
    # print("数据格式检查")
    if not DataOperation.data_check():
        print("数据格式检查未通过，请检查文档")
        return
    print("数据格式检查通过")
    print("-----------------------------------------------------")
    # print("数据计算")
    OvertimePayCalculation.calculate_data()
    print("-----------------------------------------------------")
    # print("写入数据")
    DataOperation.set_data()
    print("-----------------------------------------------------")
    print("End")
    # input("\n\nPress the enter key to exit.")


if __name__ == "__main__":
    main()
