const divNewAlert = document.getElementById('div-alert');
const nav = document.getElementById('nav');
const navbar = document.getElementById('navbar');
function addClassIfWidthBelow991px(element) {
    if (window.innerWidth <= 991) {
        element.classList.add('mb-2');
    }
}

function displayNotification(message, type, container) {
    return new Promise((resolve) => {
        const notificationDiv = document.createElement('div');
        notificationDiv.className = `alert alert-${type}`;
        notificationDiv.textContent = message;
        container.appendChild(notificationDiv);
        setTimeout(() => {
            notificationDiv.remove();
            resolve();
        }, 2000);
    });
}
function signOut() {
    localStorage.removeItem('token');
    window.location.href = '/';
}