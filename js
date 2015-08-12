function loadtest(p) 
{
    this.page = p;
    $("#" + c_obj).html("<div align='center'><img src='" + '/' + "images/loading.gif'>正在读取数据...</div>");
    $.ajax({
        type: "post",
        url: '/' + 'item/ajaxpage.asp' + "?labelid=" + '20127957470240' + "&infoid=" + '' + "&classid=" + '20138907766269' + "&refreshtype=" + 'Folder' + "&specialid=" + '' + "&curpage=" + p + getUrlParam(),
        success: function(d) {
            $("#" + c_obj).html("<ul>" + d + "</ul>");
        }
    });
}

function loadtest(p) 
{
    this.page = p;
    $.ajax({
        type: "post",
        url: 'http://www.qyggzyjy.com/' + 'item/ajaxpage.asp' + "?labelid=" + '20127957470240' + "&infoid=" + '' + "&classid=" + '20138907766269' + "&refreshtype=" + 'Folder' + "&specialid=" + '' + "&curpage=" + p + '&id=1514',
        success: function(d) {
            alert(d)
        }
    });
}

function url(p)
{
    url = '/' + 'item/ajaxpage.asp' + "?labelid=" + '20127957470240' + "&infoid=" + '' + "&classid=" + '20138907766269' + "&refreshtype=" + 'Folder' + "&specialid=" + '' + "&curpage=" + p + getUrlParam()
    alert(url)
}

ASP.NET_SessionId=2nilcdld2ldvwxctoix1ykld
ASP.NET_SessionId=2nilcdld2ldvwxctoix1ykld

6FA100BB-20150228-025839-140a2d-0496ae
6FA100BB-20150228-025839-140a2d-0496ae


function tab(id, type) {

    for (var i = 1; i < 8; i++) {
        if (document.getElementById(type + "_" + i)) {
            document.getElementById(type + "_" + i).className = "";
            document.getElementById(type + "_" + i + '_content').style.display = "none";
        }
    }
    if (document.getElementById(id + '_content')) {
        document.getElementById(id).className = "dq";
        document.getElementById(id + '_content').style.display = "";
    }
}

function initPage(id,docObj){
    //判断数组中是否存在该变量，如果存在则
    var obj = _getPagefromArr(id);
    if (!( obj != null && typeof(obj)!="undefined" && obj !="undefined"  )){
        obj = new ucap_pageinfo(id);
        if( docObj ){
            obj.docObj = docObj;
        }
        ucap_pageinfo_list_arr.push( obj );
    }else if(docObj){
        obj.docObj = docObj;
    }
    obj.setObj();
    //默认定位到第一页
    obj.toPage(1);
    //将标志位设回
    obj.m_bFirst  = false;
}