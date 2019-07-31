
function updata() {
            $.ajax({
                type:"POST",
                url:"query_user/",
                data:{'username':$('#query_name').val()},
                dataType:"json",
                success:function(data){
                    document.getElementById('id').innerText = data.id;
                    document.getElementById('head_image').src = data.head_image;
                    document.getElementById('username').innerText = data.username;
                    document.getElementById('nickname').innerText = data.nickname;
                    document.getElementById('telephone').innerText = data.telephone;
                    document.getElementById('sex').innerText = data.sex;
                    alert("查询成功");
                },
                error:function (e) {
                    alert("查询失败");
                }
            })
        }

function get_user(id) {
    $.ajax({
        type:"GET",
        url:"query_passage/",
        data:{'pid':$('#query_passage_pid').val(), 'type':$('#query_passage_type').val()},
        dataType:"json",
        success:function (data) {
            document.getElementById('query_passage_pid2').innerText = data.data.pid;
            document.getElementById('query_passage_ptitle').innerText = data.data.ptitle;
            document.getElementById('query_passage_purl').innerText = data.data.purl;
            document.getElementById('query_passage_ppic').src = data.data.ppic;
            alert(data.msg)
        },
        error:function(e){
            alert("收藏失败")
        }
    })
}

$(document).ready(function(id, page) {
    // $("#modify_image_head_image").on("change",upload(id,page))

});
    // document.getElementById('modify_image_head_image').click();
    // var fileDom = document.getElementById('modify_image_head_image');
    // var img = document.getElementById('head_image');
    // var file = fileDom.files[0];
    // var reader = new FileReader();
    // reader.readAsDataURL(file);
    // var form = document.getElementById('modify_image_form');

function upload(id) {
    var formData = new FormData();
    formData.append("head_image",$("#modify_image_head_image")[0].files[0]);
    formData.append("type",$('#modify_image_type').val());
    formData.append("id",id);
    $.ajax({
        type:"POST",
        url:"/manage/user_manage/modify_image/",
        contentType:false,
        processData:false,
        data:formData,
        dataType:"json",
        success:function (data) {
            document.getElementById('head_image').src = data.head_image;
            alert(data.msg)
        },
        error:function(e){
            alert("修改头像失败")
        }
    })
}





