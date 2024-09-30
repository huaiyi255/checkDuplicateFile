# checkDuplicateFile
同时检查多个文件夹内重复文件，先比对文件大小，文件大小相同的分组比对hash，hash相同保留文件名最短的文件。

代码都有注释，可随意修改自定义使用，清理电脑文件。

使用前请测试一下脚本，确定命令没错，需要删除的文件没错，之后再去掉注释运行脚本删除文件，**数据无价!!!**

## 使用
使用命令：python checkfile1.py  D:\  C:\git 

默认只列出重复文件，不删除，如果需要删除数据，请把如下代码部分注释去掉
![image](https://github.com/user-attachments/assets/d1a928d9-1779-49be-ba89-3eea5bc8725a)

## 测试
checkfile1.py 在检测文件数量较小时快一些，checkfile2.py 在检测数量非常大时快一些

```
checkfile1.py  
总计检测文件数：526，共检测并删除重复文件2个，花费时间0.06599807739257812秒
总计检测文件数：117740，共检测并删除重复文件20034个，花费时间198.63330149650574秒

checkfile2.py  
总计检测文件数：526，共检测并删除重复文件2个，花费时间0.0712282657623291秒
总计检测文件数：117740，共检测并删除重复文件20034个，花费时间187.19425177574158秒
```

## 结语
如果存在问题或者新需求，改进的方向，欢迎提交issue
