const crawler = require("crawler");
const lowdb = require('lowdb')
  t fileSync = require('lowdb/adapters/FileSync')
    apter = new fileSync('./db/db.json')
     = lowdb(adapter)
    
    ome defaults (required if your JSON file is empty)
  efaults({ popular_new: [] })
  .write()

  t c = new crawler({ 
  teLimit: 1000 
  
  
    
     URLs with custom callbacks & parameters
      
      s://store.steampowered.com/search/results?sort_by=Released_DESC&filter=popularnew&snr=1_7_7_popularnew_7&page=1&l=schinese&cc=cn',
      ue,
        
        callback won't be called
        tion (error, res, done) {
        
        g(error);
          
          ate.now()
          $
          ult_container > div > a').each(function (index, element) {
          $(element).attr('data-ds-appid');
          c(appid)) {
      .get('popular_new')
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