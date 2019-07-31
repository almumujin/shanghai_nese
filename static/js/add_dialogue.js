function add_dialogue(sid) {
        $.ajax({
        type:"POST",
        url:"/manage/scene_manage/add_dialogue/",
        data:{'type':'web','dname':$('#dname').val(),'dlyric':$('#dlyric').val(),
            'durl':$('#durl').val()},
        dataType:"json",
        processData: false,
        contentType:false,
        success:function (data) {
            alert(data.msg)
        },
        error:function(e){
            alert("添加对话失败")
        }
    })
}