// ARAYA WALKTHROUGH SYSTEM - Created autonomously by Araya
class ArayaWalkthroughGuide {
    startTour(name, steps) {
        steps.forEach((step, i) => {
            setTimeout(() => {
                const div = document.createElement("div");
                div.innerHTML = `<div style="position:fixed;top:20px;right:20px;background:#667eea;color:white;padding:20px;border-radius:10px;z-index:999999;max-width:400px;box-shadow:0 10px 40px rgba(0,0,0,0.3);"><h3>${step.title}</h3><p>${step.description}</p><button onclick="this.parentElement.remove()" style="background:white;color:#667eea;border:none;padding:10px 20px;border-radius:5px;cursor:pointer;font-weight:bold;">Next →</button></div>`;
                document.body.appendChild(div.firstChild);
            }, i * 5000);
        });
    }
}
window.ArayaGuide = new ArayaWalkthroughGuide();
console.log("🤖 Araya Walkthrough System Active");