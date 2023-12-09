var selectedEndDates = [];

document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');
  var checkoutLink = document.getElementById('checkout-link');
  var dateDisplay = document.getElementById('dateDisplay');
  var selectedDatesDisplay = document.getElementById('selectedDatesDisplay');

  var today = new Date(); // Get today's date
  var clicksCount = 0;

  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    events: eventData,
    selectable: true,
    selectAllow: function(info) {
      // Disable the selection if it's a day before or including today
      var selectedDate = info.start;
      var todayYear = today.getFullYear();
      var todayMonth = today.getMonth();
      var todayDay = today.getDate();

      var selectedYear = selectedDate.getFullYear();
      var selectedMonth = selectedDate.getMonth();
      var selectedDay = selectedDate.getDate();

      if (selectedYear < todayYear ||
        (selectedYear === todayYear && selectedMonth < todayMonth) ||
        (selectedYear === todayYear && selectedMonth === todayMonth && selectedDay <= todayDay)) {
        return false;
      }
      return true; // Allow selection for other days
    },
    select: function(info) {
      var start = info.start;
      var end = info.end;
      var endDate = end.toISOString().split('T')[0];
      clicksCount += 1;

      if (selectedEndDates.length > 0) {
        // Calculate the range of dates between the first and second selection
        var startDate = new Date(selectedEndDates[0]);
        var selectedEndDate = new Date(endDate);
        var currentDate = new Date(Math.min(startDate, selectedEndDate)); // Ensure chronological order
        var endDate = new Date(Math.max(startDate, selectedEndDate)); // Ensure chronological order

        var dateRange = [];
        while (currentDate <= endDate) {
          var dateStr = currentDate.toISOString().split('T')[0];
          if (!selectedEndDates.includes(dateStr)) { // Check if the date is already in the array
            dateRange.push(dateStr);
          }
          currentDate.setDate(currentDate.getDate() + 1);
        }

        // Push all unique dates in the range into selectedEndDates
        selectedEndDates = selectedEndDates.concat(dateRange);
      } else {
        selectedEndDates.push(endDate);
      }

      if (clicksCount > 2) {
        clicksCount = 1;
        removeSelectedDatesHighlight(selectedEndDates);
        selectedEndDates = [];
        var endDate = end.toISOString().split('T')[0];
        selectedEndDates.push(endDate);
        dateDisplay.style.visibility = 'hidden';
        dateDisplay.style.opacity = 0;
      } else {
        dateDisplay.style.visibility = 'visible';
        dateDisplay.style.opacity = 1;
        selectedDatesDisplay.textContent = formatSelectedDates(selectedEndDates);
      }

      highlightSelectedDates(selectedEndDates);

      checkoutLink.href = '/checkout/' + '?dates=' + selectedEndDates.join(',');
    },
    firstDay: 1,
    locale: (language_code === 'sk') ? 'sk' : 'en',
    buttonText: {
      today: (language_code === 'sk') ? 'Aktuálny mesiac' : 'This month'
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

function removeSelectedDatesHighlight(selectedDates) {
  selectedDates.forEach(function(date) {
    var dateElement = document.querySelector('.fc-day[data-date="' + date + '"]');
    if (dateElement) {
      dateElement.classList.remove('selected-date');
    }
  });
}

function formatSelectedDates(dates) {
  if (dates.length === 0) {
    return '';
  }

  // Function to format dates as DD.MM.YYYY
  var sortedDates = dates.map(function (dateString) {
    return new Date(dateString);
  }).sort(function (a, b) {
    return a - b;
  });

  var firstDate = sortedDates[0];
  var lastDate = sortedDates[sortedDates.length - 1];

  var firstDateFormatted = formatDate(firstDate);
  var lastDateFormatted = formatDate(lastDate);

  return firstDateFormatted + ' - ' + lastDateFormatted;
}

function formatDate(date) {
  var day = date.getDate().toString().padStart(2, '0');
  var month = (date.getMonth() + 1).toString().padStart(2, '0');
  var year = date.getFullYear();
  return day + '.' + month + '.' + year;
}