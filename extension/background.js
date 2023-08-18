// background.js
chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  if (request.action === "getActiveTabUrl") {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      const activeTab = tabs[0];
      const activeTabUrl = activeTab.url;
      
      sendResponse({url: activeTabUrl});
    });

    // Important: Return true to keep the message channel open for sendResponse
    return true;
  }
});
