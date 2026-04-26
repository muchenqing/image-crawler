!function(t,e){"object"==typeof exports&&"undefined"!=typeof module?module.exports=e():"function"==typeof define&&define.amd?define(e):(t=t||self).Zooming=e()}(this,function(){"use strict";var t="auto",e="zoom-in",i="zoom-out",n="grab",s="move";function o(t,e,i){var n={passive:!1};!(arguments.length>3&&void 0!==arguments[3])||arguments[3]?t.addEventListener(e,i,n):t.removeEventListener(e,i,n)}function r(t,e){if(t){var i=new Image;i.onload=function(){e&&e(i)},i.src=t}}function a(t){return t.dataset.original?t.dataset.original:"A"===t.parentNode.tagName?t.parentNode.getAttribute("href"):null}function l(t,e,i){!function(t){var e=h.transitionProp,i=h.transformProp;if(t.transition){var n=t.transition;delete t.transition,t[e]=n}if(t.transform){var s=t.transform;delete t.transform,t[i]=s}}(e);var n=t.style,s={};for(var o in e)i&&(s[o]=n[o]||""),n[o]=e[o];return s}var h={transitionProp:"transition",transEndEvent:"transitionend",transformProp:"transform",transformCssProp:"transform"},c=h.transformCssProp,u=h.transEndEvent;var d=function(){},f={enableGrab:!0,preloadImage:!1,closeOnWindowResize:!0,transitionDuration:.4,transitionTimingFunction:"cubic-bezier(0.4, 0, 0, 1)",bgColor:"rgb(0,0,0)",bgOpacity:.95,scaleBase:1,scaleExtra:2.5,scrollThreshold:5,zIndex:998,customSize:null,onOpen:d,onClose:d,onGrab:d,onMove:d,onRelease:d,onBeforeOpen:d,onBeforeClose:d,onBeforeGrab:d,onBeforeRelease:d,onImageLoading:d,onImageLoaded:d},p={init:function(t){var e,i;e=this,i=t,Object.getOwnPropertyNames(Object.getPrototypeOf(e)).forEach(function(t){e[t]=e[t].bind(i)})},click:function(t){if(t.preventDefault(),m(t))return window.open(this.target.srcOriginal||t.currentTarget.src,"_blank");this.shown?this.released?this.close():this.release():this.open(t.currentTarget)},scroll:function(){var t=document.documentElement||document.body.parentNode||document.body,e=window.pageXOffset||t.scrollLeft,i=window.pageYOffset||t.scrollTop;null===this.lastScrollPosition&&(this.lastScrollPosition={x:e,y:i});var n=this.lastScrollPosition.x-e,s=this.lastScrollPosition.y-i,o=this.options.scrollThreshold;(Math.abs(s)>=o||Math.abs(n)>=o)&&(this.lastScrollPosition=null,this.close())},keydown:function(t){(function(t){return"Escape"===(t.key||t.code)||27===t.keyCode})(t)&&(this.released?this.close():this.release(this.close))},mousedown:function(t){if(y(t)&&!m(t)){t.preventDefault();var e=t.clientX,i=t.clientY;this.pressTimer=setTimeout(function(){this.grab(e,i)}.bind(this),200)}},mousemove:function(t){this.released||this.move(t.clientX,t.clientY)},mouseup:function(t){y(t)&&!m(t)&&(clearTimeout(this.pressTimer),this.released?this.close():this.release())},touchstart:function(t){t.preventDefault();var e=t.touches[0],i=e.clientX,n=e.clientY;this.pressTimer=setTimeout(function(){this.grab(i,n)}.bind(this),200)},touchmove:function(t){if(!this.released){var e=t.touches[0],i=e.clientX,n=e.clientY;this.move(i,n)}},touchend:function(t){(function(t){t.targetTouches.length})(t)||(clearTimeout(this.pressTimer),this.released?this.close():this.release())},clickOverlay:function(){this.close()},resizeWindow:function(){this.close()}};function y(t){return 0===t.button}function m(t){return t.metaKey||t.ctrlKey}var g={init:function(t){this.el=document.createElement("div"),this.instance=t,this.parent=document.body,l(this.el,{position:"fixed",top:0,left:0,right:0,bottom:0,opacity:0}),this.updateStyle(t.options),o(this.el,"click",t.handler.clickOverlay.bind(t))},updateStyle:function(t){l(this.el,{zIndex:t.zIndex,backgroundColor:t.bgColor,transition:"opacity\n        "+t.transitionDuration+"s\n        "+t.transitionTimingFunction})},insert:function(){this.parent.appendChild(this.el)},remove:function(){this.parent.removeChild(this.el)},fadeIn:function(){this.el.offsetWidth,this.el.style.opacity=this.instance.options.bgOpacity},fadeOut:function(){this.el.style.opacity=0}},v="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},b=function(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")},w=function(){function t(t,e){for(var i=0;i<e.length;i++){var n=e[i];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(t,n.key,n)}}return function(e,i,n){return i&&t(e.prototype,i),n&&t(e,n),e}}(),x=Object.assign||function(t){for(var e=1;e<arguments.length;e++){var i=arguments[e];for(var n in i)Object.prototype.hasOwnProperty.call(i,n)&&(t[n]=i[n])}return t},O={init:function(t,e){this.el=t,this.instance=e,this.srcThumbnail=this.el.getAttribute("src"),this.srcset=this.el.getAttribute("srcset"),this.srcOriginal=a(this.el),this.rect=this.el.getBoundingClientRect(),this.translate=null,this.scale=null,this.styleOpen=null,this.styleClose=null},zoomIn:function(){var t=this.instance.options,e=t.zIndex,s=t.enableGrab,o=t.transitionDuration,r=t.transitionTimingFunction;this.translate=this.calculateTranslate(),this.scale=this.calculateScale(),this.styleOpen={position:"relative",zIndex:e+1,cursor:s?n:i,transition:c+"\n        "+o+"s\n        "+r,transform:"translate3d("+this.translate.x+"px, "+this.translate.y+"px, 0px)\n        scale("+this.scale.x+","+this.scale.y+")",height:this.rect.height+"px",width:this.rect.width+"px"},this.el.offsetWidth,this.styleClose=l(this.el,this.styleOpen,!0)},zoomOut:function(){this.el.offsetWidth,l(this.el,{transform:"none"})},grab:function(t,e,i){var n=k(),o=n.x-t,r=n.y-e;l(this.el,{cursor:s,transform:"translate3d(\n        "+(this.translate.x+o)+"px, "+(this.translate.y+r)+"px, 0px)\n        scale("+(this.scale.x+i)+","+(this.scale.y+i)+")"})},move:function(t,e,i){var n=k(),s=n.x-t,o=n.y-e;l(this.el,{transition:c,transform:"translate3d(\n        "+(this.translate.x+s)+"px, "+(this.translate.y+o)+"px, 0px)\n        scale("+(this.scale.x+i)+","+(this.scale.y+i)+")"})},restoreCloseStyle:function(){l(this.el,this.styleClose)},restoreOpenStyle:function(){l(this.el,this.styleOpen)},upgradeSource:function(){if(this.srcOriginal){var t=this.el.parentNode;this.srcset&&this.el.removeAttribute("srcset");var e=this.el.cloneNode(!1);e.setAttribute("src",this.srcOriginal),e.style.position="fixed",e.style.visibility="hidden",t.appendChild(e),setTimeout(function(){this.el.setAttribute("src",this.srcOriginal),t.removeChild(e)}.bind(this),50)}},downgradeSource:function(){this.srcOriginal&&(this.srcset&&this.el.setAttribute("srcset",this.srcset),this.el.setAttribute("src",this.srcThumbnail))},calculateTranslate:function(){var t=k(),e=this.rect.left+this.rect.width/2,i=this.rect.top+this.rect.height/2;return{x:t.x-e,y:t.y-i}},calculateScale:function(){var t=this.el.dataset,e=t.zoomingHeight,i=t.zoomingWidth,n=this.instance.options,s=n.customSize,o=n.scaleBase;if(!s&&e&&i)return{x:i/this.rect.width,y:e/this.rect.height};if(s&&"object"===(void 0===s?"undefined":v(s)))return{x:s.width/this.rect.width,y:s.height/this.rect.height};var r=this.rect.width/2,a=this.rect.height/2,l=k(),h={x:l.x-r,y:l.y-a},c=h.x/r,u=h.y/a,d=o+Math.min(c,u);if(s&&"string"==typeof s){var f=i||this.el.naturalWidth,p=e||this.el.naturalHeight,y=parseFloat(s)*f/(100*this.rect.width),m=parseFloat(s)*p/(100*this.rect.height);if(d>y||d>m)return{x:y,y:m}}return{x:d,y:d}}};function k(){var t=document.documentElement;return{x:Math.min(t.clientWidth,window.innerWidth)/2,y:Math.min(t.clientHeight,window.innerHeight)/2}}function S(t,e,i){["mousedown","mousemove","mouseup","touchstart","touchmove","touchend"].forEach(function(n){o(t,n,e[n],i)})}return function(){function i(t){b(this,i),this.target=Object.create(O),this.overlay=Object.create(g),this.handler=Object.create(p),this.body=document.body,this.shown=!1,this.lock=!1,this.released=!0,this.lastScrollPosition=null,this.pressTimer=null,this.options=x({},f,t),this.overlay.init(this),this.handler.init(this)}return w(i,[{key:"listen",value:function(t){if("string"==typeof t)for(var i=document.querySelectorAll(t),n=i.length;n--;)this.listen(i[n]);else"IMG"===t.tagName&&(t.style.cursor=e,o(t,"click",this.handler.click),this.options.preloadImage&&r(a(t)));return this}},{key:"config",value:function(t){return t?(x(this.options,t),this.overlay.updateStyle(this.options),this):this.options}},{key:"open",value:function(t){var e=this,i=arguments.length>1&&void 0!==arguments[1]?arguments[1]:this.options.onOpen;if(!this.shown&&!this.lock){var n="string"==typeof t?document.querySelector(t):t;if("IMG"===n.tagName){if(this.options.onBeforeOpen(n),this.target.init(n,this),!this.options.preloadImage){var s=this.target.srcOriginal;null!=s&&(this.options.onImageLoading(n),r(s,this.options.onImageLoaded))}this.shown=!0,this.lock=!0,this.target.zoomIn(),this.overlay.insert(),this.overlay.fadeIn(),o(document,"scroll",this.handler.scroll),o(document,"keydown",this.handler.keydown),this.options.closeOnWindowResize&&o(window,"resize",this.handler.resizeWindow);return o(n,u,function t(){o(n,u,t,!1),e.lock=!1,e.target.upgradeSource(),e.options.enableGrab&&S(document,e.handler,!0),i(n)}),this}}}},{key:"close",value:function(){var e=this,i=arguments.length>0&&void 0!==arguments[0]?arguments[0]:this.options.onClose;if(this.shown&&!this.lock){var n=this.target.el;this.options.onBeforeClose(n),this.lock=!0,this.body.style.cursor=t,this.overlay.fadeOut(),this.target.zoomOut(),o(document,"scroll",this.handler.scroll,!1),o(document,"keydown",this.handler.keydown,!1),this.options.closeOnWindowResize&&o(window,"resize",this.handler.resizeWindow,!1);return o(n,u,function t(){o(n,u,t,!1),e.shown=!1,e.lock=!1,e.target.downgradeSource(),e.options.enableGrab&&S(document,e.handler,!1),e.target.restoreCloseStyle(),e.overlay.remove(),i(n)}),this}}},{key:"grab",value:function(t,e){var i=arguments.length>2&&void 0!==arguments[2]?arguments[2]:this.options.scaleExtra,n=arguments.length>3&&void 0!==arguments[3]?arguments[3]:this.options.onGrab;if(this.shown&&!this.lock){var s=this.target.el;this.options.onBeforeGrab(s),this.released=!1,this.target.grab(t,e,i);return o(s,u,function t(){o(s,u,t,!1),n(s)}),this}}},{key:"move",value:function(t,e){var i=arguments.length>2&&void 0!==arguments[2]?arguments[2]:this.options.scaleExtra,n=arguments.length>3&&void 0!==arguments[3]?arguments[3]:this.options.onMove;if(this.shown&&!this.lock){this.released=!1,this.body.style.cursor=s,this.target.move(t,e,i);var r=this.target.el;return o(r,u,function t(){o(r,u,t,!1),n(r)}),this}}},{key:"release",value:function(){var e=this,i=arguments.length>0&&void 0!==arguments[0]?arguments[0]:this.options.onRelease;if(this.shown&&!this.lock){var n=this.target.el;this.options.onBeforeRelease(n),this.lock=!0,this.body.style.cursor=t,this.target.restoreOpenStyle();return o(n,u,function t(){o(n,u,t,!1),e.lock=!1,e.released=!0,i(n)}),this}}}]),i}()});

