const fs = require("fs");

const fetch = require("node-fetch")
const path = require('path')
const DOWNLOAD_PATH = path.join(__dirname, 'images');

const CONFIG = {
    load() {
        try {
            let bf = fs.readFileSync(path.join(__dirname) + '/config.json');
            return JSON.parse(bf.toString())
        } catch {
            return null
        }
    },
    save(data = {}) {
        for (const k in start_config) {
            if (!(k in data)) {
                data[k] = start_config[k]
            }
        }
        fs.writeFileSync(path.join(__dirname) + '/config.json', JSON.stringify(data, null, 4))
    }
}

const start_config = CONFIG.load() || {
    page: null,
    index: 0,
    end_page: null,
    data_path: "./data.json",
}

main()

async function main() {
    let buffer = fs.readFileSync(path.join(__dirname, start_config.data_path));
    let urlMap = JSON.parse(buffer.toString());
    let num = 0
    for (let k in urlMap) {
        num += urlMap[k].length
    }
    print_info("图片总数", num)

    let flag = {
        page: false,
        index: false,
    }
    for (const page in urlMap) {
        if (page === start_config.end_page) {
            break
        }
        if (!flag.page && start_config.page && start_config.page !== page) {
            continue
        }
        flag.page = true
        for (let index = 0; index < urlMap[page].length; index++) {
            if (!flag.index && start_config.index !== index) {
                continue
            }
            flag.index = true
            print_info(`当前第${page}页 图片下标:${index}`)
            let url = urlMap[page][index]
            let filename = url.substring(url.indexOf('origin/') + 'origin/'.length, url.indexOf('?response-content'));
            print_info(`正在请求下载接口`, filename)
            await request_download(filename).then(async res => {
                print_info(`请求下载接口响应结果 ${filename}`, res)
                if (res.code === 0) {
                    try {
                        if (await download(url, page, filename)) {
                            print_info('下载成功', filename)
                        } else {
                            print_error('下载失败', filename)
                        }
                    } catch (e) {
                        print_error('下载失败', filename, e.message)
                    }
                } else {
                    print_error('请求下载接口失败', filename)
                }
            }).finally(() => {
                CONFIG.save({page, index})
            })
        }
    }
}


async function request_download(filename) {
    let resp = await fetch("https://api.zzzmh.cn/bz/v3/download", {
        "headers": {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6",
            "content-type": "application/json; charset=UTF-8",
            "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"99\", \"Google Chrome\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "x-requested-with": "XMLHttpRequest",
            "origin": "https://bz.zzzmh.cn/",
            "Referer": "https://bz.zzzmh.cn/",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Mobile Safari/537.36"
        },
        "body": JSON.stringify({
            id: filename.substring(0, filename.indexOf('.')),
        }),
        "method": "POST"
    });
    return await resp.json()
}

async function download(url, filepath, filename) {
    let resp = await fetch(url, {
        headers: {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6",
            "content-type": "application/json; charset=UTF-8",
            "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"99\", \"Google Chrome\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "x-requested-with": "XMLHttpRequest",
            "origin": "https://bz.zzzmh.cn/",
            "Referer": "https://bz.zzzmh.cn/",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Mobile Safari/537.36",
            "referrerPolicy": "strict-origin-when-cross-origin",
        }
    });
    print_info(`响应状态码 status ${resp.status} ${filename}`)
    if (resp.status === 200) {
        let bf = await resp.buffer();
        let fp = `${DOWNLOAD_PATH}/${filepath}/${filename}`
        if (!fs.existsSync(fp)) {
            fs.mkdirSync(path.dirname(fp), {recursive: true})
        }
        fs.writeFileSync(fp, bf)
        return true
    }
    return false
}


function print() {
    let message = []
    for (let argument of arguments) {
        if (typeof argument === 'object') {
            argument = JSON.stringify(argument)
        }
        message.push(argument)
    }
    message = message.join(' ')
    console.log(message)
    fs.appendFileSync(path.join(__dirname) + '/aoaostar.log', `[${dateFormat(new Date())}]${message}\n`)
}

function print_info() {
    print('[INFO]', ...arguments)
}

function print_error() {
    print('[ERROR]', ...arguments)
}

function dateFormat(date, format = 'YYYY-MM-DD HH:mm:ss') {
    const config = {
        YYYY: date.getFullYear(),
        MM: date.getMonth() < 9 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1,
        DD: date.getDate() < 10 ? '0' + date.getDate() : date.getDate(),
        HH: date.getHours() < 10 ? '0' + date.getHours() : date.getHours(),
        mm: date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes(),
        ss: date.getSeconds() < 10 ? '0' + date.getSeconds() : date.getSeconds(),
    }
    for (const key in config) {
        format = format.replace(key, config[key])
    }
    return format
}