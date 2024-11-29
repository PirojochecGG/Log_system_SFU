let lastActivity = new Date();

function getCsrfToken() {
    const cookies = document.cookie.split('; ');
    for (const cookie of cookies) {
        const [name, value] = cookie.split('=');
        if (name === 'csrftoken') return value;
    }
    return '';
}

document.addEventListener("mousemove", () => (lastActivity = new Date()));
document.addEventListener("keydown", () => (lastActivity = new Date()));

setInterval(() => {
    const now = new Date();
    const idleTime = now - lastActivity;

    if (idleTime > 30 * 60 * 1000) {
        fetch("/logout/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCsrfToken(),
            },
            credentials: "same-origin",
        })
            .then(() => {
                window.location.href = "/login/";
            });
    }
}, 60000);