// 图片预加载：preloadImage:!1											1关闭 0启动
// 图片展开动画时间：transitionDuration:.4								0.4秒
// 动画函数：transitionTimingFunction:"cubic-bezier(0.4, 0, 0, 1)"
// 遮罩背景颜色：bgColor:"rgb(0,0,0)
// 遮罩透明度：bgOpacity:.95
// 缩放比例：scaleBase:1
// 抓取图像时额外缩放比例：scaleExtra:2
// 滚动关闭：scrollThreshold:5

// 进度条
$(document).ready(function () {

    const bar = document.createElement("div");
    bar.id = "Load";
    document.body.appendChild(bar);

    let currentRequestId = 0;  // <-- 记录最新请求
    let timeoutTimer = null;

    function startProgress() {
        bar.style.transition = "none";
        bar.style.width = "0%";
        bar.offsetHeight;
        bar.style.transition = "";
        bar.style.opacity = "1";
        setTimeout(() => bar.style.width = "3%", 0); //进度条默认位置

        if (timeoutTimer) clearTimeout(timeoutTimer);
        timeoutTimer = setTimeout(() => {
            bar.style.width = "100%";
            setTimeout(() => bar.style.opacity = "0", 500);
        }, 10000); // 10 秒超时
    }

    function updateProgress(loaded, total) {
        let percent = Math.floor((loaded / total) * 100);
        bar.style.width = percent + "%";

        if (percent >= 100) {
            if (timeoutTimer) {
                clearTimeout(timeoutTimer);
                timeoutTimer = null;
            }
            setTimeout(() => bar.style.width = "100%", 150);
            setTimeout(() => bar.style.opacity = "0", 500);
        }
    }


    (function() {

        const _ajax = $.ajax;

        $.ajax = function(options) {
            const success = options.success;

            options.success = function(html) {

                // 请求分配唯一ID
                const reqId = ++currentRequestId;

                // 解析图片
                const temp = document.createElement("div");
                temp.innerHTML = html;
                const imgs = temp.querySelectorAll("img");

                if (imgs.length > 0) {

                    // 最新请求执行
                    if (reqId === currentRequestId) {
                        startProgress();
                    }

                    let loaded = 0;
                    let total = imgs.length;

                    imgs.forEach(imgEl => {
                        const realUrl = imgEl.getAttribute("src");
                        const preload = new Image();
                        preload.src = realUrl;

                        const handle = () => {
                            // 旧请求忽略
                            if (reqId !== currentRequestId) return;

                            loaded++;
                            updateProgress(loaded, total);
                        };

                        if (preload.complete) {
                            handle();
                        } else {
                            preload.onload = handle;
                            preload.onerror = handle;
                        }
                    });
                }

                success(html);
            };

            return _ajax(options);
        };
    })();
});
// 进度条


