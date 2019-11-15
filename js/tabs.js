var tabs = document.querySelectorAll('.js-tab');

function setupTabs() {
  for (var i = 0; i < tabs.length; i += 1) {
    var tab = tabs[i],
        tabSelector = tab.getAttribute('href'),
        tabContent = document.querySelector(tabSelector);

    if (tabContent) {
      tab.setAttribute('aria-selected', 'false');
      tabContent.classList.add('u-hide');

      tab.addEventListener('click', function(e) {
        e.preventDefault();
        toggleTab(event.currentTarget);
      });
    }
  }
}

function toggleTab(tab) {
  var tabSelector = tab.getAttribute('href'),
      tabContent = document.querySelector(tabSelector);

  for (var i = 0; i < tabs.length; i += 1) {
    if (tabs[i] !== tab) {
      var otherTabSelector = tabs[i].getAttribute('href'),
          otherTabContent = document.querySelector(otherTabSelector);
      
      tabs[i].setAttribute('aria-selected', 'false');
      tabs[i].classList.remove('active');
      otherTabContent.classList.add('u-hide');
    }
  }

  tab.setAttribute('aria-selected', 'true');
  tab.classList.toggle('active');
  tabContent.classList.toggle('u-hide');

  if (tab.classList.contains('active')) {
    var breakpoint = 620,
        rect = tabContent.getBoundingClientRect(),
        yOffset = tab.offsetHeight;

    if (window.innerWidth <= breakpoint) {
      yOffset = 10;
    }

    window.scroll({
      behavior: 'smooth',
      top: (pageYOffset + rect.top) - yOffset
    });
  }
}

setupTabs();