function setupTabs() {
  var tabs = document.querySelectorAll(".js-tab");

  for (var i = 0; i < tabs.length; i += 1) {
    var tab = tabs[i];
    var tabSelector = tab.getAttribute("href");
    var tabContent = document.querySelector(tabSelector);

    if (tabContent) {
      tab.setAttribute("aria-selected", "false");
      tabContent.classList.add("u-hide");

      tab.addEventListener("click", function (e) {
        e.preventDefault();
        toggleTab(e.currentTarget);
      });
    }
  }

  function toggleTab(tab) {
    var tabSelector = tab.getAttribute("href");
    var tabContent = document.querySelector(tabSelector);

    for (var i = 0; i < tabs.length; i += 1) {
      if (tabs[i] !== tab) {
        var otherTabSelector = tabs[i].getAttribute("href");
        var otherTabContent = document.querySelector(otherTabSelector);

        tabs[i].setAttribute("aria-selected", "false");
        tabs[i].classList.remove("active");
        otherTabContent.classList.add("u-hide");
      }
    }

    tab.setAttribute("aria-selected", "true");
    tab.classList.toggle("active");
    tabContent.classList.toggle("u-hide");

    if (tab.classList.contains("active")) {
      var breakpoint = 620;
      var yOffset = 200;
      var rect = tabContent.getBoundingClientRect();
      var inView = window.innerHeight - yOffset > rect.top;
      var scrollTarget = window.scrollY + yOffset;

      if (window.innerWidth <= breakpoint) {
        scrollTarget = pageYOffset + rect.top - 10;
      }

      if (!inView) {
        window.scroll({
          behavior: "smooth",
          top: scrollTarget,
        });
      }
    }
  }
}

function setOSDownloadURLs() {
  var api = "https://api.github.com/repos/CanonicalLtd/multipass/releases";
  var downloadButtons = document.querySelectorAll(".js-download");
  var tabbedMenu = document.querySelector(".js-tabbed-menu");
  var json = "";

  tabbedMenu.classList.remove("u-hide");

  fetch(api)
    .then(function (response) {
      return response.json();
    })
    .then(function (myJson) {
      json = myJson;
      setupDownloadButtons();
    });

  function setupDownloadButtons() {
    for (var i = 0; i < downloadButtons.length; i++) {
      generateDownloadButton(downloadButtons[i]);
    }
  }

  function generateDownloadButton(button) {
    var os = button.dataset.os;
    var version = button.querySelector(".js-version");
    var assetInfo = getAssetInfo(os);
    if (assetInfo) {
      button.setAttribute("href", assetInfo.url);
      button
        .querySelector(".p-link--external")
        .classList.remove("p-link--external");
    }
    if (version) {
      version.innerText = assetInfo.name;
    }
  }

  function getAssetInfo(os) {
    var releases = json;
    for (var i = 0; i < releases.length; i++) {
      var release = releases[i];
      var assets = release.assets;
      for (var q = 0; q < assets.length; q++) {
        var asset = assets[q];
        if (asset.name.includes(os) && !release.prerelease) {
          if (asset.browser_download_url && release.tag_name) {
            return {
              url: asset.browser_download_url,
              name: release.tag_name,
            };
          } else {
            return false;
          }
          break;
        }
      }
    }
  }
}

const copyToClipboard = str => {
  const el = document.createElement("textarea"); // Create a <textarea> element
  el.value = str; // Set its value to the string that you want copied
  el.setAttribute("readonly", ""); // Make it readonly to be tamper-proof
  el.style.position = "absolute";
  el.style.left = "-9999px"; // Move outside the screen to make it invisible
  document.body.appendChild(el); // Append the <textarea> element to the HTML document
  const selected =
    document.getSelection().rangeCount > 0 // Check if there is any content selected previously
      ? document.getSelection().getRangeAt(0) // Store selection if found
      : false; // Mark as false to know no selection existed before
  el.select(); // Select the <textarea> content
  document.execCommand("copy"); // Copy - only works as a result of a user action (e.g. click events)
  document.body.removeChild(el); // Remove the <textarea> element
  if (selected) {
    // If a selection existed before copying
    document.getSelection().removeAllRanges(); // Unselect everything on the HTML document
    document.getSelection().addRange(selected); // Restore the original selection
  }
};

var codeSnippetActions = document.querySelectorAll(".p-code-copyable__action");

for (var codeSnippetAction of codeSnippetActions) {
  codeSnippetAction.addEventListener(
    "click",
    function (e) {
      const clipboardValue = this.previousSibling.previousSibling.value;
      copyToClipboard(clipboardValue);
    },
    false
  );
}

setOSDownloadURLs();
setupTabs();
