document.addEventListener("DOMContentLoaded", function () {


  const customTagsInput = document.getElementById('custom-tags-input');
  const customTagsSuggestions = document.getElementById('custom-tags-suggestions');
  const customTagsContainer = document.getElementById('custom-tags-container');

  const predefinedTags = [
    "one",
    "two",
    "three",
    "four"
    // Add more predefined tags as needed
  ]

  function showTagsSuggestions(matchedTags) {
    const suggestionsHTML = matchedTags.map(tag => `<div class="p-2 cursor-pointer hover:bg-gray-100">${tag}</div>`).join('');
    customTagsSuggestions.innerHTML = suggestionsHTML;
    customTagsSuggestions.classList.remove('hidden');

    customTagsSuggestions.querySelectorAll('div').forEach(div => {
      div.addEventListener('click', event => {
        const selectedTag = event.target.textContent;
        if (!customTagsContainer.querySelector(`[data-tag="${selectedTag}"]`)) {
          addTag(selectedTag);
        }
        customTagsInput.value = '';
        hideTagsSuggestions();
      });
    });
  }

  function hideTagsSuggestions() {
    customTagsSuggestions.innerHTML = '';
    customTagsSuggestions.classList.add('hidden');
  }

  customTagsInput.addEventListener('input', () => {
    const inputValue = customTagsInput.value.toLowerCase().trim();
    const matchedTags = predefinedTags.filter(tag => tag.toLowerCase().includes(inputValue));

    if (matchedTags.length > 0) {
      showTagsSuggestions(matchedTags);
    } else {
      hideTagsSuggestions();
    }
  });

  customTagsInput.addEventListener('focus', () => {
    if (predefinedTags.length > 0) {
      showTagsSuggestions(predefinedTags);
    }
  });

  document.addEventListener('click', event => {
    if (!customTagsInput.contains(event.target) && !customTagsSuggestions.contains(event.target)) {
      hideTagsSuggestions();
    }
  });

  customTagsInput.addEventListener('keydown', event => {
    if (event.key === 'Enter' && customTagsInput.value.trim() !== '') {
      addTag(customTagsInput.value.trim());
      customTagsInput.value = '';
      event.preventDefault();
    }
  });

  customTagsContainer.addEventListener('click', event => {
    if (event.target.classList.contains('tag-close')) {
      const tagToRemove = event.target.getAttribute('data-tag');
      const tagElement = event.target.parentElement;
      customTagsContainer.removeChild(tagElement);
    }
  });

  function addTag(tagText) {
    const tagElement = document.createElement('div');
    tagElement.className = 'custom-tag';
    tagElement.innerHTML = `
          <span class="tag-text">${tagText}</span>
          <span class="tag-close" data-tag="${tagText}">x</span>
      `;
    customTagsContainer.appendChild(tagElement);
  }


  // Send the post
  const saveButton = document.querySelector("#save_bookmark_button");
saveButton.addEventListener("click", saveBookmark);

async function saveBookmark() {
    myUrl = "http://localhost:8000";

    const saveButtonIcon = saveButton.querySelector(".fa-floppy-disk");
    const spinnerIcon = '<i class="fa-solid fa-spinner fa-spin px-2"></i>';

    const originalButtonText = saveButton.innerHTML;
    saveButton.innerHTML = spinnerIcon + ' Saving...';
    saveButton.disabled = true;

    const url = document.querySelector("#bookmark-url").value;
    const title = document.querySelector("#bookmark-title").value;
    const description = document.querySelector("#bookmark-description").value;
    const note = document.querySelector("#bookmark-note").value;
    const collection = document.querySelector("#collection-helper-text").value;

    const customTagsContainer = document.querySelector("#custom-tags-container");
    const customTagsInputElements = customTagsContainer.querySelectorAll(".custom-tag");

    const customTags = Array.from(customTagsInputElements).map(input => input.querySelector(".tag-text").innerText);
    const uniqueCustomTags = [...new Set(customTags)]; // Remove duplicates

    // Get JWT token from cookie asynchronously
    function getJwtToken(callback) {
        chrome.cookies.get({ url: myUrl, name: 'access_token' }, function (cookie) {
            if (callback) {
                callback(cookie.value);
            }
        });
    }

    // Use the JWT token in the async callback
    getJwtToken(async function (jwtToken) {
        const headers = {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${jwtToken}`
        };

        const bookmarkData = {
            url,
            title,
            description,
            note,
            collection,
            tags: uniqueCustomTags,
        };

        try {
            const response = await fetch("http://localhost:8000/api/bookmarks/", {
                method: "POST",
                headers: headers,
                body: JSON.stringify(bookmarkData),
            });

            if (response.ok) {
                // Bookmark saved successfully
                console.log("Bookmark saved!");
            }
            else if (response.status === 401) {
              // Unauthorized, redirect to login page
              chrome.tabs.create({ url: "http://localhost:8000/accounts/logout" });
            }
             else {
                // Handle error
                console.error("Error saving bookmark");
            }
        } catch (error) {
            console.error("Error:", error);
        } finally {
            // Restore the button's original state
            saveButton.innerHTML = "Saved";
            saveButton.disabled = false;
        }
    });
  }

});




// Get URL and title of the active tab

chrome.tabs.query({ 'active': true, 'windowId': chrome.windows.WINDOW_ID_CURRENT },
  function (tabs) {
    const activeTab = tabs[0];
    const activeTabUrl = activeTab.url;
    const activeTabTitle = activeTab.title;

    // Set URL and title of the active tab
    const urlElement = document.querySelector("#bookmark-url");
    urlElement.value = activeTabUrl;

    const titleElement = document.querySelector("#bookmark-title");
    titleElement.value = activeTabTitle;

  }
);
