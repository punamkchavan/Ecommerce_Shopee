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

    // Get the CSRF token from the HTML
const getCsrfToken = () => {
    const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
    return csrfInput ? csrfInput.value : '';
};

// Add CSRF token to the headers of your fetch request
const loginForm = document.getElementById('loginForm'); // Replace with your form ID
loginForm.addEventListener('submit', async function (event) {
    event.preventDefault();

    const formData = new FormData(loginForm);
    const csrfToken = getCsrfToken();

    const response = await axios('/user/check-login', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken, // Include CSRF token in the headers
        },
        body: formData
    });

    const data = await response.json();

    if (response.status === 201) {
        if (data.role === 'admin') {
            window.location.href = '/admin_product_list';
        } else {
            window.location.href = '/main.Home';
        }
    } else {
        alert(data.message);
    }
});


