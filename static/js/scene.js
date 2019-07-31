function delete_dialogue(did) {
        $.ajax({
        type:"POST",
        url:"/manage/scene_manage/delete_dialogue/",
        data:{'did':did,'type':'web'},
        dataType:"json",
        // processData: false,
        // contentType:false,
        success:function (data) {
            alert(data.msg)
        },
        error:function(e){
            alert("删除对话失败")
        }
    })
}