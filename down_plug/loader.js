"use strict";
function onload() {
    addCssUrl(chrome.extension.getURL("toastr.min.css")), addCssUrl(chrome.extension.getURL("loader.css")), contentEval('var BrowserPlatformUrl = "' + chrome.extension.getURL("BrowserPlatform.js") + '";'), contentEval('var jQueryExUrl = "' + chrome.extension.getURL("jquery.min.js") + '";'), contentEval('var ToastrUrl = "' + chrome.extension.getURL("toastr.min.js") + '";'), contentEval(HandlePixivPage)
}
function contentEval(e) {
    "function" == typeof e && (e = "(" + e + ")();");
    var t = document.createElement("script");
    t.setAttribute("type", "application/javascript"), t.textContent = e, document.documentElement.appendChild(t), document.documentElement.removeChild(t)
}
function addCssUrl(e) {
    var t = document.createElement("link");
    t.rel = "stylesheet", t.href = e, document.head.appendChild(t)
}
function HandlePixivPage() {
    function e() {
        "undefined" != typeof jQuery && "undefined" != typeof toastr && t()
    }

    var t = function () {
        toastr.options = {
            closeButton: !1,
            debug: !1,
            newestOnTop: !1,
            progressBar: !1,
            positionClass: "toast-top-right",
            preventDuplicates: !1,
            onclick: null,
            showDuration: "300",
            hideDuration: "1000",
            timeOut: "5000",
            extendedTimeOut: "1000",
            showEasing: "swing",
            hideEasing: "linear",
            showMethod: "fadeIn",
            hideMethod: "fadeOut"
        }, jQuery(document).on("click", ".PixivAnimatDownloadLink", function () {
            if (jQuery("a._signup").length > 0)return void toastr.error("请先登录网站");
            var e = jQuery(this).attr("PixivId"), t = jQuery(this).attr("PixivUrl");
            return t && ("member_illust.php?" == t.substr(0, 18) && (t = "/" + t), "/" == t.substr(0, 1) && (t = window.location.protocol + "//" + window.location.host + t)), window.postMessage({
                event: "DownloadFromPageUrl",
                PixivId: e,
                PixivUrl: t
            }, window.location.origin), !1
        });
        var e = function (e, t) {
            return '<a class="PixivAnimatDownloadLink PixivAnimatDownloadLinkIcon" PixivId="' + e + '" PixivUrl="' + t + '" href="javascript:void(0);" title="download by Pixiv Animat Downloader"><span class="icon"><span class="icon-download"></span></span></a>'
        }, t = function (t) {
            var n = /artworks\/([0-9]+)/;
            t.find("a").each(function () {
                var t = jQuery(this);
                if (0 == t.find("a.PixivAnimatDownloadLink").length) {
                    var a = t.attr("href"), o = n.exec(a);
                    null != o && t.find("img,figure").length > 0 && t.append(jQuery(e(o[1], a)))
                }
            }), t.find("section#js-react-search-mid div._3IpHIQ_ a.PKslhVT").each(function () {
                var t = jQuery(this);
                if (0 == t.find("a.PixivAnimatDownloadLink").length) {
                    var a = t.attr("href"), o = n.exec(a);
                    null != o && t.append(jQuery(e(o[1], a)))
                }
            });
            var a = n.exec(window.location.href);
            if (null != a) {
                if (0 == jQuery(".ImagePagePixivAnimatDownloadLink").length) {
                    var o = null, i = "", r = "";
                    if (t.find("button.gtm-main-bookmark").length > 0) {
                        var s = t.find("button.gtm-main-bookmark").first();
                        i = s.parent().attr("class"), r = s.parent().next().find("button").first().attr("class"), o = s.parent()
                    } else for (var d = t.find("a"), l = 0; l < d.length; l++)if ("/bookmark_add.php" == new URL(d[l].href).pathname) {
                        var c = jQuery(d[l]);
                        i = c.parent().attr("class"), r = c.parent().next().find("button").first().attr("class"), o = c.parent();
                        break
                    }
                    if (null != o) {
                        var u = jQuery('<div class="' + i + '"><button type="button" class="' + r + ' PixivAnimatDownloadLink ImagePagePixivAnimatDownloadLink" PixivId="' + a[1] + '" PixivUrl="' + window.location.href + '"><svg viewBox="0 0 100 100" style="width:32px;vertical-align:middle;"><path fill="#000000" stroke="none" d=" M 70 47 Q 68.75 47 67.9 47.9 L 53 62.75 53 20 Q 53 18.75 52.15 17.9 51.25 17 50 17 48.75 17 47.9 17.9 47 18.75 47 20 L 47 62.75 32.15 47.9 Q 31.25 47 30 47 28.75 47 27.9 47.9 27 48.75 27 50 27 51.25 27.9 52.15 L 47.9 72.15 Q 48.75 73 50 73 51.25 73 52.15 72.15 L 72.15 52.15 Q 73 51.25 73 50 73 48.75 72.15 47.9 71.25 47 70 47 M 82.15 82.15 Q 83 81.25 83 80 83 78.75 82.15 77.9 81.25 77 80 77 L 20 77 Q 18.75 77 17.9 77.9 17 78.75 17 80 17 81.25 17.9 82.15 18.75 83 20 83 L 80 83 Q 81.25 83 82.15 82.15 Z"></path></svg><span>下载</span></button></div>');
                        o.after(u)
                    }
                }
            } else t.find("div.popular-introduction-overlay").length > 0 && (t.find("._premium-lead-popular-d-body a .title").css("display", "block"), t.find("div.popular-introduction-overlay").first().remove())
        };
        jQuery("body").bind("DOMNodeInserted", function (e) {
            t(jQuery(e.target).parent().parent())
        }), t(jQuery(document));
        var n = "https:" == document.location.protocol ? "https://" : "http://", a = document.createElement("script");
        a.type = "text/javascript", a.async = !0, a.src = n + "s5.cnzz.com/stat.php?id=1276301425";
        var o = document.createElement("div");
        o.style.display = "none", o.appendChild(a), document.body.appendChild(o)
    }, n = function () {
        if ("undefined" == typeof toastr) {
            var t = document.getElementsByTagName("HEAD").item(0), n = document.createElement("script");
            n.type = "text/javascript", n.src = ToastrUrl, n.onload = function () {
                e()
            }, t.appendChild(n)
        } else e()
    };
    !function () {
        if ("undefined" == typeof jQuery) {
            var e = document.getElementsByTagName("HEAD").item(0), t = document.createElement("script");
            t.type = "text/javascript", t.src = jQueryExUrl, t.onload = function () {
                n()
            }, e.appendChild(t)
        } else n()
    }()
}
var PixivAnimatDownloaderExtensionId = chrome.runtime.id;
if ("/search.php" == window.location.pathname) {
    var mutationCallback = function (e) {
        var t = !1, n = !0, a = !1, o = void 0;
        try {
            for (var i, r = e[Symbol.iterator](); !(n = (i = r.next()).done); n = !0) {
                var s = i.value;
                if ("childList" == s.type) {
                    var d = !0, l = !1, c = void 0;
                    try {
                        for (var u, v = s.addedNodes[Symbol.iterator](); !(d = (u = v.next()).done); d = !0) {
                            var m = u.value;
                            if ("meta" == m.localName && "meta-global-data" == m.id) {
                                var p = JSON.parse(m.content);
                                p && p.userData && (p.userData.premium ? chrome.runtime.sendMessage({
                                    event: "PixivUserIsPremium",
                                    value: !0
                                }) : (p.userData.premium = !0, p.premium = {
                                    popularSearch: !0,
                                    adsHide: !1,
                                    novelCoverReupload: !0
                                }, m.content = JSON.stringify(p), chrome.runtime.sendMessage({
                                    event: "PixivUserIsPremium",
                                    value: !1
                                }))), t = !0;
                                break
                            }
                        }
                    } catch (e) {
                        l = !0, c = e
                    } finally {
                        try {
                            !d && v.return && v.return()
                        } finally {
                            if (l)throw c
                        }
                    }
                }
                if (t)break
            }
        } catch (e) {
            a = !0, o = e
        } finally {
            try {
                !n && r.return && r.return()
            } finally {
                if (a)throw o
            }
        }
        t && observer.disconnect()
    }, observer = new MutationObserver(mutationCallback);
    observer.observe(document.documentElement, {attributes: !1, childList: !0, subtree: !0})
}
document.addEventListener("DOMContentLoaded", function () {
    onload()
}), chrome.runtime.onMessage.addListener(function (e, t, n) {
    "DownloaderTaskStart" == e.event ? contentEval(function () {
        toastr.success("下载任务添加成功")
    }) : "NotFoundLocalServer" == e.event ? contentEval(function () {
        toastr.error("Pixiv Animat Downloader 本地程序未连接，请确认程序已启动<br/>注意：启动程序后可能会有数秒延迟")
    }) : "LocalServerVersionTooLow" == e.event ? contentEval(function () {
        toastr.error("Pixiv Animat Downloader 本地程序版本过低，请升级")
    }) : "DownloaderExisted" == e.event && contentEval(function () {
            toastr.error("下载任务已存在")
        })
}), window.addEventListener("message", function (e) {
    e.source == window && e.data && "DownloadFromPageUrl" == e.data.event && chrome.runtime.sendMessage(e.data)
});
