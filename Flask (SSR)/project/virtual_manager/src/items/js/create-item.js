$(document).ready(function () {
  // TODO: https://youtu.be/nRHbOOSTprk
  // TODO: Improve check buttons data biding
  if ($('#data').html()){
    const data = JSON.parse($('#data').html())
    Object.entries(data).forEach(([key, value]) => {
      if (key == "is_product") {
        $(`#is_product${value}`).prop('checked', true)
        if (value == 1) {
          $('#salePriceDiv').show()
        }
      } else {
        $(`#${key}`).val(value)
      }
    })
  } 
  
  let salePrice = $('#sale_price').val()
  $('#sale_price').on('keyup', function () {
    salePrice = $('#sale_price').val()
  })

  $('[name="is_product"]').change(function () {
    if ($(this).val() == 1) {
      $('#salePriceDiv').show()
      $('#sale_price').val(salePrice)
    } else {
      $('#salePriceDiv').hide()
      $('#sale_price').val(null)
    }
  })
})