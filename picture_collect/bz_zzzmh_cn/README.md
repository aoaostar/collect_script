## 极简壁纸采集

采集原始地址

```
https://bz.zzzmh.cn
```

## 使用方式
> 由于目标网站不便于采集，所以需要使用油猴插件进行采集  
> 需要手动对验证码进行验证  
> 采集地址有实效，请及时下载！  

### 安装油猴插件  
> 目录下`script.js`文件代码   

![img_3.png](images/img_3.png)

### 采集图片地址
> 先设置每页96最大，以快速采集  

![img_1.png](images/img_1.png)

### 导出图片URL地址（JSON格式）
![img_2.png](images/img_2.png)

### 复制`图片URL地址`到`data.json`
> 如正在采集，需要查看采集状态  
> 可以打开 <https://www.aoaostar.com> 进行导出

### 使用`nodejs`运行`main.js`
![](images/img.png)

## 指令

```
npm install
node main.js
```