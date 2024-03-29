$('.slider').slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 3500,
    arrows: true,
    dots: true,
    prevArrow: '<button type="button" class="slick-prev"><i class="fa-solid fa-arrow-left-to-arc"></i></button>',
    nextArrow: '<button type="button" class="slick-next"><i class="fa-solid fa-arrow-right-to-arc"></i></button>',
    customPaging: function(slider, i) {
        return '<button type="button" class="custom-dot"></button>';
    }
});

function smoothScroll(targetId) {
    var target = document.getElementById(targetId);
    if (target) {
      var targetPosition = target.offsetTop; // Get the target element's position
      var startPosition = window.pageYOffset; // Get current position
      var distance = targetPosition - startPosition;
      var duration = 1000; // Set the duration of the scroll in milliseconds
      let start = null;

      // Function to perform the scrolling animation
      function animation(currentTime) {
        if (start === null) {
          start = currentTime;
        }
        var timeElapsed = currentTime - start;
        var run = ease(timeElapsed, startPosition, distance, duration);
        window.scrollTo(0, run);
        if (timeElapsed < duration) {
          requestAnimationFrame(animation);
        }
      }

      // Easing function for smooth scrolling
      function ease(t, b, c, d) {
        t /= d / 2;
        if (t < 1) return c / 2 * t * t + b;
        t--;
        return -c / 2 * (t * (t - 2) - 1) + b;
      }

      requestAnimationFrame(animation);
    }
}

function scrollToTop() {
  const startPosition = window.pageYOffset; // Get current position
  const distance = -startPosition; // Calculate the distance to scroll to the top
  const duration = 1000; // Set the duration of the scroll in milliseconds
  let start = null;

  // Function to perform the scrolling animation
  function animation(currentTime) {
    if (start === null) {
      start = currentTime;
    }
    const timeElapsed = currentTime - start;
    const run = ease(timeElapsed, startPosition, distance, duration);
    window.scrollTo(0, run);
    if (timeElapsed < duration) {
      requestAnimationFrame(animation);
    }
  }

  // Easing function for smooth scrolling
  function ease(t, b, c, d) {
    t /= d / 2;
    if (t < 1) return c / 2 * t * t + b;
    t--;
    return -c / 2 * (t * (t - 2) - 1) + b;
  }

  requestAnimationFrame(animation);
}