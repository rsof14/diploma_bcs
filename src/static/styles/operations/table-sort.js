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
        console.log("button");
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

