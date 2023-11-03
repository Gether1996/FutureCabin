var selectedEndDates = [];

document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');
  var checkoutLink = document.getElementById('checkout-link');
  var dateDisplay = document.getElementById('dateDisplay');
  var selectedDatesDisplay = document.getElementById('selectedDatesDisplay');

  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    events: eventData,
    selectable: true,
    selectAllow: function(info) {
      // Only allow the selection if there are less than 2 selections
      return selectedEndDates.length < 2;
    },
    select: function(info) {
    var today = document.querySelector('.fc-day-today');

      today.addEventListener('click', function(e) {
        e.target.classList.add('selected-date');
      });
      var start = info.start;
      var end = info.end;

      var endDate = end.toISOString().split('T')[0];
      selectedEndDates.push(endDate);

      if (selectedEndDates.length === 2) {
        // Display the selected dates if exactly two dates are picked
        dateDisplay.style.visibility = 'visible';
        dateDisplay.style.opacity = 1;
        selectedDatesDisplay.textContent = formatSelectedDates(selectedEndDates);
      }

      highlightSelectedDates(selectedEndDates);

      checkoutLink.href = '/checkout/' + '?dates=' + selectedEndDates.join(',');
    },
    firstDay: 1,
    locale: 'sk', // Set the locale to Slovak
    buttonText: {
      today: 'Aktuálny Mesiac' // Customize the "today" button text to Slovak
    }
  });

  calendar.render();
});

function highlightSelectedDates(selectedDates) {
  // Helper function to add a CSS class to the selected dates
  selectedDates.forEach(function (date) {
    var dateElement = document.querySelector('.fc-day[data-date="' + date + '"]');
    if (dateElement) {
      dateElement.classList.add('selected-date');
    }
  });
}

function formatSelectedDates(dates) {
  // Function to format dates as DD.MM.YYYY
  var sortedDates = dates.map(function (dateString) {
    return new Date(dateString);
  }).sort(function (a, b) {
    return a - b;
  });

  var formattedDates = sortedDates.map(function (date) {
    var day = date.getDate().toString().padStart(2, '0');
    var month = (date.getMonth() + 1).toString().padStart(2, '0');
    var year = date.getFullYear();
    return day + '.' + month + '.' + year;
  });

  return formattedDates.join(' - ');
}