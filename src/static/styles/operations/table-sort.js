class ItcModal {
  #template = '<div class="itc-modal-backdrop"><div class="itc-modal-content"><div class="itc-modal-header"><div class="itc-modal-title">{{title}}</div><span class="itc-modal-btn-close" title="Закрыть">×</span></div><div class="itc-modal-body">{{content}}</div>{{footer}}</div></div>';
  // ...
}

$(document).ready(function() {
      console.log('start');
      $('.sortable').click(function() {
        var table = $(this).parents('table').eq(0);
        var rows = table.find('tr:gt(0)').toArray().sort(comparer($(this).index()));
        this.asc = !this.asc;
        if (!this.asc) {
          rows = rows.reverse();
        }
        table.children('tbody').empty().html(rows);
      });

       $("#form_operations").click(function(){
       var checked_rows = [];
        var checked = $("#OperationTable tr").filter(':has(:checkbox:checked)').find('td:eq(1)');
        checked.each(function() {
            checked_rows.push(this.textContent);
        });
        const result = confirm(`Сформировать операции и загрузить заявку в терминал  по следующим портфелям: ${checked_rows}?`);
        if (result == true) {
            $('#portfolios').val(checked_rows);
            console.log($('#portfolios').val);
            $('#formOperations').submit();
        }
    });

    var operations = $("#OperationsString").text().trimStart();
    console.log(operations)
    if (operations.includes('ACCOUNT')) {
//        $('#portfolios_').val(getCheckedRows());
        $('#total_operations').val(operations);
        $("#staticBackdrop").modal('show');

//        const preview = prompt("Предварительный просмотр сформированного документа", operations);
//        if (preview != null) {
//            $('#portfolios_').val(getCheckedRows());
//            $('#total_operations').val(preview);
//            console.log($('#total_operations').val);
//            console.log($('#portfolios').val);
//            $('#sendOperations').submit();
//        }
//        else {
//        $("#OperationsString").text('');
//        }
    }

    $("#OperationSubmit").click(function(){
        $('#sendOperations').submit();
    });

    });

function comparer(index) {
    return function(a, b) {
        var valA = getCellValue(a, index), valB = getCellValue(b, index)
        return $.isNumeric(valA) && $.isNumeric(valB) ? valA - valB : valA.toString().localeCompare(valB)
    }
}

function getCellValue(row, index) {
  return $(row).children('td').eq(index).text();
}


function getCheckedRows() {
    var checked_rows = [];
        var checked = $("#OperationTable tr").filter(':has(:checkbox:checked)').find('td:eq(1)');
        checked.each(function() {
            checked_rows.push(this.textContent);
        });
       return checked_rows
}