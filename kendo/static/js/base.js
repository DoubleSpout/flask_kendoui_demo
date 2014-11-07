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
            //"subscript",
            //"superscript",
            //"createTable",
            //"addRowAbove",
            //"addRowBelow",
            //"addColumnLeft",
            //"addColumnRight",
            //"deleteRow",
            //"deleteColumn",
            "viewHtml",
            //"formatting",
            //"fontName",
            //"fontSize",
            //"foreColor",
            //"backColor"
        ]

window.is_show_array = [
              { text: "启用", value: true },
              { text: "不启用", value: false}
            ]

window.toolbarAry = [
            { name: "create", text: "添加" }
          ]


window.commandAry = [
            { name: "edit", text: {edit: "编辑", update: "确定",  cancel: "取消"} },
            { name: "destroy", text: "删除"}
          ]



//下拉菜单
window.dropdown_init = function($obj, $array,onchange,init){
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

}





})