$(document).ready(function() {


    $("#companytickers").on('change', function(){
      let company_id = document.getElementById('companytickers').value;

      $.ajax({
        url: "../company_overview/"+company_id,
        dataType: 'json',
        success: function (data) {
            document.getElementById('company-details').innerHTML = data['name'];
        }
      });
    });


  });
