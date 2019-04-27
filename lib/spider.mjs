/**
 * 爬虫核心
 */

import crawler from 'crawler'
import { pipeline } from './pipeline'

class spider {

    /**
     * 
     * @param rateLimit 速率限制
     */
    static config(rateLimit) {
        return new crawler({
            rateLimit: rateLimit
        })
    }

    /**
     * 
     * @param obj 爬虫实例
     * @param url 链接
     * @param jQuery 启用 jQuery
     * @param dom 解析 dom 规则
     * @param pipeline_name 管道名称
     */
    static job(obj, url, jQuery, dom, pipeline_name) {
        obj.queue([{
            uri: url,
            jQuery: jQuery,

            // The global callback won't be called
            callback: function (error, res, done) {
                if (error) {
                    console.log(error)
                } else {
                    const $ = res.$

                    // 分发管道
                    pipeline.rule($, dom, pipeline_name)     
                }
                done()
            }
        }])
    }
}

export { spider }