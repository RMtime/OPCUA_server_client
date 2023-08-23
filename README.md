## OPCUA系统

1. 这个系统还没来得及引入数据库，因此点位持久化有待实现
2. 客户端2的数据生成逻辑，为了仿真，我们可能需要引入时间序列模型等机器学习甚至深度学习的模型和方法来实现更为复杂精细的数据生成
3. 程序性能的进一步优化，我认为程序的时间复杂度和空间复杂度可能依然有提升的空间
4. 程序的实时性，实时性对于仿真任务来说也相当重要，这一点可能在我的程序中没能很好地照顾到
5. 程序的功能性可以进一步提升，比如可以在UI界面中加入树型结构展示来方便服务器结构的查看，以及加入日志系统方便维护等。
6. 服务器和客户端的加密等安全措施尚未引入（证书和密钥配置等）
7. url = 'opc.tcp://==admin@==localhost:6000/freeopcua/server'，客户端访问地址这样写可保证获取读写权限，不加则只能读不能写

![image-20230823135036805](.\image-20230823135036805.png)

==问题==

1. 文件式点位配置还未debug通（文件点位没问题，文件添加时报错）

2. 属性配置界面的组件直接调用的是组件自己的get方法，虽然写了绑定到StringVar()对象上，但是不知道为什么StringVar().get()只能得到空字符串

3. 可能有控件生命周期的原因，属性配置界面第二次启动可能回报组件对象不存在的错

   ### 以上bug如果修复敬请不吝赐教！

## 点位树

==注意== 需要下载安装graphviz并添加到环境变量才能使用，具体详见[Graphviz官网](https://graphviz.gitlab.io/)

![image-20230823135348654](.\image-20230823135348654.png)



"# OPCUA_server_client" 
