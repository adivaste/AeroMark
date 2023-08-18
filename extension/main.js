chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "getActiveTabUrl") {
      const url = window.location.href;
      sendResponse({ url: url });
    }
  });
  