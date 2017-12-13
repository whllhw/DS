let table_2 = $('#datatables2').DataTable({
    "processing": true,
    "serverSide": true,
    "ajax": {
        "url": "/api/edges",
        "type": "GET"
    },
    "columns": [
        {"data":"id"},
        {"data": "head"},
        {"data": "tail"},
        {"data": "duration"},
        {"data":"ES"},
        {"data":"LS"},
        {"data":"TF"},
        {"data":"Is_Critcal_Path"},
        {"data":"EF"},
        {"data":"LF"},
        {"data":"FF"},
        {"data": "name"},
        {"data": "note"},
        {
            "data": null,
            "defaultContent": '<button type="button" class="btn btn-info">Edit</button>' + '&nbsp;&nbsp' +
            '<button type="button" class="btn btn-danger">Delete</button>'
        }
    ]
});

[4,5,6,7,8,9,10].forEach(function(i){
    table_2.column(i).visible(false);
});

let id_2 = 0;

$('#datatables2 tbody').on('click', 'button', function () {
    console.log(this);
    let data = table_2.row($(this).parents('tr')).data();
    let class_name = $(this).attr('class');
    if (class_name == 'btn btn-info') {
        // EDIT button
        $('#id_2').val(data['id']);
        $('#head').val(data['head']);
        $('#tail').val(data['tail']);
        $('#duration').val(data['duration']);
        $('#noteEdge').val(data['note']);
        $('#name').val(data['name']);

        $('#type_2').val('edit');
        $('#modal_title_2').text('EDIT');
        $("#myModal_2").modal();
    } else {
        // DELETE button
        $('#modal_title').text('DELETE');
        $("#confirm_2").modal();
    }

    id_2 = data['id'];

});

$('#edgeForm').on('submit', function (e) {
    e.preventDefault();
    let $this = $(this);
    let type = $('#type_2').val();
    let method = '';
    let url = '/api/edges';
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
        table_2.ajax.reload();
        $('#myModal_2').modal('hide');
    }).error(function (jqXHR, textStatus, errorThrown) {
        console.log(jqXHR)
    });
});

$('#confirm_2').on('click', '#delete', function (e) {
    $.ajax({
        url: '/api/edges/' + id_2 + '/',
        method: 'DELETE'
    }).success(function (data, textStatus, jqXHR) {
        table_2.ajax.reload();
        $('#confirm_2').modal('hide');
    }).error(function (jqXHR, textStatus, errorThrown) {
        console.log(jqXHR)
    });
});


$('#new_2').on('click', function (e) {
    $('#id_2').val('');
    $('#head').val('');
    $('#tail').val('');
    $('#duration').val('');
    $('#noteEdge').val('');
    $('#name').val('');

    $('#type_2').val('new');
    $('#modal_title').text('NEW');
    $("#myModal_2").modal();
});

$('#showResult').click(function(e){
    e.preventDefault();
    [4,5,6,8,9,10].forEach(function(i){
    table_2.column(i).visible(true);
});
    table_2.ajax.url('/api/resultEdge').load();
    
});