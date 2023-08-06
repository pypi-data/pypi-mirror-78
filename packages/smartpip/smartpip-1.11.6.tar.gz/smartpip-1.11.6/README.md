<!--
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
-->

# SmartPip base on Airflow


[![License](http://img.shields.io/:license-Apache%202-blue.svg)](http://www.apache.org/licenses/LICENSE-2.0.txt)


Airflow is a platform to programmatically author, schedule, and monitor
workflows.

When workflows are defined as code, they become more maintainable,
versionable, testable, and collaborative.

Use Airflow to author workflows as directed acyclic graphs (DAGs) of tasks.
The Airflow scheduler executes your tasks on an array of workers while
following the specified dependencies. Rich command line utilities make
performing complex surgeries on DAGs a snap. The rich user interface
makes it easy to visualize pipelines running in production,
monitor progress, and troubleshoot issues when needed.

But actually, most cases we don't need so much functions, the factory only use some of them,
what they want is, **deploy easy, develop easy, system integration**. but airflow use every
function as operator, no benefit to do code automatic, and what we mostly use is
python operator, we can use it to do almost every thing, and it is easy to customize.
SmartPip is born for this as we choose another way

we keep all functions of airflow(1.10.1), so you can use it as airflow as well

## What is New on SmartPip
- DAG setup code automatic
- user control enhancement
- Token auth with data portal
- New UI to fit with new DAG setup

## Getting started
安装方法:
```shell
//pip安装
pip install smartpip
//安装依赖,请使用项目中的requirements.txt安装
pip install -r requirements.txt
//如果要升级
pip install --upgrade smartpip
```

##### 我们保留了所有Airflow的功能, 所以基础使用方法你可以参考以下
Please visit the Airflow Platform documentation (latest **stable** release) for help with [installing Airflow](https://airflow.incubator.apache.org/installation.html), getting a [quick start](https://airflow.incubator.apache.org/start.html), or a more complete [tutorial](https://airflow.incubator.apache.org/tutorial.html).

Documentation of GitHub master (latest development branch): [ReadTheDocs Documentation](https://airflow.readthedocs.io/en/latest/)

For further information, please visit the [Airflow Wiki](https://cwiki.apache.org/confluence/display/AIRFLOW/Airflow+Home).
##### SmartPip start
###### 关于权限
- airflow在initdb后需要你手动创建用户, smartpip会自动创建一个用户admin,密码admin
- smartpip 增加了visitor(只读)和Authority(设定用户可见内容), 你可以Web UI , Admin-->Users中进行管理
- 如果你有数据平台需要管理smartpip, 你可以开启smart认证
```shell
# url for smartdata portal 你的数据平台url
p_url = https://your portal url
# appkey for smartdata, can't use %,&,?,+, 数据平台之间的秘钥
appkey = xxxxxxxxxxx
# airflow默认的API是无权限的, 所以你可以修改为smart_auth
# How to authenticate users of the API
auth_backend = airflow.api.auth.backend.smart_auth
```
##### DAG生成自动化
我们不希望在airflow的UI上做自动化生成, 因为使用数据平台进行管理更合适
所以在SmartPip中我们为Airflow新增了DAG生成API, UI可以在数据平台管理,
当然我们也期望someone能贡献在SmartPip中新增管理UI的PR, 因为我们目前没有开发计划
```python
#API method sample as python request
AIRFLOW_URL = 'xxx'
APPKEY = 'xxxxx'
# your setup which can be get in you portal UI
owner = 'john'
schedule_interval = '10 0 * * *'
schedule_rate = 'day'  #每周,每月
project_name = 'P1'    # which is used as id and file name
# the job will execute in dag by sequence as listed, first item is to use what driver to execute
# 数据库及文件类型,文件命名,参数
job_list = '''
#hive_sql predict para1,para2
#impala_sql center
#hive_sql huli
#impala_sql test1
#ktr test para3
'''
dag_sequence ='''
predict >> center
huli >> [test1,test]
'''
retries=5
dag_remark='finance'
kwargs = {
    'owner':owner,
    'project_name':project_name,
    'schedule_interval':schedule_interval,
    'schedule_rate':schedule_rate,
    'job_list':job_list,
    'dag_sequence':dag_sequence,
    'token': APPKEY
}

#Use SmartPip API to generate dag files and script file
import requests
import json
url = f'{AIRFLOW_URL}/api/experimental/create_dagfile'
response = requests.post(url,data=json.dumps(kwargs),headers={'Content-Type': 'application/json'})
print(response.text)
```
更多设定参考 [DAG设定](https://www.smartchart.cn/blog/article/2019/9/11/15.html)

## Beyond the Horizon

Airflow **is not** a data streaming solution. Tasks do not move data from
one to the other (though tasks can exchange metadata!). Airflow is not
in the [Spark Streaming](http://spark.apache.org/streaming/)
or [Storm](https://storm.apache.org/) space, it is more comparable to
[Oozie](http://oozie.apache.org/) or
[Azkaban](https://azkaban.github.io/).

SmartPip is Airflow, But **we focus on the integration with data portal with the
overall data analytic solution**, so you can refer to the is [article](https://www.smartchart.cn/blog/article/2020/6/17/44.html)
to know more about us, we're glad to support you how to better use airflow

Workflows are expected to be mostly static or slowly changing. You can think
of the structure of the tasks in your workflow as slightly more dynamic
than a database structure would be. Airflow workflows are expected to look
similar from a run to the next, this allows for clarity around
unit of work and continuity.

## Principles

- **Dynamic**:  Airflow pipelines are configuration as code (Python), allowing for dynamic pipeline generation. This allows for writing code that instantiates pipelines dynamically.
- **Extensible**:  Easily define your own operators, executors and extend the library so that it fits the level of abstraction that suits your environment.
- **Elegant**:  Airflow pipelines are lean and explicit. Parameterizing your scripts is built into the core of Airflow using the powerful **Jinja** templating engine.
- **Scalable**:  Airflow has a modular architecture and uses a message queue to orchestrate an arbitrary number of workers. Airflow is ready to scale to infinity.

## User Interface

- **DAGs**: Overview of all DAGs in your environment.
![](/docs/img/dags.png)

- **Tree View**: Tree representation of a DAG that spans across time.
![](/docs/img/tree.png)

- **Graph View**: Visualization of a DAG's dependencies and their current status for a specific run.
![](/docs/img/graph.png)

- **Task Duration**: Total time spent on different tasks over time.
![](/docs/img/duration.png)

- **Gantt View**: Duration and overlap of a DAG.
![](/docs/img/gantt.png)

- **Code View**:  Quick way to view source code of a DAG.
![](/docs/img/code.png)