// 图片加载相关
$(document).ready(function () {

    // 全局配置
    const CONFIG = {
        PUSH_LIMIT: 2,        // 同时加载图片数量
        PUSH_INTERVAL: 30,     // 出图间隔 ms
        AUTO_LOAD_DELAY: 2000 // 到底自动加载.延迟 ms
    };

    // 页面初始化
    var zooming = null;
    if (typeof Zooming !== 'undefined') {
        zooming = new Zooming();
    }

    var $grid = $('#imgarray');
    var page = 1;
    var end = 0;
    var loading = false;

    // 图片加载初始化

    if ($grid.find('.grid-sizer').length === 0) {
        $grid.prepend('<div class="grid-sizer"></div>');
    }

    function initIsotope() {
        $grid.isotope({
            itemSelector: '.grid-item',
            percentPosition: true,
            transitionDuration: '0.4s',
            masonry: {
                columnWidth: '.grid-sizer'
            }
        });
    }

    // 图片加载后初始化
    function appendItems($items) {

        $items.find('img').each(function () {
            $(this).css({
                width: '100%',
                height: 'auto',
                objectFit: 'cover',
                display: 'block'
            });
            this.loading = 'lazy';
        });

        $grid.append($items);

        if (!$grid.data('isotope')) {
            initIsotope();
        } else {
            $grid.isotope('appended', $items);
            $grid.isotope('layout');
        }

        if (zooming) zooming.listen('.img-zoomable');
    }

    // 加载队列控制
    // 加载队列
    var pushQueue = [];   // 等待加载
    var pushing = false; // 是否正在加载

    function pushNext() {

        if (pushing) return;
        if (pushQueue.length === 0) return;

        pushing = true;

        // 图片加载数量
        var count = Math.min(CONFIG.PUSH_LIMIT, pushQueue.length);
        var $batch = $();

        for (var i = 0; i < count; i++) {
            $batch = $batch.add(pushQueue.shift());
        }

        appendItems($batch);

        // 出图速度
        setTimeout(function () {
            pushing = false;
            pushNext();
        }, CONFIG.PUSH_INTERVAL);
    }

    // 图片加载
    function loadPage(p) {

        if (end || loading) return;
        loading = true;

        $.ajax({
            url: 'New.php?page=' + p,
            type: 'get',
            dataType: 'html',

            success: function (data) {
                loading = false;

                if (!data) {
                    end = 1;
                    return;
                }

                var $items = $(data).filter('.grid-item');

                if ($items.length === 0) {
                    end = 1;
                    return;
                }

                // 第1页：一次性加载（废弃）
                // if (p === 0) {
                //     $items.imagesLoaded().always(function () {
                //         appendItems($items);
                //     });
                //     return;
                // }

                // 后续页.动态加载（废弃）
                // $items.each(function () {

                //     var $item = $(this);
                //     var $img = $item.find('img');
                //     var pushed = false;

                //     function enqueue() {
                //         if (pushed) return;
                //         pushed = true;

                //         // 加载完成顺序
                //         pushQueue.push($item);

                //         // 显示
                //         pushNext();
                //     }

                //     // 缓存
                //     if ($img[0] && $img[0].complete) {
                //         enqueue();
                //     } else {
                //         $img.one('load error', enqueue);
                //     }
                // });

                // 不区分页码.直接加载
                $items.each(function () {

                    var $item = $(this);
                    var $img = $item.find('img');
                    var pushed = false;

                    function enqueue() {
                        if (pushed) return;
                        pushed = true;

                        $item.imagesLoaded().always(function () {
                            pushQueue.push($item);
                            pushNext();
                        });
                    }

                    if ($img[0] && $img[0].complete) {
                        enqueue();
                    } else {
                        $img.one('load error', enqueue);
                    }
                });

            },

            error: function () {
                loading = false;
            }
        });
    }

    // 初始化加载第一页全部图
    loadPage(page);

    // 调用翻页
    window.addPage = function () {
        if (end) {
            alert("已到底");
            return;
        }
        page++;
        loadPage(page);
    };

    // 自动加载（滚动到底部时）
    let autoTimer = null;
    let sentinel = document.getElementById('CD');
    let observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !loading && !end) {

                // 延迟任务
                if (autoTimer) return;

                autoTimer = setTimeout(() => {
                    autoTimer = null;
                    addPage();
                }, CONFIG.AUTO_LOAD_DELAY);
            }
        });
    });

    observer.observe(sentinel);
    // 自动加载（滚动到底部时）


