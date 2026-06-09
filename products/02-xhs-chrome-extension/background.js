// background.js - Service Worker
chrome.runtime.onInstalled.addListener(() => {
  console.log("小红书AI文案助手已安装");
});

// Listen for messages from popup or content scripts
chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  if (message.type === "GET_API_KEY") {
    chrome.storage.local.get("apiKey").then(({ apiKey }) => {
      sendResponse({ apiKey: apiKey || "" });
    });
    return true; // Keep channel open for async
  }
});
