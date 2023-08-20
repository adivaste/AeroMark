// contentScript.js

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.action === "fetchToken") {
    chrome.cookies.get({ name: "access_token", url: "http://localhost:8000" }, function(cookie) {
      const token = cookie ? cookie.value : null;
      sendResponse({ token: token });
    });
    return true;  // Indicates that sendResponse will be called asynchronously
  }
});
