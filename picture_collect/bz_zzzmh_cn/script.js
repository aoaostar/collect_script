// ==UserScript==
// @name         极简壁纸抓取工具
// @namespace    http://zzzmh.aoaostar.com
// @version      1.0
// @description  给老子啪啪啪
// @author       Pluto
// @match        https://bz.zzzmh.cn/index
// @match        https://www.aoaostar.com
// @icon         https://www.google.com/s2/favicons?sz=64&domain=zzzmh.cn
// @license      GPL-3.0 License
// @supportURL   https://www.aoaostar.com
// @homepageURL  https://github.com/aoaostar
// @grant        GM_registerMenuCommand
// @grant        GM_addElement
// @grant        GM_setValue
// @grant        GM_getValue
// @grant        GM_deleteValue
// @grant        GM_notification
// @grant        GM_log
// ==/UserScript==


const COLLECT_URL = 'collect_url'
const SPIDER_STATUS = 'spider_status'
const MenuFunc = {
    getUrl() {
        output(MAIN.collectUrl())
    },
    outputCollectUrl() {
        output(JSON.stringify(GM_getValue(COLLECT_URL, {})))
    },
    Clear() {
        GM_deleteValue(COLLECT_URL)
        GM_notification('爬取的URL已经清理完毕~')
    }
}

const MAIN = {
    gogogo() {
        GM_setValue(SPIDER_STATUS, true)
        GM_notification('冲冲冲~')
        const stop = () => {
            clearInterval(interval)
            MAIN.stopstopstop()
        }
        let interval = setInterval(() => {
            $loading.show('小爬爬正在运行中', `正在爬取第${MAIN.currentPage()}页`)
            if (!GM_getValue(SPIDER_STATUS)) {
                stop()
                return
            }
            if (MAIN.hasCaptcha()) {
                GM_notification('发现验证码，快来帮我干掉它~')
                clearInterval(interval)
                $loading.close()
                let mInterval = setInterval(() => {
                    if (!MAIN.hasCaptcha() && GM_getValue(SPIDER_STATUS)) {
                        clearInterval(mInterval)
                        MAIN.gogogo()
                    }
                })
                return
            }
            let urls = MAIN.collectUrl();
            if (urls.length <= 0) {
                return;
            }
            if (urls[0] === GM_getValue('sign')) {
                return;
            }
            GM_setValue('sign', urls[0])
            let urlData = GM_getValue(COLLECT_URL, {});
            urlData[`page_${MAIN.currentPage()}`] = urls
            GM_log(urlData)
            GM_setValue(COLLECT_URL, urlData)
            if (MAIN.isLastPage()) {
                GM_notification('爬虫爬完啦~')
                stop()
                return
            }
            MAIN.nextPage()
        }, 1000)

    },
    stopstopstop() {
        GM_setValue(SPIDER_STATUS, false)
        GM_notification('爬虫已结束，哎，累死啦~')
        $loading.close()
    },
    isLastPage() {
        return document.querySelector('.pagination-bar .vue_pagination_item:last-child')?.classList.contains('_selected')
    },
    hasCaptcha() {
        return document.querySelector('.verifybox .verifybox-top')?.offsetHeight > 0
    },
    collectUrl() {
        let aArr = document.querySelectorAll('.img-box .down-span > a')
        let urlList = []
        for (const item of aArr) {
            urlList.push(item.href)
        }
        return urlList
    },
    nextPage() {
        document.querySelector('.vue_pagination_next.vue_pagination_item').click()
    },

    currentPage() {
        return parseInt(document.querySelector('.pagination-bar .vue_pagination_item._selected')?.innerText) || 0
    },
}

const $loading = {
    instance: null,
    close: () => {
        this.instance.close()
    },
    show: (title, message = '') => {
        let index = Swal.fire({
            title: title,
            text: message,
            allowOutsideClick: false,
        })
        Swal.showLoading()
        this.instance = index
        return index
    },
}

const MenuCommands = [
    {
        title: "😊 获取当前页面图片链接",
        func: MenuFunc.getUrl
    },
    {
        title: "😈 小爬爬给朕冲锋",
        func: MAIN.gogogo
    },
    {
        title: "👿 小爬爬给朕停下",
        func: MAIN.stopstopstop
    },
    {
        title: "💋 导出爬取的URL",
        func: MenuFunc.outputCollectUrl
    },
    {
        title: "👻 清除爬取的URL",
        func: MenuFunc.Clear
    },
]


function output(text, title = 'URL地址') {
    if (Array.isArray(text)) {
        text = text.join('\n')
    }
    Swal.fire({
        input: 'textarea',
        inputLabel: title,
        inputValue: text,
        showCancelButton: true,
        confirmButtonText: "复制",
    }).then((result) => {
        if (result.isConfirmed) {
            copy(text)
            Swal.fire('复制成功!', '', 'success')
        }
    })
}

function copy(text) {
    let oInput = document.createElement('textarea');
    oInput.value = text;
    document.body.appendChild(oInput);
    oInput.select(); // 选择对象
    document.execCommand("Copy"); // 执行浏览器复制命令
    oInput.className = 'oInput';
    oInput.style.display = 'none';
    oInput.remove();
}

function register_menu_command() {
    for (const command of MenuCommands) {
        GM_registerMenuCommand(command.title, command.func)
    }
}


(function () {
    'use strict';
    GM_addElement('script', {
        src: "//cdn.jsdelivr.net/npm/sweetalert2@11",
        type: 'text/javascript'
    });
    register_menu_command()
    if (window.location.hostname === 'bz.zzzmh.cn' && GM_getValue(SPIDER_STATUS)) {
        MAIN.gogogo()
    }
})();
