import execjs
import ethers

with open('./blockchain/src/EFT_function.js', 'r') as f:
    EFT_function_js_code = f.read()


# create execjs environment
ctx = execjs.get("Node")

# import tools
ctx.eval('ethers = require("ethers")')
ctx.eval('fs = require("fs")')

exec_EFT = ctx.compile(EFT_function_js_code)

# 執行js函數
result = exec_EFT.call('Owner')

# result = ctx.call("add", 1, 2)  # 執行 JavaScript 函數，取得結果
result_str = str(result)  # 將結果轉換為 Python 字串
# result_int = int(result)  # 將結果轉換為 Python 數字
# result_bool = bool(result)  # 將結果轉換為 Python 布林值

print(result_str)