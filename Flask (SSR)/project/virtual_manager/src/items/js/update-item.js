$(document).ready(function () {
  if ($("#is_product1").prop('checked')) {
    $('#salePriceDiv').show()
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