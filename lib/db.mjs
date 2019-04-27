/**
 * 数据库管道
 */

import lowdb from 'lowdb'
import {default as fileSync} from 'lowdb/adapters/FileSync'

class db {
  
  /**
   * 如果数据库不存在,则会自动创建
   * @param path 写入数据库路径
   */
  static config(path) {
    const adapter = new fileSync(path)
    console.log(`Created database in ${path}`)
    return lowdb(adapter)
  }

  /**
   * 
   * @param path 需要写入的路径
   * @param keyname 需要写入的字段
   * @param data 需要写入的值
   */
  static push(path, keyname, data) {
    const db = this.config(path)
    db.defaults({[keyname]: []}).write()
    console.log(`Created keyname of ${keyname}`)

    db.get(keyname)
        .push(data)
        .write()

    console.log(`Push data success`)
  }
}

export { db }
