function add_collection() {
    $.ajax({
        type:"POST",
        url:"/manage/passage_manage/add_collection/",
        data:{'cid':$('#cid').val(),'cpid':$('#cpid').val(),'date':$('#date').val(),'type':'web'},
        dataType:"json",
        // processData: false,
        // contentType:false,
        success:function (data) {
            alert(data.msg)
        },
        error:function(e){
            alert("添加收藏失败")
        }
    })
}