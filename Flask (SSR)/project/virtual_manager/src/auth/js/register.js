// handles data biding
$(document).ready(function () {
  if ($('#data').html()) {
    const data = JSON.parse($('#data').html())
    Object.entries(data).forEach(([key, value]) => {
      $(`#${key}`).val(value)
    })
  }

  // Check username on keyup
  let flag = undefined
  let q = null
  
  function fetch_username_status() {
    $.get(`${window.location.href}?q=${q}`, function (status){
      flag = JSON.parse(status)
      display_username_status()
    })
  }
  
  function display_username_status() {
    if (flag == false) {
      $('#username_error').html(`
        <span class="text-success" id="username_status"><i class="bi bi-check-circle"></i> Username available.</span>
      `)
      $('#submit-btn').prop('disabled', false)
    } else if (flag == true) {
      $('#username_error').html(`
        <span class="text-danger" id="username_status"><i class="bi bi-x-circle"></i> Username unavailable.</span>
      `)
      $('#submit-btn').prop('disabled', true)
    } else {
      $('#username_error').html(`
        <span class="text-danger" id="username_status"><i class="bi bi-x-circle"></i> ${data}</span>
      `)
      $('#submit-btn').prop('disabled', true)
    }
  }
  
  const check_username = {
    setup () {
      if (typeof this.timeoutID === "number") {
        this.cancel()
      }

      this.timeoutID = setTimeout(fetch_username_status, 3000)
    },
    
    cancel() {
      clearTimeout(this.timeoutID)
    }
  }
  
  $('#username').keyup(function () {
    flag = null
    q = $(this).val()

    $('#username_error').html(`
      <div class="text-secondary" id="username_spinner">
        <span class="spinner-border spinner-border-sm" aria-hidden="true"></span>
        <span role="status">Checking usernames...</span>
      </div>`
    )

    if (q.length > 0) {
      check_username.setup()
    } else {
      $('#username_spinner').remove()
    }
  })
})