// 页面内图片清空按钮
(function initClearButton() {

    const CLEAR_CONFIG = {
        selector: '.col-xl-3',
        bottom: '10px',
        zIndex: 8999,
        showLimit: 79    // 超过这个数量显示删除按钮
    };

    const btn = document.createElement('div');
    btn.id = 'clearGridBtn';

    btn.innerHTML = `<span class="clear-btn-text">🗑️清除图片🗑️</span>`;

    // 按钮样式
    Object.assign(btn.style, {
        position: 'fixed',
        left: '50%',
        bottom: CLEAR_CONFIG.bottom,

        height: '30px',
        padding: '0 18px',
        borderRadius: '999px',

        background: 'rgba(255,255,255,0.75)',
        display: 'flex',
        alignItems: 'center',
        gap: '10px',

        cursor: 'pointer',
        zIndex: CLEAR_CONFIG.zIndex,
        boxShadow: '0 8px 20px rgba(0,0,0,.35)',
        backdropFilter: 'blur(6px)'
    });

    // 按钮动画CSS
    const style = document.createElement('style');
    style.innerHTML = `
    #clearGridBtn {
        transform: translate(-50%, 120px); /* 初始在屏幕外 */
        opacity: 0;
        transition: all .45s cubic-bezier(.2,.8,.2,1);
    }

    /* 显示：滑入 */
    #clearGridBtn.show {
        transform: translate(-50%, 0);
        opacity: 1;
    }

    /* 点击：滑出 */
    #clearGridBtn.exit {
        transform: translate(-50%, 140px);
        opacity: 0;
    }
  
    /* 减少GPU缓存 */
    #clearGridBtn {
        will-change: transform, opacity;
    }

    /* hover 单独控制 scale（不会破坏位移） */
    @media (hover: hover) {
        #clearGridBtn:hover {
            transform: translate(-50%, 0) scale(1.1);
        }
    }

    /* 删除动画 */
    .fly-up-remove {
        opacity: 0;
        transition:
            transform 0.6s cubic-bezier(.2,.8,.2,1),
            opacity 0.4s ease,
            filter 0.4s ease;
        filter: blur(3px);
    }
    `;
    document.head.appendChild(style);

    // 彩虹文字
    const text = btn.querySelector('.clear-btn-text');
    Object.assign(text.style, {
        fontSize: '15px',
        background:
            'linear-gradient(270deg,#ff0000,#ff00d6,#006eff,#00e4ff,#4dd2ff,#4d4dff,#b84dff,#ff4da6)',
        backgroundSize: '400% 400%',
        WebkitBackgroundClip: 'text',
        WebkitTextFillColor: 'transparent',
        animation:
            'rainbowFlow 6s linear infinite, glowPulse 2s ease-in-out infinite alternate',
        textShadow:
            '0 0 8px rgba(255,255,255,0.3), 0 0 20px rgba(255,255,255,0.2)',
        userSelect: 'none'
    });

    // 显示控制
    function updateButtonVisibility() {
        const count = document.querySelectorAll(CLEAR_CONFIG.selector).length;

        if (count > CLEAR_CONFIG.showLimit) {

            // 重置到屏幕外
            btn.classList.remove('show');

            // 强制重排
            btn.offsetHeight;

            // 触发动画
            btn.classList.add('show');
            btn.classList.remove('exit');

        } else {
            btn.classList.remove('show');
        }
    }

    // 监听变化
    const observer = new MutationObserver(updateButtonVisibility);
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });

    // 点击事件
    btn.addEventListener('click', function () {

        const targets = document.querySelectorAll(CLEAR_CONFIG.selector);

        if (targets.length === 0) {
            showToast('当前没有图片');
            return;
        }

        btn.classList.add('exit');
        btn.classList.remove('show');

        // 临时禁用点击.防连点
        btn.style.pointerEvents = 'none';

        targets.forEach(el => {
            const rotate = (Math.random() * 20 - 10);
            const x = (Math.random() * 60 - 30);
            const y = -(500 + Math.random() * 250);

            el.style.transform = `translate(${x}px, ${y}px) rotate(${rotate}deg) scale(0.85)`;
            el.classList.add('fly-up-remove');
        });

        setTimeout(() => {

            targets.forEach(el => el.remove());

            rebuildIsotope();
            updateButtonVisibility();

        }, 400);


        function rebuildIsotope() {
            if ($grid && $grid.data('isotope')) {
                $grid.isotope('destroy');
            }

            if ($grid.find('.grid-sizer').length === 0) {
                $grid.prepend('<div class="grid-sizer"></div>');
            }

            setTimeout(() => {
                initIsotope();
            }, 50);
        }

        // 恢复点击时间
        setTimeout(() => {
            btn.style.pointerEvents = 'auto';
        }, 1000);

        showToast(`已清理 ${targets.length} 张图片\n加载新图中`);
    });

    document.body.appendChild(btn);

})();

