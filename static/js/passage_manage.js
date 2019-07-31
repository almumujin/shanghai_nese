
function add_passage() {
    $.ajax({
        type: "POST",
        url: "add_passage/",
        data: {'ptitle': $('#ptitle').val(),'purl':$('#purl').val()},
        dataType: "json",
        success: function (data) {
            alert("添加成功")
         },
        error:function (e) {
            alert("添加失败")
        }
    })
}

function add_collection() {
    $.ajax({
        type:"POST",
        url:"add_collection/",
        data:{'id':$('#add_collection_id').val(),'pid':$('#add_collection_pid').val(),
        'date':$('#add_collection_date').val(), 'type':$('#add_collection_type').val(),
        'password':$('#add_collection_password').val()},
        dataType:"json",
        success:function (data) {
            alert(data.msg)
        },
        error:function(e){
            alert("收藏失败")

        }
    })
}
function delete_passage(pid) {
    $.ajax({
        type:"POST",
        url:"delete_passage/",
        data:{'pid': pid, 'type': 'web'},
        dataType:"json",
        success:function (data) {
            alert(data.msg)
        },
        error:function(e){
            alert("收藏失败")
        }
    })
}

function query_passage() {
    $.ajax({
        type:"POST",
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

function cancel_collection(cid, cpid, date) {
    $.ajax({
        type:"POST",
        url:"/manage/passage_manage/cancel_collection/",
        data:{'cpid': cpid, 'type': 'web', 'cid':cid, 'date':date},
        dataType:"json",
        success:function (data) {
            alert(data.msg)
        },
        error:function(e){
            alert("取消收藏失败")
        }
    })
}
