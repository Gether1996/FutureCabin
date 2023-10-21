var selectedEndDates = [];

document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');
  var checkoutLink = document.getElementById('checkout-link');
  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    events: eventData,
    selectable: true,
    selectAllow: function(info) {
      // Only allow the selection if there are less than 2 selections
      return selectedEndDates.length < 2;
    },
    select: function(info) {
      var start = info.start;
      var end = info.end;

      // Format the selected end dates in "yyyy-mm-dd" format
      var endDate = end.toISOString().split('T')[0];
      selectedEndDates.push(endDate);

      highlightSelectedDates(selectedEndDates);

      checkoutLink.href = '/checkout/' + '?dates=' + selectedEndDates.join(',');
    },
    firstDay: 1,
    locale: 'sk', // Set the locale to Slovak
    buttonText: {
      today: 'Dnes' // Customize the "today" button text to Slovak
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