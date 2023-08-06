# Scrahub SDK for Python

[中文](https://github.com/zwgk/scrahub-sdk/blob/master/python/README-zh.md) | English

The SDK for Python contains two parts:
1. CLI Tool
2. Utility Tools

## CLI Tool

The CLI Tool is mainly designed for those who are more comfortable using command line tools to interact with Scrahub. 

The installation of the CLI Tool is simple:

```bash
pip install scrahub-sdk
```

Then, you can use the `scrahub` command in the command prompt to action with Scrahub.

Check the help document below, or you can refer to [the official documentation (Chinese)](https://docs.scrahub.cn/SDK/CLI.html). 

```
scrahub --help
```

## Utility Tools

Utility tools mainly provide some `helper` methods to make it easier for you to integrate your spiders into Scrahub, e.g. saving results.

Below are integration methods of Scrapy and general Python spiders with Scrahub.

⚠️Note: make sure you have already installed `scrahub-sdk` using pip.

##### Scrapy Integration

In `settings.py` in your Scrapy project, find the variable named `ITEM_PIPELINES` (a `dict` variable). Add content below.

```python
ITEM_PIPELINES = {
    'scrahub.pipelines.ScrahubMongoPipeline': 888,
}
```

Then, start the Scrapy spider. After it's done, you should be able to see scraped results in **Task Detail -> Result**

##### General Python Spider Integration

Please add below content to your spider files to save results.

```python
# import result saving method
from scrahub import save_item

# this is a result record, must be dict type
result = {'name': 'scrahub'}

# call result saving method
save_item(result)
```

Then, start the spider. After it's done, you should be able to see scraped results in **Task Detail -> Result**
