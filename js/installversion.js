var api = 'https://api.github.com/repos/CanonicalLtd/multipass/releases';
var downloadButtons = document.querySelectorAll('.js-download');
var json = '';

fetch(api)
.then(function(response) {
  return response.json();
})
.then(function(myJson) {
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
  var version = button.querySelector('.js-version');
  var assetInfo = getAssetInfo(os);
  if (assetInfo) {
    button.setAttribute('href', assetInfo.url);
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
            name: release.tag_name
          }
        } else {
          return false;
        }
        break;
      }
    }
  }
}