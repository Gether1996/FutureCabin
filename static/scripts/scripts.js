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