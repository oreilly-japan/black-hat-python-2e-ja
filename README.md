# サイバーセキュリティプログラミング 第2版

---

![表紙](black-hat-python-2e-ja.png)

---

本リポジトリはオライリー・ジャパン発行書籍『[サイバーセキュリティプログラミング 第2版](https://www.amazon.co.jp/dp/4873119731/)』のサポートサイトです。

## サンプルコード

### ファイル構成

|フォルダ名 |説明                         |
|:--        |:--                          |
|appendix-A |付録Aで使用するソースコード  |
|...        |...                          |
|chapter-01 |1章で使用するソースコード    |
|chapter-02 |2章で使用するソースコード    |
|...        |...                          |
|chapter-11 |11章で使用するソースコード   |

サンプルコードの解説は本書籍をご覧ください。

## 正誤表

下記の誤りがありました。お詫びして訂正いたします。

本ページに掲載されていない誤植など間違いを見つけた方は、japan@oreilly.co.jpまでお知らせください。

### 第1刷

#### ■6章 P.134 L.20
**誤**
```
        else:
            sites = list()
            if response.get('webPages'):
                sites = response['webPages']['value']
            if len(sites):
                for site in sites:
                    print('*'*100)  # ❺
                    print('Name: %s       ' % site['name'])
                    print('URL: %s        ' % site['url'])
                    print('Description: %r' % site['snippet'])
                    print('*'*100)

                    java_url = URL(site['url'])
                    if not self._callbacks.isInScope(java_url):  # ❻
                        print('Adding %s to Burp scope' % site['url'])
                        self._callbacks.includeInScope(java_url)
                    else:
                        print('Empty response from Bing.: %s'
                                % bing_query_string)
        return
```
**正**
```
        else:
            sites = list()
            if response.get('webPages'):
                sites = response['webPages']['value']
            if len(sites):
                for site in sites:
                    print('*'*100)  # ❺
                    print('Name: %s       ' % site['name'])
                    print('URL: %s        ' % site['url'])
                    print('Description: %r' % site['snippet'])
                    print('*'*100)

                    java_url = URL(site['url'])
                    if not self._callbacks.isInScope(java_url):  # ❻
                        print('Adding %s to Burp scope' % site['url'])
                        self._callbacks.includeInScope(java_url)
            else:
                print('Empty response from Bing.: %s'
                        % bing_query_string)
        return
```

#### ■付録A P.245 L.27
**誤**
```
def build_help():
    res = ("cmd <command>: Execute Windows commands.\r\n"
           "fil <filepath>: Upload file from victim.\r\n"
           "dir <extention:e.g. .pdf>: Search for files \
                                with speficied extension.\r\n"
           "scr: Take screenshot.\r\n"
           "exit: Terminate this bot.\r\n"
           "Just upload a file: Bot will execute \
                                        the uploaded file.\r\n"
           "help: Display this help.")
    return res
```
**正**
```
def build_help():
    res = ("cmd <command>: Execute Windows commands.\r\n"
           "fil <filepath>: Upload file from victim.\r\n"
           "dir <extension:e.g. .pdf>: Search for files \
                                with specified extension.\r\n"
           "scr: Take screenshot.\r\n"
           "exit: Terminate this bot.\r\n"
           "Just upload a file: Bot will execute \
                                        the uploaded file.\r\n"
           "help: Display this help.")
    return res
```

## Twitter APIのプラン改訂について
Twitter社のAPIアクセスプランの改訂により、フリーAPIを用いてのツイート取得ができなくなることが[アナウンスされています](https://twitter.com/TwitterDev/status/1641222782594990080)。本書の付録C「Twitter IoCクローラー」に記載した手法を引き続きご利用になりたい方は、「Basic」以上の有償プランへの加入が必要になります。詳しくは[Twitter社のホームページ](https://developer.twitter.com/en/portal/products/basic)をご確認ください。