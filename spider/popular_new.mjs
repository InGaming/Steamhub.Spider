import { spider } from '../lib/spider.mjs'


class popular_new {
  spider() {
    /**
     * 参数说明请浏览 ../lib/spider.mjs
     */
    const c = spider.config(1000)
    const url = 'https://store.steampowered.com/search/results?sort_by=Released_DESC&filter=popularnew&snr=1_7_7_popularnew_7&page=1&l=schinese&cc=cn'
    const rule = '#search_result_container > div > a'
    spider.job(c, url, true, rule, 'popular_new')
  }
}

const popular_news = new popular_new()
popular_news.spider()