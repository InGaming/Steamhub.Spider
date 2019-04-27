import crawler from 'crawler'
import { db as lowdb } from '../lib/db.mjs'


class popular_new {
  spider() {
    const self = this
    
    const c = new crawler({
      rateLimit: 1000
    })


    // Queue URLs with custom callbacks & parameters
    c.queue([{
      uri: 'https://store.steampowered.com/search/results?sort_by=Released_DESC&filter=popularnew&snr=1_7_7_popularnew_7&page=1&l=schinese&cc=cn',
      jQuery: true,

      // The global callback won't be called
      callback: function (error, res, done) {
        if (error) {
          console.log(error)
        } else {
          const date = Date.now()
          const $ = res.$
          let data = []
          $('#search_result_container > div > a').each(function (index, element) {
            let appid = $(element).attr('data-ds-appid')
            if (self.isNumeric(appid)) {
              data.push({ id: index, appid: parseInt(appid), create_at: date })
            }
          })
          lowdb.push('./db/db.json', 'popular_new', data)
        }
        done()
      }
    }])
  }
  isNumeric(n) {
    return !isNaN(parseFloat(n)) && isFinite(n)
  }
}

const popular_news = new popular_new()
popular_news.spider()