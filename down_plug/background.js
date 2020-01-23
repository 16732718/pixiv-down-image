"use strict";

function _classCallCheck(t, e) {
    if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
}

var _createClass = function () {
    function t(t, e) {
        for (var r = 0; r < e.length; r++) {
            var o = e[r];
            o.enumerable = o.enumerable || !1, o.configurable = !0, "value" in o && (o.writable = !0), Object.defineProperty(t, o.key, o)
        }
    }

    return function (e, r, o) {
        return r && t(e.prototype, r), o && t(e, o), e
    }
}(), Constants = {
    LocalHost: "127.0.0.1",
    LocalServerStartPort: 5000,
    LocalServerEndPort: 7310,
    LocalServerMinVersion: "2.0.0.0"
}, StaticData = {
    LocalServerPort: 0,
    LocalServerVersion: "1.0.0.0",
    findingPort: !1,
    findPort: Constants.LocalServerStartPort,
    PopupConnectPort: null,
    DownloaderMaps: {},
    PixivUserIsPremium: !1
};
chrome.runtime.onConnect.addListener(function (t) {
    "PopupOpened" == t.name && (t.onMessage.addListener(PopupConnectPortOnMessage), t.onDisconnect.addListener(PopupConnectPortOnDisconnect), StaticData.PopupConnectPort = t)
});
var PopupConnectPortOnMessage = function (t) {
    if ("GetDownloadTask" == t.event) {
        var e = [], r = Object.keys(StaticData.DownloaderMaps);
        r.reverse();
        for (var o = 0; o < r.length; o++) {
            var a = StaticData.DownloaderMaps[r[o]], n = "(Loading...)";
            a.IllustInfo && a.IllustInfo.illustTitle && (n = a.IllustInfo.illustTitle);
            var i = {
                pixiv_id: a.PixivId,
                title: n,
                infotext: (100 * a.Progress).toFixed(2) + "%",
                progress: a.Progress
            };
            a.Error && (i.error = !0, i.infotext = a.Error), e.push(i)
        }
        StaticData.PopupConnectPort.postMessage({event: "RefreshDownloadTaskList", tasks: e})
    } else if ("ClearTaskList" == t.event) {
        var s = [], l = Object.keys(StaticData.DownloaderMaps);
        l.reverse();
        for (var d = 0; d < l.length; d++) if (StaticData.DownloaderMaps[l[d]].Running) {
            var u = StaticData.DownloaderMaps[l[d]], c = "(Loading...)";
            u.IllustInfo && u.IllustInfo.illustTitle && (c = u.IllustInfo.illustTitle);
            var v = {
                pixiv_id: u.PixivId,
                title: c,
                infotext: (100 * u.Progress).toFixed(2) + "%",
                progress: u.Progress
            };
            u.Error && (v.error = !0, v.infotext = u.Error), s.push(v)
        } else delete StaticData.DownloaderMaps[l[d]];
        StaticData.PopupConnectPort.postMessage({event: "RefreshDownloadTaskList", tasks: s})
    } else if ("DownloadRetry" == t.event) {
        var h = t.PixivId;
        void 0 !== StaticData.DownloaderMaps["pid" + h.toString()] && StaticData.DownloaderMaps["pid" + h.toString()].Retry()
    }
}, PopupConnectPortOnDisconnect = function () {
    StaticData.PopupConnectPort = null
};
chrome.runtime.onMessage.addListener(function (t, e, r) {
    // alert('DownloadFromPageUrl:' + t.event + 'StaticData.LocalServerPort:' + t.PixivUrl)

    if (0 == StaticData.LocalServerPort) return void chrome.tabs.sendMessage(e.tab.id, {event: "NotFoundLocalServer"});
    chrome.cookies.get({url: `${t.PixivUrl}`, name: 'PHPSESSID'},
        function (cookie) {
            if (cookie) {
                $.ajax({
                    url: `http://${Constants.LocalHost}:${StaticData.findPort}/api/?url=${t.PixivUrl}&cookie=${cookie.value}`,
                    type: 'GET',
                    dataType: "fetch",
                    success: function (r) {
                        alert('ok')
                    },
                    error: function (e) {
                        // StaticData.findPort++, StaticData.findPort <= Constants.LocalServerEndPort ? t() : StaticData.findingPort = !1
                    },
                });
            }
            else {
                console.log('Can\'t get cookie! Check the name!');
            }
        });
    return void chrome.tabs.sendMessage(e.tab.id, {event: "DownloaderTaskStart"});

    if ("DownloadFromPageUrl" == t.event) {
        // if (!VersionCompare(StaticData.LocalServerVersion, Constants.LocalServerMinVersion)) return void chrome.tabs.sendMessage(e.tab.id, {event: "LocalServerVersionTooLow"});
        if (void 0 !== StaticData.DownloaderMaps["pid" + t.PixivId.toString()]) {
            if (StaticData.DownloaderMaps["pid" + t.PixivId.toString()].Running) return void chrome.tabs.sendMessage(e.tab.id, {
                event: "DownloaderExisted",
                PixivId: t.PixivId
            });
            delete StaticData.DownloaderMaps["pid" + t.PixivId.toString()]
        }
        // var o = new ImageDownloader(t.PixivId, t.PixivUrl);
        // o.DownloadFromPageUrl(), StaticData.DownloaderMaps["pid" + t.PixivId.toString()] = o, chrome.tabs.sendMessage(e.tab.id, {
        //     event: "DownloaderTaskStart",
        //     PixivId: t.PixivId
        // })
    } else "PixivUserIsPremium" == t.event && (StaticData.PixivUserIsPremium = t.value)
});
var extraInfoSpec = ["blocking", "requestHeaders"];
chrome.webRequest.OnBeforeSendHeadersOptions.hasOwnProperty("EXTRA_HEADERS") && extraInfoSpec.push("extraHeaders"), chrome.webRequest.onBeforeSendHeaders.addListener(function (t) {
    for (var e in t.requestHeaders) {
        if ("referer-ex" == t.requestHeaders[e].name.toLowerCase()) return t.requestHeaders[e].name = "Referer", {requestHeaders: t.requestHeaders}
    }
    return {}
}, {urls: ["<all_urls>"]}, extraInfoSpec);
var RedirectEvent = chrome.webRequest.onBeforeRequest;
navigator.userAgent.toLowerCase().indexOf("firefox") > -1 && (RedirectEvent = chrome.webRequest.onHeadersReceived), RedirectEvent.addListener(function (t) {
    var e = new URL(t.url);
    if ("www.pixiv.net" == e.host && "/ajax/search/illustrations/" == e.pathname.substr(0, 27) && !StaticData.PixivUserIsPremium) {
        var r = void 0 !== e.searchParams ? e.searchParams : new URLSearchParams(e.search.length > 0 && "?" == e.search.substr(0, 1) ? e.search.substr(1) : e.search),
            o = r.has("order") ? r.get("order") : "";
        if ("popular_d" == o || "popular_male_d" == o || "popular_female_d" == o || r.has("blt")) return {redirectUrl: e.protocol + "//pixiv-search.wifi169.com/?search_url=" + encodeURIComponent(t.url)}
    }
    return {}
}, {urls: ["<all_urls>"]}, ["blocking"]);
var FindLocalServer = function t() {
    StaticData.findingPort = !0, $.ajax({
        context: this,
        type: "GET",
        url: "http://" + Constants.LocalHost + ":" + StaticData.findPort + "/check",
        success: function (e) {
            alert('find ok')
            void 0 !== e.Status && 200 == e.Status ? (StaticData.LocalServerPort = StaticData.findPort, StaticData.LocalServerVersion = e.Version, StaticData.findingPort = !1) : (StaticData.findPort++, StaticData.findPort <= Constants.LocalServerEndPort ? t() : StaticData.findingPort = !1)
        },
        error: function (e) {
            alert('find failed' + JSON.stringify(e))
            StaticData.findPort++, StaticData.findPort <= Constants.LocalServerEndPort ? t() : StaticData.findingPort = !1
        },
        dataType: "JSON",
    })
}, CheckLocalServer = function () {
    // if (!StaticData.findingPort) return 0 == StaticData.LocalServerPort ? (StaticData.findPort = Constants.LocalServerStartPort, void FindLocalServer()) : void $.ajax({
    //     type: "GET",
    //     url: "http://" + Constants.LocalHost + ":" + StaticData.LocalServerPort + "/check",
    //     data: "",
    //     success: function (t) {
    //         void 0 === t.Status || 200 != t.Status ? (StaticData.LocalServerPort = 0, StaticData.findPort = Constants.LocalServerStartPort, FindLocalServer()) : StaticData.LocalServerVersion = t.Version
    //     },
    //     error: function (e) {
    //         StaticData.LocalServerPort = 0, StaticData.findPort = Constants.LocalServerStartPort, FindLocalServer()
    //     },
    //     dataType: "JSON",
    //     timeout: 2000
    // })
    $.ajax({
        type: "GET",
        url: `http://${Constants.LocalHost}:${StaticData.findPort}/check`,
        data: "",
        success: function (t) {
            // void 0 === t.status || 200 != t.status ? (StaticData.LocalServerPort = 0, StaticData.findPort = Constants.LocalServerStartPort) : StaticData.LocalServerVersion = t.Version
        },
        error: function (t) {
            t.status == 200 ? StaticData.LocalServerPort = 1 : StaticData.LocalServerPort = 0;
        },
        dataType: "JSON",
    })
};
setInterval(CheckLocalServer, 5e3);

