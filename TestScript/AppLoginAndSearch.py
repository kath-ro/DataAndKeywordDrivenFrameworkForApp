from Utils.ParseExcel import ParseExcel
from Config.VarConfig import *
from Action.PageAction import *
import traceback
from TestScript.write_result import write_result
from TestScript.SearchApp import searchData

def main():
    try:
        excelObj = ParseExcel()
        excelObj.loadWorkBook(dataFilePath)
        caseSheet = excelObj.getSheetByName("测试用例")
        caseNum = excelObj.getRowsNumber(caseSheet)
        isExecuteCaseCols = excelObj.getColumn(caseSheet, testCase_isExecute)
        # 记录需要执行的用例个数
        requiredCaseNum = 0
        # 记录执行成功的用例个数
        successfulCaseNum = 0
        for idx, i in enumerate(isExecuteCaseCols[1:]):
            caseName = excelObj.getCellOfValue(caseSheet, rowNo=idx + 2, colsNo=testCase_testCaseName)
            if i.value == "y":
                requiredCaseNum += 1
                caseRow = excelObj.getRow(caseSheet, idx + 2)
                frameworkName = caseRow[testCase_frameworkName - 1].value
                stepSheetName = caseRow[testCase_testStepSheetName - 1].value

                if frameworkName == "关键字":
                    print("************* 调用关键字驱动 *************")
                    # 根据用例步骤sheet表名获取用例步骤sheet表对象
                    stepSheet = excelObj.getSheetByName(stepSheetName)
                    # 用例步骤数
                    stepNum = excelObj.getRowsNumber(stepSheet)
                    # 记录用户步骤执行成功的个数
                    successfulStepNum = 0
                    for j in range(2, stepNum + 1):
                        # 用例步骤表中第一行是标题行，无需执行
                        stepRow = excelObj.getRow(stepSheet, j)
                        # 获取用例步骤描述
                        stepDescription = stepRow[caseStep_caseStepDescription - 1].value
                        # 获取函数名
                        keyWord = stepRow[caseStep_keyWord - 1].value
                        # 获取操作元素的定位方式
                        locationType = stepRow[caseStep_locationType - 1].value
                        # 获取操作元素定位表达式
                        locatorExpression = stepRow[caseStep_locatorExpression - 1].value
                        # 获取函数中的参数
                        operatorValue = stepRow[caseStep_operatorValue - 1].value
                        if isinstance(operatorValue, int):
                            operatorValue = str(operatorValue)
                        if keyWord and locationType and locatorExpression and operatorValue:
                            # input_string(locationType, locatorExpression, inputContent)
                            step = keyWord + "('%s', '%s', '%s')" %(locationType, locatorExpression, operatorValue)
                        elif keyWord and locationType and locatorExpression:
                            step = keyWord + "('%s', '%s')" %(locationType, locatorExpression)
                        elif keyWord and operatorValue:
                            step = keyWord + "('%s')" %operatorValue
                        elif keyWord:
                            step = keyWord + "()"
                        try:
                            # 用例步骤执行
                            print(step)
                            eval(step)
                            successfulStepNum += 1
                            write_result(excelObj, stepSheet, "Pass", j, "caseStep")
                            print("执行步骤[%s]成功" %stepDescription)
                        except Exception as err:
                            errPicPath = capture_screen()
                            errMsg = traceback.format_exc()
                            write_result(excelObj, stepSheet, "Faild", j, "caseStep", errMsg, errPicPath)
                            print("执行步骤[%s]失败\n异常信息：%s" %(stepDescription, str(traceback.format_exc())))
                    if successfulStepNum == stepNum - 1:
                        successfulCaseNum += 1
                        write_result(excelObj, caseSheet, "Pass", idx + 2, "testCase")
                        print("用例[%s]执行成功" %caseName)
                    else:
                        write_result(excelObj, caseSheet, "Faild", idx + 2, "testCase")
                        print("用例[%s]执行失败" %caseName)
                elif frameworkName == "数据":
                    print("************* 调用数据驱动 *************")
                    dataSourceSheetName = caseRow[testCase_dataSourceSheetName - 1].value
                    # 步骤表对象
                    stepSheet = excelObj.getSheetByName(stepSheetName)
                    # 数据表对象
                    dataSheet = excelObj.getSheetByName(dataSourceSheetName)
                    result = searchData(excelObj, stepSheet, dataSheet)
                    if result:
                        successfulCaseNum += 1
                        write_result(excelObj, caseSheet, "Pass", idx + 2, "testCase")
                        print("用例[%s]执行成功" %caseName)
                    else:
                        write_result(excelObj, caseSheet, "Faild", idx + 2, "testCase")
                        print("用例[%s]执行失败" % caseName)
            else:
                write_result(excelObj, caseSheet, "", idx + 2, "testCase")
                print("用例%s被设置忽略执行" %caseName)
        print("共%s条用例，%s条用例需要执行，本次执行通过%s条" %(caseNum - 1, requiredCaseNum, successfulCaseNum))
    except Exception as err:
        raise err

if __name__ == "__main__":
    main()