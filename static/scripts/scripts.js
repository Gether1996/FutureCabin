function logoutConfirmation() {
    Swal.fire({
        title: 'Odhlásiť?',
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Áno',
        confirmButtonColor: 'rgba(0, 0, 40, 0.9)',
        cancelButtonText: 'Nie'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = "/logout/";
        }
    });
}

function switchLanguage(language_code) {
  fetch("/switch_language/" + String(language_code) + '/', {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      'X-CSRFToken': csrf_token,
    },
  })
    .then(response => response.json())
    .then(data => {
      Swal.fire({
        position: 'top',
        title: (language_code === 'sk') ? 'Switching to slovak.' : 'Prepínam na angličtinu.',
        icon: 'info',
        iconColor: 'rgba(0, 0, 40, 0.9)',
        showConfirmButton: false,
        timer: 900
      });
      setTimeout(function () {
        location.reload();
      }, 900);
    })
    .catch(error => {
      console.error("Error switching language:", error);
    });
}