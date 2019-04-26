const crawler = require("crawler");
const lowdb = require('lowdb')
const fileSync = require('lowdb/adapters/FileSync')
const adapter = new fileSync('./db/db.json')
const db = lowdb(adapter)

// Set some defaults (required if your JSON file is empty)
db.defaults({ games: [] })
  .write()

const c = new crawler({
  rateLimit: 1000
});


// Queue URLs with custom callbacks & parameters
c.queue([{
  uri: 'https://store.steampowered.com/search/results?sort_by=Released_DESC&filter=popularnew&snr=1_7_7_popularnew_7&page=1&l=schinese&cc=cn',
  jQuery: true,

  // The global callback won't be called
  callback: function (error, res, done) {
    if (error) {
      console.log(error);
    } else {
      const date = Date.now()
      const $ = res.$
      $('#search_result_container > div > a').each(function (index, element) {
        let appid = $(element).attr('data-ds-appid');
        if (isNumeric(appid)) {
          db.get('games')
          .push({ id: index, appid: parseInt(appid), create_at: date })
          .write()
        }
      })
    }
    done();
  }
}]);

const isNumeric = (n) => {
  return !isNaN(parseFloat(n)) && isFinite(n);
}