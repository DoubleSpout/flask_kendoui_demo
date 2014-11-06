$(function(){


//高亮当前路径
$('#leftBar a').each(function(){
    if(location.pathname.indexOf('/home/index') == 0) return;
    var aHref = $(this).attr('href')
    if(location.pathname.indexOf('aHref') == 0){
        $(this).parent().addClass('active')
    }
})
//高亮当前路径






})