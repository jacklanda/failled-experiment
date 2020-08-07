##                                社交媒体热点事件的观点倾向分析

```这里必须是简体中文~
我以后可以在GitHub上写日记叻       __       upset = {
      __  __ ____   _____ ___   / /_                "time": "一天半" ，
     / / / // __ \ / ___// _ \ / __/                "task": "老师布置的简单学术考核" ，
    / /_/ // /_/ /(__  )/  __// /_                  "result": "没能按时完成" ,
    \__,_// .___//____/ \___/ \__/                  "quote": "我妈:机会留给有准备的人"，
         /_/ 	      			 	    "mood": "那我一定是那个没有准备好的笨蛋 ☹"
	      			  		}		  
```

<img src='https://img.shields.io/badge/python-v3.8.3-blue' align='left' /><img src='https://img.shields.io/badge/jieba-v0.42.1-green' align='left' /><img src='https://img.shields.io/badge/gensim-v3.8.3-purple' align='' />



### 实验内容

---

- 针对近期社媒上的热点话题「肖战工作室致歉信」，分别从国内主流社媒平台「微博」、「知乎」、「抖音」、「快手」以及「B站」的PC/移动端 web页面爬取该热点事件的相关言论。根据所获取的数据集，藉由数据可视化的途径，分析不同平台用户关于同一事件发言的情感倾向（积极/消极/中性）的差别，并总结各情感倾向下分别表达了哪些观点。

### 实验环境

---

- 硬件平台：

  <img src="https://s1.ax1x.com/2020/07/18/Uggjln.png" alt="image-20200715162936534" style="zoom:80%;" />

- 开发环境：CPython-3.8.3

  - 调用库：requests,  re,  pymongo,  jieba,  

    ​                pandas,  numpy，gensim 等（详见requirements.txt)

- 编辑器：VIM 8.2.0914-0 

- 调试器：IPython-7.15.0 + Ipdb-0.13.3

- 数据库：MonogoDB ( shell version v4.2.6 )

- 其它工具：Mozilla Firefox-78.0.2(for Manjaro Linux ×64)

  

### 实验方案

___

- #### 实验思路：

  - 本次实验选取社媒上的热点话题「肖战工作室致歉信」；
  - 借助中间人抓包，分析并测试各社媒平台下的目标接口，分别从国内主流社媒平台「微博」、「知乎」、「抖音」、「快手」以及「B站」的PC/移动端的 web页面 爬取该热点事件的相关言论；
  - 通过 CPython下的 第三方HTTP库「requests」实现正向代理，请求接口，爬取数据；
  - 根据爬取得到的原始数据，通过 内置模块「re」进行数据预处理对获取的相关言论进行数据预处理后入库（同时将保存为 ./metadata/ 下的 .csv 或 .txt 文件）；
  - 采用网络上下载的停用词和他人收集的语料，通过第三方库「结巴分词」对语料进行分词。

