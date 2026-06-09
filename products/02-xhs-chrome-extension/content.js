// content.js - Injected into xiaohongshu.com
// Adds an AI helper button next to the editor on Xiaohongshu

function injectHelperButton() {
  // Look for the post editor
  const editorAreas = document.querySelectorAll(
    '[class*="editor"], [class*="post"], [class*="publish"], textarea, [contenteditable="true"]'
  );

  if (editorAreas.length === 0) return;

  // Avoid duplicate injection
  if (document.getElementById("xhs-ai-helper-btn")) return;

  const btn = document.createElement("button");
  btn.id = "xhs-ai-helper-btn";
  btn.innerHTML = "✍️ AI帮写";
  btn.style.cssText = `
    position: fixed;
    bottom: 100px;
    right: 30px;
    z-index: 9999;
    background: linear-gradient(135deg, #ff2442, #ff6b81);
    color: white;
    border: none;
    border-radius: 24px;
    padding: 10px 20px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 0 4px 16px rgba(255,36,66,.4);
    transition: all .2s;
  `;

  btn.addEventListener("mouseenter", () => {
    btn.style.transform = "translateY(-2px)";
    btn.style.boxShadow = "0 6px 20px rgba(255,36,66,.5)";
  });
  btn.addEventListener("mouseleave", () => {
    btn.style.transform = "translateY(0)";
    btn.style.boxShadow = "0 4px 16px rgba(255,36,66,.4)";
  });

  btn.addEventListener("click", () => {
    // Open extension popup
    chrome.runtime.sendMessage({ type: "OPEN_POPUP" });
  });

  document.body.appendChild(btn);
}

// Run on page load
setTimeout(injectHelperButton, 2000);

// Also watch for DOM changes (SPA navigation)
const observer = new MutationObserver(() => {
  if (!document.getElementById("xhs-ai-helper-btn")) {
    injectHelperButton();
  }
});

observer.observe(document.body, { childList: true, subtree: true });
