import execjs

# 指定使用 Node.js 環境
ctx = execjs.get('node')
result = ctx.eval("2 + 3")
print(result)

# # 引入 ethers 套件
ctx.eval("ethers = require('ethers')")

# # 使用 ethers 套件產生新的錢包
# private_key = ethers.utils.sha256('test')
# wallet = ethers.Wallet(private_key)

# # 將錢包地址以 JSON 格式回傳
# return_data = {
#     'address': wallet.address
# }

# # 將 JSON 轉成字串
# return_json = execjs.eval("JSON.stringify({})".format(return_data))

# # 印出回傳字串
# print(return_json)


