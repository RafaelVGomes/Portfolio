$(document).ready(function () {
  let username = false
  let password = false

  if (!$("#username").val() && !$("#password").val()) {
    $("#submit-btn").prop('disabled', true)
  }
  
  function check_fields() {
    if (username && password) {
      $("#submit-btn").prop('disabled', false)
    } else (
      $("#submit-btn").prop('disabled', true)
    )
  }

  $("#username").keyup(function() {
    if ($(this).val().length >= 3) {
      username = true
    } else {
      username = false
    }
    check_fields()
  })

  $("#password").keyup(function() {
    if ($(this).val().length >= 3) {
      password = true
    } else {
      password = false
    }
    check_fields()
  })
})