var VersionCompare = function (t, e) {
    if (t = t || "0.0.0.0", e = e || "0.0.0.0", t == e) return !0;
    for (var r = t.split("."), o = e.split("."), a = Math.max(r.length, o.length), n = 0; n < a; n++) {
        var i = ~~o[n], s = ~~r[n];
        if (s > i) return !0;
        if (s < i) return !1
    }
    return !0
}, FormatNumberLength = function (t, e) {
    for (var r = "" + t; r.length < e;) r = "0" + r;
    return r
}, ImageDownloader = function () {
    function t(e, r) {
        _classCallCheck(this, t), this.PixivId = e, this.PixivUrl = r, this.IllustInfo = null, this.Progress = 0, this.Error = "", this.Running = !0, this.DownloadUrlList = [], this.DownloadUrlIndex = 0, this.AnimatInfo = null, this.xhr = null
    }

    return _createClass(t, [{
        key: "DownloadFromPageUrl", value: function () {
            $.ajax({
                context: this, type: "GET", url: this.PixivUrl, success: function (t) {
                    this.DownloadFromPageContent(t)
                }, error: function () {
                    this.DownloadError("加载Pixiv页面失败")
                }, dataType: "TEXT", timeout: 1e4
            })
        }
    }, {
        key: "DownloadFromPageContent", value: function (t) {
            t = t.replace(/<script (.*?>)<\/script>/gi, "<noscript $1</noscript>"), t = t.replace(/(<img [^>]* )src=([^>]*>)/gi, "$1no_load_src=$2"), t = t.replace(/(\<[^\>]+) on[^\=]*\=\"[^\"]*[\"]([^\>]*\>)/g, "$1$2");
            var e = $(t);
            if (e.find("a._signup").length > 0) return void this.DownloadError("请先登录网站");
            for (var r = null, o = 0; o < e.length; o++) if ("meta" == e[o].localName && "meta-preload-data" == e[o].id) {
                var a = JSON.parse(e[o].content);
                void 0 !== a && (r = a);
                break
            }
            if (null == r || void 0 === r.illust || void 0 === r.illust || Object.keys(r.illust).length <= 0) return void this.DownloadError("分析Pixiv页面失败，可能网站已改版");
            this.IllustInfo = r.illust[Object.keys(r.illust)[0]], this.IllustInfo && !this.IllustInfo.illustTitle && this.IllustInfo.title && (this.IllustInfo.illustTitle = this.IllustInfo.title), this.DownloadFromIllustInfo()
        }
    }, {
        key: "DownloadFromIllustInfo", value: function () {
            if (this.Progress = .05, this.SendDownloadProgress(), 0 == this.IllustInfo.illustType || 1 == this.IllustInfo.illustType) if (this.IllustInfo.pageCount > 1) {
                var t = ("https://" == this.PixivUrl.substr(0, 8) ? "https" : "http") + "://www.pixiv.net/ajax/illust/" + this.PixivId + "/pages";
                $.ajax({
                    context: this, type: "GET", url: t, success: function (t) {
                        if (!t || void 0 === t.error || t.error || void 0 === t.body || void 0 === t.body.length || t.body.length < 1) return void this.DownloadError("加载多图信息失败");
                        if (t && void 0 !== t.error && !t.error && void 0 !== t.body && void 0 !== t.body.length && t.body.length > 0) {
                            for (var e = 0; e < t.body.length; e++) t.body[e].urls && t.body[e].urls.original && this.DownloadUrlList.push(t.body[e].urls.original);
                            this.LoopDownload()
                        } else this.DownloadError("加载多图信息失败")
                    }, error: function () {
                        this.DownloadError("加载多图信息失败")
                    }, dataType: "JSON", timeout: 1e4
                })
            } else this.DownloadUrlList.push(this.IllustInfo.urls.original), this.LoopDownload(); else if (2 == this.IllustInfo.illustType) {
                var e = ("https://" == this.PixivUrl.substr(0, 8) ? "https" : "http") + "://www.pixiv.net/ajax/illust/" + this.PixivId + "/ugoira_meta";
                $.ajax({
                    context: this, type: "GET", url: e, success: function (t) {
                        t && void 0 !== t.error && !t.error && void 0 !== t.body ? (this.AnimatInfo = {
                            mime_type: t.body.mime_type,
                            frames: t.body.frames
                        }, this.DownloadUrlList.push(t.body.originalSrc), this.LoopDownload()) : this.DownloadError("加载动图信息失败")
                    }, error: function () {
                        this.DownloadError("加载动图信息失败")
                    }, dataType: "JSON", timeout: 1e4
                })
            }
        }
    }, {
        key: "LoopDownload", value: function () {
            var t = this, e = new XMLHttpRequest;
            e.addEventListener("progress", function (e) {
                e.lengthComputable && (t.Progress = t.DownloadUrlIndex / t.DownloadUrlList.length * .9 + e.loaded / e.total / t.DownloadUrlList.length * .9 + .05, t.SendDownloadProgress())
            }, !1), e.addEventListener("readystatechange", function (e) {
                if (4 === this.readyState) if (200 === this.status) {
                    if (t.DownloadUrlIndex++, t.Progress = t.DownloadUrlIndex / t.DownloadUrlList.length * .9 + .05, 2 == t.IllustInfo.illustType) t.SaveAnimat(t.PixivId, t.IllustInfo.illustTitle, t.AnimatInfo, this.response); else {
                        var r = t.PixivId.toString();
                        if (t.DownloadUrlList.length > 1) {
                            var o = t.DownloadUrlList.length.toString().length;
                            r += "_" + FormatNumberLength(t.DownloadUrlIndex.toString(), o)
                        }
                        var a = this.responseURL, n = a.indexOf("?");
                        n > -1 && (a = a.substr(0, n)), n = a.lastIndexOf("."), r += n > -1 ? a.substr(n) : ".png", t.SaveImage(r, this.response)
                    }
                    t.DownloadUrlIndex < t.DownloadUrlList.length && t.LoopDownload(), t.SendDownloadProgress()
                } else t.DownloadError("下载失败")
            }, !1), e.open("GET", this.DownloadUrlList[this.DownloadUrlIndex]), e.setRequestHeader("referer-ex", this.DownloadUrlList[this.DownloadUrlIndex]), e.responseType = "arraybuffer", e.send()
        }
    }, {
        key: "Retry", value: function () {
            this.Running || "" == this.Error || (this.Progress = 0, this.Error = "", this.Running = !0, null != this.IllustInfo ? this.DownloadFromIllustInfo() : this.PixivUrl ? this.DownloadFromPageUrl() : this.DownloadError("重试时出现未知错误"), this.SendDownloadProgress())
        }
    }, {
        key: "SaveImage", value: function (t, e) {
            if (0 == StaticData.LocalServerPort) return void this.DownloadError("Pixiv Animat Downloader 主程序未连接");
            var r = this, o = new XMLHttpRequest;
            o.addEventListener("readystatechange", function (t) {
                if (4 === this.readyState) if (200 === this.status) {
                    var e = JSON.parse(this.responseText);
                    if (void 0 !== e.Status) {
                        if (200 == e.Status) return void(r.DownloadUrlIndex >= r.DownloadUrlList.length && (r.Progress = 1, r.Running = !1, r.SendDownloadProgress()));
                        if (403 == e.Status) return void r.DownloadError("保存文件失败，请确认保存目录有写入权限")
                    }
                    r.DownloadError("保存文件失败，未知错误")
                } else r.DownloadError("Pixiv Animat Downloader 主程序连接失败")
            }, !1), o.open("POST", "http://" + Constants.LocalHost + ":" + StaticData.LocalServerPort + "/SaveImage"), o.setRequestHeader("Image-Info", '{"file_name": "' + t + '"}'), o.responseType = "text", o.send(e)
        }
    }, {
        key: "SaveAnimat", value: function (t, e, r, o) {
            if (0 == StaticData.LocalServerPort) return void this.DownloadError("Pixiv Animat Downloader 主程序未连接");
            var a = this, n = new XMLHttpRequest;
            n.addEventListener("readystatechange", function (t) {
                if (4 === this.readyState) if (200 === this.status) {
                    var e = JSON.parse(this.responseText);
                    if (void 0 !== e.Status) {
                        if (200 == e.Status) return void(a.DownloadUrlIndex >= a.DownloadUrlList.length && (a.Progress = 1, a.Running = !1, a.SendDownloadProgress()));
                        if (403 == e.Status) return void a.DownloadError("保存文件失败，请确认保存目录有写入权限");
                        if (404 == e.Status) return void a.DownloadError("动画数据解压异常")
                    }
                    a.DownloadError("保存文件失败，未知错误")
                } else a.DownloadError("Pixiv Animat Downloader 主程序连接失败")
            }, !1), r.PixivId = t, r.PixivTitle = encodeURIComponent(e), n.open("POST", "http://" + Constants.LocalHost + ":" + StaticData.LocalServerPort + "/SaveAnimat"), n.setRequestHeader("Animat-Info", JSON.stringify(r)), n.responseType = "text", n.send(o)
        }
    }, {
        key: "SendDownloadProgress", value: function () {
            var t = {pixiv_id: this.PixivId, infotext: (100 * this.Progress).toFixed(2) + "%", progress: this.Progress};
            this.IllustInfo && this.IllustInfo.illustTitle && (t.title = this.IllustInfo.illustTitle), this.Error && (t.error = !0, t.infotext = this.Error), null != StaticData.PopupConnectPort && StaticData.PopupConnectPort.postMessage({
                event: "RefreshDownloadTask",
                task: t
            })
        }
    }, {
        key: "DownloadError", value: function (t) {
            this.Error = t, this.Running = !1, this.SendDownloadProgress()
        }
    }]), t
}();
