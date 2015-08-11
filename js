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