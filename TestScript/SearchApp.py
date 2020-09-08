from Config.VarConfig import *
import traceback
from TestScript.write_result import write_result


def searchData(excelObj, stepSheet, dataSheet):
    lineMap = {"A":dataSource_appName, "B": dataSource_assertKeyword}
    try:
        # 获取是否需要执行列对象
        dataIsExecuteCols = excelObj.getColumn(dataSheet, dataSource_isExecute)
        appNameCols = excelObj.getColumn(dataSheet, dataSource_appName)

        requiredDataNum = 0
        successfulDataNum = 0
        for idx, i in enumerate(dataIsExecuteCols[1:]):
            if i.value == "y":
                requiredDataNum += 1
                successfulStepNum = 0
                stepNum = excelObj.getRowsNumber(stepSheet)
                dataRow = excelObj.getRow(dataSheet, idx + 2)
                for j in range(2, stepNum + 1):
                    # 用例步骤中的第一行为标题行，无需执行
                    stepRow = excelObj.getRow(stepSheet, j)
                    # 获取用例步骤名称描述
                    stepDescription = stepRow[caseStep_caseStepDescription - 1].value
                    # 获取函数名
                    keyWord = stepRow[caseStep_keyWord - 1].value
                    # 获取操作元素的定位方式
                    locationType = stepRow[caseStep_locationType - 1].value
                    # 获取操作元素定位方式的表达式
                    locatorExpression = stepRow[caseStep_locatorExpression - 1].value
                    # 获取函数中的参数
                    operatorValue = stepRow[caseStep_operatorValue - 1].value
                    if isinstance(operatorValue, int):
                        # 数值类数据从excel取出后为long型数据，转换为字符串，方便拼接
                        operatorValue = str(operatorValue)
                    if operatorValue and operatorValue.isalpha():
                        # 如果operatorValue为字母时，则根据坐标在数据源工作表中取操作值
                        operatorValue=excelObj.getCellOfValue(dataSheet, rowNo = idx+2, colsNo = lineMap[operatorValue])
                    if keyWord and locationType and locatorExpression and operatorValue:
                        step = keyWord + "('%s','%s',u'%s')" % (locationType, locatorExpression, operatorValue)
                    elif keyWord and locationType and locatorExpression:
                        step = keyWord + "('%s','%s')" % (locationType, locatorExpression)
                    elif keyWord and operatorValue:
                        step = keyWord + "('%s')" % (operatorValue)
                    else:
                        step = keyWord + "()"
                    try:
                        # 用户步骤执行
                        eval(step)
                        successfulStepNum += 1
                    except Exception as err:
                        print("执行步骤[%s]失败\n异常信息：%s" %(stepDescription, str(traceback.format_exc())))
                if successfulStepNum == stepNum - 1:
                    successfulDataNum += 1
                    write_result(excelObj, dataSheet, "Pass", idx + 2, "dataSheet")
                else:
                    write_result(excelObj, dataSheet, "Faild", idx + 2, "dataSheet")
            else:
                # 清空需要执行数据行的执行时间和执行结果
                write_result(excelObj, dataSheet, "", idx + 2, "dataSheet")
                print("数据[%s]被设置为忽略执行" %appNameCols[idx + 1].value)
        if requiredDataNum == successfulDataNum:
            # 整个数据驱动执行成功
            return 1
        return 0
    except Exception as err:
        print("数据驱动程序发生异常\n异常信息：%s" %str(traceback.format_exc().decode("utf-8")))