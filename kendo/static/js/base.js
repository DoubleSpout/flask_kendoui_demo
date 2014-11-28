$(function(){


//高亮当前路径
$('#leftBar').find('a').each(function(){
    if(location.pathname.indexOf('/home/index') == 0) return;
    var aHref = $(this).attr('href')

    if(location.pathname.indexOf(aHref) == 0){
        $(this).parent().addClass('active')
    }
})
//高亮当前路径

window.DataHost = ''
window.editor_tools = [
            "bold",
            "italic",
            "underline",
            "strikethrough",
            "justifyLeft",
            "justifyCenter",
            "justifyRight",
            "justifyFull",
            "insertUnorderedList",
            "insertOrderedList",
            "indent",
            "outdent",
            "createLink",
            "unlink",
            "insertImage",
            "subscript",
            "superscript",
            "createTable",
            "addRowAbove",
            "addRowBelow",
            "addColumnLeft",
            "addColumnRight",
            "deleteRow",
            "deleteColumn",
            "viewHtml",
            "formatting",
            "fontName",
            "fontSize",
            "foreColor",
            "backColor"
        ]


window.is_show_array = [
              { text: "启用", value: true },
              { text: "不启用", value: false}
            ]

window.is_on_off = [
              { text: "是", value: true },
              { text: "否", value: false}
            ]

window.toolbarAry = [
            { name: "create", text: "添加" }
          ]


window.commandAry = [
            { name: "edit", text: {edit: "编辑", update: "确定",  cancel: "取消"} },
            { name: "destroy", text: "删除"}
          ]



//下拉菜单
window.dropdown_init = function($obj, $array, bleanVal, onchange,init){
      var $obj = $obj || $("#isShow_inp")
      var $array = $array || window.is_show_array
      var onchange = onchange || $.noop;

      if(init && (!$obj.val() || $obj.val()=='0')){
        $obj.val(init).change()
      }
      var appid = $obj.val()
     var isFound = 0;
     $array.forEach(function(v){
        if(v.value == appid){
            isFound++
        }
     })
     if(isFound == 0){
        $obj.val($array[0].value).change();
     }
      $obj.kendoDropDownList({
            dataTextField: "text",
            dataValueField: "value",
            dataSource: $array,
            select:onchange
        })

       if($array[0].value === true){
           n =  bleanVal == 'true' ? 0 : 1
           var dropdownlist  = $obj.data("kendoDropDownList");
           dropdownlist.select(dropdownlist.ul.children().eq(n));

        }



}







window.kendo_edit_option = {
    tools: window.editor_tools,
    messages: window.editor_messages,
    imageBrowser: {
           messages: {
            dropFilesHere: "将图片拖进来"
           },
           transport: {
                read: {
                     url:"/thumb/read",
                     type: "POST"
                },
                destroy: {
                    url: "/thumb/destroy",
                    type: "POST"
                },
                create: {
                    url: "/thumb/create",
                    type: "POST"
                },
                thumbnailUrl: "/thumb/get",
                uploadUrl: "/thumb/upload",
                imageUrl: "/static/upload/{0}"
           }
        }
}






var thumbBoxIdCount = 0;
window.multiUpload = function($uploadInp, $dataInp, maxFiles){
    var maxFiles = maxFiles || 1;
    if(!$uploadInp) throw('no $uploadInp')
    if(!$dataInp) throw('no $dataInp')
    thumbBoxIdCount++

    var domId = Date.now() + '' +thumbBoxIdCount
    var thumbTemplate = '<div class="k-edit-label w-800-l">'+
                        '<label for="pictrue"></label></div>'+
                        '<div data-container-for="pictrue" class="k-edit-field w-800-r" id="thumbBox_'+domId+'"></div>'
    var imgTemplate = '<div class="thumbDivBox"><a href="{src}" target="_blank"><img src="{src}" class="thumb"/></a>'+
                      '<a href="javascript:;" class="deletethumb">删除</a></div>'


    var filesPathArray = [];

    $uploadInp.parent().after(thumbTemplate); //插入缩略图html文件
    var thumbBox = $('#thumbBox_'+domId);

    var getDateToArrayAndPutThumb = function(){
        var v = $.trim($dataInp.val())
        if(!v){
            filesPathArray = [];
            return;
        }

        v = v.split(',');

        var str = ''
        v.forEach(function(path){
            str += imgTemplate.replace(/\{src\}/g, path);
        })
        filesPathArray = v;
        thumbBox.html(str);
    }

    var addNewPath = function(newPath){
        filesPathArray.push(newPath);
        $dataInp.val(filesPathArray.join(',')).change()
        getDateToArrayAndPutThumb()
    }

    var removePath = function(rmPath){
        filesPathArray = filesPathArray.filter(function(p){
            return p != rmPath
        })
        $dataInp.val(filesPathArray.join(',')).change()
        getDateToArrayAndPutThumb()
    }

    thumbBox.delegate('.deletethumb','click',function(){
        if(confirm('确定删除吗?')){
            var that = $(this);
            var rmpath = that.parent().find('img').attr('src');
            removePath(rmpath);
            that.parent().remove();
          }
    })


    $uploadInp.kendoUpload({
            async: {
                saveUrl: "/upload/save",
                removeUrl: "/upload/delete",
                autoUpload: true
            },
            success:function(e){
                var path = e.response.result;
                addNewPath(path)
            },
            localization:{
                select: '请选择图片',
                remove: '',
                cancel: '',
                done:'完成'
            },
            select: function(e) {
                var len = filesPathArray.length;
                if(len >= maxFiles) {
                  e.preventDefault();
                  alert("最多上传: " + maxFiles+ ' 张图片');
                }
              }
        });

    getDateToArrayAndPutThumb();//初始化老数据

}





})