let table = $('#datatables').DataTable({
    "processing": true,
    "serverSide": true,
    "ajax": {
        "url": "/api/nodes",
        "type": "GET"
    },
    "columns": [
        {"data": "id"},
        
        {"data":"ES"},
        {"data":"LS"},
        {"data": "nodeName"},
        {"data": "uid"},
        {"data": "note"},
        {
            "data": null,
            "defaultContent": '<button type="button" class="btn btn-info">Edit</button>' + '&nbsp;&nbsp' +
            '<button type="button" class="btn btn-danger">Delete</button>'
        }
    ]
});
table.column(1).visible(false);
table.column(2).visible(false);

let id = 0;

$('#datatables tbody').on('click', 'button', function () {
    
    let data = table.row($(this).parents('tr')).data();
    let class_name = $(this).attr('class');
    if (class_name == 'btn btn-info') {
        // EDIT button
        $('#id').val(data['id']);
        $('#uid').val(data['uid']);
        $('#note').val(data['note']);
        $('#nodeName').val(data['nodeName']);
        // $('#costTime').val(data['costTime']);
        $('#type').val('edit');
        $('#modal_title').text('EDIT');
        $("#myModal").modal();
    } else {
        // DELETE button
        $('#modal_title').text('DELETE');
        $("#confirm").modal();
    }

    id = data['id'];

});

$('#nodeForm').on('submit', function (e) {
    e.preventDefault();
    let $this = $(this);
    let type = $('#type').val();
    let method = '';
    let url = '/api/nodes';
    if (type == 'new') {
        // new
        method = 'POST';
    } else {
        // edit
        // url = url + id + '/';
        method = 'PUT';
    }

    $.ajax({
        url: url,
        method: method,
        data: $this.serialize()
    }).success(function (data, textStatus, jqXHR) {
        table.ajax.reload();
        $('#myModal').modal('hide');
    }).error(function (jqXHR, textStatus, errorThrown) {
        console.log(jqXHR)
    });
});

$('#confirm').on('click', '#delete', function (e) {
    $.ajax({
        url: '/api/nodes/' + id + '/',
        method: 'DELETE'
    }).success(function (data, textStatus, jqXHR) {
        table.ajax.reload();
        $('#confirm').modal('hide');
    }).error(function (jqXHR, textStatus, errorThrown) {
        console.log(jqXHR)
    });
});


$('#new').on('click', function (e) {
    $('#uid').val('');
    $('#nodeName').val('');
    $('#note').val('');
    $('#type').val('new');
    $('#modal_title').text('NEW');
    $("#myModal").modal();
});


$('#showResult').click(function(e){
    e.preventDefault();
    table.column(1).visible(true);
    table.column(2).visible(true);
    table.ajax.url('/api/result').load();

});