// 页面内图片清空按钮


//整体结束
});


// 点击复制链接
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(
        function () {
            showToast("复制成功");
        },
        function (err) {
            showToast("复制失败.请手动右键复制");
        }
    );
}

// 触发提示
function showToast(msg) {
    let toast = document.createElement("div");
    toast.innerText = msg;

    toast.style.position = "fixed";
    toast.style.bottom = "60px";
    toast.style.left = "50%";
    toast.style.transform = "translateX(-50%)";
    toast.style.background = "rgba(0,0,0,0.75)";
    toast.style.color = "#fff";
    toast.style.padding = "10px 25px";
    toast.style.borderRadius = "10px";
    toast.style.fontSize = "15px";
    toast.style.zIndex = "9999";
    toast.style.opacity = "0";
    toast.style.transition = "opacity .3s";
    toast.style.textAlign = "center"; // 文字居中

    document.body.appendChild(toast);

    // 淡入
    setTimeout(() => {
        toast.style.opacity = "1";
    }, 10);

    // 淡出
    setTimeout(() => {
        toast.style.opacity = "0";
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}


//跳转手机页面
        // function is_mobile() { 
        // var regex_match = /(nokia|iphone|android|motorola|^mot-|softbank|foma|docomo|kddi|up.browser|up.link|htc|dopod|blazer|netfront|helio|hosin|huawei|novarra|CoolPad|webos|techfaith|palmsource|blackberry|alcatel|amoi|ktouch|nexian|samsung|^sam-|s[cg]h|^lge|ericsson|philips|sagem|wellcom|bunjalloo|maui|symbian|smartphone|midp|wap|phone|windows ce|iemobile|^spice|^bird|^zte-|longcos|pantech|gionee|^sie-|portalmmm|jigs browser|hiptop|^benq|haier|^lct|operas*mobi|opera*mini|320x320|240x320|176x220)/i; 
        // var u = navigator.userAgent; 
        // if (null == u) { 
        // return true; 
        // } 
        // var result = regex_match.exec(u); 

        // if (null == result) { 
        // return false 
        // } else { 
        // return true 
        // } 
        // } 
        // if (is_mobile()) { 
        // document.location.href= 'Mobile.php'; 
        // } 

(function() {
        // 判断是否为触控设备（iPad, iPhone, Android 等）
        var isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;

        // 判断屏幕尺寸大小
        var isSmallScreen = window.innerWidth <= 1024;

        // 触控设备屏幕不大.跳转到手机版
        if (isTouchDevice && isSmallScreen) {
            // 检查当前是否已经在手机版
            if (!window.location.href.includes("Mobile.php")) {
                window.location.href = "Mobile.php";
            }
        }
})();