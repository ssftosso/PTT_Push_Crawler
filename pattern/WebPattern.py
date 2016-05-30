# -*- coding: utf8 -*-


## Xpath pattern
Pattern_SubPageURL              = '//div[@class="title"]/a/@href'
Pattern_PrePageURL              = '//a[@class="btn wide"]/@href'
Pattern_PrePageName             = '//a[@class="btn wide"]/text()'

#### Sub page content
Pattern_SubPageTitle            = '//div[@class="title"]/a/text()'
Pattern_TitleInSubPage          = '//*[@id="main-content"]/div[3]/span[@class="article-meta-value"]/text()'
Pattern_PostAccountInSubPage    = '//*[@id="main-content"]/div[1]/span[@class="article-meta-value"]/text()'

#### Push content
Pattern_PushType                = '//*[@id="main-content"]/div[@class="push"]/span[1]/text()'
Pattern_PushAccount             = '//*[@id="main-content"]/div[@class="push"]/span[2]/text()'
Pattern_PushContent             = '//*[@id="main-content"]/div[@class="push"]/span[@class="f3 push-content"]'
Pattern_PushTime                = '//*[@id="main-content"]/div[@class="push"]/span[4]/text()'



#### Get Board list
Pattern_GetHref                 = '//p/a/@href'


