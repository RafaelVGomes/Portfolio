$(document).ready(function () {
  $('#itemsContainer').hide()
  if ($('#productData').html()) {
    const data = JSON.parse($('#productData').html())
    Object.entries(data).forEach(([key, value]) => {
      if (key == "has_recipe") {
        $(`#has_recipe${value}`).prop('checked', true)
        if (value == 1) {
          $('#itemsContainer').show()
        }
      } else {
        $(`#${key}`).val(value)
      }
    })
  }

  $('[name="has_recipe"]').change(function () {
    if ($(this).val() == 1) {
      $('#itemsContainer').show()

      $("#itemsColumn").find("input[type=checkbox]:checked").each(function () {
        $(this).prop('checked', false)
      })
    } else {
      $('#itemsContainer').hide()

      let deletedForms = []

      $("#itemsColumn").find("input[type=checkbox]").each(function () {
        $(this).prop('checked', true)
      })

      $("#inlineFormsTotal").val($("#itemsColumn").children().length)

      $("#itemsColumn").find("input[type=checkbox]:checked").each(function () {
        const form = $($(this).val())
        const index = Number(form.attr('id').match(/(\d$)/g)[0])
        deletedForms.push(index)
      })

      $("#deletedInlineForms").val(deletedForms)
    }
  })

  $('#delItemBtn').attr('disabled', 'disabled')

  let checked = 0
  $('input[type=checkbox]').click(function () {
    let formsAmount = $("#itemsColumn").children().length
    if (this.checked) {
      checked++
    } else {
      checked--
    }

    if (checked == formsAmount || formsAmount < 2) {
      $('#delItemBtn').attr('disabled', 'disabled')
    } else {
      $('#delItemBtn').removeAttr('disabled')
    }
  })

  let createdForms = []
  if (!$('#recipesData').html()) {
    createdForms.push(0)
    $("#createdInlineForms").val(createdForms)
  }

  $("#inlineFormsTotal").val($("#itemsColumn").children().length)
  $('#addItemBtn').click(function () {
    const index = Number($("#inlineFormsTotal").val())
    const form = $(`#inlineForm${index - 1}`).clone(true)
    const formId = form.attr('id').replace(index - 1, index)
    const delForm = form.find(`#delForm${index - 1}`)
    const delFormId = delForm.attr('id').replace(index - 1, index)
    const delFormVal = delForm.attr('value').replace(index - 1, index)
    const select = form.find("select")
    const amount = form.find(`#itemAmount${index - 1}`)
    const amountId = amount.attr('id').replace(index - 1, index)
    const name = select.attr("name").replace(index - 1, index)

    form.attr('id', formId)
    delForm.attr('id', delFormId)
    delForm.prop('checked', false)
    delForm.val(delFormVal)
    select.attr('name', name)
    select.children().each(function () {
      $(this).prop('selected', false)
    })
    select.children().first().prop('selected', true)
    amount.attr('name', name)
    amount.val(null)
    amount.attr('id', amountId)

    $("#itemsColumn").append(form)
    $("#inlineFormsTotal").val(index + 1)

    if ($("#itemsColumn").children().length > 1) {
      $('#delItemBtn').removeAttr('disabled')
    }

    createdForms.push(index)
    $("#createdInlineForms").val(createdForms)
  })

  let deletedForms = []
  $("#delItemBtn").click(function () {
    $("#itemsColumn").find("input[type=checkbox]:checked").each(function () {
      const form = $($(this).val())
      const index = Number(form.attr('id').match(/(\d$)/g)[0])
      deletedForms.push(index)
      form.hide()
      $("#inlineFormsTotal").val($("#inlineFormsTotal").val() - 1)
      checked--
    })

    $("#deletedInlineForms").val(deletedForms)

    let formsAmount = $("#itemsColumn").children().length
    if (checked == formsAmount || formsAmount < 2) {
      $('#delItemBtn').attr('disabled', 'disabled')
    } else {
      $('#delItemBtn').removeAttr('disabled')
    }
  })
})