fastAPI 框架
```
├─app --项目
│  │  run.py --项目启动文件
│  │  __init__.py
│  │  
│  ├─api --接口
│  │  │  __init__.py
│  │  │  
│  │  ├─config --配置文件
│  │  │  │  config.py
│  │  │  │  __init__.py
│  │  │          
│  │  ├─logs --日志文档
│  │  │      2022-04-07_error.log
│  │  │      2022-04-07_log.log
│  │  │      
│  │  ├─public --公共函数
│  │  │  │  public.py
│  │  │  │  __init__.py
│  │  │          
│  │  ├─v1 --版本号+业务代码
│  │  │  │  login.py 
│  │  │  │  user.py
│  │  │  │  __init__.py --接口路由注册
│  │  │  │  
│  │  │  ├─extensions --日志配置
│  │  │  │  │  logger.py
│  │  │  │  │  __init__.py
│  │          
│  ├─curd --数据库增删改查
│  │  │  City_curd.py
│  │  │  User_curd.py
│  │  │  __init__.py
│  │          
│  ├─File --文档
│  │  ├─file_data
│  │  │  │  user_data.py --文档数据
│  │  │  │  __init__.py
│  │  │          
│  │  ├─file_result --本地文件
│  │  │      
│  │  └─file_test --本地保存文件
│  │          
│  ├─model --数据库配置
│  │  │  __init__.py
│  │  │  
│  │  ├─test01
│  │  │  │  database.py 
│  │  │  │  models.py
│  │  │  │  __init__.py
│  │          
│  ├─schemas --数据类型
│  │  │  annotation_api_user.py
│  │  │  City_schemas.py
│  │  │  User_schemas.py
│  │  │  __init__.py
│  │  │  
│  │          
│  ├─tests --自动化测试
│  │      __init__.py
│  │      

```