function add_passage() {
    // var form = document.getElementById('add_passage_form');
    var formData = new FormData();
    formData.append("ppic",$('#ppic')[0].files[0]);
    formData.append("purl",$('#purl').val());
    formData.append("type",'web');
    formData.append("ptitle",$('#ptitle').val());

    $.ajax({
        type:"POST",
        url:"/manage/passage_manage/add_passage/",
        data:formData,
        dataType:"json",
        processData: false,
        contentType:false,
        success:function (data) {
            alert(data.msg)
        },
        error:function(e){
            alert("添加文章失败")
        }
    })
}

function upload() {
    var form = document.getElementById('add_passage_form');
    var formData = new FormData(form);
    formData.append("ppic",$('#ppic')[0].files[0]);
    // formData.append("type",'web');
    // formData.append('ptitle',$('#ptitle').val());
    // formData.append("purl",$('#purl').val());
    // alert(formData.ppic)
    $.ajax({
        type:"POST",
        url:"/manage/passage_manage/add_passage/",
        data:formData,
        dataType:"json",
        success:function (data) {
            alert(data.msg)
        },
        error:function(e){
            alert("添加文章失败")
        }
    })
}


// function read_image() {
//     var image = '';
//
//
// }