- #### 实验方法：

  #### 数据源的选取：

  - [x] <span style='color: #4fc3f7'>知乎： </span>

  > [如何看待 7 月 14 日肖战工作室发布的致歉信，承认对粉丝管理上存在疏忽和缺位？]: https://www.zhihu.com/question/406914039

  - [x] <span style='color: #f48fb1'>B站： </span>

  > [【抵制肖战】数据分析肖战现状，问问肖战粉丝:举世皆敌的感觉如何？]: https://www.bilibili.com/video/BV1QZ4y1M7Yt?from=search&amp;seid=2802586105820332741
  >

  - [x] <span style='color: #f4d03f'>微博： </span>

  > [新浪娱乐 #肖战工作室致歉信#]: https://weibo.com/1642591402/JbcWS3QUf?type=comment#_rnd1595047751155
  >

  - [ ] <span style='color: #8e44ad'>抖音： </span>`待完成`

  - [ ] <span style='color: #ff5722'>快手： </span>`待完成`

  

  #### 爬取模块的设计：

  - 目标接口分析：
    - 知乎：接口参数构成较简单，且无明显的访问限制，故为提高定向爬取效率，采用多线程爬取。
    
    - B站：接口参数构成较简单，限定接口返回数 <20 即可，生成 url列表 供线程池的调用，以实现多线程爬取操作。
    
    - 微博：接口参数构成较复杂，采用通过模拟登陆微博PC端后进行相关接口的爬取操作，微博接口在模拟登陆过程提交的POST请求中的有效载荷携带了用户登陆输入的账号、密码等信息，且该信息通过了 RSA 算法进行加密。需要注意的是，短时间内切勿通过脚本多次尝试模拟登陆微博与下行数据，否则将触发微博的访问频率限制。受限后，仅能通过等待较长时间后才可解封（对于单一 IP 而言）。
    
      

  - 爬取模块的实现：

    - [x] 知乎爬虫：同B站爬虫，通过multiprocessing.dummpy的Pool方法实现多线程爬取

    - [x] B站爬虫：B站视频评论区的评论接口对单一 IP 有访问频率限制，若超过其访问限制，

      则返回「code: '412'」, 「'message': 请求被拦截」字段。需等待一段时间后才可解封。

    - [x] 微博爬虫：通过模拟登陆的途径，爬取特定微博消息下的所有评论。微博的接口需要通过每一次请求返回得到相应参数，这些参数将用于构造下一次请求的参数体，同时由于微博页面的针对单一 IP 的限流措施，故微博抓取模块采用同步单线程模型实现。

    - [ ] 抖音爬虫：`待完成`

    - [ ] 快手爬虫：`待完成`

    - [x] 所设计及实现的爬虫将严格遵守相应网站下 .robots.txt 中的规定，且爬取数据仅供学习使用

  

  #### 数据预处理的实现：

  - 在各爬虫将爬取到的数据入库前，先通过 re.findall('[\u4e00-\u9fa5]+') 方法正则匹配中文内容，

    再经由 ' '.join() 方法将匹配的中文子串拼接为一个字符串，随后入库存储

  - 对 语料 进行正则匹配，去除其中包含的非中文内容（不足：会误筛英文句词）以及脏数据，使用网络上他人制作的停用词文件，借助「结巴分词」实现语料的虚词、无意义动词、名词的去除后，入库

    

  #### 数据挖掘的实现：

  - 词向量构建
    - 采用基于「Distributed Representation」的 word2vec 词嵌入方法，对入库后的干净文本，训练语言模型，在训练的过程中，将用于训练的每个输入词语进行降维操作，每个词都映射成一个唯一的n维向量（本实验采用n=300)，并保存生成的词向量模型。通过 word2vec 来实现词向量的构建
    - 对数据进行随机切分，生成测试训练集和测试集，生成训练集和测试集计算每段话的向量
  - 训练SVM模型
    - 对输入语句进行分类，实现情感判断
  - 补充：
    - 在修复了细小的 BUG 后，所训练的模型最终起到了情感分析的作用，为了对中性层标签提供可靠的语料支持，还手动增加了客观表述的维基中文语料 demo，以实现对中性层的训练。

  

  #### 数据库存储的设计：
  
  - 由于 MongoDB 在高并发下写入性能优良，且自己所设计的爬虫均采用
  
    基于 Python 多线程编程的模型实现，为 I/O 密集型进程，具备一定的并发量；
  
  - 存储的数据对象是以 RESTful 下的 JSON 格式为主，存取对象（包括爬取数据、语料）的事务性较弱，且存取对象基本为 键值对数据，契合MongoDB自带的 BSON 数据类型；
  
  - 对于插入操作，嵌套的列表/字典对象较扁平，其中的多数可通过python下的一次遍历O(n)获取到键值对的值；对于查询操作，MongoDB是基于 B树 的索引结构，查询一条数据所需要的平均随机IO次数会比 SQL 依赖的 B+ 树少，故单条数据的查询性能优于 SQL；
  
    综上，采用 MongoDB 作为数据库，而不考虑以构造联表的形式进行存储的关系型数据库；
  
  
  
  #### 数据可视化的实现:

    - 知乎：

         - 词云：<img src="https://ftp.bmp.ovh/imgs/2020/07/38c2007e3b5a81ef.png" style="zoom:43%;" />

         - 饼图：<img src="https://ftp.bmp.ovh/imgs/2020/07/460fe6ed27d46117.png" style="zoom:80%;" />

    - 微博：

         - 词云：<img src="https://ftp.bmp.ovh/imgs/2020/07/888d4e45b9770d1f.png" style="zoom:43%;" />
         
         - 饼图：<img src="https://ftp.bmp.ovh/imgs/2020/07/d59b971f834dfffb.png" style="zoom:80%;" />

    - B 站：

         - 词云：<img src="https://ftp.bmp.ovh/imgs/2020/07/fc03870326b5dc2a.png" style="zoom:43%;" />

         - 饼图：<img src="https://ftp.bmp.ovh/imgs/2020/07/bf0c5f5c0277c2a2.png" style="zoom:80%;" />

         - 对比直方图：<img src="https://ftp.bmp.ovh/imgs/2020/07/d999c9eae0e26571.png" style="zoom:80%;" />

        <span style='color:#a8a8a8'>            （注：B站的 negative矩形（红色）被 neutral矩形（黄色）遮挡住了，可以饼图为参考）</span>


