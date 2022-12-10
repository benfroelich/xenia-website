function get_toasts() {
  return document.querySelectorAll('.toast')
}

function init_toasts() {
  get_toasts().forEach((toast_elem) => {
    toast_inst = new bootstrap.Toast(toast_elem);
  })
}

function show_toasts() {
  get_toasts().forEach((toast_elem) => {
    toast_inst = new bootstrap.Toast(toast_elem);
    toast_inst.show()
  })
}

window.onload = () => {
  init_toasts()

  toasts = get_toasts()
  // also set up the "unhide" button
  if(toasts) {
    console.log("some toast for you")
    toast_button = document.getElementById('toast-restore')
    if(toast_button) {
      toast_button.addEventListener('click', show_toasts)
    }
  }
}

// TODO: add a toast show button
//const toastTrigger = document.getElementById('liveToastBtn')
//const toastLiveExample = document.getElementById('liveToast')
//if (toastTrigger) {
//  toastTrigger.addEventListener('click', () => {
//    const toast = new bootstrap.Toast(toastLiveExample)
//    toast.show()
//  })
//}
//const myToastEl = document.getElementById('myToast')
//myToastEl.addEventListener('hidden.bs.toast', () => {
//  // do something...
//})
