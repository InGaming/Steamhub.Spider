import lowdb from 'lowdb'
import { default as fileSync } from 'lowdb/adapters/FileSync'

class db {
    static config(path) {
        const adapter = new fileSync(path)
        console.log(`Created database in ${path}`)
        return lowdb(adapter)
    }

    static push(path, keyname, data) {
        const db = this.config(path)
        db.defaults({ [keyname]: [] }).write()
        console.log(`Created keyname of ${keyname}`)

        db.get(keyname)
            .push(data)
            .write()
        
        console.log(`Push data success`)
    }

}

export { db }