### 实验结论

---

- 通过可视化的饼图得知：关于「肖战工作室致歉」这个话题，在知乎上的相关回答中，持消极意见的人数占其测试集的 50.2%，B站上持消极意见的评论占其测试集的 36.0%，微博上持消极意见的评论占其测试集的 29.2%，因此，可推断：在各自的取样下，知乎上存在更多的网友对该事件持消极态度，B站上则有更多的人对该事件保持中性的态度。

- 通过可视化的条形图得知：半数微博用户持消极态度，B站上的用户更多是持中性态度，微博上的用户持积极态度与持消极和中性态度之和的用户人数大致相等。

- 通过可视化的词云图得知：知乎上的用户所持的消极态度所表达的主要观点为：「肖战应该道歉」；

  B站上的用户所持的消极态度所表达的主要观点有：「恶心人」、「肖战必糊」

  微博上的用户所持的积极态度所表达的主要观点有：「构建良好网络环境」、「支持肖战」

- 综上可猜测：可能由于不同社交平台上用户群体的主要构成不同，体现为不同用户群体对于同一事件看法/态度形成了较大的差异性。

### 使用指南

---

- 解压 「中文信息处理-任务三.zip」

- 安装依赖：

  ```shell
  pip install -r requirements.txt
  ```

- 将工作目录切换至该文件夹下，运行 app.py 文件

### 实验相关数据及代码  

---

详见: ./src
      ./metadata     

目录下的相关文件

### To-Do List

---

- 移动平台流视频社媒评论 的爬取

- 代码健壮性和复用性较差，有待重构
- <span style="border-bottom:2px dashed #FF0000;"><span style='color:      #FF0000'>自己真的是啥都不懂 /(ㄒoㄒ)/</span></span>
- 训练语料的选取有待进一步地优化
- 训练的结果的准确性未进行校核，情感分析的可靠性存疑！

### 引用参考

---

- 文献：
  
  - > `word2vec Parameter Learning Explained - Xin Rong`
    
  - > `Efficient Estimation of World Representations in Vector Space - Tomas Mikolov, Kai Chen, Greg Corrado, Jeffrey Dean - Google 2013`
  
  - > `《面向多源社交网络舆情的情感分析算法研究》彭浩,朱望鹏 ,赵丹丹,吴松洋《信息技术》2019年第2期`
  
- 书籍：
  
  - >  `《流畅的Python》p424  Luciano Ramalho[巴西] 著  人民邮电出版社 2017年5月第1版`
  
  - >  `《左手MongoDB，右手Redis》p2  谢乾坤著  电子工业出版社 2019年2月第1版`
  
- 文档和源码:    
  
  - > *https://radimrehurek.com/gensim/auto_examples/tutorials/run_word2vec.html#sphx-glr-auto-examples-tutorials-run-word2vec-py*	`《gensim 中文文档》`
    
  - > *https://www.kancloud.cn/luponu/sklearn-doc-zh/889722*	`《scikit-learn 中文文档》`
  
  - > https://github.com/fxsjy/jieba	`《jieba 中文文档》`
  
  - > https://github.com/brightmart/nlp_chinese_corpus	`实验语料来源`
  
  - > *https://github.com/Python3Spiders/WeiboSuperSpider*	`微博爬虫源码参考`
  
  - > *https://github.com/maowankuiDji/Word2Vec-sentiment*	`情感分析部分源码参考&语料来源` 
