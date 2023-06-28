@echo off 
if "%1"=="h" goto begin
:: 创建vbs脚本，在其中以隐藏窗口模式运行 bat 脚本
start mshta vbscript:createobject("wscript.shell").run("""%~nx0"" h",0)(window.close)&&exit 
:begin 
:: 实际被执行的 bat 命令
python translate_tools_gui.py