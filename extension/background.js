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


// chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
//   if (request.action === "getToken") {
//       const jwtToken = getCookie('access_token');  // Get JWT token from cookie
//       console.log(jwtToken)
//       sendResponse({ token: jwtToken });  // Send the token back to popup
//   }
// });

// function getCookie(name) {
//   const cookies = document.cookie.split(';');
  
//   for (const cookie of cookies) {
//     const [cookieName, cookieValue] = cookie.trim().split('=');
//     if (cookieName === name) {
//       return cookieValue;
//     }
//   }
  
//   return null; // Return null if the cookie with the given name is not found
// }


// background.js

// background.js

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.action === "fetchToken") {
    myUrl = "http://localhost:8000"
    chrome.cookies.get({url: myUrl, name: 'access_token'}, function(cookie) {
        // do something with the cookie
        sendResponse({token: cookie});
  });
  
  
  }
  return true;  // Indicates that sendResponse will be called asynchronously
});
