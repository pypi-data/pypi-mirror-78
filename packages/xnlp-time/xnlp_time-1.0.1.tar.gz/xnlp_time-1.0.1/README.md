# **xnlp_time** 

## 处理时间模块集合

### 安装
    pip install xnlp-time

## 测试
```python
from xnlp_time import TimeExtractor

time_ext = TimeExtractor()


def time_extractor_parse(query):
    """
    时间提取解析
    :param query:
    :return:
    """
    result = time_ext.parse(query)
    return result


if __name__ == '__main__':

    texts = [
        '去年的今天',
        '明天',
        '后天',
        '去年的五一',
        '去年的五月十一号',
        '明年的今天',
        '明年的十月一日',
        '腊月十三',
        '端午节',
        '十一',
        '劳动节',
        '植树节',
        '双十一',
        '元旦',
        '春节',
        '圣诞节',
        '元宵节',
        '正月十五',
        '八一',
        '六一',
        '儿童节',
        '妇女节',
        '万圣节',
        '大后天',
        '明后两天',
        '下午两点',
        '上午两点',
        '昨晚，前晚，明晚',
        '上月今天天气咋样',
        '昨天夜里两点',
        '大后天',
        '大前天',
        '腊八节'
    ]
    for text in texts:
        print('query：{},result：{}'.format(text, time_extractor_parse(text)))
    print("********the end********")
```

