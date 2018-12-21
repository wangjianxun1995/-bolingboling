var currentCid = 1; // 当前分类 id
var cur_page = 1; // 当前页
var total_page = 1;  // 总页数
var data_querying = false;   // 是否正在向后台获取数据

// if(!data_querying){
//                 data_querying = true
//                 if (cur_page<total_page){
//                     updateNewsData()
//                 }

$(function () {

    //请求数据更新
    updateNewsData()
    // 首页分类切换
    $('.menu li').click(function () {
        var clickCid = $(this).attr('data-cid')
        $('.menu li').each(function () {
            $(this).removeClass('active')
        })
        $(this).addClass('active')

        if (clickCid != currentCid) {
            // 记录当前分类id
            currentCid = clickCid

            // 重置分页参数
            cur_page = 1
            total_page = 1
            updateNewsData()
        }
    })

    //页面滚动加载相关
    $(window).scroll(function () {

        // 浏览器窗口高度
        var showHeight = $(window).height();

        // 整个网页的高度
        var pageHeight = $(document).height();

        // 页面可以滚动的距离
        var canScrollHeight = pageHeight - showHeight;

        // 页面滚动了多少,这个是随着页面滚动实时变化的
        var nowScroll = $(document).scrollTop();

        if ((canScrollHeight - nowScroll) < 100) {
            // TODO 判断页数，去更新新闻数据
            // 当前是 第1页 总页数是 100
            // 当有一次滚动满足条件的时候  我们就去请求数据
            // 用一个标记位 来记录我们已经请求的数据
            if(!data_querying){
                data_querying = true
                if (cur_page<total_page){
                    updateNewsData()
                }

            }else {
                data_querying =false
            }
        }
    })
})

function updateNewsData() {
    params ={
        'cid':currentCid , // 默认cid
        'page':cur_page,
        'per_page':20

    }


    // 更新新闻数据
    // $.ajax({
    //     url:'news_list',
    //     type:'get',
    //     data:params,
    //     success:function (resp) {
    //
    //     }
    //
    // })
    $.get('/news_list',params,function (resp) {
        if (resp.errno=='0'){
            total_page =resp.total_page
            //先清空类名为list_con的原有数据
            $('.list_con').html('')
            // 显示数据
            // 显示数据
            for (var i=0;i<resp.news_list.length;i++) {
                var news = resp.news_list[i]
                var content = '<li>'
                content += '<a href="#" class="news_pic fl"><img src="' + news.index_image_url + '?imageView2/1/w/170/h/170"></a>'
                content += '<a href="#" class="news_title fl">' + news.title + '</a>'
                content += '<a href="#" class="news_detail fl">' + news.digest + '</a>'
                content += '<div class="author_info fl">'
                content += '<div class="source fl">来源：' + news.source + '</div>'
                content += '<div class="time fl">' + news.create_time + '</div>'
                content += '</div>'
                content += '</li>'
                $(".list_con").append(content)
            }
        }
    })
}
